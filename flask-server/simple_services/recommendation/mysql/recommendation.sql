-- Database: `recommendation`
--
CREATE DATABASE IF NOT EXISTS `recommendation` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `recommendation`;

DROP TABLE IF EXISTS `recommendations`;
CREATE TABLE IF NOT EXISTS `recommendations` (
    `recommendation_id` INT PRIMARY KEY AUTO_INCREMENT,
    `event_id` INT FOREIGN KEY REFERENCES `events`(`event_id`),
    `recommendation_name` varchar(64) NOT NULL,
    `recommendation_address` varchar(256),
)   ENGINE=InnoDB DEFAULT CHARSET=utf8;
