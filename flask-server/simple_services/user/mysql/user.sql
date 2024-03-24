-- Database: `user`
--
CREATE DATABASE IF NOT EXISTS `user` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `user`;

-- ---------------------------------------------------------------- --
--                     USER TABLE                        --
-- ---------------------------------------------------------------- --
DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `user_id` INT AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(64) UNIQUE NOT NULL,
  `email` VARCHAR(120) UNIQUE NOT NULL,
  `password` VARCHAR(128),
  `telegram_id` VARCHAR(64) UNIQUE
  `telegram_tag` varchar(64) NOT NULL
  -- PRIMARY KEY (`chatid`)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- INSERT INTO notification(chatid,telegramtag) 
-- VALUES 
-- ('121187187', '@bokyannn'),
-- ('788802319', '@hotatementai');
