
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
  `password_hash` VARCHAR(128),
  `telegram_id` VARCHAR(64) UNIQUE,
  `telegram_tag` varchar(64) NOT NULL,
  `image` VARCHAR(256)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `user` (`user_id`, `username`, `email`, `password_hash`, `telegram_tag`, `image`, `telegram_id`) VALUES
(1, 'string', 'string', 'string', 'string', 'https://images.unsplash.com/photo-1492633423870-43d1cd2775eb?&w=128&h=128&dpr=2&q=80', NULL),
(4, 'ssidfng', 'stdfring', 'string', 'string', NULL, NULL),
(3, 'ssidasd', 'stdfng', 'strsng', 'strsng', NULL, NULL),
(5, 'test2', 'std128yuyuihojie', 'pbkdf2:sha256:600000$Ant22xex5VCnUclw$b65776c52241f4a3394e58a264f8d01e8cbf960c9a72399c3d4c36047327432d', '@strsng', NULL, NULL),
(2, 'asdf','asdf@gmail.com', 'pbkdf2:sha256:600000$wuJc5iUSEK6zno34$7dc148975d26ef794afc7c90cae1e1969ceca8aa58c911842cd63fb64a9316f0', '@asdf', 'https://images.unsplash.com/photo-1492633423870-43d1cd2775eb?&w=128&h=128&dpr=2&q=80', NULL);
