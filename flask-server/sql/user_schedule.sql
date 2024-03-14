-- Database: `user_schedule`
--
CREATE DATABASE IF NOT EXISTS `user_schedule` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `user_schedule`;

-- ---------------------------------------------------------------- --
--                     USER SCHEDULE TABLE                        --
-- ---------------------------------------------------------------- --
DROP TABLE IF EXISTS `user_schedule`;
CREATE TABLE IF NOT EXISTS `user_schedule` (
  `scheduleID` INT AUTO_INCREMENT PRIMARY KEY,
  `eventID` INT NOT NULL,
  `userID` INT NOT NULL,
  `weekday` CHAR NOT NULL,
  `start_time` DATETIME NOT NULL,
  `end_time` DATETIME NOT NULL,
  `reason` VARCHAR(255)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

