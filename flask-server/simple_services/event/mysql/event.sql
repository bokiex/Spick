-- Database: `event`
CREATE DATABASE IF NOT EXISTS `scheduler` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
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
    `recommendation_photo`  VARCHAR(1024) NOT NULL,
    `event_id` varchar(6) NOT NULL,
    FOREIGN KEY (event_id) REFERENCES event(event_id)

) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `optimized` (
    `event_id` VARCHAR(6) NOT NULL,
    `attendee_id` INT, 
    `start_time` timestamp,
    `end_time` timestamp,
    PRIMARY KEY (`event_id`, `attendee_id`,`start_time`,`end_time`)
)   ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- Dumping data for table `event`
--

INSERT INTO `event` (`event_id`, `event_name`, `event_desc`, `datetime_start`, `datetime_end`, `time_out`, `event_location`, `user_id`, `reservation_name`, `reservation_address`, `image`) VALUES
('GHKBDH', 'next test', 'fuck la', '2024-03-26 10:44:00', '2024-03-27 10:44:00', '2024-03-28 10:44:00', NULL, 5, NULL, NULL, 'image_2024-03-14_19-37-35.png'),
('ICAPVA', 'hahhaa', 'sdsss', '2024-03-27 10:33:00', '2024-03-28 10:33:00', '2024-03-27 10:33:00', NULL, 1, NULL, NULL, 'event.jpg'),
('KKPTMA', 'just another test', 'dont mind me im just testing', '2024-03-26 14:06:00', '2024-03-27 14:06:00', '2024-03-26 14:09:00', NULL, 1, NULL, NULL, 'image_2024-02-18_16-42-40.png'),
('OEOODQ', 'hahhaa', 'sdsss', '2024-03-27 10:33:00', '2024-03-28 10:33:00', '2024-03-27 10:33:00', NULL, 1, NULL, NULL, 'event.jpg'),
('SWJOML', 'this is test', 'just testing for fun only', '2024-03-27 13:46:00', '2024-03-28 13:46:00', '2024-03-26 13:50:00', NULL, 1, NULL, NULL, 'BPAS TO-BE FINALLLLLLLLLLLLLLLLLLL (1) (2).png'),
('SYFZHF', 'asdf', 'sdf', '2024-03-27 21:31:00', '2024-03-28 21:31:00', '2024-03-27 21:31:00', NULL, 1, NULL, NULL, 'image_2024-03-14_19-37-35 (3).png'),
('UATCBT', 'hahhaa', 'sdsss', '2024-03-27 10:33:00', '2024-03-28 10:33:00', '2024-03-27 10:33:00', NULL, 1, NULL, NULL, 'event.jpg'),
('VMIRTT', 'last TEST', 'hopefully this is the last test lol', '2024-03-26 11:27:00', '2024-03-27 11:27:00', '2024-03-28 11:27:00', NULL, 1, NULL, NULL, 'pexels-cottonbro-studio-6624087.jpg'),
('XDMSJF', 'esd ', 'esd meeting', '2024-03-27 21:40:00', '2024-03-28 21:40:00', '2024-03-27 21:40:00', NULL, 1, NULL, NULL, 'image_2024-03-14_19-37-35 (3).png'),
('XUMWIH', 'test your mom', 'test your mother!!!', '2024-03-26 10:41:00', '2024-03-27 10:41:00', '2024-03-28 10:41:00', NULL, 1, NULL, NULL, 'photo_2024-02-05 17.47.15.jpeg'),
('ZWWKDR', 'sdf', 'asdf', '2024-03-26 19:56:00', '2024-03-27 19:56:00', '2024-03-26 19:56:00', NULL, 1, NULL, NULL, 'DALL·E 2024-03-17 16.26.13 - Design a sophisticated and sleek smart fragrance bottle. The bottle is made of high-quality glass with a minimalist shape and smooth lines, showcasing.webp');

-- --------------------------------------------------------
INSERT INTO `invitee` (`event_id`, `user_id`, `status`) VALUES
('GHKBDH', 3, NULL),
('GHKBDH', 5, NULL),
('ICAPVA', 3, NULL),
('KKPTMA', 3, NULL),
('KKPTMA', 4, NULL),
('OEOODQ', 3, NULL),
('SWJOML', 3, NULL),
('SWJOML', 4, NULL),
('SYFZHF', 1, NULL),
('UATCBT', 3, NULL),
('VMIRTT', 1, NULL),
('VMIRTT', 4, NULL),
('XDMSJF', 1, NULL),
('XDMSJF', 3, NULL),
('XUMWIH', 1, NULL),
('XUMWIH', 3, NULL),
('ZWWKDR', 1, NULL),
('ZWWKDR', 4, NULL);

-- --------------------------------------------------------

