-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Feb 04, 2023 at 01:50 PM
-- Server version: 10.3.29-MariaDB-0+deb10u1
-- PHP Version: 7.3.29-1~deb10u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `WeatherSenseWireless`
--

-- --------------------------------------------------------

--
-- Table structure for table `WeatherRack3`
--

CREATE TABLE IF NOT EXISTS `WeatherRack3` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `MessageID` int(11) NOT NULL,
  `SerialNumber` int(11) NOT NULL,
  `OutdoorTemperature` float NOT NULL,
  `OutdoorHumidity` float NOT NULL,
  `TotalRain` float NOT NULL,
  `SunlightVisible` float NOT NULL,
  `VisibleLightLux100` int(11) NOT NULL,
  `WindDirection` float NOT NULL,
  `WindSpeed` float NOT NULL,
  `WindForce` int(11) NOT NULL,
  `Noise` float NOT NULL,
  `BarometricPressure` float NOT NULL,
  `BarometricPressureSeaLevel` float NOT NULL,
  `AQI` float NOT NULL,
  `AQI24Average` float NOT NULL DEFAULT 0,
  `PM2_5` int(11) NOT NULL,
  `PM10` int(11) NOT NULL,
  `CPUTemperature` float NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `WeatherRack3Power`
--

CREATE TABLE IF NOT EXISTS `WeatherRack3Power` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `TimeStamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `MessageID` int(11) NOT NULL,
  `SerialNumber` int(11) NOT NULL,
  `BatteryCapacity` int(11) NOT NULL,
  `LoadVoltage` float NOT NULL,
  `LoadCurrent` float NOT NULL,
  `BatteryVoltage` float NOT NULL,
  `BatteryCurrent` float NOT NULL,
  `SolarPanelVoltage` float NOT NULL,
  `SolarPanelCurrent` float NOT NULL,
  `BatteryPower` float NOT NULL,
  `LoadPower` float NOT NULL,
  `SolarPower` float NOT NULL,
  `WakeCount` int(11) NOT NULL,
  `AuxA` int(11) NOT NULL,
  `Min_Battery_Voltage_Today_Volts` float NOT NULL,
  `Max_Charge_Current_Today_Amps` float NOT NULL,
  `Max_Discharge_Current_Today_Amps` float NOT NULL,
  `Charge_Amp_Hrs_Today_Amp_Hours` float NOT NULL,
  `Discharge_Amp_Hrs_Today_Amp_Hours` float NOT NULL,
  `Charge_Watt_Hrs_Today_Watt_Hours` float NOT NULL,
  `Discharge_Watt_Hrs_Today_Watt_Hours` float NOT NULL,
  `Controller_Uptime_Days` float NOT NULL,
  `Total_Battery_Over_Charges_Count` float NOT NULL,
  `Total_Battery_Full_Charges_Count` float NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
