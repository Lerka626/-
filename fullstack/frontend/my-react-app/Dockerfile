# frontend/my-react-app/Dockerfile

# --- СТАДИЯ 1: Сборка React-приложения ---
FROM node:20-alpine AS builder

# Аргумент для API URL
ARG VITE_API_BASE_URL=http://localhost:8000

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем package.json и package-lock.json для установки зависимостей
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем все остальные файлы проекта
COPY . .

# Создаем .env файл с переменной окружения
RUN echo "VITE_API_BASE_URL=${VITE_API_BASE_URL}" > .env

# Собираем статические файлы для продакшена
RUN npm run build

# --- СТАДИЯ 2: Обслуживание статики через Nginx ---
FROM nginx:stable-alpine

# Копируем собранные файлы из стадии "builder" в директорию веб-сервера Nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# Копируем кастомный конфиг Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Указываем, что контейнер будет слушать порт 80
EXPOSE 80

# Команда для запуска Nginx
CMD ["nginx", "-g", "daemon off;"]