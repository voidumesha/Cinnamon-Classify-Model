-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 03, 2025 at 06:30 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cinnalyze`
--

-- --------------------------------------------------------

--
-- Table structure for table `barkimage`
--

CREATE TABLE `barkimage` (
  `barkId` int(11) NOT NULL,
  `User_id` int(11) NOT NULL,
  `date_time_stamp` datetime NOT NULL,
  `image` mediumblob DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `extractedfeatures`
--

CREATE TABLE `extractedfeatures` (
  `barkId` int(11) NOT NULL,
  `color` varchar(50) NOT NULL,
  `texture` varchar(50) NOT NULL,
  `pattern` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `feedback`
--

CREATE TABLE `feedback` (
  `id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `message` text NOT NULL,
  `rating` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `feedback`
--

INSERT INTO `feedback` (`id`, `email`, `message`, `rating`, `created_at`) VALUES
(1, 'B@gmail.com', 'Cupiri', 4, '2024-08-01 16:10:31'),
(2, 'M@gmail.com', 'yes\nno', 1, '2024-08-01 16:21:25'),
(3, 'malithi123@gmail.com', 'Yes satisfied.\nCan you improve the buttons click with statement\n', 2, '2024-08-02 15:55:16'),
(4, 'amanda123@gmail.com', 'Yes satisfied.\nVery good app\n', 2, '2024-08-02 16:01:32'),
(5, 'k@gmail.com', 'test answer', 2, '2024-11-18 12:36:25'),
(6, 'k@gmail.com', 'ruwan test', 4, '2024-11-18 12:37:03');

-- --------------------------------------------------------

--
-- Table structure for table `message`
--

CREATE TABLE `message` (
  `Message_id` int(11) NOT NULL,
  `barkId` int(11) NOT NULL,
  `Quality_Name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `pastrecord`
--

CREATE TABLE `pastrecord` (
  `Record_id` int(100) NOT NULL,
  `Message_id` int(11) NOT NULL,
  `Seven_Days_update` int(11) NOT NULL,
  `Recommendation` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `quality`
--

CREATE TABLE `quality` (
  `Quality_id` int(100) NOT NULL,
  `Quality_Name` varchar(50) NOT NULL,
  `Description` varchar(500) NOT NULL,
  `barkId` int(11) NOT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user_table`
--

CREATE TABLE `user_table` (
  `User_id` int(100) NOT NULL,
  `firstName` text NOT NULL,
  `lastName` text NOT NULL,
  `email` text NOT NULL,
  `phoneNumber` text NOT NULL,
  `password` text NOT NULL,
  `isVerified` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_table`
--

INSERT INTO `user_table` (`User_id`, `firstName`, `lastName`, `email`, `phoneNumber`, `password`, `isVerified`) VALUES
(1, 'r', 'u', 'ru@gmail.com', '0719175066', '$2a$10$II27CvgnuOwaU3Hk1Xf0SeXuvtkn8HLy9OazJNUbEWXuP/jXy80um', 0),
(2, 'i', 's', 'is@gmail.com', '0719175066', '$2a$10$YHKh1u5O8IUuEXQolW9ZVeSSSMJXr6P1mHlQWLHtQw6O/v2jng1em', 0),
(3, 'ni', 'ga', 'niru@gmail.com', '0719175066', '$2a$10$bChEdzrPDD1kCTzOziZmS.IWasG6AwyrSLnQJTR0SiBG.bbfR8/Em', 0),
(4, 'k', 'g', 'k@gmail.com', '0719175066', '$2a$10$uOCDjTfgjl5JEJN7TlO0Gun69F/sxIyGs8zY/NPtun62LxnvW9m0W', 1),
(5, 'Nalani', 'Lokuge', 'nalani@gmail.com', '0719175066', '$2a$10$GQXQ/96srhAK/ZBAroF2r.XiYCRlBRLiO3ZDD3kAVtQPpKCqc1AZi', 0),
(6, 'Namal', 'Ravihara', 'namal@gmail.com', '0719175066', '$2a$10$dFNBRdhrnj0A3ORRm5kOh.Xsw1Di.nwB/.nI1l1TGldJuNX0n0V6S', 0),
(7, 'Amanda', 'Jeewanthi', 'ama@gmail.com', '0719175066', '$2a$10$AVvEfdBZPXxmES0hcM.KUOxmAEbdhNEaHS/jQ75o0Dk669VlxZJcu', 0),
(8, 'Je', 'wa', 'j@gmail.com', '0719175066', '$2a$10$bjfCICpZN/eMcv/1qFrQNOC7Z7Yi2KWIwEZethGWAvsKkZ3fUgpYG', 0),
(9, 'A', 'B', 'cd@gmail.com', '0719175066', '$2a$10$1OsAPZEK.FA9.9YxJE13DugcH1OXxLv1LJRHllxf88hCRbk2AYKl6', 0),
(10, 'E', 'F', 'e@gmail.com', '0719175066', '$2a$10$HkI0V3r5/S4G88DyoiRTUehq1zHkVHq6jo4sHXSR567Dmj06LhFPq', 0),
(11, 'V', 'A', 'v@gmail.com', '0719175066', '$2a$10$bb6zHZOF5VATloFmqF3O1.QXrP5iuGlxsaW4g.xQxNcetwYlfP1My', 1),
(12, 'Asanka', 'Silva', 'asanka@gmail.com', '0772424254', '$2a$10$/zwjRrezJD0LVOoZR0RK6.b8uZQzGVgmlXwohLr1sWOes/Zh6qJD.', 1),
(13, 'Leo', 'Silva', 'l@gmail.com', '0772424254', '$2a$10$FxeEHCSYS5JP0D2gy7Qd..o7lbSoTOhW5iR4Qk5ixzy.l3gZa.uGy', 1);

-- --------------------------------------------------------

--
-- Table structure for table `verification_codes`
--

CREATE TABLE `verification_codes` (
  `id` int(11) NOT NULL,
  `phoneNumber` varchar(15) NOT NULL,
  `verificationCode` varchar(15) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `verification_codes`
--

INSERT INTO `verification_codes` (`id`, `phoneNumber`, `verificationCode`, `created_at`) VALUES
(0, '0772424254', '114207', '2024-11-14 17:14:59'),
(0, '0714906606', '151721', '2024-11-16 13:00:31'),
(0, '0714906606', '151721', '2024-11-16 13:00:31'),
(0, '0772424254', '830676', '2024-11-14 17:30:23'),
(0, '0772424254', '375750', '2024-11-14 17:30:25'),
(0, '1234567890', '433460', '2024-11-16 12:06:48'),
(0, '1234567890', '110336', '2024-11-16 12:07:49'),
(0, '1234567890', '908152', '2024-11-16 12:10:24'),
(0, '0714906606', '151721', '2024-11-16 13:00:31'),
(0, '0714906606', '155165', '2024-11-16 13:24:00'),
(0, '0772424254', '939435', '2024-11-18 15:05:18'),
(0, '0772424254', '471253', '2024-11-18 15:57:42');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `barkimage`
--
ALTER TABLE `barkimage`
  ADD PRIMARY KEY (`barkId`),
  ADD KEY `id` (`User_id`);

--
-- Indexes for table `extractedfeatures`
--
ALTER TABLE `extractedfeatures`
  ADD KEY `extractedfeatures_ibfk_1` (`barkId`);

--
-- Indexes for table `feedback`
--
ALTER TABLE `feedback`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `message`
--
ALTER TABLE `message`
  ADD PRIMARY KEY (`Message_id`),
  ADD KEY `barkId` (`barkId`);

--
-- Indexes for table `pastrecord`
--
ALTER TABLE `pastrecord`
  ADD PRIMARY KEY (`Record_id`),
  ADD KEY `Message_id` (`Message_id`);

--
-- Indexes for table `quality`
--
ALTER TABLE `quality`
  ADD PRIMARY KEY (`Quality_id`),
  ADD KEY `barkId` (`barkId`);

--
-- Indexes for table `user_table`
--
ALTER TABLE `user_table`
  ADD PRIMARY KEY (`User_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `barkimage`
--
ALTER TABLE `barkimage`
  MODIFY `barkId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT for table `feedback`
--
ALTER TABLE `feedback`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `quality`
--
ALTER TABLE `quality`
  MODIFY `Quality_id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;

--
-- AUTO_INCREMENT for table `user_table`
--
ALTER TABLE `user_table`
  MODIFY `User_id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `barkimage`
--
ALTER TABLE `barkimage`
  ADD CONSTRAINT `barkimage_ibfk_1` FOREIGN KEY (`User_id`) REFERENCES `user_table` (`User_id`);

--
-- Constraints for table `pastrecord`
--
ALTER TABLE `pastrecord`
  ADD CONSTRAINT `pastrecord_ibfk_1` FOREIGN KEY (`Message_id`) REFERENCES `pastrecord` (`Record_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
