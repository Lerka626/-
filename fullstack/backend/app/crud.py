import json
from datetime import datetime
from typing import List, Optional
import asyncpg

# --- Функции чтения (SELECT) ---

async def get_all_passports(conn: asyncpg.Connection):
    return await conn.fetch("SELECT * FROM passports ORDER BY id")

async def get_passport_embeddings(conn: asyncpg.Connection) -> List[tuple[int, List[float]]]:
    passports = await conn.fetch("SELECT id, embanding FROM passports WHERE embanding IS NOT NULL")
    return [[p['id'], json.loads(p['embanding'])] for p in passports]

async def get_passport_by_id(conn: asyncpg.Connection, passport_id: int):
    return await conn.fetchrow("SELECT * FROM passports WHERE id = $1", passport_id)

async def get_all_zips(conn: asyncpg.Connection):
    return await conn.fetch("SELECT * FROM zips ORDER BY upload_date DESC")

async def get_output_by_zip_id(conn: asyncpg.Connection, zip_id: int):
    return await conn.fetch("SELECT * FROM outputs WHERE zip_id = $1", zip_id)

# --- Функции создания (INSERT) ---

async def create_zip_record(conn: asyncpg.Connection, upload_date_str: str, rare_animals_count: int, coordinates: str) -> int:
    upload_date = datetime.strptime(upload_date_str, '%Y-%m-%d').date()
    query = 'INSERT INTO Zips (upload_date, rare_animals_count, coordinates) VALUES ($1, $2, $3) RETURNING id;'
    return await conn.fetchval(query, upload_date, rare_animals_count, coordinates)

async def create_output_record(conn: asyncpg.Connection, zip_id: int, species: str, img_name: str, confidence: float, size: float, pass_id: Optional[int]) -> int:
    query = 'INSERT INTO Outputs (zip_id, species, count, processed_photo, confidence, size, pass_id) VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING id;'
    return await conn.fetchval(query, zip_id, species, 1, img_name, confidence, size, pass_id)

async def create_passport_record(conn: asyncpg.Connection, image_preview_path: str, species: str, age: int, gender: str, cords_id: int, embedding: str, name: str) -> int:
    query = 'INSERT INTO Passports (image_preview, type, age, gender, cords_id, embanding, name) VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING id;'
    return await conn.fetchval(query, image_preview_path, species, age, gender, cords_id, embedding, name)

async def link_output_to_passport(conn: asyncpg.Connection, output_id: int, passport_id: int):
    query = 'INSERT INTO Output_Passports (output_id, passport_id) VALUES ($1, $2);'
    await conn.execute(query, output_id, passport_id)

async def create_cords_record(conn: asyncpg.Connection, date: str, coordinates: str, pass_id: Optional[int] = None) -> int:
    query = 'INSERT INTO cords (passport_id, date, coordinates) VALUES ($1, $2, $3) RETURNING id'
    parsed_date = datetime.strptime(date, '%Y-%m-%d').date() if date else datetime.now().date()
    return await conn.fetchval(query, parsed_date, coordinates)

# --- Функции обновления (UPDATE) ---

async def update_passport_cords(conn: asyncpg.Connection, pass_id: int, cords_id: int):
    query = 'UPDATE passports SET cords_id = $1 WHERE id = $2'
    await conn.execute(query, cords_id, pass_id)
