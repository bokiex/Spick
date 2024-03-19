CREATE DATABASE IF NOT EXISTS counter;
USE counter;

CREATE TABLE IF NOT EXISTS eventstatus (
    token VARCHAR(6) PRIMARY KEY,
    total_invitees INT NOT NULL,
    current_responses INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS responses (
    responseid INT AUTO_INCREMENT PRIMARY KEY,
    token VARCHAR(6),
    userID INT,
    UNIQUE(token, userID),
    FOREIGN KEY (token) REFERENCES eventstatus(token)
);
