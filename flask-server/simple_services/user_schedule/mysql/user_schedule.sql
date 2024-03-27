-- Database: `user_schedule`
--
CREATE DATABASE IF NOT EXISTS `user_schedule` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `user_schedule`;

-- ------------------------------------------------------------------
--                          USER SCHEDULE TABLE
-- ------------------------------------------------------------------
DROP TABLE IF EXISTS `user_schedule`;
CREATE TABLE IF NOT EXISTS `user_schedule` (
  `schedule_id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `event_id` VARCHAR(6) NOT NULL,
  `user_id` INT NOT NULL,
  `start_time` DATETIME NOT NULL,
  `end_time` DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
