-- phpMyAdmin SQL Dump
-- version 4.0.4
-- http://www.phpmyadmin.net
--
-- Client: localhost
-- Généré le: Lun 09 Mars 2015 à 16:05
-- Version du serveur: 5.6.12-log
-- Version de PHP: 5.4.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de données: `presence_management`
--
CREATE DATABASE IF NOT EXISTS `presence_management` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `presence_management`;

-- --------------------------------------------------------

--
-- Structure de la table `presence`
--

CREATE TABLE IF NOT EXISTS `presence` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` datetime NOT NULL,
  `user_id` varchar(255) NOT NULL,
  `updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
<<<<<<< HEAD
  KEY `fk_presence_user1_idx` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=7 ;

--
-- Contenu de la table `presence`
--
=======
  KEY `fk_presence_user1_idx` (`user_id`),
  CONSTRAINT `fk_presence_user1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
<<<<<<< HEAD
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- L'exportation de données n'été pas sélectionné.
=======
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
>>>>>>> e65a8a35a8884e1ef63b5551ff95a0d4f98dcdc8

INSERT INTO `presence` (`id`, `date`, `user_id`, `updated`) VALUES
<<<<<<< HEAD
(1, '2015-03-09 14:19:18', '1234567890', '2015-03-09 13:19:24'),
(2, '2015-03-09 14:19:29', 'befg', '2015-03-09 13:19:34'),
(3, '2015-03-09 14:53:11', 'test', '2015-03-09 13:53:17'),
(4, '2015-03-09 14:34:19', '1234567890', '2015-03-09 15:37:46'),
(5, '2015-03-09 14:34:19', '1234567890', '2015-03-09 15:38:21'),
(6, '2015-03-09 14:34:19', '1234567890', '2015-03-09 15:40:37');

-- --------------------------------------------------------
=======
	(1, '2015-03-09 14:19:18', '1234567890', '2015-03-09 14:19:24'),
	(2, '2015-03-09 14:19:29', 'befg', '2015-03-09 14:19:34'),
	(3, '2015-03-09 14:53:11', 'test', '2015-03-09 14:53:17'),
	(4, '2015-03-09 14:34:19', '1234567890', '2015-03-09 16:37:46'),
	(5, '2015-03-09 14:34:19', '1234567890', '2015-03-09 16:38:21'),
	(6, '2015-03-09 14:34:19', '1234567890', '2015-03-09 16:40:37');
/*!40000 ALTER TABLE `presence` ENABLE KEYS */;
>>>>>>> c4d3a43da8906fbc94296bb9408ab5a737a84598
>>>>>>> e65a8a35a8884e1ef63b5551ff95a0d4f98dcdc8

--
-- Structure de la table `promotion`
--

CREATE TABLE IF NOT EXISTS `promotion` (
  `id` varchar(255) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `late` int(11) DEFAULT '15',
  `upadted` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

<<<<<<< HEAD
--
-- Contenu de la table `promotion`
--

INSERT INTO `promotion` (`id`, `name`, `late`, `upadted`) VALUES
('BO30440', 'RIL13', 15, '2015-02-25 14:34:03'),
('BO30441', 'RARE13', 15, '2015-03-09 10:06:30');
=======
<<<<<<< HEAD
-- L'exportation de données n'été pas sélectionné.
=======
-- Export de données de la table presence_management.promotion: ~2 rows (environ)
/*!40000 ALTER TABLE `promotion` DISABLE KEYS */;
INSERT INTO `promotion` (`id`, `name`, `late`, `upadted`) VALUES
	('BO30440', 'RIL13', 15, '2015-02-25 15:34:03'),
	('BO30441', 'RARE13', 15, '2015-03-09 11:06:30');
/*!40000 ALTER TABLE `promotion` ENABLE KEYS */;
>>>>>>> c4d3a43da8906fbc94296bb9408ab5a737a84598
>>>>>>> e65a8a35a8884e1ef63b5551ff95a0d4f98dcdc8

-- --------------------------------------------------------

--
-- Structure de la table `room`
--

CREATE TABLE IF NOT EXISTS `room` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `raspberry_id` varchar(255) DEFAULT NULL COMMENT 'adresse MAC du raspberry client',
  `token` varchar(255) DEFAULT NULL,
  `updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `raspberry_id_UNIQUE` (`raspberry_id`)
<<<<<<< HEAD
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=8 ;

--
-- Contenu de la table `room`
--
=======
<<<<<<< HEAD
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- L'exportation de données n'été pas sélectionné.
=======
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
>>>>>>> e65a8a35a8884e1ef63b5551ff95a0d4f98dcdc8

INSERT INTO `room` (`id`, `name`, `raspberry_id`, `token`, `updated`) VALUES
<<<<<<< HEAD
(1, 'Cap Ferret', 'DNZ867DZAD7AZ', NULL, '2015-02-26 10:55:23'),
(2, 'BORDEAUX', NULL, NULL, '2015-02-26 15:12:46'),
(3, 'LACANAU', 'AGIGS657DSBO', NULL, '2015-02-26 16:01:00'),
(6, 'LACANAU', 'AGIGS657DS', NULL, '2015-02-26 16:04:28'),
(7, 'LACANAUX', 'AGIGS657DSzqdzqdqz', NULL, '2015-02-26 16:06:13');

-- --------------------------------------------------------
=======
	(1, 'Cap Ferret', 'DNZ867DZAD7AZ', NULL, '2015-02-26 11:55:23'),
	(2, 'BORDEAUX', NULL, NULL, '2015-02-26 16:12:46'),
	(3, 'LACANAU', 'AGIGS657DSBO', NULL, '2015-02-26 17:01:00'),
	(6, 'LACANAU', 'AGIGS657DS', NULL, '2015-02-26 17:04:28'),
	(7, 'LACANAUX', 'AGIGS657DSzqdzqdqz', NULL, '2015-02-26 17:06:13');
/*!40000 ALTER TABLE `room` ENABLE KEYS */;
>>>>>>> c4d3a43da8906fbc94296bb9408ab5a737a84598
>>>>>>> e65a8a35a8884e1ef63b5551ff95a0d4f98dcdc8

--
-- Structure de la table `scheduling`
--

CREATE TABLE IF NOT EXISTS `scheduling` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_start` datetime NOT NULL,
  `date_end` datetime DEFAULT NULL,
  `room_id` int(11) NOT NULL,
  `promotion_id` varchar(255) NOT NULL,
  `user_id` varchar(255) NOT NULL,
  `updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_scheduling_promotion1_idx` (`promotion_id`),
  KEY `fk_scheduling_user1_idx` (`user_id`),
<<<<<<< HEAD
  KEY `fk_scheduling_room1_idx` (`room_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=7 ;

--
-- Contenu de la table `scheduling`
--

INSERT INTO `scheduling` (`id`, `date_start`, `date_end`, `room_id`, `promotion_id`, `user_id`, `updated`) VALUES
(2, '2015-03-09 08:30:00', '2015-03-09 12:30:00', 1, 'BO30440', '1234567891', '2015-03-09 10:00:57'),
(3, '2015-03-09 13:30:00', '2015-03-09 17:30:00', 1, 'BO30440', '1234567891', '2015-03-09 10:01:18'),
(5, '2015-03-09 08:30:00', '2015-03-09 12:30:00', 3, 'BO30441', 'test', '2015-03-09 10:07:50'),
(6, '2015-03-09 13:30:00', '2015-03-09 17:30:00', 3, 'BO30441', 'test', '2015-03-09 10:07:42');

-- --------------------------------------------------------
=======
  KEY `fk_scheduling_room1_idx` (`room_id`),
  CONSTRAINT `fk_scheduling_user1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_scheduling_promotion1` FOREIGN KEY (`promotion_id`) REFERENCES `promotion` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_scheduling_room1` FOREIGN KEY (`room_id`) REFERENCES `room` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
<<<<<<< HEAD
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- L'exportation de données n'été pas sélectionné.
=======
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- Export de données de la table presence_management.scheduling: ~4 rows (environ)
/*!40000 ALTER TABLE `scheduling` DISABLE KEYS */;
INSERT INTO `scheduling` (`id`, `date_start`, `date_end`, `room_id`, `promotion_id`, `user_id`, `updated`) VALUES
	(2, '2015-03-09 08:30:00', '2015-03-09 12:30:00', 1, 'BO30440', '1234567891', '2015-03-09 11:00:57'),
	(3, '2015-03-09 13:30:00', '2015-03-09 17:30:00', 1, 'BO30440', '1234567891', '2015-03-09 11:01:18'),
	(5, '2015-03-09 08:30:00', '2015-03-09 12:30:00', 3, 'BO30441', 'test', '2015-03-09 11:07:50'),
	(6, '2015-03-09 13:30:00', '2015-03-09 17:30:00', 3, 'BO30441', 'test', '2015-03-09 11:07:42');
/*!40000 ALTER TABLE `scheduling` ENABLE KEYS */;
>>>>>>> c4d3a43da8906fbc94296bb9408ab5a737a84598
>>>>>>> e65a8a35a8884e1ef63b5551ff95a0d4f98dcdc8

--
-- Structure de la table `user`
--

CREATE TABLE IF NOT EXISTS `user` (
  `id` varchar(255) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `firstname` varchar(255) DEFAULT NULL,
  `mail` varchar(255) NOT NULL,
  `promotion_id` varchar(255) DEFAULT NULL,
  `updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_user_promotion_idx` (`promotion_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

<<<<<<< HEAD
--
-- Contenu de la table `user`
--

INSERT INTO `user` (`id`, `name`, `firstname`, `mail`, `promotion_id`, `updated`) VALUES
('1234567890', 'DOS SANTOS', 'Julien', 'julien.dossantos@viacesi.fr', 'BO30440', '2015-02-25 14:34:29'),
('1234567891', 'TOUCHARD', 'Benjamin', 'benjamin.touchard@viacesi.fr', NULL, '2015-03-09 12:52:06'),
('1433361', 'LORGERIE', 'DENIS', 'denis.lorgerie@viacesi.fr', 'BO30440', '2015-03-09 14:32:50'),
('befg', 'HERMEL', 'Nicolas', 'hermelnico@gmail.com', 'BO30440', '2015-02-26 16:32:22'),
('BHDZBH', 'HERMEL', NULL, 'jjjj@viacesi.fr', NULL, '2015-03-09 15:21:56'),
('BHDZBHDZBAJHDZA', 'HERMEL', NULL, 'jjjj@viacesi.fr', NULL, '2015-03-09 15:21:56'),
('test', 'TEST', 'TEST', 'test@viacesi.fr', 'BO30441', '2015-03-09 13:54:12');

--
-- Contraintes pour les tables exportées
--

--
-- Contraintes pour la table `presence`
--
ALTER TABLE `presence`
  ADD CONSTRAINT `fk_presence_user1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `scheduling`
--
ALTER TABLE `scheduling`
  ADD CONSTRAINT `fk_scheduling_user1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_scheduling_promotion1` FOREIGN KEY (`promotion_id`) REFERENCES `promotion` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_scheduling_room1` FOREIGN KEY (`room_id`) REFERENCES `room` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Contraintes pour la table `user`
--
ALTER TABLE `user`
  ADD CONSTRAINT `fk_user_promotion` FOREIGN KEY (`promotion_id`) REFERENCES `promotion` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

=======
<<<<<<< HEAD
-- L'exportation de données n'été pas sélectionné.
=======
-- Export de données de la table presence_management.user: ~7 rows (environ)
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` (`id`, `name`, `firstname`, `mail`, `promotion_id`, `updated`) VALUES
	('1234567890', 'DOS SANTOS', 'Julien', 'julien.dossantos@viacesi.fr', 'BO30440', '2015-02-25 15:34:29'),
	('1234567891', 'TOUCHARD', 'Benjamin', 'benjamin.touchard@viacesi.fr', NULL, '2015-03-09 13:52:06'),
	('1433361', 'LORGERIE', 'DENIS', 'denis.lorgerie@viacesi.fr', 'BO30440', '2015-03-09 15:32:50'),
	('befg', 'HERMEL', 'Nicolas', 'hermelnico@gmail.com', 'BO30440', '2015-02-26 17:32:22'),
	('BHDZBH', 'HERMEL', NULL, 'jjjj@viacesi.fr', NULL, '2015-03-09 16:21:56'),
	('BHDZBHDZBAJHDZA', 'HERMEL', NULL, 'jjjj@viacesi.fr', NULL, '2015-03-09 16:21:56'),
	('test', 'TEST', 'TEST', 'test@viacesi.fr', 'BO30441', '2015-03-09 14:54:12');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
>>>>>>> c4d3a43da8906fbc94296bb9408ab5a737a84598
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
>>>>>>> e65a8a35a8884e1ef63b5551ff95a0d4f98dcdc8
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
