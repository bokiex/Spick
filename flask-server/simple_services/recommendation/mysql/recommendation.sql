-- Database: `recommendation`
--
CREATE DATABASE IF NOT EXISTS `recommendation` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `recommendation`;

DROP TABLE IF EXISTS `recommendations`;
CREATE TABLE IF NOT EXISTS `recommendations` (
    `recommendation_id` INT PRIMARY KEY AUTO_INCREMENT,
    `event_id` INT FOREIGN KEY REFERENCES `events`(`event_id`),
    `location_name` varchar(64) NOT NULL,
    `location_desc` varchar(256),
    `latitude` DECIMAL(10, 8),
    `longitude` DECIMAL(11, 8),
)   ENGINE=InnoDB DEFAULT CHARSET=utf8;
