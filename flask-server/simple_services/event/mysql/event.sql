-- Database: `event`
--
CREATE DATABASE IF NOT EXISTS `event` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `event`;

-- ---------------------------------------------------------------- --
--                              EVENT TABLE                         --
-- ---------------------------------------------------------------- --
DROP TABLE IF EXISTS `invitee`;
DROP TABLE IF EXISTS `image`;
DROP TABLE IF EXISTS `recommendation`;
DROP TABLE IF EXISTS `event`;
CREATE TABLE IF NOT EXISTS `event` (
    `event_id` varchar(6) PRIMARY KEY,
    `event_name` varchar(64) NOT NULL,
    `event_desc` varchar(256),
    `image` varchar(1024),
    `datetime_start` timestamp,
    `datetime_end` timestamp,
    `time_out` timestamp,
    `reservation_name` varchar(64),
    `reservation_address` varchar(64),
    `event_location` varchar(64),
    `user_id` INT
)   ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `invitee` (
    `event_id` varchar(6) NOT NULL,
    `user_id` INT,
    `status` varchar(6),
    FOREIGN KEY (event_id) REFERENCES event(event_id),
    PRIMARY KEY (`event_id`, `user_id`)
)   ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS `recommendation` (
    `recommendation_id` INT AUTO_INCREMENT PRIMARY KEY,
    `recommendation_name` VARCHAR(256) NOT NULL,
    `recommendation_address` VARCHAR(256) NOT NULL,
    `event_id` varchar(6) NOT NULL,
    FOREIGN KEY (event_id) REFERENCES event(event_id)

) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `Optimized` (
    `event_id` VARCHAR(6) NOT NULL,
    `attendee_id` INT, 
    `start_time` timestamp,
    `end_time` timestamp,
    PRIMARY KEY (`event_id`, `attendee_id`,`start_time`,`end_time`)
)   ENGINE=InnoDB DEFAULT CHARSET=utf8;