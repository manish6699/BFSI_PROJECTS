-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: May 03, 2019 at 11:38 AM
-- Server version: 5.7.23
-- PHP Version: 7.2.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bankwithfd`
--

-- --------------------------------------------------------

--
-- Table structure for table `account`
--

DROP TABLE IF EXISTS `account`;
CREATE TABLE IF NOT EXISTS `account` (
  `acc_no` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(20) DEFAULT NULL,
  `balance` int(11) DEFAULT NULL,
  `doac` date DEFAULT NULL,
  `cus_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`acc_no`),
  KEY `cus_id` (`cus_id`)
) ENGINE=MyISAM AUTO_INCREMENT=26 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `account`
--

INSERT INTO `account` (`acc_no`, `type`, `balance`, `doac`, `cus_id`) VALUES
(1, 'savings', 4550, '2019-04-21', 1),
(2, 'savings', 2350, '2019-04-21', 2),
(3, 'current', 5000, '2019-04-21', 3),
(4, 'savings', 1000, '2019-04-21', 4),
(5, 'fixed deposit', 5000, '2019-04-21', 1),
(16, 'savings', 1001, '2019-04-23', 7),
(8, 'current', 5000, '2019-04-21', 2),
(17, 'savings', 48900, '2019-04-23', 7),
(10, 'fixed deposit', 10000, '2019-04-21', 5),
(23, 'savings', 0, '2019-04-30', 10),
(13, 'savings', 45000, '2019-04-22', 6),
(18, 'savings', 0, '2019-04-30', 8),
(14, 'fixed deposit', 100000, '2019-04-22', 6),
(19, 'savings', 450, '2019-04-30', 9),
(20, 'fixed deposit', 1000, '2019-04-30', 9),
(21, 'savings', 0, '2019-04-30', 9),
(22, 'current', 5000, '2019-04-30', 9),
(25, 'fixed deposit', 5000, '2019-05-01', 11);

-- --------------------------------------------------------

--
-- Table structure for table `closed_acc_history`
--

DROP TABLE IF EXISTS `closed_acc_history`;
CREATE TABLE IF NOT EXISTS `closed_acc_history` (
  `acc_no` int(11) NOT NULL AUTO_INCREMENT,
  `closedate` date DEFAULT NULL,
  PRIMARY KEY (`acc_no`)
) ENGINE=MyISAM AUTO_INCREMENT=25 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `closed_acc_history`
--

INSERT INTO `closed_acc_history` (`acc_no`, `closedate`) VALUES
(12, '2019-04-22'),
(9, '2019-04-22'),
(7, '2019-04-22'),
(15, '2019-04-23'),
(11, '2019-04-30'),
(24, '2019-05-01');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
CREATE TABLE IF NOT EXISTS `customer` (
  `cus_id` int(11) NOT NULL AUTO_INCREMENT,
  `f_name` varchar(40) DEFAULT NULL,
  `l_name` varchar(40) DEFAULT NULL,
  `ad_line1` varchar(50) DEFAULT NULL,
  `ad_line2` varchar(50) DEFAULT NULL,
  `state` varchar(20) DEFAULT NULL,
  `city` varchar(30) DEFAULT NULL,
  `pincode` int(11) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`cus_id`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`cus_id`, `f_name`, `l_name`, `ad_line1`, `ad_line2`, `state`, `city`, `pincode`, `password`) VALUES
(1, 'manish', 'reddy', 'dananjayan layout', 'kithagnur', 'karnataka', 'bengaluru', 560036, 'manish123'),
(2, 'naveen', 'reddy', 'dananjayan layout', 'kithagnur', 'karnataka', 'bengaluru', 560036, 'naveen123'),
(3, 'tony', 'stark', 'no. 4', 'old delhi', 'delhi', 'delhi', 670032, 'tonys123'),
(4, 'devilliers', 'ab', 'ub city', 'banargata road', 'karnataka', 'bengaluru', 560072, 'devilliers123'),
(5, 'vamsi', 'krishna', 'no. 6b street', 'nri layout', 'karnataka', 'bengaluru', 560038, 'vamsi123'),
(6, 'deepa', 'acharya', 'krpuram', 'bangalore', 'KARNATAKA', 'BENGALURU', 560036, 'deepa123'),
(7, 'Raja', 'Pells', 'lop', 'lpop', 'KARNATAKA', 'nellore', 560036, '12345678'),
(8, 'aron', 'finch', '#2 param layout', 'kalkeri', 'karnataka', 'bengaluru', 560045, 'aron12234'),
(9, 'aron', 'finch', '#2 param layout', 'kalkeri', 'karnataka', 'bengaluru', 560045, 'aron1234'),
(10, 'rony', 'shaw', '#no4 puram ghat', 'varanasi', 'uttar pradesh', 'varanasi', 870032, 'rony1234'),
(11, 'nilmani', 'rastogi', 'no 5 desi street', 'fasug layout', 'nepal', 'nepal', 898464, 'nilmani123');

-- --------------------------------------------------------

--
-- Table structure for table `fd_account`
--

DROP TABLE IF EXISTS `fd_account`;
CREATE TABLE IF NOT EXISTS `fd_account` (
  `fd_accno` int(11) NOT NULL,
  `cus_id` int(11) DEFAULT NULL,
  `fd_amount` int(11) DEFAULT NULL,
  `fd_period` int(11) DEFAULT NULL,
  PRIMARY KEY (`fd_accno`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `fd_account`
--

INSERT INTO `fd_account` (`fd_accno`, `cus_id`, `fd_amount`, `fd_period`) VALUES
(5, 1, 5000, 12),
(6, 1, 1000, 12),
(10, 5, 10000, 12),
(11, 2, 5000, 12),
(14, 6, 100000, 12),
(20, 9, 1000, 12),
(25, 11, 5000, 12);

-- --------------------------------------------------------

--
-- Table structure for table `loan_account`
--

DROP TABLE IF EXISTS `loan_account`;
CREATE TABLE IF NOT EXISTS `loan_account` (
  `loan_accno` int(11) NOT NULL AUTO_INCREMENT,
  `cus_id` int(11) DEFAULT NULL,
  `loan_amount` int(11) DEFAULT NULL,
  `repayment_term` int(11) DEFAULT NULL,
  PRIMARY KEY (`loan_accno`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `loan_account`
--

INSERT INTO `loan_account` (`loan_accno`, `cus_id`, `loan_amount`, `repayment_term`) VALUES
(1, 2, 1000, 12),
(2, 1, 1000, 12),
(4, 6, 30000, 12),
(5, 7, 25000, 16),
(6, 2, 1000, 12),
(7, 2, 1000, 12),
(8, 4, 2000, 12),
(9, 9, 2000, 12);

-- --------------------------------------------------------

--
-- Table structure for table `transaction_details`
--

DROP TABLE IF EXISTS `transaction_details`;
CREATE TABLE IF NOT EXISTS `transaction_details` (
  `t_id` int(11) NOT NULL AUTO_INCREMENT,
  `acc_no` int(11) DEFAULT NULL,
  `time_stamp` timestamp NULL DEFAULT NULL,
  `type` varchar(40) DEFAULT NULL,
  `amount` int(11) DEFAULT NULL,
  PRIMARY KEY (`t_id`)
) ENGINE=MyISAM AUTO_INCREMENT=30 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `transaction_details`
--

INSERT INTO `transaction_details` (`t_id`, `acc_no`, `time_stamp`, `type`, `amount`) VALUES
(1, 1, '2019-04-20 18:30:00', 'deposit', 5000),
(2, 1, '2019-04-20 18:30:00', 'withdrawal', 100),
(3, 1, '2019-04-20 18:30:00', 'transfer', 2500),
(4, 2, '2019-04-20 18:30:00', 'transfer', 100),
(5, 2, '2019-04-20 18:30:00', 'transfer', 200),
(6, 1, '2019-04-20 18:30:00', 'transfer', 50),
(7, 1, '2019-04-20 18:30:00', 'transfer', 100),
(8, 12, '2019-04-21 18:30:00', 'deposit', 20000),
(9, 12, '2019-04-21 18:30:00', 'withdrawal', 10000),
(10, 13, '2019-04-21 18:30:00', 'transfer', 5000),
(11, 15, '2019-04-22 18:30:00', 'deposit', 4000),
(12, 15, '2019-04-22 18:30:00', 'deposit', 750),
(13, 17, '2019-04-22 18:30:00', 'transfer', 1000),
(14, 17, '2019-04-22 18:30:00', 'withdrawal', 100),
(15, 24, '2019-04-30 18:30:00', 'withdrawal', 1000),
(16, 24, '2019-04-30 18:30:00', 'transfer', 1000),
(17, 4, '2019-05-02 18:30:00', 'deposit', 1000),
(18, 16, '2019-05-02 18:30:00', 'deposit', 1000),
(19, 19, '2019-05-02 18:30:00', 'deposit', 1000),
(20, 19, '2019-05-02 18:30:00', 'withdrawal', 100),
(21, 19, '2019-05-02 18:30:00', 'withdrawal', 50),
(22, 19, '2019-05-02 18:30:00', 'withdrawal', 50),
(23, 19, '2019-05-02 18:30:00', 'withdrawal', 50),
(24, 19, '2019-05-02 18:30:00', 'withdrawal', 50),
(25, 19, '2019-05-02 18:30:00', 'withdrawal', 50),
(26, 19, '2019-05-02 18:30:00', 'withdrawal', 50),
(27, 19, '2019-05-02 18:30:00', 'withdrawal', 50),
(28, 19, '2019-05-02 18:30:00', 'withdrawal', 50),
(29, 19, '2019-05-02 18:30:00', 'withdrawal', 50);

-- --------------------------------------------------------

--
-- Table structure for table `transfer`
--

DROP TABLE IF EXISTS `transfer`;
CREATE TABLE IF NOT EXISTS `transfer` (
  `tr_id` int(11) NOT NULL AUTO_INCREMENT,
  `from_ac_no` int(11) DEFAULT NULL,
  `to_ac_no` int(11) DEFAULT NULL,
  `amount` int(11) NOT NULL,
  PRIMARY KEY (`tr_id`),
  KEY `from_ac_no` (`from_ac_no`),
  KEY `to_ac_no` (`to_ac_no`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `transfer`
--

INSERT INTO `transfer` (`tr_id`, `from_ac_no`, `to_ac_no`, `amount`) VALUES
(1, 1, 2, 2500),
(2, 2, 1, 100),
(3, 2, 1, 200),
(4, 1, 2, 50),
(5, 1, 2, 100),
(6, 13, 12, 5000),
(7, 17, 1, 1000),
(8, 24, 1, 1000);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
