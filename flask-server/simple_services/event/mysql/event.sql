-- Database: `event`
--
CREATE DATABASE IF NOT EXISTS `event` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `event`;

-- ---------------------------------------------------------------- --
--                              EVENT TABLE                         --
-- ---------------------------------------------------------------- --
DROP TABLE IF EXISTS `invitee`;
DROP TABLE IF EXISTS `event`;
CREATE TABLE IF NOT EXISTS `event` (
    `event_id` INT PRIMARY KEY AUTO_INCREMENT,
    `event_name` varchar(64) NOT NULL,
    `event_desc` varchar(256),
    `start_time` timestamp,
    `end_time` timestamp,
    `time_out` timestamp,
    `event_location` varchar(64),
    `user_id` INT
)   ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `invitee` (
    `event_id` INT,
    `user_id` INT,
    `status` varchar(64),
    FOREIGN KEY (event_id) REFERENCES event(event_id)
    PRIMARY KEY (`event_id`, `user_id`)
)   ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `recommendation`;
CREATE TABLE IF NOT EXISTS `recommendation` (
    `recommendation_id` INT AUTO_INCREMENT PRIMARY KEY,
    `recommendation_name` VARCHAR(64) NOT NULL,
    `recommendation_address` VARCHAR(64) NOT NULL,
    `event_id` INT NOT NULL,
    FOREIGN KEY (event_id) REFERENCES event(event_id)

) ENGINE=InnoDB DEFAULT CHARSET=utf8;
