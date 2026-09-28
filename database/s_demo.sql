/*
SQLyog Ultimate v12.5.0 (64 bit)
MySQL - 8.0.30 : Database - s_demo
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`s_demo` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `s_demo`;

/*Table structure for table `ai_operational_insights` */

DROP TABLE IF EXISTS `ai_operational_insights`;

CREATE TABLE `ai_operational_insights` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `impact_level` enum('high','medium','low') DEFAULT 'high',
  `potential_savings` decimal(12,2) DEFAULT '0.00',
  `status` enum('new','actioned','dismissed') DEFAULT 'new',
  `generated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `ai_operational_insights` */

insert  into `ai_operational_insights`(`id`,`title`,`description`,`impact_level`,`potential_savings`,`status`,`generated_at`) values (1,'Overtime Optimization in Trafford Depot','AI analysis identified 42 hours of unplanned overtime across night shifts. Auto-scheduling open shift redistribution can reduce overtime costs.','high',14200.00,'new','2026-09-01 23:26:35'),(2,'Guard Patrol Route Efficiency Alert','Re-sequencing NFC checkpoint scans at Canary Wharf reduces guard fatigue and improves patrol coverage density by 14%.','medium',6500.00,'new','2026-09-01 23:26:35');

/*Table structure for table `attendance` */

DROP TABLE IF EXISTS `attendance`;

CREATE TABLE `attendance` (
  `id` int NOT NULL AUTO_INCREMENT,
  `shift_id` int NOT NULL,
  `guard_id` int NOT NULL,
  `site_id` int NOT NULL,
  `clock_in_at` datetime DEFAULT NULL,
  `clock_out_at` datetime DEFAULT NULL,
  `status` enum('pending','present','late','absent','no_show') NOT NULL DEFAULT 'pending',
  `override_reason` text,
  `check_in_latitude` decimal(10,7) DEFAULT NULL,
  `check_in_longitude` decimal(10,7) DEFAULT NULL,
  `created_by` int DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_by` int DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `shift_id` (`shift_id`),
  KEY `idx_attendance_guard` (`guard_id`),
  KEY `idx_attendance_site` (`site_id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `attendance` */

insert  into `attendance`(`id`,`shift_id`,`guard_id`,`site_id`,`clock_in_at`,`clock_out_at`,`status`,`override_reason`,`check_in_latitude`,`check_in_longitude`,`created_by`,`created_at`,`updated_by`,`updated_at`) values (1,1,4,3,'2026-08-03 08:03:00','2026-08-03 16:02:00','present',NULL,33.7294000,73.0931000,1,'2026-08-06 22:11:03',NULL,NULL),(2,2,5,4,'2026-08-04 20:17:00','2026-08-05 04:04:00','late',NULL,24.7980000,67.3060000,1,'2026-08-06 22:11:03',NULL,NULL),(3,3,3,3,'2026-08-01 08:00:00','2026-08-01 16:00:00','present',NULL,NULL,NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(4,4,4,4,'2026-08-01 08:00:00','2026-08-01 16:00:00','present',NULL,NULL,NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(5,5,5,5,'2026-08-01 08:00:00','2026-08-01 16:00:00','present',NULL,NULL,NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(6,6,6,6,'2026-08-01 08:00:00','2026-08-01 16:00:00','present',NULL,NULL,NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(7,7,7,7,'2026-08-01 08:00:00','2026-08-01 16:00:00','present',NULL,NULL,NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(8,8,8,8,'2026-08-01 08:00:00','2026-08-01 16:00:00','present',NULL,NULL,NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(9,9,9,9,'2026-08-01 08:00:00','2026-08-01 16:00:00','present',NULL,NULL,NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(10,10,10,10,'2026-08-01 08:00:00','2026-08-01 16:00:00','present',NULL,NULL,NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(11,11,11,11,'2026-08-01 08:00:00','2026-08-01 16:00:00','present',NULL,NULL,NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(12,12,12,12,'2026-08-01 08:00:00','2026-08-01 16:00:00','present',NULL,NULL,NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(13,13,13,13,'2026-08-01 08:00:00','2026-08-01 16:00:00','present',NULL,NULL,NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(14,14,14,14,'2026-08-01 08:00:00','2026-08-01 16:00:00','present',NULL,NULL,NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(15,15,15,15,'2026-08-01 08:00:00','2026-08-01 16:00:00','present',NULL,NULL,NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(16,16,16,16,'2026-08-01 08:00:00','2026-08-01 16:00:00','present',NULL,NULL,NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(17,17,17,17,'2026-08-01 08:00:00','2026-08-01 16:00:00','present',NULL,NULL,NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(18,18,18,18,'2026-08-01 08:00:00','2026-08-01 16:00:00','present',NULL,NULL,NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(19,19,19,19,'2026-08-01 08:00:00','2026-08-01 16:00:00','present',NULL,NULL,NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(20,20,20,20,'2026-08-01 08:00:00','2026-08-01 16:00:00','present',NULL,NULL,NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(21,21,21,21,'2026-08-01 08:00:00','2026-08-01 16:00:00','present',NULL,NULL,NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(22,22,22,22,'2026-08-01 08:00:00','2026-08-01 16:00:00','present',NULL,NULL,NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(23,23,23,23,'2026-08-01 08:00:00','2026-08-01 16:00:00','present',NULL,NULL,NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(24,24,24,24,'2026-08-01 08:00:00','2026-08-01 16:00:00','present',NULL,NULL,NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(25,25,25,25,'2026-08-01 08:00:00','2026-08-01 16:00:00','present',NULL,NULL,NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(26,26,26,26,'2026-08-01 08:00:00','2026-08-01 16:00:00','present',NULL,NULL,NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(27,27,27,27,'2026-08-01 08:00:00','2026-08-01 16:00:00','present',NULL,NULL,NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(28,28,28,28,'2026-08-01 08:00:00','2026-08-01 16:00:00','present',NULL,NULL,NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(29,29,29,29,'2026-08-01 08:00:00','2026-08-01 16:00:00','present',NULL,NULL,NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(30,30,30,30,'2026-08-01 08:00:00','2026-08-01 16:00:00','present',NULL,NULL,NULL,NULL,'2026-08-11 19:59:47',NULL,NULL);

/*Table structure for table `charge_rates` */

DROP TABLE IF EXISTS `charge_rates`;

CREATE TABLE `charge_rates` (
  `id` int NOT NULL AUTO_INCREMENT,
  `client_name` varchar(150) NOT NULL,
  `site_id` int DEFAULT NULL,
  `day_charge` decimal(10,2) DEFAULT '18.50',
  `night_charge` decimal(10,2) DEFAULT '22.00',
  `holiday_charge` decimal(10,2) DEFAULT '27.75',
  `overtime_charge` decimal(10,2) DEFAULT '27.75',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `charge_rates` */

insert  into `charge_rates`(`id`,`client_name`,`site_id`,`day_charge`,`night_charge`,`holiday_charge`,`overtime_charge`,`updated_at`) values (1,'Apex Retail Group UK',1,22.00,26.00,33.00,33.00,'2026-09-01 23:16:31'),(2,'Metropolitan Logistics Hub',2,24.00,28.00,36.00,36.00,'2026-09-01 23:16:31');

/*Table structure for table `client_ai_conversations` */

DROP TABLE IF EXISTS `client_ai_conversations`;

CREATE TABLE `client_ai_conversations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `user_query` text NOT NULL,
  `ai_response` text NOT NULL,
  `intent` varchar(100) DEFAULT 'general_inquiry',
  `retrieved_doc_url` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `client_ai_conversations` */

insert  into `client_ai_conversations`(`id`,`user_id`,`user_query`,`ai_response`,`intent`,`retrieved_doc_url`,`created_at`) values (1,1,'Show me last week\'s incident count for Oxford Street site','During the week of August 24–31, 2026, 1 security incident (Shoplifting & Restraint) was logged at Oxford Street Flagship. The situation was resolved with zero loss.','incident_summary','/docs/incidents/INC-2026-088.pdf','2026-09-01 23:26:35'),(2,1,'What is the SIA licence compliance score for assigned guards?','100% of all assigned security officers on your site hold valid, audited SIA frontline licences with active DBS checks.','compliance_check','/docs/compliance/SIA_Audit_Report.pdf','2026-09-01 23:26:35');

/*Table structure for table `client_contracts` */

DROP TABLE IF EXISTS `client_contracts`;

CREATE TABLE `client_contracts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `client_name` varchar(150) NOT NULL,
  `site_id` int DEFAULT NULL,
  `contract_title` varchar(255) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `billing_cycle` enum('weekly','biweekly','monthly') DEFAULT 'monthly',
  `contract_value` decimal(12,2) DEFAULT '0.00',
  `status` enum('active','pending_renewal','expired','cancelled') DEFAULT 'active',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `client_contracts` */

insert  into `client_contracts`(`id`,`client_name`,`site_id`,`contract_title`,`start_date`,`end_date`,`billing_cycle`,`contract_value`,`status`,`created_at`) values (1,'Apex Retail Group UK',1,'Oxford Street Flagship Master Service Agreement','2026-01-01','2027-12-31','monthly',185000.00,'active','2026-09-01 23:19:44'),(2,'Metropolitan Logistics Hub',2,'Trafford Logistics Perimeter Defense SLA','2026-03-01','2027-02-28','monthly',142000.00,'active','2026-09-01 23:19:44'),(3,'Horizon Financial Centre',3,'Canary Wharf Executive Protection Contract','2025-09-01','2026-09-30','monthly',220000.00,'pending_renewal','2026-09-01 23:19:44');

/*Table structure for table `custom_forms` */

DROP TABLE IF EXISTS `custom_forms`;

CREATE TABLE `custom_forms` (
  `id` int NOT NULL AUTO_INCREMENT,
  `form_title` varchar(150) NOT NULL,
  `category` varchar(50) DEFAULT 'general',
  `fields_json` json NOT NULL,
  `status` enum('active','archived') DEFAULT 'active',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `custom_forms` */

insert  into `custom_forms`(`id`,`form_title`,`category`,`fields_json`,`status`,`created_at`) values (1,'Perimeter Security Audit Form','inspection','[{\"type\": \"text\", \"label\": \"Inspector Name\"}, {\"type\": \"select\", \"label\": \"Fence Integrity\", \"options\": [\"Intact\", \"Damaged\", \"Breached\"]}, {\"type\": \"checkbox\", \"label\": \"CCTV Operational\"}, {\"type\": \"textarea\", \"label\": \"Audit Findings\"}]','active','2026-09-01 23:01:03');

/*Table structure for table `customers` */

DROP TABLE IF EXISTS `customers`;

CREATE TABLE `customers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer` varchar(255) DEFAULT NULL,
  `customer_code` varbinary(255) DEFAULT NULL,
  `email` varchar(225) DEFAULT NULL,
  `phone_number` varchar(255) DEFAULT NULL,
  `status` int DEFAULT '1',
  `address` varbinary(255) DEFAULT NULL,
  `photo_url` varchar(225) DEFAULT NULL,
  `created_by` int DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_by` int DEFAULT NULL,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `billing_rate` decimal(12,2) NOT NULL DEFAULT '0.00',
  `contract_start` date DEFAULT NULL,
  `contract_end` date DEFAULT NULL,
  `sla_terms` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `customers` */

insert  into `customers`(`id`,`customer`,`customer_code`,`email`,`phone_number`,`status`,`address`,`photo_url`,`created_by`,`created_at`,`updated_by`,`updated_at`,`billing_rate`,`contract_start`,`contract_end`,`sla_terms`) values (1,'Ashfaque','ABC','ashfaque@gmail.com','12336',1,'Lahore',NULL,1,'2026-08-04 22:46:13',5,'2026-08-04 22:46:15',0.00,NULL,NULL,NULL),(2,'ABC Security','af36b706-5789-44cd-a218-f8170f522bef','contact@gmail.com','022556',1,'022556',NULL,5,'2026-08-04 23:43:51',NULL,'2026-08-04 23:43:51',0.00,NULL,NULL,NULL),(3,'Acme Properties','CUST-ACME','billing@acme.test','+92 300 1111111',1,'Blue Area, Islamabad',NULL,1,'2026-08-06 22:11:03',NULL,'2026-08-06 22:11:03',1800.00,'2026-01-01','2026-12-31','24/7 guard coverage; 4-hour incident response.'),(4,'Nexus Logistics','CUST-NEXUS','accounts@nexus.test','+92 300 2222222',1,'Port Qasim, Karachi',NULL,1,'2026-08-06 22:11:03',NULL,'2026-08-06 22:11:03',2100.00,'2026-01-01','2026-12-31','Day and night warehouse coverage.'),(5,'Customer 5','CUST-BULK-5','cust5@test.com','+92300000005',1,'Address 5',NULL,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',1050.00,'2026-01-01','2026-12-31',NULL),(6,'Customer 6','CUST-BULK-6','cust6@test.com','+92300000006',1,'Address 6',NULL,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',1060.00,'2026-01-01','2026-12-31',NULL),(7,'Customer 7','CUST-BULK-7','cust7@test.com','+92300000007',1,'Address 7',NULL,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',1070.00,'2026-01-01','2026-12-31',NULL),(8,'Customer 8','CUST-BULK-8','cust8@test.com','+92300000008',1,'Address 8',NULL,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',1080.00,'2026-01-01','2026-12-31',NULL),(9,'Customer 9','CUST-BULK-9','cust9@test.com','+92300000009',1,'Address 9',NULL,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',1090.00,'2026-01-01','2026-12-31',NULL),(10,'Customer 10','CUST-BULK-10','cust10@test.com','+923000000010',1,'Address 10',NULL,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',1100.00,'2026-01-01','2026-12-31',NULL),(11,'Customer 11','CUST-BULK-11','cust11@test.com','+923000000011',1,'Address 11',NULL,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',1110.00,'2026-01-01','2026-12-31',NULL),(12,'Customer 12','CUST-BULK-12','cust12@test.com','+923000000012',1,'Address 12',NULL,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',1120.00,'2026-01-01','2026-12-31',NULL),(13,'Customer 13','CUST-BULK-13','cust13@test.com','+923000000013',1,'Address 13',NULL,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',1130.00,'2026-01-01','2026-12-31',NULL),(14,'Customer 14','CUST-BULK-14','cust14@test.com','+923000000014',1,'Address 14',NULL,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',1140.00,'2026-01-01','2026-12-31',NULL),(15,'Customer 15','CUST-BULK-15','cust15@test.com','+923000000015',1,'Address 15',NULL,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',1150.00,'2026-01-01','2026-12-31',NULL),(16,'Customer 16','CUST-BULK-16','cust16@test.com','+923000000016',1,'Address 16',NULL,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',1160.00,'2026-01-01','2026-12-31',NULL),(17,'Customer 17','CUST-BULK-17','cust17@test.com','+923000000017',1,'Address 17',NULL,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',1170.00,'2026-01-01','2026-12-31',NULL),(18,'Customer 18','CUST-BULK-18','cust18@test.com','+923000000018',1,'Address 18',NULL,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',1180.00,'2026-01-01','2026-12-31',NULL),(19,'Customer 19','CUST-BULK-19','cust19@test.com','+923000000019',1,'Address 19',NULL,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',1190.00,'2026-01-01','2026-12-31',NULL),(20,'Customer 20','CUST-BULK-20','cust20@test.com','+923000000020',1,'Address 20',NULL,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',1200.00,'2026-01-01','2026-12-31',NULL),(21,'Customer 21','CUST-BULK-21','cust21@test.com','+923000000021',1,'Address 21',NULL,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',1210.00,'2026-01-01','2026-12-31',NULL),(22,'Customer 22','CUST-BULK-22','cust22@test.com','+923000000022',1,'Address 22',NULL,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',1220.00,'2026-01-01','2026-12-31',NULL),(23,'Customer 23','CUST-BULK-23','cust23@test.com','+923000000023',1,'Address 23',NULL,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',1230.00,'2026-01-01','2026-12-31',NULL),(24,'Customer 24','CUST-BULK-24','cust24@test.com','+923000000024',1,'Address 24',NULL,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',1240.00,'2026-01-01','2026-12-31',NULL),(25,'Customer 25','CUST-BULK-25','cust25@test.com','+923000000025',1,'Address 25',NULL,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',1250.00,'2026-01-01','2026-12-31',NULL),(26,'Customer 26','CUST-BULK-26','cust26@test.com','+923000000026',1,'Address 26',NULL,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',1260.00,'2026-01-01','2026-12-31',NULL),(27,'Customer 27','CUST-BULK-27','cust27@test.com','+923000000027',1,'Address 27',NULL,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',1270.00,'2026-01-01','2026-12-31',NULL),(28,'Customer 28','CUST-BULK-28','cust28@test.com','+923000000028',1,'Address 28',NULL,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',1280.00,'2026-01-01','2026-12-31',NULL),(29,'Customer 29','CUST-BULK-29','cust29@test.com','+923000000029',1,'Address 29',NULL,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',1290.00,'2026-01-01','2026-12-31',NULL),(30,'Customer 30','CUST-BULK-30','cust30@test.com','+923000000030',1,'Address 30',NULL,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',1300.00,'2026-01-01','2026-12-31',NULL);

/*Table structure for table `executive_bi_metrics` */

DROP TABLE IF EXISTS `executive_bi_metrics`;

CREATE TABLE `executive_bi_metrics` (
  `id` int NOT NULL AUTO_INCREMENT,
  `metric_key` varchar(100) NOT NULL,
  `metric_value` decimal(14,2) NOT NULL,
  `metric_category` varchar(100) NOT NULL,
  `period_date` date NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `executive_bi_metrics` */

insert  into `executive_bi_metrics`(`id`,`metric_key`,`metric_value`,`metric_category`,`period_date`,`created_at`) values (1,'annual_recurring_revenue',2840000.00,'financial','2026-08-31','2026-09-01 23:26:35'),(2,'gross_profit_margin_pct',35.80,'financial','2026-08-31','2026-09-01 23:26:35'),(3,'total_labor_cost',1420000.00,'operational','2026-08-31','2026-09-01 23:26:35'),(4,'sla_compliance_rate_pct',99.10,'sla','2026-08-31','2026-09-01 23:26:35');

/*Table structure for table `finance_integrations` */

DROP TABLE IF EXISTS `finance_integrations`;

CREATE TABLE `finance_integrations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `platform` enum('xero','quickbooks','sage') NOT NULL,
  `status` enum('connected','disconnected','sync_error') DEFAULT 'disconnected',
  `config_json` text,
  `last_synced_at` datetime DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `finance_integrations` */

insert  into `finance_integrations`(`id`,`platform`,`status`,`config_json`,`last_synced_at`,`updated_at`) values (1,'xero','connected',NULL,'2026-09-01 12:00:00','2026-09-01 23:11:26'),(2,'quickbooks','connected',NULL,'2026-09-01 10:30:00','2026-09-01 23:11:26'),(3,'sage','disconnected',NULL,NULL,'2026-09-01 23:11:26'),(4,'xero','connected',NULL,'2026-09-01 23:14:48','2026-09-01 23:14:48'),(5,'quickbooks','connected',NULL,'2026-09-01 23:14:58','2026-09-01 23:14:58'),(6,'xero','connected',NULL,'2026-09-01 23:32:44','2026-09-01 23:32:44'),(7,'quickbooks','connected',NULL,'2026-09-01 23:32:45','2026-09-01 23:32:45');

/*Table structure for table `guard_availabilities` */

DROP TABLE IF EXISTS `guard_availabilities`;

CREATE TABLE `guard_availabilities` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `guard_id` int(11) NOT NULL,
  `day_of_week` enum('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday') NOT NULL,
  `start_at` datetime DEFAULT NULL,
  `end_at` datetime DEFAULT NULL,
  `status` enum('available','preferred','unavailable') DEFAULT 'available',
  `notes` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_guard_day` (`guard_id`,`day_of_week`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `guard_availabilities` */

/*Table structure for table `guard_compliance` */

DROP TABLE IF EXISTS `guard_compliance`;

CREATE TABLE `guard_compliance` (
  `id` int NOT NULL AUTO_INCREMENT,
  `guard_id` int NOT NULL,
  `sia_license_number` varchar(100) DEFAULT NULL,
  `sia_expiry_date` date DEFAULT NULL,
  `sia_status` enum('valid','expiring_soon','expired','unverified') DEFAULT 'unverified',
  `dbs_certificate_number` varchar(100) DEFAULT NULL,
  `dbs_issue_date` date DEFAULT NULL,
  `dbs_status` enum('valid','expired','unverified') DEFAULT 'unverified',
  `right_to_work_type` varchar(100) DEFAULT NULL,
  `rtw_expiry_date` date DEFAULT NULL,
  `rtw_status` enum('valid','expiring_soon','expired','unverified') DEFAULT 'unverified',
  `is_scheduling_blocked` tinyint(1) DEFAULT '0',
  `notes` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_guard_compliance_guard` (`guard_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `guard_compliance` */

insert  into `guard_compliance`(`id`,`guard_id`,`sia_license_number`,`sia_expiry_date`,`sia_status`,`dbs_certificate_number`,`dbs_issue_date`,`dbs_status`,`right_to_work_type`,`rtw_expiry_date`,`rtw_status`,`is_scheduling_blocked`,`notes`,`created_at`,`updated_at`) values (1,1,'SIA-99201948','2027-05-15','valid','DBS-0098231','2024-01-10','valid','UK Passport','2030-12-31','valid',0,NULL,'2026-09-01 23:11:26','2026-09-01 23:11:26'),(2,2,'SIA-11029384','2026-10-01','expiring_soon','DBS-0044812','2023-06-12','valid','Share Code / Visa','2026-11-15','expiring_soon',0,NULL,'2026-09-01 23:11:26','2026-09-01 23:11:26'),(3,3,'SIA-77401928','2026-08-01','expired','DBS-0019283','2022-04-01','expired','Biometric Residence Permit','2026-08-01','expired',1,NULL,'2026-09-01 23:11:26','2026-09-01 23:11:26'),(4,4,'SIA-44019283','2026-08-01','expired','DBS-0033192','2022-02-15','expired','UK Passport','2030-10-10','expired',1,NULL,'2026-09-01 23:16:31','2026-09-01 23:16:31');

/*Table structure for table `guard_documents` */

DROP TABLE IF EXISTS `guard_documents`;

CREATE TABLE `guard_documents` (
  `id` int NOT NULL AUTO_INCREMENT,
  `guard_id` int NOT NULL,
  `document_type` varchar(100) NOT NULL,
  `document_name` varchar(255) NOT NULL,
  `file_url` varchar(500) DEFAULT NULL,
  `expiry_date` date DEFAULT NULL,
  `status` enum('approved','pending_review','expired','rejected') DEFAULT 'pending_review',
  `uploaded_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `guard_documents` */

insert  into `guard_documents`(`id`,`guard_id`,`document_type`,`document_name`,`file_url`,`expiry_date`,`status`,`uploaded_at`) values (1,1,'SIA Licence Card Front','sia_front_g1001.pdf','#','2027-05-15','approved','2026-09-01 23:16:31'),(2,2,'Right to Work Share Code Verification','rtw_sharecode_g1002.pdf','#','2026-11-15','approved','2026-09-01 23:16:31');

/*Table structure for table `guard_requests` */

DROP TABLE IF EXISTS `guard_requests`;

CREATE TABLE `guard_requests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `guard_id` int NOT NULL,
  `type` enum('leave','swap') NOT NULL,
  `shift_id` int DEFAULT NULL,
  `target_shift_id` int DEFAULT NULL,
  `target_guard_id` int DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `reason` text,
  `status` enum('pending','approved','rejected') NOT NULL DEFAULT 'pending',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_guard_requests_guard` (`guard_id`),
  KEY `idx_guard_requests_status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `guard_requests` */

insert  into `guard_requests`(`id`,`guard_id`,`type`,`shift_id`,`target_shift_id`,`target_guard_id`,`start_date`,`end_date`,`reason`,`status`,`created_at`,`updated_at`) values (1,2,'leave',NULL,NULL,NULL,'2026-08-12','2026-08-15','Personal leave for 1 days','approved','2026-08-11 19:56:09',NULL),(2,1,'swap',3,1,2,NULL,NULL,'Requesting swap due to family event 2','pending','2026-08-11 19:56:09',NULL),(3,2,'swap',1,2,1,NULL,NULL,'Requesting swap due to family event 3','pending','2026-08-11 19:56:09',NULL),(4,1,'leave',NULL,NULL,NULL,'2026-08-13','2026-08-16','Personal leave for 4 days','approved','2026-08-11 19:56:09',NULL),(5,2,'swap',3,1,1,NULL,NULL,'Requesting swap due to family event 5','pending','2026-08-11 19:56:09',NULL),(6,1,'swap',1,2,2,NULL,NULL,'Requesting swap due to family event 6','approved','2026-08-11 19:56:09',NULL),(7,2,'leave',NULL,NULL,NULL,'2026-08-11','2026-08-13','Personal leave for 7 days','approved','2026-08-11 19:56:09',NULL),(8,1,'leave',NULL,NULL,NULL,'2026-08-26','2026-08-30','Personal leave for 8 days','pending','2026-08-11 19:56:09',NULL),(9,2,'swap',1,2,1,NULL,NULL,'Requesting swap due to family event 9','pending','2026-08-11 19:56:09',NULL),(10,1,'swap',2,3,2,NULL,NULL,'Requesting swap due to family event 10','approved','2026-08-11 19:56:09',NULL),(11,2,'leave',NULL,NULL,NULL,'2026-08-14','2026-08-18','Personal leave for 11 days','approved','2026-08-11 19:56:09',NULL),(12,1,'leave',NULL,NULL,NULL,'2026-08-24','2026-08-25','Personal leave for 12 days','rejected','2026-08-11 19:56:09',NULL),(13,2,'leave',NULL,NULL,NULL,'2026-08-15','2026-08-18','Personal leave for 13 days','approved','2026-08-11 19:56:09',NULL),(14,1,'swap',3,1,2,NULL,NULL,'Requesting swap due to family event 14','approved','2026-08-11 19:56:09',NULL),(15,2,'swap',1,2,1,NULL,NULL,'Requesting swap due to family event 15','pending','2026-08-11 19:56:09',NULL),(16,1,'swap',2,3,2,NULL,NULL,'Requesting swap due to family event 16','pending','2026-08-11 19:56:09',NULL),(17,2,'swap',3,1,1,NULL,NULL,'Requesting swap due to family event 17','approved','2026-08-11 19:56:09',NULL),(18,1,'leave',NULL,NULL,NULL,'2026-08-12','2026-08-15','Personal leave for 18 days','pending','2026-08-11 19:56:09',NULL),(19,2,'leave',NULL,NULL,NULL,'2026-08-28','2026-08-31','Personal leave for 19 days','approved','2026-08-11 19:56:09',NULL),(20,1,'leave',NULL,NULL,NULL,'2026-08-01','2026-08-04','Personal leave for 20 days','rejected','2026-08-11 19:56:09',NULL),(21,2,'leave',NULL,NULL,NULL,'2026-08-17','2026-08-20','Personal leave for 21 days','pending','2026-08-11 19:56:09',NULL),(22,1,'swap',2,3,2,NULL,NULL,'Requesting swap due to family event 22','approved','2026-08-11 19:56:09',NULL),(23,2,'swap',3,1,1,NULL,NULL,'Requesting swap due to family event 23','approved','2026-08-11 19:56:09',NULL),(24,1,'swap',1,2,2,NULL,NULL,'Requesting swap due to family event 24','rejected','2026-08-11 19:56:09',NULL),(25,2,'leave',NULL,NULL,NULL,'2026-08-10','2026-08-11','Personal leave for 25 days','rejected','2026-08-11 19:56:09',NULL),(26,1,'leave',NULL,NULL,NULL,'2026-08-18','2026-08-19','Personal leave for 26 days','pending','2026-08-11 19:56:09',NULL),(27,2,'swap',1,2,1,NULL,NULL,'Requesting swap due to family event 27','pending','2026-08-11 19:56:09',NULL),(28,1,'swap',2,3,2,NULL,NULL,'Requesting swap due to family event 28','pending','2026-08-11 19:56:09',NULL),(29,2,'leave',NULL,NULL,NULL,'2026-08-25','2026-08-27','Personal leave for 29 days','pending','2026-08-11 19:56:09',NULL),(30,1,'leave',NULL,NULL,NULL,'2026-08-04','2026-08-08','Personal leave for 30 days','pending','2026-08-11 19:56:09',NULL);

/*Table structure for table `guard_telemetry` */

DROP TABLE IF EXISTS `guard_telemetry`;

CREATE TABLE `guard_telemetry` (
  `id` int NOT NULL AUTO_INCREMENT,
  `guard_id` int NOT NULL,
  `latitude` decimal(10,7) NOT NULL,
  `longitude` decimal(10,7) NOT NULL,
  `battery_level` int DEFAULT '100',
  `patrol_status` enum('on_patrol','stationary','sos_alert','off_duty') DEFAULT 'on_patrol',
  `speed_kmh` decimal(5,2) DEFAULT '0.00',
  `last_ping_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_telemetry_guard` (`guard_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `guard_telemetry` */

/*Table structure for table `guards` */

DROP TABLE IF EXISTS `guards`;

CREATE TABLE `guards` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(225) DEFAULT NULL,
  `last_name` varchar(225) DEFAULT NULL,
  `guard_code` varbinary(255) DEFAULT NULL,
  `email` varchar(225) DEFAULT NULL,
  `gender` enum('male','female','other') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `dob` datetime DEFAULT NULL,
  `phone_number` varchar(255) DEFAULT NULL,
  `guard_passport` varchar(255) DEFAULT NULL,
  `license_number` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `license_expiry` datetime DEFAULT NULL,
  `status` int DEFAULT '1',
  `address` varbinary(255) DEFAULT NULL,
  `photo_url` varchar(225) DEFAULT NULL,
  `created_by` int DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_by` int DEFAULT NULL,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `emergency_contact` varchar(255) DEFAULT NULL,
  `employment_status` varchar(30) NOT NULL DEFAULT 'active',
  `pay_rate` decimal(12,2) NOT NULL DEFAULT '0.00',
  `skills` json DEFAULT NULL,
  `availability_preferences` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `guards` */

insert  into `guards`(`id`,`first_name`,`last_name`,`guard_code`,`email`,`gender`,`dob`,`phone_number`,`guard_passport`,`license_number`,`license_expiry`,`status`,`address`,`photo_url`,`created_by`,`created_at`,`updated_by`,`updated_at`,`emergency_contact`,`employment_status`,`pay_rate`,`skills`,`availability_preferences`) values (1,'Ashfaque','Solangi','d812f633-0aa1-4fd7-abc9-c56a685393b1','ashfaqueaas1995@gmail.com','male','2026-08-05 00:00:00','02141324123','1243124','4123412','2026-08-01 00:00:00',1,'R/O Village Dedar',NULL,5,'2026-08-05 22:25:06',NULL,'2026-08-05 22:25:06',NULL,'active',0.00,NULL,NULL),(2,'Female','Female','e51f6acf-c14c-49c9-bc2b-390a2d2b4e22','new@gmail.com','female','2026-08-04 00:00:00','234123','431243124','123412341','2026-07-31 00:00:00',1,'Lhr',NULL,5,'2026-08-05 22:45:31',5,'2026-08-05 22:45:31',NULL,'active',0.00,NULL,NULL),(3,'Ashfaque','Ahmed','6ac35631-2975-4e63-bf34-e714657bc79f','aliguddu855@gmail.com','male','2026-07-31 00:00:00','03463397797','1234123','324312','2026-07-31 00:00:00',1,'Lahore',NULL,5,'2026-08-05 23:02:40',5,'2026-08-05 23:02:40',NULL,'active',0.00,NULL,NULL),(4,'Ali','Khan','GUARD-ALI','ali.khan@test.local','male','1992-05-12 00:00:00','+92 300 3333333','PK-10001','LIC-10001','2027-05-12 00:00:00',1,'Islamabad',NULL,1,'2026-08-06 22:11:03',NULL,'2026-08-06 22:11:03','Sara Khan +92 300 4333333','active',900.00,'[\"unarmed\", \"first aid\"]','Available for day shifts.'),(5,'Sana','Ahmed','GUARD-SANA','sana.ahmed@test.local','female','1995-09-20 00:00:00','+92 300 4444444','PK-10002','LIC-10002','2027-09-20 00:00:00',1,'Karachi',NULL,1,'2026-08-06 22:11:03',NULL,'2026-08-06 22:11:03','Usman Ahmed +92 300 5444444','active',950.00,'[\"unarmed\", \"CCTV\"]','Available for night shifts.'),(6,'Naveed','Javed','GUARD-NEW-1','naveed.javed1@test.local',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',NULL,'active',900.00,NULL,NULL),(7,'Zeeshan','Qureshi','GUARD-NEW-2','zeeshan.qureshi2@test.local',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',NULL,'active',900.00,NULL,NULL),(8,'Tariq','Javed','GUARD-NEW-3','tariq.javed3@test.local',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',NULL,'active',900.00,NULL,NULL),(9,'Tariq','Hussain','GUARD-NEW-4','tariq.hussain4@test.local',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',NULL,'active',900.00,NULL,NULL),(10,'Faisal','Javed','GUARD-NEW-5','faisal.javed5@test.local',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',NULL,'active',900.00,NULL,NULL),(11,'Naveed','Iqbal','GUARD-NEW-6','naveed.iqbal6@test.local',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',NULL,'active',900.00,NULL,NULL),(12,'Kashif','Hussain','GUARD-NEW-7','kashif.hussain7@test.local',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',NULL,'active',900.00,NULL,NULL),(13,'Zeeshan','Malik','GUARD-NEW-8','zeeshan.malik8@test.local',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',NULL,'active',900.00,NULL,NULL),(14,'Imran','Shah','GUARD-NEW-9','imran.shah9@test.local',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',NULL,'active',900.00,NULL,NULL),(15,'Ahmed','Khan','GUARD-NEW-10','ahmed.khan10@test.local',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',NULL,'active',900.00,NULL,NULL),(16,'Kashif','Khan','GUARD-NEW-11','kashif.khan11@test.local',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',NULL,'active',900.00,NULL,NULL),(17,'Usman','Shah','GUARD-NEW-12','usman.shah12@test.local',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',NULL,'active',900.00,NULL,NULL),(18,'Faisal','Khan','GUARD-NEW-13','faisal.khan13@test.local',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',NULL,'active',900.00,NULL,NULL),(19,'Kashif','Ali','GUARD-NEW-14','kashif.ali14@test.local',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',NULL,'active',900.00,NULL,NULL),(20,'Naveed','Iqbal','GUARD-NEW-15','naveed.iqbal15@test.local',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',NULL,'active',900.00,NULL,NULL),(21,'Kashif','Hussain','GUARD-NEW-16','kashif.hussain16@test.local',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',NULL,'active',900.00,NULL,NULL),(22,'Ahmed','Ali','GUARD-NEW-17','ahmed.ali17@test.local',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',NULL,'active',900.00,NULL,NULL),(23,'Tariq','Khan','GUARD-NEW-18','tariq.khan18@test.local',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',NULL,'active',900.00,NULL,NULL),(24,'Faisal','Raza','GUARD-NEW-19','faisal.raza19@test.local',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',NULL,'active',900.00,NULL,NULL),(25,'Tariq','Javed','GUARD-NEW-20','tariq.javed20@test.local',NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',NULL,'active',900.00,NULL,NULL),(26,'GuardFN26','GuardLN26','GUARD-BULK-26','guard26@test.com','male',NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',NULL,'active',900.00,NULL,NULL),(27,'GuardFN27','GuardLN27','GUARD-BULK-27','guard27@test.com','male',NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',NULL,'active',900.00,NULL,NULL),(28,'GuardFN28','GuardLN28','GUARD-BULK-28','guard28@test.com','male',NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',NULL,'active',900.00,NULL,NULL),(29,'GuardFN29','GuardLN29','GUARD-BULK-29','guard29@test.com','male',NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',NULL,'active',900.00,NULL,NULL),(30,'GuardFN30','GuardLN30','GUARD-BULK-30','guard30@test.com','male',NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',NULL,'active',900.00,NULL,NULL),(31,'new guard list','guard','6ea1e01a-e8e7-4711-a6cc-56be03abc969','guard@gmail.com','male','2012-08-24 00:00:00','02141324123','1243124','4123412','2026-08-01 00:00:00',1,'R/O Village Dedar',NULL,5,'2026-08-24 23:14:11',NULL,'2026-08-24 23:14:11',NULL,'active',0.00,NULL,NULL);

/*Table structure for table `hazard_reports` */

DROP TABLE IF EXISTS `hazard_reports`;

CREATE TABLE `hazard_reports` (
  `id` int NOT NULL AUTO_INCREMENT,
  `hazard_code` varchar(50) DEFAULT NULL,
  `site_id` int DEFAULT NULL,
  `guard_id` int DEFAULT NULL,
  `title` varchar(255) NOT NULL,
  `hazard_type` enum('slip_trip','electrical','structural','fire_hazard','lighting','chemical','other') DEFAULT 'other',
  `severity` enum('low','medium','high') DEFAULT 'medium',
  `status` enum('open','mitigated','resolved') DEFAULT 'open',
  `notes` text,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `hazard_reports` */

insert  into `hazard_reports`(`id`,`hazard_code`,`site_id`,`guard_id`,`title`,`hazard_type`,`severity`,`status`,`notes`,`created_at`) values (1,'HAZ-2001',NULL,NULL,'Exposed Conduit Wires','electrical','high','open','Conduit cover damaged near West Stairwell landing floor 2.','2026-08-24 22:54:33'),(2,'HAZ-2002',NULL,NULL,'Loose Overhead Floodlight Bracket','structural','medium','open','Outdoor LED floodlight loose after high wind storm.','2026-08-24 22:54:33'),(3,'HAZ-2003',NULL,NULL,'Hydraulic Oil Leak Near Elevator','slip_trip','high','mitigated','Absorbent pads applied. Maintenance ticket submitted.','2026-08-24 22:54:33');

/*Table structure for table `hr_employee_profiles` */

DROP TABLE IF EXISTS `hr_employee_profiles`;

CREATE TABLE `hr_employee_profiles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `guard_id` int NOT NULL,
  `job_title` varchar(100) DEFAULT 'Security Officer',
  `tax_code` varchar(20) DEFAULT '1257L',
  `bank_sort_code` varchar(20) DEFAULT '20-40-60',
  `bank_account_number` varchar(20) DEFAULT '88291044',
  `emergency_contact_name` varchar(100) DEFAULT NULL,
  `emergency_contact_phone` varchar(50) DEFAULT NULL,
  `employment_type` enum('full_time','part_time','zero_hours','subcontractor') DEFAULT 'full_time',
  `onboarding_status` enum('invited','in_progress','completed','verified') DEFAULT 'completed',
  `annual_leave_allowance` int DEFAULT '28',
  `annual_leave_taken` int DEFAULT '4',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_hr_profile_guard` (`guard_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `hr_employee_profiles` */

insert  into `hr_employee_profiles`(`id`,`guard_id`,`job_title`,`tax_code`,`bank_sort_code`,`bank_account_number`,`emergency_contact_name`,`emergency_contact_phone`,`employment_type`,`onboarding_status`,`annual_leave_allowance`,`annual_leave_taken`,`created_at`) values (1,1,'Senior Security Officer','1257L','20-40-60','88291044','Sarah Vance (Wife)','+44 7700 900881','full_time','verified',28,5,'2026-09-01 23:19:44'),(2,2,'Security Gate Supervisor','1257L','20-40-60','88291044','Dmitri Rostov (Father)','+44 7700 900882','full_time','verified',28,8,'2026-09-01 23:19:44'),(3,3,'Mobile Patrol Specialist','1257L','20-40-60','88291044','Claire O\'Connor','+44 7700 900883','zero_hours','completed',20,2,'2026-09-01 23:19:44');

/*Table structure for table `incidents` */

DROP TABLE IF EXISTS `incidents`;

CREATE TABLE `incidents` (
  `id` int NOT NULL AUTO_INCREMENT,
  `incident_code` varchar(50) DEFAULT NULL,
  `site_id` int DEFAULT NULL,
  `reported_by_guard_id` int DEFAULT NULL,
  `title` varchar(255) NOT NULL,
  `category` enum('trespass','theft','property_damage','medical','fire','unauthorized_access','other') DEFAULT 'other',
  `severity` enum('low','medium','high','critical') DEFAULT 'medium',
  `status` enum('open','investigating','resolved','closed') DEFAULT 'open',
  `description` text,
  `location_details` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `incidents` */

insert  into `incidents`(`id`,`incident_code`,`site_id`,`reported_by_guard_id`,`title`,`category`,`severity`,`status`,`description`,`location_details`,`created_at`,`updated_at`) values (1,'INC-1001',NULL,NULL,'Unauthorized Perimeter Entry','trespass','high','investigating','Individual triggered motion sensors at South Wall. Officer dispatched.','Gate 4 Perimeter Fence','2026-08-24 22:54:33','2026-08-24 22:54:33'),(2,'INC-1002',NULL,NULL,'Lobby Glass Door Damage','property_damage','medium','open','Crack observed on lower panel of revolving entrance door.','Main Building Lobby','2026-08-24 22:54:33','2026-08-24 22:54:33'),(3,'INC-1003',NULL,NULL,'Overheated Transformer Warning','fire','critical','open','Thermal camera registered 92C on Main Distribution Board 3.','Electrical Substation B','2026-08-24 22:54:33','2026-08-24 22:54:33'),(4,'INC-1004',NULL,NULL,'Medical Assistance Required','medical','low','resolved','Contractor slipped on wet ramp. First aid applied on site.','Loading Dock Ramp B','2026-08-24 22:54:33','2026-08-24 22:54:33');

/*Table structure for table `invoices` */

DROP TABLE IF EXISTS `invoices`;

CREATE TABLE `invoices` (
  `id` int NOT NULL AUTO_INCREMENT,
  `invoice_number` varchar(64) NOT NULL,
  `customer_id` int NOT NULL,
  `site_id` int DEFAULT NULL,
  `period_start` date NOT NULL,
  `period_end` date NOT NULL,
  `hours_billed` decimal(10,2) NOT NULL DEFAULT '0.00',
  `rate` decimal(12,2) NOT NULL DEFAULT '0.00',
  `total_amount` decimal(12,2) NOT NULL DEFAULT '0.00',
  `status` enum('draft','issued','paid','overdue','void') NOT NULL DEFAULT 'draft',
  `generated_from_attendance` tinyint(1) NOT NULL DEFAULT '1',
  `created_by` int DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_by` int DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `invoice_number` (`invoice_number`),
  KEY `idx_invoice_customer` (`customer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `invoices` */

insert  into `invoices`(`id`,`invoice_number`,`customer_id`,`site_id`,`period_start`,`period_end`,`hours_billed`,`rate`,`total_amount`,`status`,`generated_from_attendance`,`created_by`,`created_at`,`updated_by`,`updated_at`) values (1,'INV-2026-001',3,3,'2026-08-01','2026-08-31',7.98,1800.00,14364.00,'issued',1,1,'2026-08-06 22:11:03',NULL,NULL),(2,'INV-BULK-2',2,2,'2026-08-01','2026-08-31',160.00,0.00,15000.00,'issued',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(3,'INV-BULK-3',3,3,'2026-08-01','2026-08-31',160.00,0.00,15000.00,'issued',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(4,'INV-BULK-4',4,4,'2026-08-01','2026-08-31',160.00,0.00,15000.00,'issued',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(5,'INV-BULK-5',5,5,'2026-08-01','2026-08-31',160.00,0.00,15000.00,'issued',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(6,'INV-BULK-6',6,6,'2026-08-01','2026-08-31',160.00,0.00,15000.00,'issued',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(7,'INV-BULK-7',7,7,'2026-08-01','2026-08-31',160.00,0.00,15000.00,'issued',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(8,'INV-BULK-8',8,8,'2026-08-01','2026-08-31',160.00,0.00,15000.00,'issued',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(9,'INV-BULK-9',9,9,'2026-08-01','2026-08-31',160.00,0.00,15000.00,'issued',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(10,'INV-BULK-10',10,10,'2026-08-01','2026-08-31',160.00,0.00,15000.00,'issued',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(11,'INV-BULK-11',11,11,'2026-08-01','2026-08-31',160.00,0.00,15000.00,'issued',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(12,'INV-BULK-12',12,12,'2026-08-01','2026-08-31',160.00,0.00,15000.00,'issued',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(13,'INV-BULK-13',13,13,'2026-08-01','2026-08-31',160.00,0.00,15000.00,'issued',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(14,'INV-BULK-14',14,14,'2026-08-01','2026-08-31',160.00,0.00,15000.00,'issued',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(15,'INV-BULK-15',15,15,'2026-08-01','2026-08-31',160.00,0.00,15000.00,'issued',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(16,'INV-BULK-16',16,16,'2026-08-01','2026-08-31',160.00,0.00,15000.00,'issued',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(17,'INV-BULK-17',17,17,'2026-08-01','2026-08-31',160.00,0.00,15000.00,'issued',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(18,'INV-BULK-18',18,18,'2026-08-01','2026-08-31',160.00,0.00,15000.00,'issued',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(19,'INV-BULK-19',19,19,'2026-08-01','2026-08-31',160.00,0.00,15000.00,'issued',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(20,'INV-BULK-20',20,20,'2026-08-01','2026-08-31',160.00,0.00,15000.00,'issued',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(21,'INV-BULK-21',21,21,'2026-08-01','2026-08-31',160.00,0.00,15000.00,'issued',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(22,'INV-BULK-22',22,22,'2026-08-01','2026-08-31',160.00,0.00,15000.00,'issued',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(23,'INV-BULK-23',23,23,'2026-08-01','2026-08-31',160.00,0.00,15000.00,'issued',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(24,'INV-BULK-24',24,24,'2026-08-01','2026-08-31',160.00,0.00,15000.00,'issued',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(25,'INV-BULK-25',25,25,'2026-08-01','2026-08-31',160.00,0.00,15000.00,'issued',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(26,'INV-BULK-26',26,26,'2026-08-01','2026-08-31',160.00,0.00,15000.00,'issued',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(27,'INV-BULK-27',27,27,'2026-08-01','2026-08-31',160.00,0.00,15000.00,'issued',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(28,'INV-BULK-28',28,28,'2026-08-01','2026-08-31',160.00,0.00,15000.00,'issued',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(29,'INV-BULK-29',29,29,'2026-08-01','2026-08-31',160.00,0.00,15000.00,'issued',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(30,'INV-BULK-30',30,30,'2026-08-01','2026-08-31',160.00,0.00,15000.00,'issued',1,NULL,'2026-08-11 19:59:47',NULL,NULL);

/*Table structure for table `leave_requests` */

DROP TABLE IF EXISTS `leave_requests`;

CREATE TABLE `leave_requests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `guard_id` int NOT NULL,
  `leave_type` enum('annual_leave','sick_leave','unpaid','compassionate') DEFAULT 'annual_leave',
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `total_days` int DEFAULT '1',
  `reason` text,
  `status` enum('pending','approved','rejected') DEFAULT 'pending',
  `approved_by` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `leave_requests` */

insert  into `leave_requests`(`id`,`guard_id`,`leave_type`,`start_date`,`end_date`,`total_days`,`reason`,`status`,`approved_by`,`created_at`) values (1,1,'annual_leave','2026-09-15','2026-09-20',5,'Family summer vacation in Cornwall','approved',NULL,'2026-09-01 23:19:44'),(2,2,'sick_leave','2026-08-10','2026-08-12',2,'Flu and fever','approved',NULL,'2026-09-01 23:19:44'),(3,3,'annual_leave','2026-10-01','2026-10-05',4,'Personal leave request','pending',NULL,'2026-09-01 23:19:44');

/*Table structure for table `media_files` */

DROP TABLE IF EXISTS `media_files`;

CREATE TABLE `media_files` (
  `id` int NOT NULL AUTO_INCREMENT,
  `incident_id` int DEFAULT NULL,
  `file_name` varchar(255) NOT NULL,
  `file_type` enum('image','video','document') DEFAULT 'image',
  `file_url` varchar(500) NOT NULL,
  `file_size` varchar(50) DEFAULT NULL,
  `uploaded_by` int DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `media_files` */

insert  into `media_files`(`id`,`incident_id`,`file_name`,`file_type`,`file_url`,`file_size`,`uploaded_by`,`created_at`) values (1,NULL,'perimeter_gate4_breach_photo.jpg','image','https://images.unsplash.com/photo-1557597774-9d273605dfa9?w=600&auto=format&fit=crop&q=60','2.4 MB',NULL,'2026-09-01 23:01:03');

/*Table structure for table `patrol_logs` */

DROP TABLE IF EXISTS `patrol_logs`;

CREATE TABLE `patrol_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `site_id` int DEFAULT NULL,
  `guard_id` int DEFAULT NULL,
  `checkpoint_name` varchar(150) NOT NULL,
  `status` enum('passed','missed','flagged') DEFAULT 'passed',
  `scanned_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `latitude` decimal(10,7) DEFAULT NULL,
  `longitude` decimal(10,7) DEFAULT NULL,
  `notes` text,
  PRIMARY KEY (`id`),
  KEY `idx_patrol_site` (`site_id`),
  KEY `idx_patrol_guard` (`guard_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `patrol_logs` */

insert  into `patrol_logs`(`id`,`site_id`,`guard_id`,`checkpoint_name`,`status`,`scanned_at`,`latitude`,`longitude`,`notes`) values (1,1,1,'Checkpoint A - Main Entrance Gate','passed','2026-09-01 23:04:01',NULL,NULL,'Rounds completed. Perimeter secure.'),(2,1,1,'Checkpoint B - East Warehouse Door 3','passed','2026-09-01 23:04:01',NULL,NULL,'Lock verified.'),(3,1,1,'Checkpoint C - North Fence Corner','flagged','2026-09-01 23:04:01',NULL,NULL,'Spotlight bulb flickered.');

/*Table structure for table `pay_rates` */

DROP TABLE IF EXISTS `pay_rates`;

CREATE TABLE `pay_rates` (
  `id` int NOT NULL AUTO_INCREMENT,
  `role_name` varchar(100) NOT NULL,
  `site_id` int DEFAULT NULL,
  `day_rate` decimal(10,2) DEFAULT '12.50',
  `night_rate` decimal(10,2) DEFAULT '14.50',
  `holiday_rate` decimal(10,2) DEFAULT '18.75',
  `overtime_rate` decimal(10,2) DEFAULT '18.75',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `pay_rates` */

insert  into `pay_rates`(`id`,`role_name`,`site_id`,`day_rate`,`night_rate`,`holiday_rate`,`overtime_rate`,`updated_at`) values (1,'Senior Security Officer',1,14.50,16.50,21.75,21.75,'2026-09-01 23:16:31'),(2,'Retail Security Guard',1,13.50,15.00,20.25,20.25,'2026-09-01 23:16:31'),(3,'Logistics Gatekeeper',2,15.00,17.50,22.50,22.50,'2026-09-01 23:16:31');

/*Table structure for table `payroll_entries` */

DROP TABLE IF EXISTS `payroll_entries`;

CREATE TABLE `payroll_entries` (
  `id` int NOT NULL AUTO_INCREMENT,
  `payroll_reference` varchar(64) NOT NULL,
  `guard_id` int NOT NULL,
  `period_start` date NOT NULL,
  `period_end` date NOT NULL,
  `hours_worked` decimal(10,2) NOT NULL DEFAULT '0.00',
  `pay_rate` decimal(12,2) NOT NULL DEFAULT '0.00',
  `deductions` decimal(12,2) NOT NULL DEFAULT '0.00',
  `net_amount` decimal(12,2) NOT NULL DEFAULT '0.00',
  `status` enum('draft','approved','paid') NOT NULL DEFAULT 'draft',
  `generated_from_attendance` tinyint(1) NOT NULL DEFAULT '1',
  `created_by` int DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_by` int DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_payroll_guard` (`guard_id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `payroll_entries` */

insert  into `payroll_entries`(`id`,`payroll_reference`,`guard_id`,`period_start`,`period_end`,`hours_worked`,`pay_rate`,`deductions`,`net_amount`,`status`,`generated_from_attendance`,`created_by`,`created_at`,`updated_by`,`updated_at`) values (1,'PAY-2026-001',4,'2026-08-01','2026-08-31',7.98,900.00,0.00,7182.00,'approved',1,1,'2026-08-06 22:11:03',NULL,NULL),(2,'PAY-BULK-2',2,'2026-08-01','2026-08-31',160.00,0.00,0.00,5000.00,'approved',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(3,'PAY-BULK-3',3,'2026-08-01','2026-08-31',160.00,0.00,0.00,5000.00,'approved',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(4,'PAY-BULK-4',4,'2026-08-01','2026-08-31',160.00,0.00,0.00,5000.00,'approved',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(5,'PAY-BULK-5',5,'2026-08-01','2026-08-31',160.00,0.00,0.00,5000.00,'approved',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(6,'PAY-BULK-6',6,'2026-08-01','2026-08-31',160.00,0.00,0.00,5000.00,'approved',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(7,'PAY-BULK-7',7,'2026-08-01','2026-08-31',160.00,0.00,0.00,5000.00,'approved',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(8,'PAY-BULK-8',8,'2026-08-01','2026-08-31',160.00,0.00,0.00,5000.00,'approved',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(9,'PAY-BULK-9',9,'2026-08-01','2026-08-31',160.00,0.00,0.00,5000.00,'approved',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(10,'PAY-BULK-10',10,'2026-08-01','2026-08-31',160.00,0.00,0.00,5000.00,'approved',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(11,'PAY-BULK-11',11,'2026-08-01','2026-08-31',160.00,0.00,0.00,5000.00,'approved',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(12,'PAY-BULK-12',12,'2026-08-01','2026-08-31',160.00,0.00,0.00,5000.00,'approved',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(13,'PAY-BULK-13',13,'2026-08-01','2026-08-31',160.00,0.00,0.00,5000.00,'approved',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(14,'PAY-BULK-14',14,'2026-08-01','2026-08-31',160.00,0.00,0.00,5000.00,'approved',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(15,'PAY-BULK-15',15,'2026-08-01','2026-08-31',160.00,0.00,0.00,5000.00,'approved',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(16,'PAY-BULK-16',16,'2026-08-01','2026-08-31',160.00,0.00,0.00,5000.00,'approved',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(17,'PAY-BULK-17',17,'2026-08-01','2026-08-31',160.00,0.00,0.00,5000.00,'approved',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(18,'PAY-BULK-18',18,'2026-08-01','2026-08-31',160.00,0.00,0.00,5000.00,'approved',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(19,'PAY-BULK-19',19,'2026-08-01','2026-08-31',160.00,0.00,0.00,5000.00,'approved',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(20,'PAY-BULK-20',20,'2026-08-01','2026-08-31',160.00,0.00,0.00,5000.00,'approved',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(21,'PAY-BULK-21',21,'2026-08-01','2026-08-31',160.00,0.00,0.00,5000.00,'approved',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(22,'PAY-BULK-22',22,'2026-08-01','2026-08-31',160.00,0.00,0.00,5000.00,'approved',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(23,'PAY-BULK-23',23,'2026-08-01','2026-08-31',160.00,0.00,0.00,5000.00,'approved',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(24,'PAY-BULK-24',24,'2026-08-01','2026-08-31',160.00,0.00,0.00,5000.00,'approved',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(25,'PAY-BULK-25',25,'2026-08-01','2026-08-31',160.00,0.00,0.00,5000.00,'approved',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(26,'PAY-BULK-26',26,'2026-08-01','2026-08-31',160.00,0.00,0.00,5000.00,'approved',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(27,'PAY-BULK-27',27,'2026-08-01','2026-08-31',160.00,0.00,0.00,5000.00,'approved',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(28,'PAY-BULK-28',28,'2026-08-01','2026-08-31',160.00,0.00,0.00,5000.00,'approved',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(29,'PAY-BULK-29',29,'2026-08-01','2026-08-31',160.00,0.00,0.00,5000.00,'approved',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(30,'PAY-BULK-30',30,'2026-08-01','2026-08-31',160.00,0.00,0.00,5000.00,'approved',1,NULL,'2026-08-11 19:59:47',NULL,NULL);

/*Table structure for table `performance_reviews` */

DROP TABLE IF EXISTS `performance_reviews`;

CREATE TABLE `performance_reviews` (
  `id` int NOT NULL AUTO_INCREMENT,
  `guard_id` int NOT NULL,
  `reviewer_name` varchar(100) DEFAULT 'Operations Director',
  `overall_rating` decimal(2,1) DEFAULT '4.8',
  `punctuality_score` decimal(2,1) DEFAULT '5.0',
  `conduct_score` decimal(2,1) DEFAULT '4.8',
  `feedback` text,
  `review_date` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `performance_reviews` */

insert  into `performance_reviews`(`id`,`guard_id`,`reviewer_name`,`overall_rating`,`punctuality_score`,`conduct_score`,`feedback`,`review_date`) values (1,1,'Sarah Jenkins (Ops Manager)',4.9,5.0,4.9,'Officer Vance demonstrated exceptional leadership during the recent Oxford St shoplifting restraint.','2026-08-15'),(2,2,'Sarah Jenkins (Ops Manager)',4.7,4.8,4.7,'Consistently reliable on night shifts with meticulous visitor log verification.','2026-08-01');

/*Table structure for table `purchase_orders` */

DROP TABLE IF EXISTS `purchase_orders`;

CREATE TABLE `purchase_orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `po_number` varchar(64) NOT NULL,
  `supplier_id` int NOT NULL,
  `order_date` date NOT NULL,
  `total_amount` decimal(12,2) NOT NULL DEFAULT '0.00',
  `status` enum('draft','approved','received','cancelled') NOT NULL DEFAULT 'draft',
  `notes` text,
  `created_by` int DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_by` int DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `po_number` (`po_number`),
  KEY `idx_po_supplier` (`supplier_id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `purchase_orders` */

insert  into `purchase_orders`(`id`,`po_number`,`supplier_id`,`order_date`,`total_amount`,`status`,`notes`,`created_by`,`created_at`,`updated_by`,`updated_at`) values (1,'PO-2026-001',1,'2026-08-01',25000.00,'approved','Twenty uniform sets.',1,'2026-08-06 22:11:03',NULL,NULL),(2,'PO-BULK-2',2,'2026-08-01',5000.00,'approved',NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(3,'PO-BULK-3',3,'2026-08-01',5000.00,'approved',NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(4,'PO-BULK-4',4,'2026-08-01',5000.00,'approved',NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(5,'PO-BULK-5',5,'2026-08-01',5000.00,'approved',NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(6,'PO-BULK-6',6,'2026-08-01',5000.00,'approved',NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(7,'PO-BULK-7',7,'2026-08-01',5000.00,'approved',NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(8,'PO-BULK-8',8,'2026-08-01',5000.00,'approved',NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(9,'PO-BULK-9',9,'2026-08-01',5000.00,'approved',NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(10,'PO-BULK-10',10,'2026-08-01',5000.00,'approved',NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(11,'PO-BULK-11',11,'2026-08-01',5000.00,'approved',NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(12,'PO-BULK-12',12,'2026-08-01',5000.00,'approved',NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(13,'PO-BULK-13',13,'2026-08-01',5000.00,'approved',NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(14,'PO-BULK-14',14,'2026-08-01',5000.00,'approved',NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(15,'PO-BULK-15',15,'2026-08-01',5000.00,'approved',NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(16,'PO-BULK-16',16,'2026-08-01',5000.00,'approved',NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(17,'PO-BULK-17',17,'2026-08-01',5000.00,'approved',NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(18,'PO-BULK-18',18,'2026-08-01',5000.00,'approved',NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(19,'PO-BULK-19',19,'2026-08-01',5000.00,'approved',NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(20,'PO-BULK-20',20,'2026-08-01',5000.00,'approved',NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(21,'PO-BULK-21',21,'2026-08-01',5000.00,'approved',NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(22,'PO-BULK-22',22,'2026-08-01',5000.00,'approved',NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(23,'PO-BULK-23',23,'2026-08-01',5000.00,'approved',NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(24,'PO-BULK-24',24,'2026-08-01',5000.00,'approved',NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(25,'PO-BULK-25',25,'2026-08-01',5000.00,'approved',NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(26,'PO-BULK-26',26,'2026-08-01',5000.00,'approved',NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(27,'PO-BULK-27',27,'2026-08-01',5000.00,'approved',NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(28,'PO-BULK-28',28,'2026-08-01',5000.00,'approved',NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(29,'PO-BULK-29',29,'2026-08-01',5000.00,'approved',NULL,NULL,'2026-08-11 19:59:47',NULL,NULL),(30,'PO-BULK-30',30,'2026-08-01',5000.00,'approved',NULL,NULL,'2026-08-11 19:59:47',NULL,NULL);

/*Table structure for table `roles` */

DROP TABLE IF EXISTS `roles`;

CREATE TABLE `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `role_code` varchar(30) NOT NULL,
  `role_name` varchar(100) NOT NULL,
  `sort_order` int NOT NULL DEFAULT '0',
  `status` tinyint(1) NOT NULL DEFAULT '1',
  `is_super_admin` tinyint(1) NOT NULL DEFAULT '0',
  `permissions` json DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `role_code` (`role_code`)
) ENGINE=InnoDB AUTO_INCREMENT=86 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `roles` */

insert  into `roles`(`id`,`role_code`,`role_name`,`sort_order`,`status`,`is_super_admin`,`permissions`) values (1,'madmin','mAdmin',1,1,1,NULL),(2,'manager','Manager',2,1,0,'[\"dashboard\", \"sites\", \"guards\", \"shifts\", \"operations\", \"finance\", \"users\"]'),(3,'guard','Guard',3,1,0,'[\"dashboard\", \"sites/sites\", \"shifts/shifts\", \"operations/shifts\", \"operations/attendance\", \"finance/payroll\", \"guards/requests\"]'),(4,'dispatcher','Dispatcher',4,1,0,NULL),(13,'client','Client',5,1,0,NULL);

/*Table structure for table `shift_assignments` */

DROP TABLE IF EXISTS `shift_assignments`;

CREATE TABLE `shift_assignments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `shift_id` int NOT NULL,
  `guard_id` int NOT NULL,
  `created_by` int DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_shift_guard` (`shift_id`,`guard_id`),
  KEY `idx_assignment_guard` (`guard_id`),
  KEY `idx_assignment_shift` (`shift_id`)
) ENGINE=InnoDB AUTO_INCREMENT=77 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `shift_assignments` */

insert  into `shift_assignments`(`id`,`shift_id`,`guard_id`,`created_by`,`created_at`) values (1,1,4,1,'2026-08-11 19:57:44'),(2,2,5,1,'2026-08-11 19:57:44'),(3,3,4,1,'2026-08-11 19:57:44'),(34,18,15,5,'2026-08-24 22:36:20'),(35,27,22,5,'2026-08-25 20:30:01'),(36,27,4,5,'2026-08-25 20:30:01'),(37,20,4,5,'2026-08-25 20:30:57'),(38,4,0,1,'2026-09-01 22:59:40'),(39,5,0,1,'2026-09-01 22:59:40'),(40,6,0,1,'2026-09-01 22:59:40'),(41,7,0,1,'2026-09-01 22:59:40'),(42,8,0,1,'2026-09-01 22:59:40'),(43,9,0,1,'2026-09-01 22:59:40'),(44,10,0,1,'2026-09-01 22:59:40'),(45,11,0,1,'2026-09-01 22:59:40'),(46,12,0,1,'2026-09-01 22:59:40'),(47,13,0,1,'2026-09-01 22:59:40'),(48,14,0,1,'2026-09-01 22:59:40'),(49,15,0,1,'2026-09-01 22:59:40'),(50,16,0,1,'2026-09-01 22:59:40'),(51,17,0,1,'2026-09-01 22:59:40'),(52,18,0,1,'2026-09-01 22:59:40'),(53,19,0,1,'2026-09-01 22:59:40'),(54,20,0,1,'2026-09-01 22:59:40'),(55,21,0,1,'2026-09-01 22:59:40'),(56,22,0,1,'2026-09-01 22:59:40'),(57,23,0,1,'2026-09-01 22:59:40'),(58,24,0,1,'2026-09-01 22:59:40'),(59,25,0,1,'2026-09-01 22:59:40'),(60,26,0,1,'2026-09-01 22:59:40'),(61,27,0,1,'2026-09-01 22:59:40'),(62,28,0,1,'2026-09-01 22:59:40'),(63,29,0,1,'2026-09-01 22:59:40'),(64,30,0,1,'2026-09-01 22:59:40'),(65,31,0,1,'2026-09-01 22:59:40'),(66,32,0,1,'2026-09-01 22:59:40'),(67,33,0,1,'2026-09-01 22:59:40');

/*Table structure for table `shift_swap_requests` */

DROP TABLE IF EXISTS `shift_swap_requests`;

CREATE TABLE `shift_swap_requests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `shift_id` int NOT NULL,
  `requester_guard_id` int NOT NULL,
  `target_guard_id` int DEFAULT NULL,
  `reason` varchar(255) DEFAULT NULL,
  `status` enum('pending','approved','rejected','cancelled') DEFAULT 'pending',
  `manager_note` varchar(255) DEFAULT NULL,
  `created_by` int DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `shift_swap_requests` */

insert  into `shift_swap_requests`(`id`,`shift_id`,`requester_guard_id`,`target_guard_id`,`reason`,`status`,`manager_note`,`created_by`,`created_at`,`updated_at`) values (1,4,1,2,'Personal family commitment on weekend','pending',NULL,NULL,'2026-08-24 23:04:35','2026-08-24 23:04:35'),(2,4,2,NULL,'Open trade request for night shift','pending',NULL,NULL,'2026-08-24 23:04:35','2026-08-24 23:04:35'),(3,6,1,4,'change','pending',NULL,5,'2026-08-24 23:11:29','2026-08-24 23:11:29');

/*Table structure for table `shifts` */

DROP TABLE IF EXISTS `shifts`;

CREATE TABLE `shifts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `shift_code` varchar(64) NOT NULL,
  `site_id` int NOT NULL,
  `guard_id` int DEFAULT NULL,
  `start_at` datetime NOT NULL,
  `end_at` datetime NOT NULL,
  `break_minutes` int NOT NULL DEFAULT '0',
  `status` enum('scheduled','completed','cancelled','open') NOT NULL DEFAULT 'scheduled',
  `instructions` text,
  `created_by` int DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_by` int DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `shift_code` (`shift_code`),
  KEY `idx_shift_site_time` (`site_id`,`start_at`),
  KEY `idx_shift_guard_time` (`guard_id`,`start_at`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `shifts` */

insert  into `shifts`(`id`,`shift_code`,`site_id`,`guard_id`,`start_at`,`end_at`,`break_minutes`,`status`,`instructions`,`created_by`,`created_at`,`updated_by`,`updated_at`) values (1,'SHIFT-ACME-01',3,4,'2026-08-03 08:00:00','2026-08-03 16:00:00',0,'completed','Day shift.',1,'2026-08-06 22:11:03',NULL,NULL),(2,'SHIFT-NEXUS-01',4,5,'2026-08-03 20:00:00','2026-08-04 04:00:00',0,'completed','Night shift.',1,'2026-08-06 22:11:03',5,NULL),(3,'SHIFT-ACME-02',3,4,'2026-07-30 08:00:00','2026-07-30 16:00:00',0,'scheduled','Day shift.',1,'2026-08-06 22:11:03',5,NULL),(4,'SHIFT-NEW-1',2,0,'2026-08-08 08:00:00','2026-08-08 16:00:00',0,'scheduled',NULL,1,'2026-08-11 19:56:39',NULL,NULL),(5,'SHIFT-NEW-2',5,0,'2026-08-26 08:00:00','2026-08-26 16:00:00',0,'scheduled',NULL,1,'2026-08-11 19:56:39',NULL,NULL),(6,'SHIFT-NEW-3',19,0,'2026-08-01 08:00:00','2026-08-01 16:00:00',0,'scheduled',NULL,1,'2026-08-11 19:56:39',NULL,NULL),(7,'SHIFT-NEW-4',8,0,'2026-08-07 08:00:00','2026-08-07 16:00:00',0,'scheduled',NULL,1,'2026-08-11 19:56:39',NULL,NULL),(8,'SHIFT-NEW-5',7,0,'2026-08-22 08:00:00','2026-08-22 16:00:00',0,'scheduled',NULL,1,'2026-08-11 19:56:39',NULL,NULL),(9,'SHIFT-NEW-6',20,0,'2026-08-10 08:00:00','2026-08-10 16:00:00',0,'scheduled',NULL,1,'2026-08-11 19:56:39',NULL,NULL),(10,'SHIFT-NEW-7',12,0,'2026-08-23 08:00:00','2026-08-23 16:00:00',0,'scheduled',NULL,1,'2026-08-11 19:56:39',NULL,NULL),(11,'SHIFT-NEW-8',12,0,'2026-08-09 08:00:00','2026-08-09 16:00:00',0,'scheduled',NULL,1,'2026-08-11 19:56:39',NULL,NULL),(12,'SHIFT-NEW-9',17,0,'2026-08-13 08:00:00','2026-08-13 16:00:00',0,'scheduled',NULL,1,'2026-08-11 19:56:39',NULL,NULL),(13,'SHIFT-NEW-10',11,0,'2026-08-12 08:00:00','2026-08-12 16:00:00',0,'scheduled',NULL,1,'2026-08-11 19:56:39',5,NULL),(14,'SHIFT-NEW-11',15,0,'2026-08-19 08:00:00','2026-08-19 16:00:00',0,'scheduled',NULL,1,'2026-08-11 19:56:39',NULL,NULL),(15,'SHIFT-NEW-12',15,0,'2026-08-07 08:00:00','2026-08-07 16:00:00',0,'scheduled',NULL,1,'2026-08-11 19:56:39',NULL,NULL),(16,'SHIFT-NEW-13',3,0,'2026-08-14 08:00:00','2026-08-14 16:00:00',0,'scheduled',NULL,1,'2026-08-11 19:56:39',NULL,NULL),(17,'SHIFT-NEW-14',20,0,'2026-08-08 08:00:00','2026-08-08 16:00:00',0,'scheduled',NULL,1,'2026-08-11 19:56:39',NULL,NULL),(18,'SHIFT-NEW-15',15,0,'2026-08-05 03:00:00','2026-08-05 11:00:00',0,'scheduled',NULL,1,'2026-08-11 19:56:39',5,NULL),(19,'SHIFT-NEW-16',17,0,'2026-08-01 08:00:00','2026-08-01 16:00:00',0,'scheduled',NULL,1,'2026-08-11 19:56:39',NULL,NULL),(20,'SHIFT-NEW-17',11,0,'2026-08-04 03:00:00','2026-08-04 11:00:00',0,'scheduled',NULL,1,'2026-08-11 19:56:39',5,NULL),(21,'SHIFT-NEW-18',15,0,'2026-08-18 08:00:00','2026-08-18 16:00:00',0,'scheduled',NULL,1,'2026-08-11 19:56:39',NULL,NULL),(22,'SHIFT-NEW-19',9,0,'2026-08-22 08:00:00','2026-08-22 16:00:00',0,'scheduled',NULL,1,'2026-08-11 19:56:39',NULL,NULL),(23,'SHIFT-NEW-20',20,0,'2026-08-15 08:00:00','2026-08-15 16:00:00',0,'scheduled',NULL,1,'2026-08-11 19:56:39',NULL,NULL),(24,'SHIFT-NEW-21',20,0,'2026-08-21 08:00:00','2026-08-21 16:00:00',0,'scheduled',NULL,1,'2026-08-11 19:56:39',NULL,NULL),(25,'SHIFT-NEW-22',6,0,'2026-08-08 08:00:00','2026-08-08 16:00:00',0,'scheduled',NULL,1,'2026-08-11 19:56:39',NULL,NULL),(26,'SHIFT-NEW-23',19,0,'2026-08-09 08:00:00','2026-08-09 16:00:00',0,'scheduled',NULL,1,'2026-08-11 19:56:39',NULL,NULL),(27,'SHIFT-NEW-24',13,0,'2026-08-06 03:00:00','2026-08-06 11:00:00',0,'scheduled',NULL,1,'2026-08-11 19:56:39',5,NULL),(28,'SHIFT-NEW-25',17,0,'2026-08-04 03:00:00','2026-08-04 11:00:00',0,'scheduled',NULL,1,'2026-08-11 19:56:39',5,NULL),(29,'SHIFT-NEW-26',3,0,'2026-08-08 08:00:00','2026-08-08 16:00:00',0,'scheduled',NULL,1,'2026-08-11 19:56:39',NULL,NULL),(30,'SHIFT-NEW-27',14,0,'2026-08-28 08:00:00','2026-08-28 16:00:00',0,'scheduled',NULL,1,'2026-08-11 19:56:39',NULL,NULL),(31,'SHIFT-NEW-28',2,0,'2026-08-16 08:00:00','2026-08-16 16:00:00',0,'scheduled',NULL,1,'2026-08-11 19:56:39',NULL,NULL),(32,'SHIFT-NEW-29',14,0,'2026-08-11 08:00:00','2026-08-11 16:00:00',0,'scheduled',NULL,1,'2026-08-11 19:56:39',NULL,NULL),(33,'SHIFT-NEW-30',13,0,'2026-08-19 08:00:00','2026-08-19 16:00:00',0,'scheduled',NULL,1,'2026-08-11 19:56:39',NULL,NULL);

/*Table structure for table `site_sla_logs` */

DROP TABLE IF EXISTS `site_sla_logs`;

CREATE TABLE `site_sla_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `site_id` int NOT NULL,
  `site_name` varchar(150) NOT NULL,
  `sla_target_pct` decimal(5,2) DEFAULT '99.00',
  `actual_performance_pct` decimal(5,2) DEFAULT '98.75',
  `status` enum('compliant','warning','breached') DEFAULT 'compliant',
  `audited_date` date NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `site_sla_logs` */

insert  into `site_sla_logs`(`id`,`site_id`,`site_name`,`sla_target_pct`,`actual_performance_pct`,`status`,`audited_date`,`created_at`) values (1,1,'Oxford Street Flagship Store',99.00,99.50,'compliant','2026-08-31','2026-09-01 23:26:35'),(2,2,'Trafford Industrial Depot',98.50,98.75,'compliant','2026-08-31','2026-09-01 23:26:35'),(3,3,'Canary Wharf Tech Hub',99.00,97.80,'warning','2026-08-31','2026-09-01 23:26:35');

/*Table structure for table `sites` */

DROP TABLE IF EXISTS `sites`;

CREATE TABLE `sites` (
  `id` int NOT NULL AUTO_INCREMENT,
  `site` varchar(255) DEFAULT NULL,
  `site_code` varbinary(255) DEFAULT NULL,
  `status` int DEFAULT '1',
  `created_by` int DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_by` int DEFAULT NULL,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `customer_id` int DEFAULT NULL,
  `address` text,
  `latitude` decimal(10,7) DEFAULT NULL,
  `longitude` decimal(10,7) DEFAULT NULL,
  `instructions` text,
  `required_guard_count` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `sites` */

insert  into `sites`(`id`,`site`,`site_code`,`status`,`created_by`,`created_at`,`updated_by`,`updated_at`,`customer_id`,`address`,`latitude`,`longitude`,`instructions`,`required_guard_count`) values (1,'Site','B0-01',1,1,'2026-08-04 21:22:50',NULL,'2026-08-04 21:22:57',NULL,NULL,NULL,NULL,NULL,1),(2,'Site ABCD','d3c009ba-467b-4a59-8e0a-99117f2b5b8d',1,2,'2026-08-04 22:23:43',2,'2026-08-04 22:23:43',NULL,NULL,NULL,NULL,NULL,1),(3,'Acme Headquarters','SITE-ACME-HQ',1,1,'2026-08-06 22:11:03',NULL,'2026-08-06 22:11:03',3,'Blue Area, Islamabad',33.7294000,73.0931000,'Check in at the reception desk. Patrol lobby and parking each hour.',2),(4,'Nexus Warehouse','SITE-NEXUS-WH',1,1,'2026-08-06 22:11:03',NULL,'2026-08-06 22:11:03',4,'Port Qasim, Karachi',24.7980000,67.3060000,'Verify delivery drivers against the dispatch register.',2),(5,'Test Site 1','SITE-NEW-1',1,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',1,NULL,NULL,NULL,NULL,2),(6,'Test Site 2','SITE-NEW-2',1,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',1,NULL,NULL,NULL,NULL,2),(7,'Test Site 3','SITE-NEW-3',1,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',1,NULL,NULL,NULL,NULL,2),(8,'Test Site 4','SITE-NEW-4',1,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',1,NULL,NULL,NULL,NULL,2),(9,'Test Site 5','SITE-NEW-5',1,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',1,NULL,NULL,NULL,NULL,2),(10,'Test Site 6','SITE-NEW-6',1,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',1,NULL,NULL,NULL,NULL,2),(11,'Test Site 7','SITE-NEW-7',1,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',1,NULL,NULL,NULL,NULL,2),(12,'Test Site 8','SITE-NEW-8',1,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',1,NULL,NULL,NULL,NULL,2),(13,'Test Site 9','SITE-NEW-9',1,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',1,NULL,NULL,NULL,NULL,2),(14,'Test Site 10','SITE-NEW-10',1,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',1,NULL,NULL,NULL,NULL,2),(15,'Test Site 11','SITE-NEW-11',1,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',1,NULL,NULL,NULL,NULL,2),(16,'Test Site 12','SITE-NEW-12',1,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',1,NULL,NULL,NULL,NULL,2),(17,'Test Site 13','SITE-NEW-13',1,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',1,NULL,NULL,NULL,NULL,2),(18,'Test Site 14','SITE-NEW-14',1,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',1,NULL,NULL,NULL,NULL,2),(19,'Test Site 15','SITE-NEW-15',1,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',1,NULL,NULL,NULL,NULL,2),(20,'Test Site 16','SITE-NEW-16',1,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',1,NULL,NULL,NULL,NULL,2),(21,'Test Site 17','SITE-NEW-17',1,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',1,NULL,NULL,NULL,NULL,2),(22,'Test Site 18','SITE-NEW-18',1,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',1,NULL,NULL,NULL,NULL,2),(23,'Test Site 19','SITE-NEW-19',1,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',1,NULL,NULL,NULL,NULL,2),(24,'Test Site 20','SITE-NEW-20',1,1,'2026-08-11 19:56:39',NULL,'2026-08-11 19:56:39',1,NULL,NULL,NULL,NULL,2),(25,'Site 25','SITE-BULK-25',1,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',25,'Site Address 25',NULL,NULL,NULL,2),(26,'Site 26','SITE-BULK-26',1,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',26,'Site Address 26',NULL,NULL,NULL,2),(27,'Site 27','SITE-BULK-27',1,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',27,'Site Address 27',NULL,NULL,NULL,2),(28,'Site 28','SITE-BULK-28',1,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',28,'Site Address 28',NULL,NULL,NULL,2),(29,'Site 29','SITE-BULK-29',1,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',29,'Site Address 29',NULL,NULL,NULL,2),(30,'Site 30','SITE-BULK-30',1,NULL,'2026-08-11 19:59:47',NULL,'2026-08-11 19:59:47',30,'Site Address 30',NULL,NULL,NULL,2);

/*Table structure for table `sos_alerts` */

DROP TABLE IF EXISTS `sos_alerts`;

CREATE TABLE `sos_alerts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `guard_id` int NOT NULL,
  `site_id` int DEFAULT NULL,
  `latitude` decimal(10,7) DEFAULT NULL,
  `longitude` decimal(10,7) DEFAULT NULL,
  `status` enum('active','acknowledged','resolved') DEFAULT 'active',
  `triggered_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `resolved_at` datetime DEFAULT NULL,
  `notes` text,
  PRIMARY KEY (`id`),
  KEY `idx_sos_status` (`status`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `sos_alerts` */

insert  into `sos_alerts`(`id`,`guard_id`,`site_id`,`latitude`,`longitude`,`status`,`triggered_at`,`resolved_at`,`notes`) values (1,2,1,51.5159000,-0.1415000,'resolved','2026-09-01 21:16:31',NULL,NULL);

/*Table structure for table `subcontractors` */

DROP TABLE IF EXISTS `subcontractors`;

CREATE TABLE `subcontractors` (
  `id` int NOT NULL AUTO_INCREMENT,
  `agency_name` varchar(150) NOT NULL,
  `contact_person` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `hourly_rate` decimal(10,2) DEFAULT '0.00',
  `active_guards_count` int DEFAULT '0',
  `status` enum('active','inactive') DEFAULT 'active',
  `notes` text,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `subcontractors` */

insert  into `subcontractors`(`id`,`agency_name`,`contact_person`,`email`,`phone`,`hourly_rate`,`active_guards_count`,`status`,`notes`,`created_at`,`updated_at`) values (1,'Titan Tactical Security Services','Robert Vance','contact@titantactical.com','+1 (555) 019-2831',34.50,14,'active','Primary 3rd-party guard provider for night shift coverage.','2026-08-24 23:00:35','2026-08-24 23:00:35'),(2,'Sentinel Mobile Patrol Corp','Deborah Miller','ops@sentinelpatrol.org','+1 (555) 012-9944',38.00,8,'active','Specialized vehicle patrol sub-contractor.','2026-08-24 23:00:35','2026-08-24 23:00:35'),(3,'Vanguard Executive Protection','James Sterling','info@vanguardprotect.com','+1 (555) 017-4411',45.00,5,'active','Armed VIP protection agency for executive events.','2026-08-24 23:00:35','2026-08-24 23:00:35');

/*Table structure for table `supplier_invoices` */

DROP TABLE IF EXISTS `supplier_invoices`;

CREATE TABLE `supplier_invoices` (
  `id` int NOT NULL AUTO_INCREMENT,
  `invoice_number` varchar(64) NOT NULL,
  `supplier_id` int NOT NULL,
  `purchase_order_id` int DEFAULT NULL,
  `invoice_date` date NOT NULL,
  `due_date` date DEFAULT NULL,
  `amount` decimal(12,2) NOT NULL DEFAULT '0.00',
  `status` enum('unpaid','partial','paid','overdue') NOT NULL DEFAULT 'unpaid',
  `created_by` int DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_by` int DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_supplier_invoice_supplier` (`supplier_id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `supplier_invoices` */

insert  into `supplier_invoices`(`id`,`invoice_number`,`supplier_id`,`purchase_order_id`,`invoice_date`,`due_date`,`amount`,`status`,`created_by`,`created_at`,`updated_by`,`updated_at`) values (1,'SUPINV-2026-001',1,1,'2026-08-02','2026-08-17',25000.00,'unpaid',1,'2026-08-06 22:11:03',NULL,NULL),(2,'SUPINV-BULK-2',2,2,'2026-08-05',NULL,5000.00,'unpaid',NULL,'2026-08-11 19:59:47',NULL,NULL),(3,'SUPINV-BULK-3',3,3,'2026-08-05',NULL,5000.00,'unpaid',NULL,'2026-08-11 19:59:47',NULL,NULL),(4,'SUPINV-BULK-4',4,4,'2026-08-05',NULL,5000.00,'unpaid',NULL,'2026-08-11 19:59:47',NULL,NULL),(5,'SUPINV-BULK-5',5,5,'2026-08-05',NULL,5000.00,'unpaid',NULL,'2026-08-11 19:59:47',NULL,NULL),(6,'SUPINV-BULK-6',6,6,'2026-08-05',NULL,5000.00,'unpaid',NULL,'2026-08-11 19:59:47',NULL,NULL),(7,'SUPINV-BULK-7',7,7,'2026-08-05',NULL,5000.00,'unpaid',NULL,'2026-08-11 19:59:47',NULL,NULL),(8,'SUPINV-BULK-8',8,8,'2026-08-05',NULL,5000.00,'unpaid',NULL,'2026-08-11 19:59:47',NULL,NULL),(9,'SUPINV-BULK-9',9,9,'2026-08-05',NULL,5000.00,'unpaid',NULL,'2026-08-11 19:59:47',NULL,NULL),(10,'SUPINV-BULK-10',10,10,'2026-08-05',NULL,5000.00,'unpaid',NULL,'2026-08-11 19:59:47',NULL,NULL),(11,'SUPINV-BULK-11',11,11,'2026-08-05',NULL,5000.00,'unpaid',NULL,'2026-08-11 19:59:47',NULL,NULL),(12,'SUPINV-BULK-12',12,12,'2026-08-05',NULL,5000.00,'unpaid',NULL,'2026-08-11 19:59:47',NULL,NULL),(13,'SUPINV-BULK-13',13,13,'2026-08-05',NULL,5000.00,'unpaid',NULL,'2026-08-11 19:59:47',NULL,NULL),(14,'SUPINV-BULK-14',14,14,'2026-08-05',NULL,5000.00,'unpaid',NULL,'2026-08-11 19:59:47',NULL,NULL),(15,'SUPINV-BULK-15',15,15,'2026-08-05',NULL,5000.00,'unpaid',NULL,'2026-08-11 19:59:47',NULL,NULL),(16,'SUPINV-BULK-16',16,16,'2026-08-05',NULL,5000.00,'unpaid',NULL,'2026-08-11 19:59:47',NULL,NULL),(17,'SUPINV-BULK-17',17,17,'2026-08-05',NULL,5000.00,'unpaid',NULL,'2026-08-11 19:59:47',NULL,NULL),(18,'SUPINV-BULK-18',18,18,'2026-08-05',NULL,5000.00,'unpaid',NULL,'2026-08-11 19:59:47',NULL,NULL),(19,'SUPINV-BULK-19',19,19,'2026-08-05',NULL,5000.00,'unpaid',NULL,'2026-08-11 19:59:47',NULL,NULL),(20,'SUPINV-BULK-20',20,20,'2026-08-05',NULL,5000.00,'unpaid',NULL,'2026-08-11 19:59:47',NULL,NULL),(21,'SUPINV-BULK-21',21,21,'2026-08-05',NULL,5000.00,'unpaid',NULL,'2026-08-11 19:59:47',NULL,NULL),(22,'SUPINV-BULK-22',22,22,'2026-08-05',NULL,5000.00,'unpaid',NULL,'2026-08-11 19:59:47',NULL,NULL),(23,'SUPINV-BULK-23',23,23,'2026-08-05',NULL,5000.00,'unpaid',NULL,'2026-08-11 19:59:47',NULL,NULL),(24,'SUPINV-BULK-24',24,24,'2026-08-05',NULL,5000.00,'unpaid',NULL,'2026-08-11 19:59:47',NULL,NULL),(25,'SUPINV-BULK-25',25,25,'2026-08-05',NULL,5000.00,'unpaid',NULL,'2026-08-11 19:59:47',NULL,NULL),(26,'SUPINV-BULK-26',26,26,'2026-08-05',NULL,5000.00,'unpaid',NULL,'2026-08-11 19:59:47',NULL,NULL),(27,'SUPINV-BULK-27',27,27,'2026-08-05',NULL,5000.00,'unpaid',NULL,'2026-08-11 19:59:47',NULL,NULL),(28,'SUPINV-BULK-28',28,28,'2026-08-05',NULL,5000.00,'unpaid',NULL,'2026-08-11 19:59:47',NULL,NULL),(29,'SUPINV-BULK-29',29,29,'2026-08-05',NULL,5000.00,'unpaid',NULL,'2026-08-11 19:59:47',NULL,NULL),(30,'SUPINV-BULK-30',30,30,'2026-08-05',NULL,5000.00,'unpaid',NULL,'2026-08-11 19:59:47',NULL,NULL);

/*Table structure for table `suppliers` */

DROP TABLE IF EXISTS `suppliers`;

CREATE TABLE `suppliers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `supplier_code` varchar(64) NOT NULL,
  `supplier` varchar(255) NOT NULL,
  `email` varchar(225) DEFAULT NULL,
  `phone_number` varchar(100) DEFAULT NULL,
  `address` text,
  `payment_terms` varchar(100) DEFAULT NULL,
  `status` tinyint(1) NOT NULL DEFAULT '1',
  `created_by` int DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_by` int DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `supplier_code` (`supplier_code`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `suppliers` */

insert  into `suppliers`(`id`,`supplier_code`,`supplier`,`email`,`phone_number`,`address`,`payment_terms`,`status`,`created_by`,`created_at`,`updated_by`,`updated_at`) values (1,'SUP-UNIFORM','Prime Uniforms','sales@primeuniforms.test','+92 300 5555555','Karachi','Net 30',1,1,'2026-08-06 22:11:03',NULL,NULL),(2,'SUP-EQUIP','Secure Equipment Co.','orders@secureequipment.test','+92 300 6666666','Lahore','Net 15',1,1,'2026-08-06 22:11:03',NULL,NULL),(3,'SUP-BULK-3','Supplier 3','sup3@test.com','+92300100003',NULL,'Net 30',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(4,'SUP-BULK-4','Supplier 4','sup4@test.com','+92300100004',NULL,'Net 30',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(5,'SUP-BULK-5','Supplier 5','sup5@test.com','+92300100005',NULL,'Net 30',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(6,'SUP-BULK-6','Supplier 6','sup6@test.com','+92300100006',NULL,'Net 30',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(7,'SUP-BULK-7','Supplier 7','sup7@test.com','+92300100007',NULL,'Net 30',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(8,'SUP-BULK-8','Supplier 8','sup8@test.com','+92300100008',NULL,'Net 30',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(9,'SUP-BULK-9','Supplier 9','sup9@test.com','+92300100009',NULL,'Net 30',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(10,'SUP-BULK-10','Supplier 10','sup10@test.com','+923001000010',NULL,'Net 30',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(11,'SUP-BULK-11','Supplier 11','sup11@test.com','+923001000011',NULL,'Net 30',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(12,'SUP-BULK-12','Supplier 12','sup12@test.com','+923001000012',NULL,'Net 30',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(13,'SUP-BULK-13','Supplier 13','sup13@test.com','+923001000013',NULL,'Net 30',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(14,'SUP-BULK-14','Supplier 14','sup14@test.com','+923001000014',NULL,'Net 30',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(15,'SUP-BULK-15','Supplier 15','sup15@test.com','+923001000015',NULL,'Net 30',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(16,'SUP-BULK-16','Supplier 16','sup16@test.com','+923001000016',NULL,'Net 30',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(17,'SUP-BULK-17','Supplier 17','sup17@test.com','+923001000017',NULL,'Net 30',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(18,'SUP-BULK-18','Supplier 18','sup18@test.com','+923001000018',NULL,'Net 30',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(19,'SUP-BULK-19','Supplier 19','sup19@test.com','+923001000019',NULL,'Net 30',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(20,'SUP-BULK-20','Supplier 20','sup20@test.com','+923001000020',NULL,'Net 30',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(21,'SUP-BULK-21','Supplier 21','sup21@test.com','+923001000021',NULL,'Net 30',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(22,'SUP-BULK-22','Supplier 22','sup22@test.com','+923001000022',NULL,'Net 30',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(23,'SUP-BULK-23','Supplier 23','sup23@test.com','+923001000023',NULL,'Net 30',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(24,'SUP-BULK-24','Supplier 24','sup24@test.com','+923001000024',NULL,'Net 30',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(25,'SUP-BULK-25','Supplier 25','sup25@test.com','+923001000025',NULL,'Net 30',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(26,'SUP-BULK-26','Supplier 26','sup26@test.com','+923001000026',NULL,'Net 30',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(27,'SUP-BULK-27','Supplier 27','sup27@test.com','+923001000027',NULL,'Net 30',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(28,'SUP-BULK-28','Supplier 28','sup28@test.com','+923001000028',NULL,'Net 30',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(29,'SUP-BULK-29','Supplier 29','sup29@test.com','+923001000029',NULL,'Net 30',1,NULL,'2026-08-11 19:59:47',NULL,NULL),(30,'SUP-BULK-30','Supplier 30','sup30@test.com','+923001000030',NULL,'Net 30',1,NULL,'2026-08-11 19:59:47',NULL,NULL);

/*Table structure for table `timesheets` */

DROP TABLE IF EXISTS `timesheets`;

CREATE TABLE `timesheets` (
  `id` int NOT NULL AUTO_INCREMENT,
  `shift_id` int DEFAULT NULL,
  `guard_id` int NOT NULL,
  `site_id` int DEFAULT NULL,
  `clock_in` datetime NOT NULL,
  `clock_out` datetime NOT NULL,
  `break_minutes` int DEFAULT '30',
  `regular_hours` decimal(5,2) DEFAULT '0.00',
  `overtime_hours` decimal(5,2) DEFAULT '0.00',
  `holiday_hours` decimal(5,2) DEFAULT '0.00',
  `pay_rate` decimal(10,2) DEFAULT '12.50',
  `charge_rate` decimal(10,2) DEFAULT '18.50',
  `gross_pay` decimal(10,2) DEFAULT '0.00',
  `gross_charge` decimal(10,2) DEFAULT '0.00',
  `status` enum('draft','submitted','approved','rejected','exported') DEFAULT 'submitted',
  `approved_by` int DEFAULT NULL,
  `approved_at` datetime DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `timesheets` */

insert  into `timesheets`(`id`,`shift_id`,`guard_id`,`site_id`,`clock_in`,`clock_out`,`break_minutes`,`regular_hours`,`overtime_hours`,`holiday_hours`,`pay_rate`,`charge_rate`,`gross_pay`,`gross_charge`,`status`,`approved_by`,`approved_at`,`created_at`) values (1,101,1,1,'2026-09-01 07:00:00','2026-09-01 19:00:00',60,8.00,3.00,0.00,13.50,20.00,168.75,260.00,'exported',NULL,NULL,'2026-09-01 23:11:26'),(2,102,2,1,'2026-09-01 19:00:00','2026-09-02 07:00:00',60,8.00,3.00,0.00,14.50,22.00,181.25,286.00,'exported',5,'2026-09-01 23:15:04','2026-09-01 23:11:26'),(3,103,3,2,'2026-08-31 08:00:00','2026-08-31 16:00:00',30,7.50,0.00,0.00,12.50,18.50,93.75,138.75,'draft',NULL,NULL,'2026-09-01 23:11:26');

/*Table structure for table `training_records` */

DROP TABLE IF EXISTS `training_records`;

CREATE TABLE `training_records` (
  `id` int NOT NULL AUTO_INCREMENT,
  `guard_id` int NOT NULL,
  `course_name` varchar(150) NOT NULL,
  `provider` varchar(150) DEFAULT 'Highfield Qualifications UK',
  `completion_date` date NOT NULL,
  `expiry_date` date DEFAULT NULL,
  `status` enum('valid','expiring_soon','expired') DEFAULT 'valid',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `training_records` */

insert  into `training_records`(`id`,`guard_id`,`course_name`,`provider`,`completion_date`,`expiry_date`,`status`,`created_at`) values (1,1,'First Aid at Work (FAW Level 3)','St John Ambulance','2024-06-15','2027-06-14','valid','2026-09-01 23:19:44'),(2,1,'Conflict Management & Physical Intervention','Highfield UK','2025-02-10','2028-02-09','valid','2026-09-01 23:19:44'),(3,2,'CCTV Control Room Operation (SIA Level 2)','Skills for Security','2024-01-20','2027-01-19','valid','2026-09-01 23:19:44');

/*Table structure for table `users` */

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `user_code` varchar(225) DEFAULT NULL,
  `name` varchar(225) DEFAULT NULL,
  `email` varchar(225) DEFAULT NULL,
  `password` varchar(225) DEFAULT NULL,
  `role_type` int DEFAULT NULL,
  `photo_url` varchar(225) DEFAULT NULL,
  `status` tinyint(1) DEFAULT '1',
  `created_by` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_by` int DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `guard_id` int DEFAULT NULL,
  `role_id` int DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `users` */

insert  into `users`(`user_id`,`user_code`,`name`,`email`,`password`,`role_type`,`photo_url`,`status`,`created_by`,`created_at`,`updated_by`,`updated_at`,`guard_id`,`role_id`) values (1,NULL,'System Admin','demo@gmail.com','$2a$10$zKs0RBxvf65ve.YJgaV5keTKJ.tLNfHr.vu5nO8ZK4T0V1tl/4DSa',NULL,NULL,1,NULL,'2026-08-02 21:41:01',5,'2026-08-02 21:41:01',NULL,NULL),(2,'3525fc19-2e7d-4c9c-8866-be794a7fbbef','Shakir Ali','shakir.ali@salesflo.com','$2a$10$beZ9cObfo34VZN.RUuPQquvLrjDkzNK.PcoOKqXwQzY846fzAUMBu',NULL,NULL,1,1,'2026-08-02 22:53:01',NULL,'2026-08-02 22:53:01',NULL,2),(3,'14b095f1-a8e9-45e0-984b-39f32275b242','Shahzaib Shah','shahzaib.us@gmail.com','$2a$10$2EuA7xeNTS8KfiuKsfN.vetGddwvaEPdZdKc87uD3O.Wvj1slVpDO',NULL,NULL,1,1,'2026-08-02 22:54:49',5,'2026-08-02 22:54:49',NULL,3),(4,'7566c778-4545-47e0-8a5d-e1046f6d9397','Faseeh abbas','Faseeh@gmail.com','$2a$10$beZ9cObfo34VZN.RUuPQquvLrjDkzNK.PcoOKqXwQzY846fzAUMBu',NULL,NULL,1,2,'2026-08-03 22:14:49',2,'2026-08-03 22:14:49',2,3),(5,'84dfab73-1ef3-41b7-b4c9-7489589d330b','ABC','abc@gmail.com','$2a$10$2EuA7xeNTS8KfiuKsfN.vetGddwvaEPdZdKc87uD3O.Wvj1slVpDO',NULL,NULL,1,2,'2026-08-04 20:11:09',5,'2026-08-04 20:11:09',NULL,1),(6,'33ab0fff-391c-41ad-95b1-853d85d0d041','Ashfaque Ahmed test','ashfaque@gmail.com','$2a$10$A92Gt8uRibeJ8qpDdg4rY.2jlVVMiCCZRraFVNdYwwegxaFfVxvkK',NULL,NULL,1,2,'2026-08-04 20:42:47',2,'2026-08-04 20:42:47',NULL,1),(7,'d812f633-0aa1-4fd7-abc9-c56a685393b1','Ashfaque Solangi','ashfaqueaas1995@gmail.com','$2a$10$68oSsSOefbky361riCwxQuWTkoHStzuO3vNU9z6p09EbwIq1kSDbO',NULL,NULL,1,NULL,'2026-08-11 20:41:15',5,'2026-08-11 20:41:15',1,3),(8,'e51f6acf-c14c-49c9-bc2b-390a2d2b4e22','Female Female','new@gmail.com','$2a$10$PN/N92j0VIBfMphkmYMeA.pS.fQB3VJMfDYyaYzDw4YeysFfDJ/WG',NULL,NULL,1,NULL,'2026-08-11 20:41:15',NULL,'2026-08-11 20:41:15',2,3),(9,'6ac35631-2975-4e63-bf34-e714657bc79f','Ashfaque Ahmed','aliguddu855@gmail.com','$2a$10$PN/N92j0VIBfMphkmYMeA.pS.fQB3VJMfDYyaYzDw4YeysFfDJ/WG',NULL,NULL,1,NULL,'2026-08-11 20:41:15',NULL,'2026-08-11 20:41:15',3,3),(10,'GUARD-ALI','Ali Khan','ali.khan@test.local','$2a$10$PN/N92j0VIBfMphkmYMeA.pS.fQB3VJMfDYyaYzDw4YeysFfDJ/WG',NULL,NULL,1,NULL,'2026-08-11 20:41:15',NULL,'2026-08-11 20:41:15',4,3),(11,'GUARD-SANA','Sana Ahmed','sana.ahmed@test.local','$2a$10$PN/N92j0VIBfMphkmYMeA.pS.fQB3VJMfDYyaYzDw4YeysFfDJ/WG',NULL,NULL,1,NULL,'2026-08-11 20:41:15',NULL,'2026-08-11 20:41:15',5,3),(12,'GUARD-NEW-1','Naveed Javed','naveed.javed1@test.local','$2a$10$PN/N92j0VIBfMphkmYMeA.pS.fQB3VJMfDYyaYzDw4YeysFfDJ/WG',NULL,NULL,1,NULL,'2026-08-11 20:41:15',NULL,'2026-08-11 20:41:15',6,3),(13,'GUARD-NEW-2','Zeeshan Qureshi','zeeshan.qureshi2@test.local','$2a$10$PN/N92j0VIBfMphkmYMeA.pS.fQB3VJMfDYyaYzDw4YeysFfDJ/WG',NULL,NULL,1,NULL,'2026-08-11 20:41:15',NULL,'2026-08-11 20:41:15',7,3),(14,'GUARD-NEW-3','Tariq Javed','tariq.javed3@test.local','$2a$10$PN/N92j0VIBfMphkmYMeA.pS.fQB3VJMfDYyaYzDw4YeysFfDJ/WG',NULL,NULL,1,NULL,'2026-08-11 20:41:15',NULL,'2026-08-11 20:41:15',8,3),(15,'GUARD-NEW-4','Tariq Hussain','tariq.hussain4@test.local','$2a$10$PN/N92j0VIBfMphkmYMeA.pS.fQB3VJMfDYyaYzDw4YeysFfDJ/WG',NULL,NULL,1,NULL,'2026-08-11 20:41:15',NULL,'2026-08-11 20:41:15',9,3),(16,'GUARD-NEW-5','Faisal Javed','faisal.javed5@test.local','$2a$10$2/yoPt6b9yo47w7MKvAWDuHlxzGbm2A5qO.vLkWu8hBq8c6AUwnui',NULL,NULL,1,NULL,'2026-08-11 20:41:15',5,'2026-08-11 20:41:15',NULL,NULL),(17,'GUARD-NEW-6','Naveed Iqbal','naveed.iqbal6@test.local','$2a$10$z8nVQamoM4xWcAbn4jmnXudJ.96Fs5fCcWKqCxKTkQcbmCLZO1QEO',NULL,NULL,1,NULL,'2026-08-11 20:41:15',5,'2026-08-11 20:41:15',NULL,NULL),(18,'GUARD-NEW-7','Kashif Hussain','kashif.hussain7@test.local','$2a$10$PN/N92j0VIBfMphkmYMeA.pS.fQB3VJMfDYyaYzDw4YeysFfDJ/WG',NULL,NULL,1,NULL,'2026-08-11 20:41:15',NULL,'2026-08-11 20:41:15',12,3),(19,'GUARD-NEW-8','Zeeshan Malik','zeeshan.malik8@test.local','$2a$10$PN/N92j0VIBfMphkmYMeA.pS.fQB3VJMfDYyaYzDw4YeysFfDJ/WG',NULL,NULL,1,NULL,'2026-08-11 20:41:15',NULL,'2026-08-11 20:41:15',13,3),(20,'GUARD-NEW-9','Imran Shah','imran.shah9@test.local','$2a$10$PN/N92j0VIBfMphkmYMeA.pS.fQB3VJMfDYyaYzDw4YeysFfDJ/WG',NULL,NULL,1,NULL,'2026-08-11 20:41:15',NULL,'2026-08-11 20:41:15',14,3),(21,'GUARD-NEW-10','Ahmed Khan','ahmed.khan10@test.local','$2a$10$PN/N92j0VIBfMphkmYMeA.pS.fQB3VJMfDYyaYzDw4YeysFfDJ/WG',NULL,NULL,1,NULL,'2026-08-11 20:41:15',NULL,'2026-08-11 20:41:15',15,3),(22,'GUARD-NEW-11','Kashif Khan','kashif.khan11@test.local','$2a$10$PN/N92j0VIBfMphkmYMeA.pS.fQB3VJMfDYyaYzDw4YeysFfDJ/WG',NULL,NULL,1,NULL,'2026-08-11 20:41:15',NULL,'2026-08-11 20:41:15',16,3),(23,'GUARD-NEW-12','Usman Shah','usman.shah12@test.local','$2a$10$PN/N92j0VIBfMphkmYMeA.pS.fQB3VJMfDYyaYzDw4YeysFfDJ/WG',NULL,NULL,1,NULL,'2026-08-11 20:41:15',NULL,'2026-08-11 20:41:15',17,3),(24,'GUARD-NEW-13','Faisal Khan','faisal.khan13@test.local','$2a$10$PN/N92j0VIBfMphkmYMeA.pS.fQB3VJMfDYyaYzDw4YeysFfDJ/WG',NULL,NULL,1,NULL,'2026-08-11 20:41:15',NULL,'2026-08-11 20:41:15',18,3),(25,'GUARD-NEW-14','Kashif Ali','kashif.ali14@test.local','$2a$10$PN/N92j0VIBfMphkmYMeA.pS.fQB3VJMfDYyaYzDw4YeysFfDJ/WG',NULL,NULL,1,NULL,'2026-08-11 20:41:15',NULL,'2026-08-11 20:41:15',19,3),(26,'GUARD-NEW-15','Naveed Iqbal','naveed.iqbal15@test.local','$2a$10$PN/N92j0VIBfMphkmYMeA.pS.fQB3VJMfDYyaYzDw4YeysFfDJ/WG',NULL,NULL,1,NULL,'2026-08-11 20:41:15',NULL,'2026-08-11 20:41:15',20,3),(27,'GUARD-NEW-16','Kashif Hussain','kashif.hussain16@test.local','$2a$10$PN/N92j0VIBfMphkmYMeA.pS.fQB3VJMfDYyaYzDw4YeysFfDJ/WG',NULL,NULL,1,NULL,'2026-08-11 20:41:15',NULL,'2026-08-11 20:41:15',21,3),(28,'GUARD-NEW-17','Ahmed Ali','ahmed.ali17@test.local','$2a$10$PN/N92j0VIBfMphkmYMeA.pS.fQB3VJMfDYyaYzDw4YeysFfDJ/WG',NULL,NULL,1,NULL,'2026-08-11 20:41:15',NULL,'2026-08-11 20:41:15',22,3),(29,'GUARD-NEW-18','Tariq Khan','tariq.khan18@test.local','$2a$10$PN/N92j0VIBfMphkmYMeA.pS.fQB3VJMfDYyaYzDw4YeysFfDJ/WG',NULL,NULL,1,NULL,'2026-08-11 20:41:15',NULL,'2026-08-11 20:41:15',23,3),(30,'GUARD-NEW-19','Faisal Raza','faisal.raza19@test.local','$2a$10$PN/N92j0VIBfMphkmYMeA.pS.fQB3VJMfDYyaYzDw4YeysFfDJ/WG',NULL,NULL,1,NULL,'2026-08-11 20:41:15',NULL,'2026-08-11 20:41:15',24,3),(31,'GUARD-NEW-20','Tariq Javed','tariq.javed20@test.local','$2a$10$PN/N92j0VIBfMphkmYMeA.pS.fQB3VJMfDYyaYzDw4YeysFfDJ/WG',NULL,NULL,1,NULL,'2026-08-11 20:41:15',NULL,'2026-08-11 20:41:15',25,3),(32,'GUARD-BULK-26','GuardFN26 GuardLN26','guard26@test.com','$2a$10$PN/N92j0VIBfMphkmYMeA.pS.fQB3VJMfDYyaYzDw4YeysFfDJ/WG',NULL,NULL,1,NULL,'2026-08-11 20:41:15',NULL,'2026-08-11 20:41:15',26,3),(33,'GUARD-BULK-27','GuardFN27 GuardLN27','guard27@test.com','$2a$10$PN/N92j0VIBfMphkmYMeA.pS.fQB3VJMfDYyaYzDw4YeysFfDJ/WG',NULL,NULL,1,NULL,'2026-08-11 20:41:15',NULL,'2026-08-11 20:41:15',27,3),(34,'GUARD-BULK-28','GuardFN28 GuardLN28','guard28@test.com','$2a$10$PN/N92j0VIBfMphkmYMeA.pS.fQB3VJMfDYyaYzDw4YeysFfDJ/WG',NULL,NULL,1,NULL,'2026-08-11 20:41:15',NULL,'2026-08-11 20:41:15',28,3),(35,'GUARD-BULK-29','GuardFN29 GuardLN29','guard29@test.com','$2a$10$PN/N92j0VIBfMphkmYMeA.pS.fQB3VJMfDYyaYzDw4YeysFfDJ/WG',NULL,NULL,1,NULL,'2026-08-11 20:41:15',NULL,'2026-08-11 20:41:15',29,3),(36,'GUARD-BULK-30','GuardFN30 GuardLN30','guard30@test.com','$2a$10$PN/N92j0VIBfMphkmYMeA.pS.fQB3VJMfDYyaYzDw4YeysFfDJ/WG',NULL,NULL,1,NULL,'2026-08-11 20:41:15',NULL,'2026-08-11 20:41:15',30,3),(37,'6ea1e01a-e8e7-4711-a6cc-56be03abc969','new guard list guard','guard@gmail.com','$2a$10$PrLEERLEoUzg2u3kQiTQpOEWz0W7MuL3FuP5WIflp7OKk498oNmi2',NULL,NULL,1,5,'2026-08-24 23:14:11',NULL,'2026-08-24 23:14:11',31,3);

/*Table structure for table `vehicle_inspections` */

DROP TABLE IF EXISTS `vehicle_inspections`;

CREATE TABLE `vehicle_inspections` (
  `id` int NOT NULL AUTO_INCREMENT,
  `guard_id` int DEFAULT NULL,
  `vehicle_plate` varchar(50) NOT NULL,
  `vehicle_model` varchar(100) DEFAULT NULL,
  `mileage` int DEFAULT '0',
  `fuel_level` enum('quarter','half','three_quarter','full') DEFAULT 'full',
  `status` enum('passed','action_required') DEFAULT 'passed',
  `inspection_notes` text,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `vehicle_inspections` */

insert  into `vehicle_inspections`(`id`,`guard_id`,`vehicle_plate`,`vehicle_model`,`mileage`,`fuel_level`,`status`,`inspection_notes`,`created_at`) values (1,NULL,'PATROL-01','Ford Explorer Security Special',42150,'full','passed','Tire pressures optimal. All strobe lights functional.','2026-08-24 22:54:33'),(2,NULL,'PATROL-02','Toyota RAV4 Hybrid Patrol',28900,'three_quarter','passed','Clean interior. Radio unit tested and working.','2026-08-24 22:54:33'),(3,NULL,'PATROL-03','Chevrolet Tahoe Mobile Command',61200,'half','action_required','Low washer fluid warning. Left headlight dim.','2026-08-24 22:54:33');

/*Table structure for table `visitor_logs` */

DROP TABLE IF EXISTS `visitor_logs`;

CREATE TABLE `visitor_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `site_id` int DEFAULT NULL,
  `visitor_name` varchar(150) NOT NULL,
  `pass_number` varchar(50) DEFAULT NULL,
  `host_person` varchar(100) DEFAULT NULL,
  `company_name` varchar(150) DEFAULT NULL,
  `entry_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `exit_time` datetime DEFAULT NULL,
  `status` enum('checked_in','checked_out') DEFAULT 'checked_in',
  `notes` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `visitor_logs` */

insert  into `visitor_logs`(`id`,`site_id`,`visitor_name`,`pass_number`,`host_person`,`company_name`,`entry_time`,`exit_time`,`status`,`notes`) values (1,NULL,'Alexander Wright','PASS-8821','Sarah Jenkins (IT Director)','Cisco Systems','2026-08-24 22:54:33',NULL,'checked_in','Network infrastructure maintenance'),(2,NULL,'Elena Rostova','PASS-8822','Michael Vance (Facilities)','Otis Elevators','2026-08-24 22:54:33',NULL,'checked_in','Quarterly elevator inspection'),(3,NULL,'Marcus Vance','PASS-8819','David Sterling (CEO)','Apex Capital','2026-08-24 22:54:33',NULL,'checked_out','Executive board consultation meeting');

/*Table structure for table `welfare_checkins` */

DROP TABLE IF EXISTS `welfare_checkins`;

CREATE TABLE `welfare_checkins` (
  `id` int NOT NULL AUTO_INCREMENT,
  `guard_id` int NOT NULL,
  `interval_minutes` int DEFAULT '60',
  `last_ping_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `status` enum('safe','checkin_due','overdue_alert') DEFAULT 'safe',
  `notes` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_welfare_guard` (`guard_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*Data for the table `welfare_checkins` */

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
