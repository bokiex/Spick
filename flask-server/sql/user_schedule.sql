-- Database: `user`
--
CREATE DATABASE IF NOT EXISTS `user_schedule` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `user_schedule`;

-- ---------------------------------------------------------------- --
--                     NOTIFICATION TABLE                        --
-- ---------------------------------------------------------------- --
DROP TABLE IF EXISTS `user_schedule`;
CREATE TABLE IF NOT EXISTS `user_schedule` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `eventID` INT NOT NULL,
    `userID` INT NOT NULL,
    `start_time` DATETIME NOT NULL,
    `end_time` DATETIME NOT NULL,
    `reason` VARCHAR(255),
    CONSTRAINT fk_user_schedule_event_id FOREIGN KEY (`eventID`) REFERENCES event(`eventID`),
    CONSTRAINT fk_user_schedule_user_id FOREIGN KEY (`userID`) REFERENCES user(`userID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

