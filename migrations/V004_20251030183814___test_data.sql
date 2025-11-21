INSERT INTO model (first_name, last_name, phone, email) VALUES 
('Анна', 'Иванова', '+79011234567', 'anna.i@test.com'),
('Виктор', 'Петров', '+79022345678', 'viktor.p@test.com'),
('Екатерина', 'Смирнова', '+79033456789', 'katya.s@test.com'),
('Дмитрий', 'Козлов', '+79044567890', 'dmitry.k@test.com'),
('Ольга', 'Васильева', '+79055678901', 'olga.v@test.com');

INSERT INTO photographer (first_name, last_name, camera, email, phone, rating) VALUES 
('Игорь', 'Соколов', 'Canon R6', 'igor.sokolov@ph.com', '+78001112233', 5),
('Мария', 'Лебедева', 'Sony A7III', 'maria.l@ph.com', '+78002223344', 4),
('Алексей', 'Морозов', 'Nikon D850', 'alexey.m@ph.com', '+78003334455', NULL),
('Светлана', 'Новикова', 'Fuji XT4', 'sveta.n@ph.com', '+78004445566', 3),
('Павел', 'Зайцев', 'Canon 5D', 'pavel.z@ph.com', '+78005556677', 4);

INSERT INTO photosession (model_id, photographer_id, location, rating) VALUES 
(1, 1, 'Киев, Студия Loft', 5), 
(2, 3, 'Одеса, Набережная', NULL), 
(3, 2, 'Львов, Лето', 4), 
(4, 4, 'Одеса, Пляж', 3),
(5, 1, 'Киев, Праздник', 5);

INSERT INTO photo (photosession_id, camera, file_path, lens, iso) VALUES 
(1, 'Canon R6', '/photos/ps1/img_001.jpg', 'RF 85mm', 100),
(1, 'Canon R6', '/photos/ps1/img_002.jpg', 'RF 35mm', 200),
(3, 'Sony A7III', '/photos/ps3/img_003.jpg', 'Sony 50mm', 400),
(4, 'Fuji XT4', '/photos/ps4/img_004.jpg', 'Fuji 18-55', 800),
(5, NULL, '/photos/ps5/img_005.jpg', NULL, 1600);