-- Database: `user`
--
CREATE DATABASE IF NOT EXISTS `user` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `user`;

-- ---------------------------------------------------------------- --
--                     USER TABLE                        --
-- ---------------------------------------------------------------- --
DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `userID` INT AUTO_INCREMENT PRIMARY KEY,
  `telegramtag` varchar(64) NOT NULL,
  PRIMARY KEY (`chatid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO notification(chatid,telegramtag) 
VALUES 
('121187187', '@bokyannn'),
('788802319', '@hotatementai');