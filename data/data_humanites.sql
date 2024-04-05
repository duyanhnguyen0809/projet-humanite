-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               11.3.2-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.6.0.6765
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for projet_humanite
CREATE DATABASE IF NOT EXISTS `projet_humanite` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `projet_humanite`;

-- Dumping structure for table projet_humanite.communes
CREATE TABLE IF NOT EXISTS `communes` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `nom` varchar(50) NOT NULL,
  `url` varchar(2048) DEFAULT NULL,
  `lat` double DEFAULT NULL,
  `lon` double DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=111 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table projet_humanite.creations
CREATE TABLE IF NOT EXISTS `creations` (
  `id_com_cree` int(10) unsigned NOT NULL,
  `id_com_affectee` int(10) unsigned NOT NULL,
  `mode` varchar(50) NOT NULL,
  `date` date NOT NULL,
  KEY `FK_creations_communes` (`id_com_cree`) USING BTREE,
  KEY `FK_creations_communes_2` (`id_com_affectee`) USING BTREE,
  CONSTRAINT `FK_creations_communes` FOREIGN KEY (`id_com_cree`) REFERENCES `communes` (`id`),
  CONSTRAINT `FK_creations_communes_2` FOREIGN KEY (`id_com_affectee`) REFERENCES `communes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table projet_humanite.fusions
CREATE TABLE IF NOT EXISTS `fusions` (
  `id_nouv_com` int(10) unsigned NOT NULL,
  `id_reuni_com` int(10) unsigned NOT NULL,
  `date` date NOT NULL,
  KEY `FK__communes` (`id_nouv_com`) USING BTREE,
  KEY `FK__communes_2` (`id_reuni_com`) USING BTREE,
  CONSTRAINT `FK__communes` FOREIGN KEY (`id_nouv_com`) REFERENCES `communes` (`id`),
  CONSTRAINT `FK__communes_2` FOREIGN KEY (`id_reuni_com`) REFERENCES `communes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Data exporting was unselected.

-- Dumping structure for table projet_humanite.modifications
CREATE TABLE IF NOT EXISTS `modifications` (
  `id_ancien` int(10) unsigned NOT NULL,
  `id_nouveau` int(10) unsigned NOT NULL,
  `date` date NOT NULL,
  KEY `FK_modifications_communes` (`id_ancien`),
  KEY `FK_modifications_communes_2` (`id_nouveau`),
  CONSTRAINT `FK_modifications_communes` FOREIGN KEY (`id_ancien`) REFERENCES `communes` (`id`),
  CONSTRAINT `FK_modifications_communes_2` FOREIGN KEY (`id_nouveau`) REFERENCES `communes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Data exporting was unselected.

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
