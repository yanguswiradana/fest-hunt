-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               8.0.42 - MySQL Community Server - GPL
-- Server OS:                    Win64
-- HeidiSQL Version:             12.10.0.7000
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for db_konser_tiket
CREATE DATABASE IF NOT EXISTS `db_konser_tiket` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `db_konser_tiket`;

-- Dumping structure for table db_konser_tiket.konser
CREATE TABLE IF NOT EXISTS `konser` (
  `nama` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `harga` int NOT NULL,
  `gambar` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `band` text COLLATE utf8mb4_unicode_ci,
  `deskripsi` text COLLATE utf8mb4_unicode_ci,
  `tanggal_waktu` datetime DEFAULT NULL,
  PRIMARY KEY (`nama`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data exporting was unselected.

-- Dumping structure for table db_konser_tiket.pembeli
CREATE TABLE IF NOT EXISTS `pembeli` (
  `id` varchar(8) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nama` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `telepon` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data exporting was unselected.

-- Dumping structure for table db_konser_tiket.tiket
CREATE TABLE IF NOT EXISTS `tiket` (
  `nomor_tiket` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nama_konser` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` enum('Tersedia','Terjual') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'Tersedia',
  PRIMARY KEY (`nomor_tiket`),
  KEY `nama_konser` (`nama_konser`),
  CONSTRAINT `tiket_ibfk_1` FOREIGN KEY (`nama_konser`) REFERENCES `konser` (`nama`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data exporting was unselected.

-- Dumping structure for table db_konser_tiket.transaksi
CREATE TABLE IF NOT EXISTS `transaksi` (
  `id_transaksi` varchar(8) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nomor_tiket` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `id_pembeli` varchar(8) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `nama_konser` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `tanggal` date NOT NULL,
  `harga_transaksi` int NOT NULL,
  PRIMARY KEY (`id_transaksi`),
  UNIQUE KEY `nomor_tiket` (`nomor_tiket`),
  KEY `id_pembeli` (`id_pembeli`),
  CONSTRAINT `transaksi_ibfk_1` FOREIGN KEY (`nomor_tiket`) REFERENCES `tiket` (`nomor_tiket`),
  CONSTRAINT `transaksi_ibfk_2` FOREIGN KEY (`id_pembeli`) REFERENCES `pembeli` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data exporting was unselected.

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
