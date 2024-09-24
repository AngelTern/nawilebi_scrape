-- MySQL dump 10.13  Distrib 8.0.39, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: nawilebi
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `login_credentials`
--

DROP TABLE IF EXISTS `login_credentials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `login_credentials` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `password` varchar(80) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_credentials`
--

/*!40000 ALTER TABLE `login_credentials` DISABLE KEYS */;
INSERT INTO `login_credentials` VALUES (2,'nawilebi','$2b$12$Le23bMt1z/yTW2WgaWMkYOGaaaZHN2hwczQ8pVrkrLe.E0NxtrLrW'),(3,'test','$2b$12$4ClMeqM1KMx/N2p0sMxvRu.FDO9dDWIvviuAOZ9Lueu3Q0Q91MqwG');
/*!40000 ALTER TABLE `login_credentials` ENABLE KEYS */;

--
-- Table structure for table `nawilebi`
--

DROP TABLE IF EXISTS `nawilebi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nawilebi` (
  `id` int NOT NULL AUTO_INCREMENT,
  `part_url` varchar(1000) DEFAULT NULL,
  `car_mark` varchar(70) DEFAULT NULL,
  `car_model` varchar(150) DEFAULT NULL,
  `part_full_name` varchar(150) DEFAULT NULL,
  `start_year` int DEFAULT NULL,
  `end_year` int DEFAULT NULL,
  `price` decimal(10,0) DEFAULT NULL,
  `original_price` decimal(10,0) DEFAULT NULL,
  `in_stock` tinyint(1) DEFAULT NULL,
  `website` varchar(255) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nawilebi`
--

/*!40000 ALTER TABLE `nawilebi` DISABLE KEYS */;
INSERT INTO `nawilebi` VALUES (1,'https://autopia.ge/ka/product/5387AGSMV75%20LFWX','SMART','FORTOW W453','საქარე მინა',2015,2024,198,NULL,1,'https://autopia.ge',NULL),(2,'https://autopia.ge/ka/product/7618BGSHABW','SKODA','RAPID','საბარგულის მინა',2012,2024,489,NULL,1,'https://autopia.ge',NULL),(3,'https://autopia.ge/ka/product/ST5201622','SEAT','TOLEDO','ბამპერის სამაგრი ძელი',1999,2005,1,NULL,0,'https://autopia.ge',NULL),(4,'https://autopia.ge/ka/product/SKRAPID12','SKODA','RAPID','საქარე მინა უსენსორო',2012,2024,188,NULL,1,'https://autopia.ge',NULL),(5,'https://autopia.ge/ka/product/PS102060402','PORSCHE','PANAMERA','ბრეკეტი ფარის მარჯვენა',2016,2024,134,NULL,1,'https://autopia.ge',NULL),(6,'https://autopia.ge/ka/product/PG3223603','PEUGEOT','207','ფრთის საფენი მარჯვენა',NULL,NULL,1,NULL,1,'https://autopia.ge',NULL),(7,'https://autopia.ge/ka/product/PS102060401','PORSCHE','PANAMERA','ბრეკეტი ფარის მარცხენა',2016,2024,134,NULL,1,'https://autopia.ge',NULL),(8,'https://autopia.ge/ka/product/NIVA','NIVA','','საქარე მინა უსენსორო',NULL,NULL,145,NULL,0,'https://autopia.ge',NULL),(9,'https://autopia.ge/ka/product/20-9411-00-1N','NISSAN','PATHFINDER','ფარი წინა მარჯვენაTYC',2013,2020,0,NULL,1,'https://autopia.ge',NULL),(10,'https://autopia.ge/ka/product/MB019002','MITSUBISHI','DELICA','საბარგულის მინა',1994,2024,198,NULL,1,'https://autopia.ge',NULL),(11,'https://autopia.ge/ka/product/MN017006','MINI','COOPER/ONE','საქარე მინა სენსორით   COOPER/CABRIO',2014,2014,198,NULL,1,'https://autopia.ge',NULL),(12,'https://autopia.ge/ka/product/ACTROS','MERCEDES','ACTROS','საქარე მინა სენსორიანი',1996,2013,450,NULL,0,'https://autopia.ge',NULL);
/*!40000 ALTER TABLE `nawilebi` ENABLE KEYS */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `address` varchar(256) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(120) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_user_name` (`name`),
  KEY `ix_user_age` (`age`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

/*!40000 ALTER TABLE `user` DISABLE KEYS */;
/*!40000 ALTER TABLE `user` ENABLE KEYS */;

--
-- Dumping routines for database 'nawilebi'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-09-22 21:47:59
