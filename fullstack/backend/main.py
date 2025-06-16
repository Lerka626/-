import os
import shutil
import uuid
from zipfile import ZipFile, is_zipfile
from pathlib import Path
import json
import asyncpg
from contextlib import asynccontextmanager
from typing import List
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from config import settings, DATE_OF_PHOTOS
from app import crud, ml_logic, schemas
from app.database import create_pool, get_db

# --- Создание папок при старте ---
for dir_path in [
    settings.UPLOADS_DIR, settings.IMAGE_DIR, settings.PASSPORTS_DIR,
    settings.CROPPED_DIR, settings.CROPPED_PASSPORTS_DIR
]:
    os.makedirs(dir_path, exist_ok=True)


# --- Управление жизненным циклом (пул БД) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Приложение запускается, создаем пул соединений...")
    pool = await create_pool()
    app.state.pool = pool
    yield
    print("Приложение останавливается, закрываем пул соединений...")
    await app.state.pool.close()


app = FastAPI(title="Rare Animal Tracker API", lifespan=lifespan, version="1.0.0")

# --- Middleware для CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене лучше указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Инициализация ML моделей ---
roboflow_client = ml_logic.get_roboflow_client()
feature_extractor = ml_logic.get_feature_extractor_model()
date_of_photo_dict = {}


# --- Вспомогательные функции ---
async def save_upload_file(upload_file: UploadFile) -> str:
    """Сохраняет загруженный файл с уникальным именем и возвращает имя файла."""
    unique_filename = f"{uuid.uuid4().hex[:10]}-{upload_file.filename}"
    file_path = os.path.join(settings.UPLOADS_DIR, unique_filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return unique_filename


async def process_zip_file(zip_path: str) -> list[str]:
    """Распаковывает ZIP-архив и возвращает список имен файлов изображений."""
    extracted_files = []
    with ZipFile(zip_path, "r") as input_zip:
        for member_name in input_zip.namelist():
            if not member_name.startswith('__MACOSX') and member_name.split(".")[-1].lower() in ["png", "jpg", "jpeg"]:
                unique_filename = f"{uuid.uuid4().hex[:10]}-{Path(member_name).name}"
                source = input_zip.open(member_name)
                target_path = Path(settings.UPLOADS_DIR) / unique_filename
                with open(target_path, "wb") as target_file:
                    shutil.copyfileobj(source, target_file)
                extracted_files.append(unique_filename)
    os.remove(zip_path)  # Удаляем архив после распаковки
    return extracted_files


# --- Эндпоинты API ---

@app.post("/upload/", response_model=schemas.UploadResponse)
async def upload_files_and_process(
        cords_sd: float = Form(...),
        cords_vd: float = Form(...),
        files: list[UploadFile] = File(...),
        conn: asyncpg.Connection = Depends(get_db)
):
    coordinates = f"{cords_sd}, {cords_vd}"
    processed_filenames = []

    for file in files:
        saved_filename = await save_upload_file(file)
        saved_filepath = os.path.join(settings.UPLOADS_DIR, saved_filename)
        if is_zipfile(saved_filepath):
            processed_filenames.extend(await process_zip_file(saved_filepath))
        elif file.content_type in ["image/jpeg", "image/png"]:
            processed_filenames.append(saved_filename)
        else:
            os.remove(saved_filepath)  # Удаляем невалидный файл
            print(f"Пропущен неверный тип файла: {file.content_type}")

    if not processed_filenames:
        raise HTTPException(status_code=400, detail="Не найдено валидных файлов для обработки.")

    # --- Основная логика обработки ---
    rare_animals_count = 0
    predictions_to_save = []
    animal_counts = {}

    for filename in processed_filenames:
        image_path = os.path.join(settings.UPLOADS_DIR, filename)
        rf_result = ml_logic.run_roboflow_inference(roboflow_client, image_path)

        if rf_result.get('visualization'):
            save_path = os.path.join(settings.IMAGE_DIR, filename)
            ml_logic.save_base64_image(rf_result['visualization'], save_path)

        for pred in rf_result.get('predictions', []):
            species = pred['class']
            animal_counts[species] = animal_counts.get(species, 0) + 1
            if species in settings.RARE_ANIMALS_LIST:
                rare_animals_count += 1

            p_data = schemas.Prediction(
                IMG=filename, type=species, date=DATE_OF_PHOTOS,
                size=str(pred['width']), confidence=str(pred['confidence'])
            )
            predictions_to_save.append({'data': p_data, 'raw_pred': pred})

    # --- Сохранение в БД ---
    zip_id = await crud.create_zip_record(conn, DATE_OF_PHOTOS, rare_animals_count, coordinates)
    pass_embeddings = await crud.get_passport_embeddings(conn)
    final_predictions_for_response = []

    for item in predictions_to_save:
        p_data, raw_pred = item['data'], item['raw_pred']
        passport_id = None
        if p_data.type in settings.RARE_ANIMALS_LIST and pass_embeddings:
            cropped_path = os.path.join(settings.CROPPED_DIR, f"crop_{p_data.IMG}")
            ml_logic.crop_and_save_animal(os.path.join(settings.UPLOADS_DIR, p_data.IMG), raw_pred, cropped_path)

            if os.path.exists(cropped_path):
                embedding = ml_logic.extract_features(feature_extractor, cropped_path)
                similar = ml_logic.find_most_similar_passports(embedding, pass_embeddings)
                if similar and similar[0][1] > settings.SIMILARITY_THRESHOLD:
                    passport_id = similar[0][0]
                    p_data.passport = passport_id
                    cords_id = await crud.create_cords_record(conn, p_data.date, coordinates, passport_id)
                    await crud.update_passport_cords(conn, passport_id, cords_id)

        output_id = await crud.create_output_record(
            conn, zip_id, p_data.type, p_data.IMG,
            float(p_data.confidence), float(p_data.size), passport_id
        )
        if passport_id:
            await crud.link_output_to_passport(conn, output_id, passport_id)

        final_predictions_for_response.append(p_data)

    return {"pred": final_predictions_for_response, "diagram": animal_counts}


@app.post("/upload_passport/", response_model=schemas.PassportInDB)
async def upload_passport(
        age: int = Form(...),
        gender: str = Form(...),
        name: str = Form(...),
        cords_sd: float = Form(...),
        cords_vd: float = Form(...),
        image_preview: UploadFile = File(...),
        conn: asyncpg.Connection = Depends(get_db)
):
    if image_preview.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(400, "Неверный тип файла изображения.")

    coordinates = f"{cords_sd}, {cords_vd}"

    # Сохраняем оригинальное фото для паспорта
    passport_photo_filename = await save_upload_file(image_preview)
    passport_photo_path = os.path.join(settings.PASSPORTS_DIR, passport_photo_filename)

    # Запускаем Roboflow для поиска животного на фото паспорта
    rf_result = ml_logic.run_roboflow_inference(roboflow_client, passport_photo_path)

    rare_animal_preds = [p for p in rf_result.get('predictions', []) if p['class'] in settings.RARE_ANIMALS_LIST]
    if not rare_animal_preds:
        os.remove(passport_photo_path)
        raise HTTPException(404, "Редкое животное на фото для паспорта не найдено.")

    # Берем первое найденное редкое животное
    animal_pred = rare_animal_preds[0]
    species = animal_pred['class']

    # Вырезаем животное и создаем эмбеддинг
    cropped_path = os.path.join(settings.CROPPED_PASSPORTS_DIR, passport_photo_filename)
    ml_logic.crop_and_save_animal(passport_photo_path, animal_pred, cropped_path)

    if not os.path.exists(cropped_path):
        os.remove(passport_photo_path)
        raise HTTPException(500, "Не удалось вырезать животное из фото.")

    embedding = ml_logic.extract_features(feature_extractor, cropped_path)
    embedding_str = json.dumps(embedding)

    # Создаем запись о координатах и сам паспорт
    cords_id = await crud.create_cords_record(conn, DATE_OF_PHOTOS, coordinates)
    passport_id = await crud.create_passport_record(
        conn, passport_photo_path, species, age, gender, cords_id, embedding_str, name
    )

    new_passport = await crud.get_passport_by_id(conn, passport_id)
    return new_passport


@app.get("/all_passports", response_model=List[schemas.PassportInDB])
async def get_all_passports(conn: asyncpg.Connection = Depends(get_db)):
    passports = await crud.get_all_passports(conn)
    return passports


@app.get("/get_passport/{passport_id}", response_model=schemas.PassportInDB)
async def get_passport(passport_id: int, conn: asyncpg.Connection = Depends(get_db)):
    passport = await crud.get_passport_by_id(conn, passport_id)
    if not passport:
        raise HTTPException(404, "Паспорт не найден")
    return passport


@app.get("/all_zips")
async def get_all_zips(conn: asyncpg.Connection = Depends(get_db)):
    return await crud.get_all_zips(conn)


@app.get("/image/processed/{image_name}")
async def get_processed_image(image_name: str):
    image_path = os.path.join(settings.IMAGE_DIR, image_name)
    if not os.path.isfile(image_path):
        raise HTTPException(status_code=404, detail="Обработанное изображение не найдено")
    return FileResponse(image_path)


@app.get("/image/passport/{image_name}")
async def get_passport_image(image_name: str):
    image_path = os.path.join(settings.PASSPORTS_DIR, image_name)
    if not os.path.isfile(image_path):
        raise HTTPException(status_code=404, detail="Фото паспорта не найдено")
    return FileResponse(image_path)
