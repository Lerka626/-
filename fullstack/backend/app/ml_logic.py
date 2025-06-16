import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.preprocessing import image as tf_image
from tensorflow.keras.applications.resnet import ResNet50, preprocess_input
from inference_sdk import InferenceHTTPClient
import base64
from config import settings


# --- Инициализация клиентов и моделей ---

def get_roboflow_client():
    """Возвращает клиент для работы с Roboflow API."""
    return InferenceHTTPClient(
        api_url=settings.ROBOFLOW_API_URL,
        api_key=settings.ROBOFLOW_API_KEY
    )


def get_feature_extractor_model() -> ResNet50:
    """Загружает и возвращает предобученную модель ResNet50 для извлечения признаков."""
    return ResNet50(
        weights=settings.RESNET_WEIGHTS,
        include_top=False,
        pooling='avg'
    )


# --- Функции извлечения признаков и сходства ---

def extract_features(model: ResNet50, img_path: str) -> list[float]:
    """Извлекает вектор признаков (эмбеддинг) из файла изображения."""
    img = tf_image.load_img(img_path, target_size=(224, 224))
    img_array = tf_image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    features = model.predict(img_array, verbose=0)  # verbose=0 отключает логи предсказания
    return list(features.flatten())


def cosine_similarity(a: list, b: list) -> float:
    """Вычисляет косинусное сходство между двумя векторами."""
    a_np, b_np = np.array(a), np.array(b)
    dot_product = np.dot(a_np, b_np)
    norm_a = np.linalg.norm(a_np)
    norm_b = np.linalg.norm(b_np)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def find_most_similar_passports(new_embedding: list[float], existing_passports: list[tuple[int, list[float]]]) -> list[
    tuple[int, float]]:
    """Находит наиболее похожие паспорта и возвращает их ID и степень сходства."""
    similarities = []
    for pass_id, pass_embedding in existing_passports:
        sim = cosine_similarity(new_embedding, pass_embedding)
        similarities.append((pass_id, sim))

    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities


# --- Функции обработки изображений ---

def run_roboflow_inference(client: InferenceHTTPClient, image_path: str):
    """Запускает детекцию объектов через Roboflow и возвращает результат."""
    try:
        # Используем стандартный метод .infer()
        result = client.infer(image_path, model_id=f"{settings.ROBOFLOW_WORKSPACE}/{settings.ROBOFLOW_WORKFLOW_ID}")
        return result
    except Exception as e:
        print(f"Ошибка при обращении к Roboflow: {e}")
        return {"predictions": []}  # Возвращаем пустую структуру в случае ошибки


def save_base64_image(base64_string: str, path: str):
    """Декодирует строку Base64 и сохраняет как файл изображения."""
    try:
        image_data = base64.b64decode(base64_string)
        with open(path, 'wb') as image_file:
            image_file.write(image_data)
    except Exception as e:
        print(f"Ошибка при сохранении base64 изображения: {e}")


def crop_and_save_animal(original_image_path: str, prediction: dict, save_path: str):
    """Вырезает объект по координатам из Roboflow и сохраняет его в файл."""
    img = cv2.imread(original_image_path)
    if img is None:
        print(f"Не удалось прочитать изображение: {original_image_path}")
        return

    x_center = prediction['x']
    y_center = prediction['y']
    width = prediction['width']
    height = prediction['height']

    x1 = int(x_center - width / 2)
    y1 = int(y_center - height / 2)
    x2 = int(x_center + width / 2)
    y2 = int(y_center + height / 2)

    # Гарантируем, что координаты не выходят за пределы изображения
    h, w, _ = img.shape
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w, x2), min(h, y2)

    cropped_img = img[y1:y2, x1:x2]
    if cropped_img.size > 0:
        cv2.imwrite(save_path, cropped_img)
    else:
        print(f"Не удалось вырезать изображение для {save_path}, возможно, неверные координаты.")
