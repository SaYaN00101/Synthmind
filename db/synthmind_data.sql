CREATE DATABASE IF NOT EXISTS synthmind_AI_DB;
USE synthmind_AI_DB;

CREATE TABLE user_data (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(250),
    Age INT,
    Gender VARCHAR(30),
    Country VARCHAR(150),
    City VARCHAR(250),
    UserID VARCHAR(100) UNIQUE,
    password VARCHAR(100),
    RegisteredAt DATETIME
);

CREATE TABLE chat_history (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    UserID VARCHAR(100),
    messege_role ENUM('user', 'assistant'),
    message_content LONGTEXT,
    DateTime DATETIME DEFAULT CURRENT_TIMESTAMP,
    Session_ID VARCHAR(100),
    Session_Title VARCHAR(250)
);
