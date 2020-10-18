/*****************************************************************************************
Script Name:  home-db creation script
Description:  Establishes the tables required to stand up home-db
******************************************************************************************
Schema:       home-db
******************************************************************************************/

--
-- Table structure for table `DEVICE`
--

DROP TABLE IF EXISTS `DEVICE`;

CREATE TABLE `DEVICE` (
  `MAC_ADDR`  VARCHAR(17)   NOT NULL,
  `NAME`      VARCHAR(40)   NOT NULL,
  `LOCATION`  VARCHAR(60)   NOT NULL,
  PRIMARY KEY (`MAC_ADDR`)
);

--
-- Table structure for table `READING`
--

DROP TABLE IF EXISTS `READING`;

CREATE TABLE `READING` (
  `ID`                INT(11)       NOT NULL AUTO_INCREMENT,
  `TYPE_CDE`          VARCHAR(1)    NOT NULL,
  `VALUE`             DECIMAL(5,2)  NOT NULL,
  `UNIT_CDE`          VARCHAR(1)    NOT NULL,
  `READING_DT`        DATETIME      NOT NULL,
  `DEVICE_MAC_ADDR`   VARCHAR(17)   NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `FK_DEVICE_MAC_ADDR` (`DEVICE_MAC_ADDR`),
  CONSTRAINT `FK_DEVICE_MAC_ADDR` FOREIGN KEY (`DEVICE_MAC_ADDR`) REFERENCES `DEVICE` (`MAC_ADDR`)
);


DELIMITER $$
CREATE FUNCTION is_device_authorized (device_mac VARCHAR(17))
RETURNS BOOLEAN
DETERMINISTIC
  BEGIN
    RETURN IF(
      (SELECT (SELECT COUNT(MAC_ADDR) FROM DEVICE WHERE MAC_ADDR = device_mac) > 0),
      TRUE,
      FALSE
    );
  END$$
DELIMITER ;