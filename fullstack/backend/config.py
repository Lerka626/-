from pydantic_settings import BaseSettings
from datetime import datetime


class Settings(BaseSettings):
    """
    Класс для хранения всех конфигурационных переменных.
    Значения могут быть переопределены переменными окружения.
    """
    # Настройки базы данных
    DB_USER: str = "postgres"
    DB_PASS: str = "mastdmastd"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "sber_project"

    # API ключи и настройки Roboflow
    ROBOFLOW_API_KEY: str = "GyLAEnCOCynKOHoO2JDF"
    ROBOFLOW_API_URL: str = "https://detect.roboflow.com"
    ROBOFLOW_WORKSPACE: str = "pe1men24"
    ROBOFLOW_WORKFLOW_ID: str = "detect-count-and-visualize-2"

    # Списки животных
    RARE_ANIMALS_LIST: list[str] = ['Irbis']

    # Пути к директориям внутри контейнера
    IMAGE_DIR: str = "savedPredictions"
    UPLOADS_DIR: str = "uploads"
    PASSPORTS_DIR: str = "passports"
    CROPPED_DIR: str = "cropped_images"
    CROPPED_PASSPORTS_DIR: str = "cropped_passports"

    # Настройки ML
    RESNET_WEIGHTS: str = 'weights/resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5'
    SIMILARITY_THRESHOLD: float = 0.9

    class Config:
        # Позволяет Pydantic читать переменные из .env файла (если он есть)
        case_sensitive = True


settings = Settings()

# Глобальная переменная для даты, которая устанавливается при запуске
DATE_OF_PHOTOS: str = datetime.today().strftime('%Y-%m-%d')
