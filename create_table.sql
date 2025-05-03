CREATE DATABASE Hand_detection;
USE Hand_detection;
CREATE TABLE hand_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    message VARCHAR(255) NOT NULL
);
