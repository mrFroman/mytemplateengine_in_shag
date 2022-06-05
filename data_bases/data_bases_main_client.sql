-- MySQL dump 10.13  Distrib 8.0.27, for Win64 (x86_64)
--
-- Host: localhost    Database: data_bases
-- ------------------------------------------------------
-- Server version	8.0.27

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `main_client`
--

DROP TABLE IF EXISTS `main_client`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_client` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `post_mail` varchar(150) NOT NULL,
  `number_phone` varchar(20) NOT NULL,
  `date_registratiom` date NOT NULL,
  `buy_ticket_id` bigint NOT NULL,
  `category_event_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `main_client_buy_ticket_id_949eba89_fk_main_events_id` (`buy_ticket_id`),
  KEY `main_client_category_event_id_df005071_fk_main_category_id` (`category_event_id`),
  CONSTRAINT `main_client_buy_ticket_id_949eba89_fk_main_events_id` FOREIGN KEY (`buy_ticket_id`) REFERENCES `main_events` (`id`),
  CONSTRAINT `main_client_category_event_id_df005071_fk_main_category_id` FOREIGN KEY (`category_event_id`) REFERENCES `main_category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_client`
--

LOCK TABLES `main_client` WRITE;
/*!40000 ALTER TABLE `main_client` DISABLE KEYS */;
INSERT INTO `main_client` VALUES (1,'syipos@mail.ru','89325632825','2020-04-20',1,1),(2,'lkjujsjh@mail.ru','89654123584','2001-03-20',1,1),(3,'hrtost@yandex.ru','89557621478','2003-01-20',2,1),(4,'keysl@gmail.com','89365478242','2020-12-20',2,1),(5,'lovtsa@icloud.com','89621475657','2014-06-20',3,2),(6,'joilust@gmial.com','89202155375','2016-08-20',3,2),(7,'qerttt@yandex.ru','89264878962','2030-04-20',4,2),(8,'tyirel@icloud.com','89456667745','2028-06-20',5,2),(9,'oltsans@icloud.com','89230144567','2010-08-20',5,2),(10,'bestra@gmail.com','89221443211','2009-08-20',6,3);
/*!40000 ALTER TABLE `main_client` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-06-05 14:31:30
