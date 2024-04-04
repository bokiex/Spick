-- Database: `reservation`
--
CREATE DATABASE IF NOT EXISTS `reservation` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `reservation`;

-- ---------------------------------------------------------------- --
--                              reservation TABLE                         --
-- ---------------------------------------------------------------- --
DROP TABLE IF EXISTS `reservation`;
CREATE TABLE IF NOT EXISTS `reservation` (
    `reservation_id` INT PRIMARY KEY AUTO_INCREMENT,
    `user_id` VARCHAR(64) NOT NULL,
    `reservation_name` VARCHAR(64) NOT NULL,
    `reservation_start_time` VARCHAR(33) NOT NULL,
    `reservation_end_time` VARCHAR(33) NOT NULL,
    `reservation_address` VARCHAR(256) NOT NULL
)   ENGINE=InnoDB DEFAULT CHARSET=utf8;