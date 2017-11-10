/*
 Navicat Premium Data Transfer

 Source Server         : 47.94.212.166
 Source Server Type    : MySQL
 Source Server Version : 50637
 Source Host           : 47.94.212.166:3306
 Source Schema         : zhihu

 Target Server Type    : MySQL
 Target Server Version : 50637
 File Encoding         : 65001

 Date: 10/11/2017 10:43:48
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for zh_followee
-- ----------------------------
DROP TABLE IF EXISTS `zh_followee`;
CREATE TABLE `zh_followee` (
  `usertoken` varchar(100) NOT NULL,
  `followeetoken` varchar(100) NOT NULL,
  `followeename` varchar(100) NOT NULL,
  KEY `usertoken` (`usertoken`),
  KEY `followeetoken` (`followeetoken`),
  CONSTRAINT `zh_followee_ibfk_1` FOREIGN KEY (`usertoken`) REFERENCES `zh_userinfo` (`nametoken`),
  CONSTRAINT `zh_followee_ibfk_2` FOREIGN KEY (`followeetoken`) REFERENCES `zh_userinfo` (`nametoken`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for zh_follower
-- ----------------------------
DROP TABLE IF EXISTS `zh_follower`;
CREATE TABLE `zh_follower` (
  `usertoken` varchar(100) NOT NULL,
  `followertoken` varchar(100) NOT NULL,
  `followername` varchar(100) NOT NULL,
  KEY `usertoken` (`usertoken`),
  KEY `followertoken` (`followertoken`),
  CONSTRAINT `zh_follower_ibfk_1` FOREIGN KEY (`usertoken`) REFERENCES `zh_userinfo` (`nametoken`),
  CONSTRAINT `zh_follower_ibfk_2` FOREIGN KEY (`followertoken`) REFERENCES `zh_userinfo` (`nametoken`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for zh_userinfo
-- ----------------------------
DROP TABLE IF EXISTS `zh_userinfo`;
CREATE TABLE `zh_userinfo` (
  `nametoken` varchar(100) NOT NULL,
  `name` varchar(40) NOT NULL,
  `followees` int(11) DEFAULT NULL,
  `followers` int(11) DEFAULT NULL,
  `headline` varchar(500) DEFAULT NULL,
  `detail_introduce` varchar(300) DEFAULT NULL,
  `major` varchar(100) DEFAULT NULL,
  `ask` int(11) DEFAULT NULL,
  `answer` int(11) DEFAULT NULL,
  `articles` int(11) DEFAULT NULL,
  `avatar_url` varchar(200) DEFAULT NULL,
  `gender` int(11) DEFAULT NULL,
  `main_page_url` varchar(200) DEFAULT NULL,
  `is_advertiser` int(11) DEFAULT NULL,
  `user_type` varchar(40) DEFAULT NULL,
  `is_org` int(11) DEFAULT NULL,
  `avatar_local_url` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`nametoken`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;
