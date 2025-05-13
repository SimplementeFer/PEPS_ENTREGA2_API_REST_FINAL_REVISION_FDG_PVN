CREATE DATABASE IF NOT EXISTS reviews_db;
USE reviews_db;

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    perfil VARCHAR(20) DEFAULT 'user', -- puede ser 'user' o 'admin'
    estado VARCHAR(20) DEFAULT 'activo', -- puede ser 'activo' o 'bloqueado'
    numeroAccesosErroneo INT DEFAULT 0,
    fechaUltimoAcceso DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de juegos
CREATE TABLE IF NOT EXISTS juegos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
