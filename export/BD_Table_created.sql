CREATE TABLE Zips (
    id SERIAL PRIMARY KEY,
    upload_date DATE NOT NULL,
    rare_animals_count INT DEFAULT 0,
    coordinates TEXT
);

CREATE TABLE Cords (
    id SERIAL PRIMARY KEY,
    passport_id INT, 
    date DATE NOT NULL,
    coordinates TEXT
);

CREATE TABLE Passports (
    id SERIAL PRIMARY KEY,
    image_preview TEXT NOT NULL,
    type TEXT NOT NULL,
    age INT,
    gender TEXT,
    cords_id INT REFERENCES Cords(id),
    embanding TEXT,
    name TEXT
);

CREATE TABLE ModelOutputs (
    id SERIAL PRIMARY KEY,
    zip_id INT REFERENCES Zips(id) ON DELETE CASCADE,
    species TEXT NOT NULL,
    count INT DEFAULT 1,
    processed_photo TEXT,
    confidence FLOAT,
    size FLOAT,
    pass_id INT REFERENCES Passports(id)
);

CREATE TABLE OutputPassports (
    id SERIAL PRIMARY KEY,
    output_id INT REFERENCES ModelOutputs(id) ON DELETE CASCADE,
    passport_id INT REFERENCES Passports(id) ON DELETE CASCADE
);

ALTER TABLE Cords
ADD CONSTRAINT fk_passport FOREIGN KEY (passport_id) REFERENCES Passports(id) ON DELETE CASCADE;

\copy Zips TO 'D:/export/zips.csv' WITH CSV HEADER
\copy Outputs TO 'D:/export/outputs.csv' WITH CSV HEADER
\copy Passports TO 'D:/export/passports.csv' WITH CSV HEADER
\copy Output_Passports TO 'D:/export/output_passports.csv' WITH CSV HEADER
\copy Cords TO 'D:/export/cords.csv' WITH CSV HEADER

# Запись и выгрузка в таблицу csv
INSERT INTO Zips (upload_date, rare_animals_count, coordinates)  
VALUES ('2025-06-09', 3, '55.7558, 37.6173');

COPY Zips TO 'D:/export/zips.csv' DELIMITER ',' CSV HEADER;
