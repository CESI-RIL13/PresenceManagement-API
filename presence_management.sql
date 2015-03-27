SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

DROP SCHEMA IF EXISTS `presence_management` ;
CREATE SCHEMA IF NOT EXISTS `presence_management` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `presence_management` ;

-- -----------------------------------------------------
-- Table `presence_management`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `presence_management`.`user` ;

CREATE  TABLE IF NOT EXISTS `presence_management`.`user` (
  `id` VARCHAR(255) NOT NULL ,
  `fullname` VARCHAR(255) NULL ,
  `mail` VARCHAR(255) NOT NULL ,
  `password` VARCHAR(255) NULL ,
  `role` ENUM('SA','Ingénieur formation','assistant','intervenant','stagiaire') NOT NULL ,
  `archived` TINYINT(1) NULL DEFAULT 0 ,
  `updated` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `presence_management`.`promotion`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `presence_management`.`promotion` ;

CREATE  TABLE IF NOT EXISTS `presence_management`.`promotion` (
  `id` VARCHAR(255) NOT NULL ,
  `name` VARCHAR(255) NULL ,
  `late` INT NULL DEFAULT 15 ,
  `archived` TINYINT(1) NULL DEFAULT 0 ,
  `upadted` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `presence_management`.`room`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `presence_management`.`room` ;

CREATE  TABLE IF NOT EXISTS `presence_management`.`room` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `name` VARCHAR(255) NOT NULL ,
  `raspberry_id` VARCHAR(255) NULL COMMENT 'adresse MAC du raspberry client' ,
  `token` VARCHAR(255) NULL ,
  `archived` TINYINT(1) NULL DEFAULT 0 ,
  `updated` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP ,
  PRIMARY KEY (`id`) ,
  UNIQUE INDEX `raspberry_id_UNIQUE` (`raspberry_id` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `presence_management`.`scheduling`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `presence_management`.`scheduling` ;

CREATE  TABLE IF NOT EXISTS `presence_management`.`scheduling` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `date_start` DATETIME NOT NULL ,
  `date_end` DATETIME NOT NULL ,
  `promotion_id` VARCHAR(255) NOT NULL ,
  `room_id` INT NOT NULL ,
  `user_id` VARCHAR(255) NULL ,
  `course` VARCHAR(255) NULL ,
  `archived` TINYINT(1) NULL DEFAULT 0 ,
  `updated` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP ,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `presence_management`.`presence`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `presence_management`.`presence` ;

CREATE  TABLE IF NOT EXISTS `presence_management`.`presence` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `date` DATETIME NOT NULL ,
  `user_id` VARCHAR(255) NOT NULL ,
  `archived` TINYINT(1) NULL DEFAULT 0 ,
  `updated` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP ,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `presence_management`.`user_has_promotion`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `presence_management`.`user_has_promotion` ;

CREATE  TABLE IF NOT EXISTS `presence_management`.`user_has_promotion` (
  `user_id` VARCHAR(255) NOT NULL ,
  `promotion_id` VARCHAR(255) NOT NULL ,
  PRIMARY KEY (`user_id`, `promotion_id`))
ENGINE = InnoDB;

USE `presence_management` ;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
