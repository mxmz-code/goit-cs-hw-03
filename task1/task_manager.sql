-- Створення бази даних
CREATE DATABASE task_manager;

-- Перехід до створеної бази даних
\c task_manager;

-- Створення таблиці користувачів
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Створення таблиці статусів
CREATE TABLE status (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Додавання статусів у таблицю status
INSERT INTO status (name) VALUES ('new'), ('in progress'), ('completed');

-- Створення таблиці завдань
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status_id INTEGER REFERENCES status(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);
