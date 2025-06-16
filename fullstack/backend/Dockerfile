FROM python:3.11-slim

# Устанавливаем переменные окружения для Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем системные зависимости, необходимые для OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    # Очищаем кэш apt для уменьшения размера образа
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями для использования кэша Docker
COPY requirements.txt .

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения, конфигурации и веса модели
COPY ./app ./app
COPY ./core ./core
COPY ./weights ./weights

# Указываем, что контейнер будет слушать порт 8000
EXPOSE 8000

# Команда для запуска приложения в продакшен режиме
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]