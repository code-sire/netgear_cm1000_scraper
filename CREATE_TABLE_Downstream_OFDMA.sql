CREATE TABLE `Downstream_OFDMA` (
    `RecordID` bigint(20) NOT NULL AUTO_INCREMENT,
    `Channel` varchar(100) DEFAULT NULL,
    `Lock_Status` varchar(100) DEFAULT NULL,
    `Modulation` varchar(100) DEFAULT NULL,
    `Channel_ID` varchar(100) DEFAULT NULL,
    `Frequency` varchar(100) DEFAULT NULL,
    `Power` varchar(100) DEFAULT NULL,
    `SNR` varchar(100) DEFAULT NULL,
    `Active_Subcarrier_Number_Range` varchar(100) DEFAULT NULL,
    `Unerrored_Codewords` varchar(100) DEFAULT NULL,
    `Correctable_Codewords` varchar(100) DEFAULT NULL,
    `Uncorrectable_Codewords` varchar(100) DEFAULT NULL,
    `Capture_DT` varchar(100) DEFAULT NULL,
    PRIMARY KEY (`RecordID`)
) ENGINE = InnoDB AUTO_INCREMENT = 18347 DEFAULT CHARSET = utf8;
