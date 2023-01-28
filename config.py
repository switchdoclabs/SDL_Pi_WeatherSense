#
#
# configuration file - contains customization for WeatherSense 
#

from builtins import hex

SWDEBUG = True

SWVERSION = "000"  # set in WeatherSenseMontor.py

# altitude of WeatherRack3 station in meters
altitude_m = 620


import uuid

#configure SkyCam Remote camera
#default
DefaultCameraRotation = 90
SkyCamRotationArray = {}
SkyCamRotationArray["DE45"] = 90
SkyCamRotationArray["3BAD"] =270 
SkyCamRotationArray["26FD"] =270 


# MySQL Logging and Password Information

enable_MySQL_Logging = True
MySQL_Host = "localhost"
MySQL_User = "root"
MySQL_Password = "password"
MySQL_Schema = "WeatherSenseWireless"

# 0 is English, 1 is metric
English_Metric = 0

# configuration for MQTT

enable_MQTT = True
MQTThost = "localhost"
MQTTport = 1883
MQTTqos = 0

# configuration for WeatherRack2
# This variables tell you how often to record values for the WeahterRack2
# You get a reading about every 45 seconds and this leads to big databases 
# about 14,000 records a week.  Remember that each FT020 Transmission is
# duplicated which means you nead a value of 2X what you want
# The default value is 20, which gives us about 1400 or about every 7.5 minutes.

RecordEveryXReadings = 20

# This variable controls how often to record the indoor T/H sensors
# You may have a total of 8 sensors and they each transmit around 60 seconds
# this will cause a possible total number of records per week of: 80,640 records
# The indoor T/H sensors also send a duplicate record but the rtl_433 software
# filters it out.
# The default value is 10, which gives us a value about every 10 minutes 
# per sensor.  Each sensor is counted seperately in the wirelessSensors.py

IndoorRecordEveryXReadings = 10
