-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Feb 17, 2020 at 09:41 PM
-- Server version: 5.7.28-0ubuntu0.18.04.4
-- PHP Version: 7.2.24-0ubuntu0.18.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `facerecognition`
--

-- --------------------------------------------------------

--
-- Table structure for table `Customer`
--
DROP TABLE IF EXISTS `Customer`;

-- Create TABLE 'Customer'
CREATE TABLE `Customer` (
  customer_id int NOT NULL AUTO_INCREMENT,
  name varchar(50) NOT NULL,
  account_name varchar(50) NOT NULL,
  password varchar(50) NOT NULL,
  PRIMARY KEY(customer_id)
)

-- ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ALTER TABLE `Customer` AUTO_INCREMENT = 1;


LOCK TABLES `Customer` WRITE;
/*!40000 ALTER TABLE `Customer` DISABLE KEYS */;
INSERT INTO `Customer` VALUES (1, "JACK", NOW(), '2021-09-01');
/*!40000 ALTER TABLE `Customer` ENABLE KEYS */;
UNLOCK TABLES;

/* List of accounts */
Create TABLE `HK_Saving_Account` (
  customer_id int NOT NULL,
  account_id int NOT NULL,
  balance float NOT NULL,
  PRIMARY KEY(account_id),
  FOREIGN KEY(customer_id) REFERENCES Customer(customer_id)
)

Create TABLE `US_Saving_Account` (
  customer_id int NOT NULL,
  account_id int NOT NULL,
  balance float NOT NULL,
  PRIMARY KEY(account_id),
  FOREIGN KEY(customer_id) REFERENCES Customer(customer_id)
)
Create TABLE `HK_Current_Account` (
  customer_id int NOT NULL,
  account_id int NOT NULL,
  balance float NOT NULL,
  PRIMARY KEY(account_id),
  FOREIGN KEY(customer_id) REFERENCES Customer(customer_id)
)
Create TABLE `US_Current_Account` (
  customer_id int NOT NULL,
  account_id int NOT NULL,
  balance float NOT NULL,
  PRIMARY KEY(account_id),
  FOREIGN KEY(customer_id) REFERENCES Customer(customer_id)
)
Create TABLE `HK_Stock_Account` (
  customer_id int NOT NULL,
  account_id int NOT NULL,
  balance float NOT NULL,
  PRIMARY KEY(account_id),
  FOREIGN KEY(customer_id) REFERENCES Customer(customer_id)
)
Create TABLE `US_Stock_Account` (
  customer_id int NOT NULL,
  account_id int NOT NULL,
  balance float NOT NULL,
  PRIMARY KEY(account_id),
  FOREIGN KEY(customer_id) REFERENCES Customer(customer_id)
)



CREATE TABLE `Transaction` (
  trans_id int NOT NULL,
  customer_id int NOT NULL,
  target_id int NOT NULL,
  amount float NOT NULL,
  trans_time time NOT NULL,
  trans_date date NOT NULL,
  PRIMARY KEY(trans_id),
  FOREIGN KEY(customer_id) REFERENCES Customer(customer_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


# Create other TABLE...

CREATE TABLE `Login` (
  customer_id int NOT NULL,
  login_time time NOT NULL,
  login_date date NOT NULL,
  FOREIGN KEY(customer_id) REFERENCES Customer(customer_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Loan` (
  customer_id int NOT NULL,
  amount float NOT NULL,
  loan_time time NOT NULL,
  loan_date date NOT NULL,
  FOREIGN KEY(customer_id) REFERENCES Customer(customer_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1

CREATE TABLE `Stock_account` (
  customer_id INT NOT NULL,
  ticker_symbol varchar(10) NOT NULL,
  quantity INT NOT NULL,
  PRIMARY KEY (`customer_id`, `ticker_symbol`)
)

CREATE TABLE `Stock_order` (
  customer_id INT NOT NULL,
  ticker_symbol varchar(10) NOT NULL,
  price FLOAT(10,4) NOT NULL,
  quantity INT NOT NULL,
  side varchar(10) NOT NULL,
  PRIMARY KEY (`customer_id`, `ticker_symbol`)
)

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
