-- Database: `event`
--
CREATE DATABASE IF NOT EXISTS `event` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `event`;

-- ---------------------------------------------------------------- --
--                              EVENT TABLE                         --
-- ---------------------------------------------------------------- --
DROP TABLE IF EXISTS `event`;
CREATE TABLE IF NOT EXISTS `event` (
    `event_id` INT PRIMARY KEY AUTO_INCREMENT,
    `event_name` varchar(64) NOT NULL,
    `start_time` timestamp,
    `end_time` timestamp,
    `event_location` varchar(64)
)   ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO events(event_name, event_location) 
VALUES 
('Picnic', 'Gardens by the Bay'),
('Arcade', 'Suntec City');
