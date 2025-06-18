from pydantic_settings import BaseSettings
from datetime import datetime


class Settings(BaseSettings):
    # Данные для локального подключения к PostgreSQL
    DB_USER: str = "postgres"
    DB_PASS: str = "mastdmastd"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "sber_project"

    # --- ИЗМЕНЕНИЕ НАЧАЛОСЬ ---

    # Список всех классов, которые предсказывает модель PyTorch.
    # ПОРЯДОК СТРОГО ВАЖЕН и определен анализом ноутбука обучения.
    SPECIES_CLASSES: list[str] = [
        "Лось",
        "Зубр",
        "Серый волк",
        "Косуля",
        "Пятнистый олень",
        "Заяц",
        "Рысь",
        "Выдра",
        "Куница",
        "Барсук",
        "Норка",
        "Енотовидная собака",
        "Хорёк",
        "Кабан"
    ]

    # Список видов, для которых будет запускаться идентификация по эмбеддингам.
    # Используйте точные названия из списка SPECIES_CLASSES.
    RARE_ANIMALS_LIST: list[str] = [
        "Зубр",
        "Выдра",
        "Рысь",
        "Норка"
    ]

    # Настройки для ДВУХ моделей
    CLASSIFIER_WEIGHTS: str = 'weights/best_resnet50.pth'
    EMBEDDER_WEIGHTS: str = 'weights/resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5'

    # --- ИЗМЕНЕНИЕ ЗАКОНЧИЛОСЬ ---

    # Пути к директориям
    IMAGE_DIR: str = "savedPredictions"
    UPLOADS_DIR: str = "uploads"
    PASSPORTS_DIR: str = "passports"

    SIMILARITY_THRESHOLD: float = 0.9

    class Config:
        case_sensitive = True


settings = Settings()

DATE_OF_PHOTOS: str = datetime.today().strftime('%Y-%m-%d')


