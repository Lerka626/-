-- Инициализация базы данных для проекта

-- Создаем таблицы
CREATE TABLE IF NOT EXISTS zips (
    id SERIAL PRIMARY KEY,
    upload_date DATE NOT NULL,
    rare_animals_count INTEGER NOT NULL,
    coordinates VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS outputs (
    id SERIAL PRIMARY KEY,
    zip_id INTEGER REFERENCES zips(id) ON DELETE CASCADE,
    species VARCHAR(100) NOT NULL,
    count INTEGER NOT NULL,
    processed_photo VARCHAR(255),
    confidence DECIMAL(3,2),
    size DECIMAL(5,2),
    pass_id INTEGER
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
    embanding TEXT,
    name VARCHAR(100),
    cords_id INTEGER REFERENCES cords(id) ON DELETE SET NULL
);

-- Добавляем ограничение для cords_id если его нет
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.table_constraints 
        WHERE constraint_name = 'passports_cords_id_fkey'
    ) THEN
        ALTER TABLE passports ADD CONSTRAINT passports_cords_id_fkey 
        FOREIGN KEY (cords_id) REFERENCES cords(id) ON DELETE SET NULL;
    END IF;
END $$;

-- База данных готова к работе
-- Паспорта будут создаваться автоматически при загрузке фото редких видов 