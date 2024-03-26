-- Database: `user_schedule`
--
CREATE DATABASE IF NOT EXISTS `user_schedule` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `user_schedule`;

-- ------------------------------------------------------------------
--                          USER SCHEDULE TABLE
-- ------------------------------------------------------------------
DROP TABLE IF EXISTS `user_schedule`;
CREATE TABLE IF NOT EXISTS `user_schedule` (
  `schedule_id` INT AUTO_INCREMENT PRIMARY KEY,
  `event_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `start_time` DATETIME NOT NULL,
  `end_time` DATETIME NOT NULL,
  PRIMARY KEY (`event_id`,`user_id`,`start_time`,`end_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
