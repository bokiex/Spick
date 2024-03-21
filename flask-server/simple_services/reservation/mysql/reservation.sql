-- Database: `reservations`
--
CREATE DATABASE IF NOT EXISTS `reservations` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `reservations`;

-- ---------------------------------------------------------------- --
--                              reservations TABLE                         --
-- ---------------------------------------------------------------- --
DROP TABLE IF EXISTS `reservations`;
CREATE TABLE IF NOT EXISTS `reservations` (
    `reservation_id` INT PRIMARY KEY AUTO_INCREMENT,
    `user_id` VARCHAR(64) NOT NULL,
    `address` VARCHAR(256) NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  
)   ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO reservations(user_id, location_lat, location_long) 
VALUES 
(1, 1.123, 1.123),
(2, 2.123, 2.123);
