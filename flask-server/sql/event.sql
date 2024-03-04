-- Database: `event`
--
CREATE DATABASE IF NOT EXISTS `event` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `event`;

-- ---------------------------------------------------------------- --
--                              EVENT TABLE                         --
-- ---------------------------------------------------------------- --
DROP TABLE IF EXISTS `event`;
CREATE TABLE IF NOT EXISTS `event` (
    `eventID` INT PRIMARY KEY AUTO_INCREMENT,
    `eventName` varchar(64) NOT NULL,
    `startTime` timestamp,
    `endTime` timestamp,
    `eventLocation` varchar(64)
)   ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO events(eventName, eventLocation) 
VALUES 
('Picnic', 'Gardens by the Bay'),
('Arcade', 'Suntec City');
