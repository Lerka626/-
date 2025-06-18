# Руководство по деплою проекта

## 🚀 Локальный деплой с Docker Compose

### Предварительные требования:
- Docker Desktop установлен и запущен
- Git (для клонирования проекта)

### Шаги для запуска:

1. **Клонируйте проект и перейдите в папку:**
```bash
cd fullstack
```

2. **Запустите проект:**
```bash
docker-compose up --build
```

3. **Дождитесь сборки и запуска всех сервисов**

4. **Откройте приложение:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- База данных: localhost:5432

### Остановка проекта:
```bash
docker-compose down
```

## 🌐 Деплой на VPS/Сервер

### Вариант 1: Простой VPS (Ubuntu/Debian)

1. **Подключитесь к серверу:**
```bash
ssh user@your-server-ip
```

2. **Установите Docker и Docker Compose:**
```bash
# Обновите систему
sudo apt update && sudo apt upgrade -y

# Установите Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Добавьте пользователя в группу docker
sudo usermod -aG docker $USER

# Установите Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Перезагрузитесь
sudo reboot
```

3. **Клонируйте проект:**
```bash
git clone <your-repo-url>
cd fullstack
```

4. **Настройте переменные окружения (создайте .env файл):**
```bash
# Создайте файл .env
cat > .env << EOF
DB_USER=postgres
DB_PASS=your_secure_password
DB_HOST=db
DB_PORT=5432
DB_NAME=sber_project
POSTGRES_PASSWORD=your_secure_password
EOF
```

5. **Обновите docker-compose.yml для продакшена:**
```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend/passports:/app/passports
      - ./backend/uploads:/app/uploads
    environment:
      - DB_USER=${DB_USER}
      - DB_PASS=${DB_PASS}
      - DB_HOST=${DB_HOST}
      - DB_PORT=${DB_PORT}
      - DB_NAME=${DB_NAME}
    depends_on:
      - db
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend/my-react-app
    ports:
      - "80:80"
    restart: unless-stopped

  db:
    image: postgres:13-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${DB_NAME}
    restart: unless-stopped

volumes:
  postgres_data:
```

6. **Запустите проект:**
```bash
docker-compose up -d --build
```

7. **Настройте Nginx (опционально):**
```bash
sudo apt install nginx -y

# Создайте конфиг для домена
sudo nano /etc/nginx/sites-available/your-domain.com

# Добавьте конфигурацию:
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Активируйте сайт
sudo ln -s /etc/nginx/sites-available/your-domain.com /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Вариант 2: Облачные платформы

#### Railway
1. Зарегистрируйтесь на railway.app
2. Подключите GitHub репозиторий
3. Railway автоматически определит docker-compose.yml
4. Настройте переменные окружения в панели

#### Heroku
1. Создайте `heroku.yml`:
```yaml
build:
  docker:
    web: ./backend
    frontend: ./frontend/my-react-app
```

2. Разверните:
```bash
heroku create your-app-name
heroku stack:set container
git push heroku main
```

#### DigitalOcean App Platform
1. Подключите GitHub репозиторий
2. Выберите Docker Compose как тип приложения
3. Настройте переменные окружения
4. Разверните

## 🔧 Настройка для продакшена

### Безопасность:
1. **Измените пароли по умолчанию**
2. **Настройте SSL/HTTPS**
3. **Ограничьте доступ к базе данных**
4. **Настройте файрвол**

### Мониторинг:
1. **Настройте логирование**
2. **Добавьте health checks**
3. **Настройте бэкапы базы данных**

### Масштабирование:
1. **Используйте load balancer**
2. **Настройте кэширование**
3. **Оптимизируйте образы Docker**

## 📝 Полезные команды

```bash
# Просмотр логов
docker-compose logs -f

# Остановка всех контейнеров
docker-compose down

# Пересборка без кэша
docker-compose build --no-cache

# Просмотр использования ресурсов
docker stats

# Очистка неиспользуемых ресурсов
docker system prune -a
```

## 🆘 Устранение неполадок

### Проблемы с портами:
```bash
# Проверьте, какие порты заняты
netstat -tulpn | grep :8000
netstat -tulpn | grep :3000
```

### Проблемы с правами доступа:
```bash
# Измените права на папки
sudo chown -R $USER:$USER .
```

### Проблемы с памятью:
```bash
# Увеличьте лимиты Docker в настройках
```

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи: `docker-compose logs`
2. Убедитесь, что все порты свободны
3. Проверьте, что Docker Desktop запущен
4. Перезапустите Docker Desktop при необходимости 