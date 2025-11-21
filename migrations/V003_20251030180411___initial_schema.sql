CREATE TABLE model (
    model_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE photographer (
    photographer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    camera VARCHAR(50),
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL,
    rating INT,

    CHECK (rating IS NULL OR (rating >= 1 AND rating <= 5))
);

CREATE TABLE photosession (
    photosession_id SERIAL PRIMARY KEY,
    model_id INT NOT NULL,
    photographer_id INT NOT NULL,
    location VARCHAR(100),
    rating INT,

    FOREIGN KEY (model_id) REFERENCES model(model_id),
    FOREIGN KEY (photographer_id) REFERENCES photographer(photographer_id),

    CHECK (rating IS NULL OR (rating >= 1 AND rating <= 5))
);

CREATE TABLE photo (
    photo_id SERIAL PRIMARY KEY,
    photosession_id INT NOT NULL,
    camera VARCHAR(50),
    file_path VARCHAR(255) NOT NULL UNIQUE,
    lens VARCHAR(50),
    iso INT,

    FOREIGN KEY (photosession_id) REFERENCES photosession(photosession_id)
);

