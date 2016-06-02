/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50627
 Source Host           : localhost
 Source Database       : gun

 Target Server Type    : MySQL
 Target Server Version : 50627
 File Encoding         : utf-8

 Date: 06/03/2016 00:41:49 AM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `gun_domains`
-- ----------------------------
DROP TABLE IF EXISTS `gun_domains`;
CREATE TABLE `gun_domains` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '域名id',
  `domain` varchar(50) DEFAULT NULL,
  `ip` varchar(1024) DEFAULT NULL,
  `status` int(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=74 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `gun_ips`
-- ----------------------------
DROP TABLE IF EXISTS `gun_ips`;
CREATE TABLE `gun_ips` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(15) DEFAULT NULL,
  `port` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
