-- Инициализация базы данных для проекта

-- Создаем таблицы
CREATE TABLE IF NOT EXISTS zips (
    id SERIAL PRIMARY KEY,
    upload_date DATE NOT NULL,
    rare_animals_count INTEGER NOT NULL,
    coordinates VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS cords (
    id SERIAL PRIMARY KEY,
    passport_id INTEGER,
    date DATE NOT NULL,
    coordinates VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS passports (
    id SERIAL PRIMARY KEY,
    image_preview VARCHAR(255),
    type VARCHAR(100) NOT NULL,
    age INTEGER,
    gender CHAR(1),
    embeding TEXT,
    name VARCHAR(100),
    cords_id INTEGER
);

CREATE TABLE IF NOT EXISTS outputs (
    id SERIAL PRIMARY KEY,
    zip_id INTEGER REFERENCES zips(id) ON DELETE CASCADE,
    species VARCHAR(100) NOT NULL,
    count INTEGER NOT NULL,
    processed_photo VARCHAR(255),
    confidence DECIMAL(3,2),
    size DECIMAL(5,2),
    pass_id INTEGER REFERENCES passports(id) ON DELETE SET NULL
);

-- Добавляем внешние ключи после создания всех таблиц
ALTER TABLE passports ADD CONSTRAINT IF NOT EXISTS passports_cords_id_fkey 
    FOREIGN KEY (cords_id) REFERENCES cords(id) ON DELETE SET NULL;

ALTER TABLE cords ADD CONSTRAINT IF NOT EXISTS cords_passport_id_fkey 
    FOREIGN KEY (passport_id) REFERENCES passports(id) ON DELETE CASCADE;

-- База данных готова к работе
-- Паспорта будут создаваться автоматически при загрузке фото редких видов 