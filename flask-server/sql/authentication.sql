-- Database: `authentication`
--
CREATE DATABASE IF NOT EXISTS `authentication` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `authentication`;

-- ---------------------------------------------------------------- --
--                     Authentication TABLE                        --
-- ---------------------------------------------------------------- --
DROP TABLE IF EXISTS `authentication`;
CREATE TABLE IF NOT EXISTS `authentication` (
  `userID` INT AUTO_INCREMENT PRIMARY KEY,
  `username` varchar(64) UNIQUE NOT NULL,
  `email` VARCHAR(120) UNIQUE NOT NULL,
  `password_hash` varchar(128)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;