CREATE TABLE `Upstream` (
    `RecordID` bigint(20) NOT NULL AUTO_INCREMENT,
    `Channel` varchar(100) DEFAULT NULL,
    `Lock_Status` varchar(100) DEFAULT NULL,
    `Modulation` varchar(100) DEFAULT NULL,
    `Channel_ID` varchar(100) DEFAULT NULL,
    `Frequency` varchar(100) DEFAULT NULL,
    `Power` varchar(100) DEFAULT NULL,
    `US_Channel_Type` varchar(10) DEFAULT NULL,
    `Symbol_Rate` varchar(20) DEFAULT NULL,
    `Capture_DT` varchar(100) DEFAULT NULL,
    PRIMARY KEY (`RecordID`)
) ENGINE = InnoDB AUTO_INCREMENT = 73393 DEFAULT CHARSET = utf8;
