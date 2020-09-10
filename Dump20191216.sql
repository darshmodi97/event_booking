CREATE DATABASE  IF NOT EXISTS `event_booking` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `event_booking`;
-- MySQL dump 10.13  Distrib 8.0.17, for Win64 (x86_64)
--
-- Host: localhost    Database: event_booking
-- ------------------------------------------------------
-- Server version	8.0.17

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
-- Dumping data for table `caterer_owner_payment`
--

LOCK TABLES `caterer_owner_payment` WRITE;
/*!40000 ALTER TABLE `caterer_owner_payment` DISABLE KEYS */;
/*!40000 ALTER TABLE `caterer_owner_payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `catering_booking`
--

LOCK TABLES `catering_booking` WRITE;
/*!40000 ALTER TABLE `catering_booking` DISABLE KEYS */;
/*!40000 ALTER TABLE `catering_booking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `catering_category`
--

LOCK TABLES `catering_category` WRITE;
/*!40000 ALTER TABLE `catering_category` DISABLE KEYS */;
INSERT INTO `catering_category` VALUES (1,'Punjabi',300),(2,'Chinese',250),(3,'Gujarati',250),(4,'Italian',200),(5,'Maxican',200);
/*!40000 ALTER TABLE `catering_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `catering_category_mapping`
--

LOCK TABLES `catering_category_mapping` WRITE;
/*!40000 ALTER TABLE `catering_category_mapping` DISABLE KEYS */;
INSERT INTO `catering_category_mapping` VALUES (11,5,1),(12,5,3);
/*!40000 ALTER TABLE `catering_category_mapping` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `catering_owner_reg`
--

LOCK TABLES `catering_owner_reg` WRITE;
/*!40000 ALTER TABLE `catering_owner_reg` DISABLE KEYS */;
INSERT INTO `catering_owner_reg` VALUES (5,'daniel',9874563210,456789,12,'Accepted');
/*!40000 ALTER TABLE `catering_owner_reg` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `client_reg`
--

LOCK TABLES `client_reg` WRITE;
/*!40000 ALTER TABLE `client_reg` DISABLE KEYS */;
INSERT INTO `client_reg` VALUES (3,'meet',9998692819,11);
/*!40000 ALTER TABLE `client_reg` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `feedback_table`
--

LOCK TABLES `feedback_table` WRITE;
/*!40000 ALTER TABLE `feedback_table` DISABLE KEYS */;
/*!40000 ALTER TABLE `feedback_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `land_owner_payment`
--

LOCK TABLES `land_owner_payment` WRITE;
/*!40000 ALTER TABLE `land_owner_payment` DISABLE KEYS */;
INSERT INTO `land_owner_payment` VALUES (7,4,1,18900,'paid','2019-12-12','11:51',3);
/*!40000 ALTER TABLE `land_owner_payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `land_owner_reg`
--

LOCK TABLES `land_owner_reg` WRITE;
/*!40000 ALTER TABLE `land_owner_reg` DISABLE KEYS */;
INSERT INTO `land_owner_reg` VALUES (4,'darsh',9998090056,12,'654123','Accepted'),(5,'qwe',12345,4,'123','Requested'),(6,'qwe',12345,5,'123','Requested'),(7,'darsh',9874563210,6,'123456','Requested'),(8,'maharshi',9876543210,7,'123454','Requested'),(9,'ANANDI',1234567890,8,'123456','Requested'),(10,'QWER',1234567890,9,'123456','Requested'),(11,'xyz',1234567890,10,'132456','Requested'),(12,'anandi',9874563210,11,'456789','Requested'),(13,'himani',1234567890,14,'123456','Requested');
/*!40000 ALTER TABLE `land_owner_reg` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `login_table`
--

LOCK TABLES `login_table` WRITE;
/*!40000 ALTER TABLE `login_table` DISABLE KEYS */;
INSERT INTO `login_table` VALUES (1,'admin@123','123',4),(2,'darshmodi1111','123',1),(3,'meet@123','123',3),(4,'qwertt','123',1),(5,'qwertt','123',1),(6,'darsh@123','123',1),(7,'maharshi@123','123',1),(8,'ANANDI.ICREATE@GMAIL.COM','123',1),(9,'QWERT@QW.CH','123',1),(10,'darshmodi1111','123',1),(11,'ANANDI.ICREATE@GMAIL.COM','123',1),(12,'daniel@123','123',2),(14,'himanikalal@gmail.com','123',1);
/*!40000 ALTER TABLE `login_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `payment`
--

LOCK TABLES `payment` WRITE;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
INSERT INTO `payment` VALUES (200,3,'2019-12-12','11:51','27000','paid',1,6);
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `roll_table`
--

LOCK TABLES `roll_table` WRITE;
/*!40000 ALTER TABLE `roll_table` DISABLE KEYS */;
INSERT INTO `roll_table` VALUES (1,'Land_owner'),(2,'Catering_owner'),(3,'Client'),(4,'Admin');
/*!40000 ALTER TABLE `roll_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `vanue_booking`
--

LOCK TABLES `vanue_booking` WRITE;
/*!40000 ALTER TABLE `vanue_booking` DISABLE KEYS */;
INSERT INTO `vanue_booking` VALUES (6,3,1,'2019-12-19','11:00','20:00','paid','2019-12-19');
/*!40000 ALTER TABLE `vanue_booking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `vanue_category`
--

LOCK TABLES `vanue_category` WRITE;
/*!40000 ALTER TABLE `vanue_category` DISABLE KEYS */;
INSERT INTO `vanue_category` VALUES (1,'Birthday'),(2,'Sangeet'),(3,'Wedding'),(4,'New year Party');
/*!40000 ALTER TABLE `vanue_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `vanue_category_mapping`
--

LOCK TABLES `vanue_category_mapping` WRITE;
/*!40000 ALTER TABLE `vanue_category_mapping` DISABLE KEYS */;
INSERT INTO `vanue_category_mapping` VALUES (1,1,1),(2,2,1),(3,4,1),(4,1,2),(5,4,2);
/*!40000 ALTER TABLE `vanue_category_mapping` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `vanue_image_mapping`
--

LOCK TABLES `vanue_image_mapping` WRITE;
/*!40000 ALTER TABLE `vanue_image_mapping` DISABLE KEYS */;
INSERT INTO `vanue_image_mapping` VALUES (1,1,'/media/Rajpath%20Club_W4vmSXD.jpg'),(2,2,'/media/sankalp.jpg');
/*!40000 ALTER TABLE `vanue_image_mapping` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `vanue_table`
--

LOCK TABLES `vanue_table` WRITE;
/*!40000 ALTER TABLE `vanue_table` DISABLE KEYS */;
INSERT INTO `vanue_table` VALUES (1,'Rajpath Club','SG Highway',1500,800,4,'Accepted',3000),(2,'sankalp','dharnidhar',400,100,13,'Accepted',4000);
/*!40000 ALTER TABLE `vanue_table` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-12-16 14:23:47
