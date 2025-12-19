-- Створення схеми
CREATE SCHEMA IF NOT EXISTS "HR";

-- 1. Таблиця моделей
CREATE TABLE "HR".model (
    model_id SERIAL PRIMARY KEY,
    first_name character varying(50) NOT NULL,
    last_name character varying(50) NOT NULL,
    phone character varying(20) NOT NULL,
    email character varying(100) UNIQUE NOT NULL
);

-- 2. Таблиця фотографів
CREATE TABLE "HR".photographer (
    photographer_id SERIAL PRIMARY KEY,
    first_name character varying(50) NOT NULL,
    last_name character varying(50) NOT NULL,
    camera character varying(50),
    email character varying(100) UNIQUE NOT NULL,
    phone character varying(20) NOT NULL,
    rating integer CHECK (
        rating >= 1
        AND rating <= 5
    )
);

-- 3. Таблиця фотосесій
CREATE TABLE "HR".photosession (
    photosession_id SERIAL PRIMARY KEY,
    model_id integer NOT NULL REFERENCES "HR".model (model_id) ON DELETE CASCADE,
    photographer_id integer NOT NULL REFERENCES "HR".photographer (photographer_id) ON DELETE CASCADE,
    location character varying(100),
    rating integer CHECK (
        rating >= 1
        AND rating <= 5
    )
);

-- 4. Таблиця фотографій
CREATE TABLE "HR".photo (
    photo_id SERIAL PRIMARY KEY,
    photosession_id integer NOT NULL REFERENCES "HR".photosession (photosession_id) ON DELETE CASCADE,
    camera character varying(50),
    file_path character varying(255) UNIQUE NOT NULL,
    lens character varying(50),
    iso integer
);

-- Додавання Flyway (якщо ви його використовуєте, якщо ні — можна видалити)
CREATE TABLE IF NOT EXISTS "HR".flyway_schema_history (
    installed_rank integer NOT NULL PRIMARY KEY,
    version character varying(50),
    description character varying(200) NOT NULL,
    type character varying(20) NOT NULL,
    script character varying(1000) NOT NULL,
    checksum integer,
    installed_by character varying(100) NOT NULL,
    installed_on timestamp without time zone DEFAULT now() NOT NULL,
    execution_time integer NOT NULL,
    success boolean NOT NULL
);