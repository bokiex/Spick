-- Database: `event`
CREATE DATABASE IF NOT EXISTS `scheduler` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
CREATE DATABASE IF NOT EXISTS `event` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `event`;

-- ---------------------------------------------------------------- --
--                              EVENT TABLE                         --
-- ---------------------------------------------------------------- --
DROP TABLE IF EXISTS `invitee`;
DROP TABLE IF EXISTS `image`;
DROP TABLE IF EXISTS `recommendations`;
DROP TABLE IF EXISTS `event`;
CREATE TABLE IF NOT EXISTS `event` (
    `event_id` varchar(6) PRIMARY KEY,
    `event_name` varchar(64) NOT NULL,
    `event_desc` varchar(256),
    `image` varchar(1024),
    `datetime_start` varchar(33),
    `datetime_end` varchar(33),
    `time_out` varchar(33),
    `reservation_name` varchar(64),
    `reservation_address` varchar(64),
    `user_id` INT
)   ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `invitee` (
    `event_id` varchar(6) NOT NULL,
    `user_id` INT,
    `status` varchar(6),
    FOREIGN KEY (event_id) REFERENCES event(event_id),
    PRIMARY KEY (`event_id`, `user_id`)
)   ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS `recommendations` (
    `recommendation_id` INT AUTO_INCREMENT PRIMARY KEY,
    `recommendation_name` VARCHAR(256) NOT NULL,
    `recommendation_address` VARCHAR(256) NOT NULL,
    `recommendation_photo`  VARCHAR(1024) NOT NULL,
    `event_id` varchar(6) NOT NULL,
    FOREIGN KEY (event_id) REFERENCES event(event_id)

) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `optimized` (
    `event_id` VARCHAR(6) NOT NULL,
    `attendee_id` INT, 
    `start_time` varchar(33),
    `end_time` varchar(33),
    PRIMARY KEY (`event_id`, `attendee_id`,`start_time`,`end_time`)
)   ENGINE=InnoDB DEFAULT CHARSET=utf8;



