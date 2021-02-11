CREATE TABLE `Connection_Issues` (
    `RecordID` int(11) NOT NULL AUTO_INCREMENT,
    `Downtime` int(11) DEFAULT NULL,
    `Capture_DT` datetime DEFAULT NULL,
    PRIMARY KEY (`RecordID`)
) ENGINE = InnoDB AUTO_INCREMENT = 4 DEFAULT CHARSET = utf8;