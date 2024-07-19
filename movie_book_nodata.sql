-- --------------------------------------------------------
-- 호스트:                          127.0.0.1
-- 서버 버전:                        10.4.32-MariaDB - mariadb.org binary distribution
-- 서버 OS:                        Win64
-- HeidiSQL 버전:                  12.7.0.6850
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- 테이블 movie_book.cancellations 구조 내보내기
CREATE TABLE IF NOT EXISTS `cancellations` (
  `cancellation_id` int(11) NOT NULL AUTO_INCREMENT,
  `reservation_id` int(11) DEFAULT NULL,
  `cancellation_time` datetime NOT NULL,
  `refund_amount` decimal(10,2) DEFAULT NULL,
  `reason` text DEFAULT NULL,
  PRIMARY KEY (`cancellation_id`),
  KEY `reservation_id` (`reservation_id`),
  CONSTRAINT `cancellations_ibfk_1` FOREIGN KEY (`reservation_id`) REFERENCES `reservations` (`reservation_id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 movie_book.movies 구조 내보내기
CREATE TABLE IF NOT EXISTS `movies` (
  `movie_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `movie_desc` text DEFAULT NULL,
  `genre` varchar(50) DEFAULT NULL,
  `duration` int(11) NOT NULL,
  `release_date` date DEFAULT NULL,
  `rating` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`movie_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 movie_book.payments 구조 내보내기
CREATE TABLE IF NOT EXISTS `payments` (
  `payment_id` int(11) NOT NULL AUTO_INCREMENT,
  `reservation_id` int(11) DEFAULT NULL,
  `amount` decimal(10,2) NOT NULL,
  `payment_method` varchar(50) DEFAULT NULL,
  `payment_time` datetime NOT NULL,
  PRIMARY KEY (`payment_id`),
  KEY `reservation_id` (`reservation_id`),
  CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`reservation_id`) REFERENCES `reservations` (`reservation_id`)
) ENGINE=InnoDB AUTO_INCREMENT=75 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 movie_book.reservations 구조 내보내기
CREATE TABLE IF NOT EXISTS `reservations` (
  `reservation_id` int(11) NOT NULL AUTO_INCREMENT,
  `showtime_id` int(11) DEFAULT NULL,
  `seat_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `reservation_time` datetime NOT NULL,
  `pay_status` varchar(20) NOT NULL DEFAULT 'unpaid',
  PRIMARY KEY (`reservation_id`),
  KEY `showtime_id` (`showtime_id`),
  KEY `seat_id` (`seat_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `reservations_ibfk_1` FOREIGN KEY (`showtime_id`) REFERENCES `showtimes` (`showtime_id`),
  CONSTRAINT `reservations_ibfk_2` FOREIGN KEY (`seat_id`) REFERENCES `seats` (`seat_id`),
  CONSTRAINT `reservations_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8701 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 movie_book.seats 구조 내보내기
CREATE TABLE IF NOT EXISTS `seats` (
  `seat_id` int(11) NOT NULL AUTO_INCREMENT,
  `theater_id` int(11) DEFAULT NULL,
  `seat_number` varchar(10) NOT NULL,
  `seat_type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`seat_id`),
  KEY `theater_id` (`theater_id`),
  CONSTRAINT `seats_ibfk_1` FOREIGN KEY (`theater_id`) REFERENCES `theaters` (`theater_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3628 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 movie_book.showtimes 구조 내보내기
CREATE TABLE IF NOT EXISTS `showtimes` (
  `showtime_id` int(11) NOT NULL AUTO_INCREMENT,
  `movie_id` int(11) DEFAULT NULL,
  `theater_id` int(11) DEFAULT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  PRIMARY KEY (`showtime_id`),
  KEY `movie_id` (`movie_id`),
  KEY `theater_id` (`theater_id`),
  CONSTRAINT `showtimes_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movies` (`movie_id`),
  CONSTRAINT `showtimes_ibfk_2` FOREIGN KEY (`theater_id`) REFERENCES `theaters` (`theater_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 movie_book.theaters 구조 내보내기
CREATE TABLE IF NOT EXISTS `theaters` (
  `theater_id` int(11) NOT NULL AUTO_INCREMENT,
  `theater_name` varchar(255) NOT NULL,
  `location` varchar(255) DEFAULT NULL,
  `capacity` int(11) NOT NULL,
  PRIMARY KEY (`theater_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 movie_book.users 구조 내보내기
CREATE TABLE IF NOT EXISTS `users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `user_password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 내보낼 데이터가 선택되어 있지 않습니다.

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
