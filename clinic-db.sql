-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: localhost    Database: quanlyphongmach
-- ------------------------------------------------------
-- Server version	8.0.30

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
-- Table structure for table `bill`
--

DROP TABLE IF EXISTS `bill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bill` (
  `id` int NOT NULL AUTO_INCREMENT,
  `examination_price` float DEFAULT NULL,
  `medicine_price` float DEFAULT NULL,
  `total_price` float DEFAULT NULL,
  `create_date` datetime DEFAULT NULL,
  `examination_id` int NOT NULL,
  `nurse_id` int NOT NULL,
  PRIMARY KEY (`id`,`examination_id`,`nurse_id`),
  KEY `examination_id` (`examination_id`),
  KEY `nurse_id` (`nurse_id`),
  CONSTRAINT `bill_ibfk_1` FOREIGN KEY (`examination_id`) REFERENCES `examination` (`id`),
  CONSTRAINT `bill_ibfk_2` FOREIGN KEY (`nurse_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bill`
--

LOCK TABLES `bill` WRITE;
/*!40000 ALTER TABLE `bill` DISABLE KEYS */;
INSERT INTO `bill` VALUES (1,100000,400,100400,'2022-08-11 00:00:00',1,3);
/*!40000 ALTER TABLE `bill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `examination`
--

DROP TABLE IF EXISTS `examination`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `examination` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sympton` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `disease_prediction` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  `registration_id` int NOT NULL,
  PRIMARY KEY (`id`,`registration_id`),
  KEY `registration_id` (`registration_id`),
  CONSTRAINT `examination_ibfk_1` FOREIGN KEY (`registration_id`) REFERENCES `registration` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `examination`
--

LOCK TABLES `examination` WRITE;
/*!40000 ALTER TABLE `examination` DISABLE KEYS */;
INSERT INTO `examination` VALUES (1,'abc','xyz','2022-08-11 00:00:00',1);
/*!40000 ALTER TABLE `examination` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `examination__medicine`
--

DROP TABLE IF EXISTS `examination__medicine`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `examination__medicine` (
  `amount` int DEFAULT NULL,
  `using_method` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `medicine_id` int NOT NULL,
  `examination_id` int NOT NULL,
  PRIMARY KEY (`medicine_id`,`examination_id`),
  KEY `examination_id` (`examination_id`),
  CONSTRAINT `examination__medicine_ibfk_1` FOREIGN KEY (`medicine_id`) REFERENCES `medicine` (`id`),
  CONSTRAINT `examination__medicine_ibfk_2` FOREIGN KEY (`examination_id`) REFERENCES `examination` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `examination__medicine`
--

LOCK TABLES `examination__medicine` WRITE;
/*!40000 ALTER TABLE `examination__medicine` DISABLE KEYS */;
INSERT INTO `examination__medicine` VALUES (7,'a',1,1),(12,'b',2,1),(3,'c',3,1);
/*!40000 ALTER TABLE `examination__medicine` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `list_registration`
--

DROP TABLE IF EXISTS `list_registration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `list_registration` (
  `id` int NOT NULL AUTO_INCREMENT,
  `max_patient` int DEFAULT NULL,
  `examination_date` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `list_registration`
--

LOCK TABLES `list_registration` WRITE;
/*!40000 ALTER TABLE `list_registration` DISABLE KEYS */;
INSERT INTO `list_registration` VALUES (1,30,'2022-08-20');
/*!40000 ALTER TABLE `list_registration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medicine`
--

DROP TABLE IF EXISTS `medicine`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medicine` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(5000) COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` float DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `medicine_unit` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medicine`
--

LOCK TABLES `medicine` WRITE;
/*!40000 ALTER TABLE `medicine` DISABLE KEYS */;
INSERT INTO `medicine` VALUES (1,'medicine 1','medicine 1',10,1,'chai'),(2,'medicine 2','medicine 2',20,1,'vỉ'),(3,'medicine 3','medicine 3',30,1,'hộp'),(4,'medicine 4','medicine 4',40,1,'chai'),(5,'medicine 5','medicine 5',50,1,'vỉ');
/*!40000 ALTER TABLE `medicine` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registration`
--

DROP TABLE IF EXISTS `registration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registration` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sex` enum('MALE','FEMALE') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `dob` date DEFAULT NULL,
  `address` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_date` datetime DEFAULT NULL,
  `examination_date` date DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `tested` tinyint(1) DEFAULT NULL,
  `paided` tinyint(1) DEFAULT NULL,
  `list_registration_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`,`list_registration_id`),
  KEY `list_registration_id` (`list_registration_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `registration_ibfk_1` FOREIGN KEY (`list_registration_id`) REFERENCES `list_registration` (`id`),
  CONSTRAINT `registration_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registration`
--

LOCK TABLES `registration` WRITE;
/*!40000 ALTER TABLE `registration` DISABLE KEYS */;
INSERT INTO `registration` VALUES (1,'Nguyễn Minh Hiếu','MALE','0123456789','2001-12-04','HCM','2022-08-11 00:00:00','2022-08-20',1,1,1,1,4);
/*!40000 ALTER TABLE `registration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registration__user`
--

DROP TABLE IF EXISTS `registration__user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registration__user` (
  `user_id` int NOT NULL,
  `registration_id` int NOT NULL,
  PRIMARY KEY (`user_id`,`registration_id`),
  KEY `registration_id` (`registration_id`),
  CONSTRAINT `registration__user_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `registration__user_ibfk_2` FOREIGN KEY (`registration_id`) REFERENCES `registration` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registration__user`
--

LOCK TABLES `registration__user` WRITE;
/*!40000 ALTER TABLE `registration__user` DISABLE KEYS */;
/*!40000 ALTER TABLE `registration__user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rules`
--

DROP TABLE IF EXISTS `rules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rules` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `amount` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rules`
--

LOCK TABLES `rules` WRITE;
/*!40000 ALTER TABLE `rules` DISABLE KEYS */;
INSERT INTO `rules` VALUES (1,'tổng số bệnh nhân một ngày',30),(2,'tiền khám ',100000);
/*!40000 ALTER TABLE `rules` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sex` enum('MALE','FEMALE') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `address` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `phone` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `joined_date` datetime DEFAULT NULL,
  `avatar` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_role` enum('ADMIN','NURSE','DOCTOR','USER') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `phone` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','MALE','2001-04-06','GCM','admin','e10adc3949ba59abbe56e057f20f883e',1,'0799507086','2022-04-06 00:00:00','123','ADMIN'),(2,'Nguyễn Thành Danh','MALE','2022-08-10','HCM','user1','e10adc3949ba59abbe56e057f20f883e',1,'0799507087','2022-08-10 00:00:00','https://res.cloudinary.com/dqifjhxxg/image/upload/v1660147084/kndiae4m6bujmincwuss.png','USER'),(3,'nurse','MALE','2001-04-06','HN','nurse','e10adc3949ba59abbe56e057f20f883e',1,'0799507088','2022-04-06 00:00:00','123','NURSE'),(4,'Nguyễn Minh Hiếu','MALE','2001-12-04','HCM','0123456789','202cb962ac59075b964b07152d234b70',1,'0123456789','2022-08-11 00:00:00',NULL,'USER'),(5,'doctor','MALE','2001-04-06','HN','doctor','e10adc3949ba59abbe56e057f20f883e',1,'0799501188','2022-04-06 00:00:00','123','DOCTOR');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-09-01 20:21:13
