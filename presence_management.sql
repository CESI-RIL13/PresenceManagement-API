-- --------------------------------------------------------
-- Hôte:                         127.0.0.1
-- Version du serveur:           5.6.17 - MySQL Community Server (GPL)
-- Serveur OS:                   Win64
-- HeidiSQL Version:             9.1.0.4867
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Export de la structure de la base pour presence_management
CREATE DATABASE IF NOT EXISTS `presence_management` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `presence_management`;


-- Export de la structure de table presence_management. presence
CREATE TABLE IF NOT EXISTS `presence` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` datetime NOT NULL,
  `user_id` varchar(255) NOT NULL,
  `archived` tinyint(1) DEFAULT '0',
  `updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Export de données de la table presence_management.presence: ~0 rows (environ)
DELETE FROM `presence`;
/*!40000 ALTER TABLE `presence` DISABLE KEYS */;
/*!40000 ALTER TABLE `presence` ENABLE KEYS */;


-- Export de la structure de table presence_management. promotion
CREATE TABLE IF NOT EXISTS `promotion` (
  `id` varchar(255) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `late` int(11) DEFAULT '15',
  `archived` tinyint(1) DEFAULT '0',
  `upadted` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Export de données de la table presence_management.promotion: ~0 rows (environ)
DELETE FROM `promotion`;
/*!40000 ALTER TABLE `promotion` DISABLE KEYS */;
/*!40000 ALTER TABLE `promotion` ENABLE KEYS */;


-- Export de la structure de table presence_management. room
CREATE TABLE IF NOT EXISTS `room` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `raspberry_id` varchar(255) DEFAULT NULL COMMENT 'adresse MAC du raspberry client',
  `token` varchar(255) DEFAULT NULL,
  `archived` tinyint(1) DEFAULT '0',
  `updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `raspberry_id_UNIQUE` (`raspberry_id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8;

-- Export de données de la table presence_management.room: ~0 rows (environ)
DELETE FROM `room`;
/*!40000 ALTER TABLE `room` DISABLE KEYS */;
INSERT INTO `room` (`id`, `name`, `raspberry_id`, `token`, `archived`, `updated`) VALUES
	(2, 'Cap-Ferret', '$5$rounds=117455$YktEuVqjoa7K6ZtK$c/rIirc1L552f/zoRqulhFHnQHtgtTOiV4QPKM1PNn8', NULL, 0, '2015-04-14 14:44:20');
/*!40000 ALTER TABLE `room` ENABLE KEYS */;


-- Export de la structure de table presence_management. scheduling
CREATE TABLE IF NOT EXISTS `scheduling` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_start` datetime NOT NULL,
  `date_end` datetime NOT NULL,
  `promotion_id` varchar(255) NOT NULL,
  `room_id` int(11) NOT NULL,
  `user_id` varchar(255) DEFAULT NULL,
  `course` varchar(255) DEFAULT NULL,
  `archived` tinyint(1) DEFAULT '0',
  `updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=171 DEFAULT CHARSET=utf8;

-- Export de données de la table presence_management.scheduling: ~0 rows (environ)
DELETE FROM `scheduling`;
/*!40000 ALTER TABLE `scheduling` DISABLE KEYS */;
/*!40000 ALTER TABLE `scheduling` ENABLE KEYS */;


-- Export de la structure de table presence_management. user
CREATE TABLE IF NOT EXISTS `user` (
  `id` varchar(255) NOT NULL,
  `fullname` varchar(255) DEFAULT NULL,
  `mail` varchar(255) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `role` enum('SA','Ingénieur formation','assistant','intervenant','stagiaire') NOT NULL,
  `archived` tinyint(1) DEFAULT '0',
  `updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `qrcode` blob,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Export de données de la table presence_management.user: ~0 rows (environ)
DELETE FROM `user`;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` (`id`, `fullname`, `mail`, `password`, `role`, `archived`, `updated`, `qrcode`) VALUES
	('1', 'Super Admin', 'sadmin@cesi.fr', '$5$rounds=99705$djyPeBTnTjtkwpc1$FTGH4WEKesmauw3MF0qhdPwpMQ72j/EX1sT/Banfso0', 'SA', 0, '2015-04-14 15:28:06', NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;


-- Export de la structure de table presence_management. user_has_promotion
CREATE TABLE IF NOT EXISTS `user_has_promotion` (
  `user_id` varchar(255) NOT NULL,
  `promotion_id` varchar(255) NOT NULL,
  `current` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`user_id`,`promotion_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Export de données de la table presence_management.user_has_promotion: ~0 rows (environ)
DELETE FROM `user_has_promotion`;
/*!40000 ALTER TABLE `user_has_promotion` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_has_promotion` ENABLE KEYS */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
