-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS APIDB;

-- Use the created database
USE APIDB;

-- Create the Users table
CREATE TABLE IF NOT EXISTS Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    role VARCHAR(10) DEFAULT 'admin',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);