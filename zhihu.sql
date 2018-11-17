/*
 Source Server Type    : MySQL
 Source Schema         : zhihu
 Target Server Type    : MySQL
 Date: 17/11/2018 15:27:27
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for business
-- ----------------------------
DROP TABLE IF EXISTS `business`;
CREATE TABLE `business` (
  `id` varchar(20) NOT NULL,
  `url` varchar(200) DEFAULT NULL,
  `avatar_url` varchar(200) NOT NULL DEFAULT '',
  `name` varchar(50) NOT NULL DEFAULT '',
  `introduction` mediumtext,
  `type` varchar(20) NOT NULL DEFAULT '',
  `excerpt` varchar(1000) NOT NULL DEFAULT '',
  `meta` json DEFAULT NULL,
  `experience` varchar(1000) NOT NULL DEFAULT '',
  PRIMARY KEY (`name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for education
-- ----------------------------
DROP TABLE IF EXISTS `education`;
CREATE TABLE `education` (
  `id` varchar(20) NOT NULL,
  `url` varchar(200) DEFAULT NULL,
  `avatar_url` varchar(200) NOT NULL DEFAULT '',
  `name` varchar(50) NOT NULL DEFAULT '',
  `introduction` mediumtext,
  `type` varchar(20) NOT NULL DEFAULT '',
  `meta` json DEFAULT NULL,
  `excerpt` varchar(1000) NOT NULL DEFAULT '',
  `experience` varchar(1000) NOT NULL DEFAULT '',
  PRIMARY KEY (`name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for employment
-- ----------------------------
DROP TABLE IF EXISTS `employment`;
CREATE TABLE `employment` (
  `id` varchar(20) NOT NULL,
  `url` varchar(200) DEFAULT NULL,
  `avatar_url` varchar(200) NOT NULL DEFAULT '',
  `name` varchar(50) NOT NULL DEFAULT '',
  `introduction` mediumtext,
  `type` varchar(20) NOT NULL DEFAULT '',
  `excerpt` varchar(1000) NOT NULL DEFAULT '',
  `experience` varchar(1000) NOT NULL DEFAULT '',
  `meta` json DEFAULT NULL,
  PRIMARY KEY (`name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for follower
-- ----------------------------
DROP TABLE IF EXISTS `follower`;
CREATE TABLE `follower` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `follower_token` varchar(200) NOT NULL DEFAULT '',
  `following_token` varchar(200) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=560994 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for following
-- ----------------------------
DROP TABLE IF EXISTS `following`;
CREATE TABLE `following` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `follower_token` varchar(200) NOT NULL DEFAULT '',
  `following_token` varchar(200) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=688277 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for location
-- ----------------------------
DROP TABLE IF EXISTS `location`;
CREATE TABLE `location` (
  `id` varchar(20) NOT NULL,
  `url` varchar(200) DEFAULT NULL,
  `avatar_url` varchar(200) NOT NULL DEFAULT '',
  `name` varchar(50) NOT NULL DEFAULT '',
  `introduction` mediumtext,
  `meta` json DEFAULT NULL,
  `type` varchar(20) NOT NULL DEFAULT '',
  `excerpt` varchar(1000) NOT NULL DEFAULT '',
  PRIMARY KEY (`name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for topic
-- ----------------------------
DROP TABLE IF EXISTS `topic`;
CREATE TABLE `topic` (
  `id` varchar(20) NOT NULL,
  `url` varchar(200) DEFAULT NULL,
  `avatar_url` varchar(200) NOT NULL DEFAULT '',
  `name` varchar(50) NOT NULL DEFAULT '',
  `meta` json DEFAULT NULL,
  `introduction` mediumtext,
  `type` varchar(20) NOT NULL DEFAULT '',
  `excerpt` varchar(1000) NOT NULL DEFAULT '',
  PRIMARY KEY (`name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for user_info
-- ----------------------------
DROP TABLE IF EXISTS `user_info`;
CREATE TABLE `user_info` (
  `sort_order` int(11) NOT NULL AUTO_INCREMENT,
  `id` varchar(100) NOT NULL DEFAULT '',
  `name` varchar(100) NOT NULL DEFAULT '',
  `headline` varchar(500) NOT NULL DEFAULT '',
  `url_token` varchar(300) NOT NULL DEFAULT '',
  `user_type` varchar(100) NOT NULL DEFAULT '',
  `avatar_hue` varchar(500) NOT NULL DEFAULT '',
  `included_text` varchar(500) NOT NULL DEFAULT '',
  `description` varchar(1000) NOT NULL DEFAULT '',
  `type` varchar(50) NOT NULL DEFAULT '',
  `avatar_url` varchar(400) NOT NULL DEFAULT '',
  `cover_url` varchar(400) NOT NULL DEFAULT '',
  `url` varchar(400) NOT NULL DEFAULT '',
  `avatar_url_template` varchar(400) NOT NULL DEFAULT '',
  `allow_message` int(11) NOT NULL DEFAULT '-1',
  `is_privacy_protected` int(11) NOT NULL DEFAULT '-1',
  `is_blocking` int(11) NOT NULL DEFAULT '-1',
  `is_advertiser` int(11) NOT NULL DEFAULT '-1',
  `is_force_renamed` int(11) NOT NULL DEFAULT '-1',
  `is_active` int(11) NOT NULL DEFAULT '-1',
  `is_blocked` int(11) NOT NULL DEFAULT '-1',
  `following_topic_count` int(11) NOT NULL DEFAULT '-1',
  `columns_count` int(11) NOT NULL DEFAULT '-1',
  `hosted_live_count` int(11) NOT NULL DEFAULT '-1',
  `thank_to_count` int(11) NOT NULL DEFAULT '-1',
  `mutual_followees_count` int(11) NOT NULL DEFAULT '-1',
  `answer_count` int(11) NOT NULL DEFAULT '-1',
  `thank_from_count` int(11) NOT NULL DEFAULT '-1',
  `vote_to_count` int(11) NOT NULL DEFAULT '-1',
  `articles_count` int(11) NOT NULL DEFAULT '-1',
  `question_count` int(11) NOT NULL DEFAULT '-1',
  `included_answers_count` int(11) NOT NULL DEFAULT '-1',
  `gender` int(11) NOT NULL DEFAULT '-1',
  `logs_count` int(11) NOT NULL DEFAULT '-1',
  `following_question_count` int(11) NOT NULL DEFAULT '-1',
  `thanked_count` int(11) NOT NULL DEFAULT '-1',
  `following_count` int(11) NOT NULL DEFAULT '-1',
  `vote_from_count` int(11) NOT NULL DEFAULT '-1',
  `pins_count` int(11) NOT NULL DEFAULT '-1',
  `included_articles_count` int(11) NOT NULL DEFAULT '-1',
  `favorite_count` int(11) NOT NULL DEFAULT '-1',
  `voteup_count` int(11) NOT NULL DEFAULT '-1',
  `commercial_question_count` int(11) NOT NULL DEFAULT '-1',
  `participated_live_count` int(11) NOT NULL DEFAULT '-1',
  `following_favlists_count` int(11) NOT NULL DEFAULT '-1',
  `favorited_count` int(11) NOT NULL DEFAULT '-1',
  `is_org` int(11) NOT NULL DEFAULT '-1',
  `follower_count` int(11) NOT NULL DEFAULT '-1',
  `following_columns_count` int(11) NOT NULL DEFAULT '-1',
  `location` json DEFAULT NULL,
  `badge` json DEFAULT NULL,
  `business` varchar(20) NOT NULL DEFAULT '',
  `employment` json DEFAULT NULL,
  `education` json DEFAULT NULL,
  `shared_count` int(11) NOT NULL DEFAULT '-1',
  `lite_favorite_content_count` int(11) NOT NULL DEFAULT '-1',
  `independent_articles_count` int(11) NOT NULL DEFAULT '-1',
  `reactions_count` int(11) NOT NULL DEFAULT '-1',
  `is_activity_blocked` int(11) NOT NULL DEFAULT '-1',
  `is_bind_sina` int(11) NOT NULL DEFAULT '-1',
  `is_hanged` int(11) NOT NULL DEFAULT '-1',
  `is_unicom_free` int(11) NOT NULL DEFAULT '-1',
  `live_count` int(11) NOT NULL DEFAULT '-1',
  `is_baned` int(11) NOT NULL DEFAULT '-1',
  `is_enable_signalment` int(11) NOT NULL DEFAULT '-1',
  `is_enable_watermark` int(11) NOT NULL DEFAULT '-1',
  `sina_weibo_url` varchar(200) NOT NULL DEFAULT '',
  `sina_weibo_name` varchar(50) NOT NULL DEFAULT '',
  `marked_answers_text` varchar(1000) NOT NULL DEFAULT '',
  `infinity` json DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间戳',
  PRIMARY KEY (`sort_order`),
  UNIQUE KEY `main_index` (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=111883 DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;
