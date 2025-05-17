# Используем официальный образ Python в качестве базового
FROM python:3.11-slim

# Устанавливаем необходимые системные библиотеки
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \ 
    libgirepository1.0-dev \
    pkg-config \
    libopencv-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей в образ
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install python-multipart

# Копируем всё приложение в рабочую директорию
COPY . .

RUN mkdir savedPredictions
RUN mkdir uploads
RUN mkdir passports
RUN mkdir cropped_passports
RUN mkdir cropped_images

# Указываем, что будет использован порт 8000
EXPOSE 8000

# Запускаем приложение, используя uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]