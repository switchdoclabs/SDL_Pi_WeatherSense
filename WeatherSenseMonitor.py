from __future__ import print_function
# import state
import sys
# from datetime import datetime
SOFTWAREVERSION = "V015"
import wirelessSensors
import MySQLdb as mdb

import time
from apscheduler.schedulers.background import BackgroundScheduler
import apscheduler.events

import SkyCamRemote
import PictureManagement
# Check for user imports
try:
    import conflocal as config
except ImportError:
    import config

import traceback


# WeatherSense SQL Database
try:

        con = mdb.connect(
          "localhost",
          "root",
          config.MySQL_Password,
          "WeatherSenseWireless"
          )

except:
        print(traceback.format_exc())
        print("--------")
        print("MySQL Database WeatherSenseWireless Not Installed.")
        print("Run this command:")
        print("sudo mysql -u root -p < WeatherSenseWireless.sql")
        print("WeatherSenseMonitor Stopped")
        print("--------")
        sys.exit("WeatherSenseMonitor Requirements Error Exit")

# Check for updates having been applied
try:

        con = mdb.connect(
          "localhost",
          "root",
          config.MySQL_Password,
          "WeatherSenseWireless"
          )
        cur = con.cursor()
        query = "SELECT * FROM SkyCamPictures"
        cur.execute(query)
        query = "SELECT * FROM RAD433MHZ"
        cur.execute(query)

except:
        #print(traceback.format_exc())
        print("--------")
        print("MySQL Database WeatherSenseWireless Updates Not Installed.")
        print("Run this command:")
        print("sudo mysql -u root -p WeatherSenseWireless < updateWeatherSenseWireless.sql")
        print("WeatherSenseMonitor Stopped")
        print("--------")
        sys.exit("WeatherSenseMonitor Requirements Error Exit")



print("-----------------")
print("WeatherSense Monitoring Software")
print("Software Version ", SOFTWAREVERSION)
print("-----------------")


##########
# set up scheduler


# Scheduler Helpers

# print out faults inside events
def ap_my_listener(event):
    if event.exception:
        print(event.exception)
        print(event.traceback)


scheduler = BackgroundScheduler()

# for debugging
scheduler.add_listener(ap_my_listener, apscheduler.events.EVENT_JOB_ERROR)

# read wireless sensor package
scheduler.add_job(wirelessSensors.readSensors)  # run in background


# process SkyCam Remote bi-directional messages 
if (config.enable_MQTT == True):
    scheduler.add_job(SkyCamRemote.startMQTT)  # run in background

# SkyCam Management Programs
scheduler.add_job(PictureManagement.cleanPictures, 'cron', day='*', hour=3, minute=4, args=["Daily Picture Clean"])

scheduler.add_job(PictureManagement.cleanTimeLapses, 'cron', day='*', hour=3, minute=10, args=["Daily Time Lapse Clean"])

scheduler.add_job(PictureManagement.buildTimeLapse, 'cron', day='*', hour=5, minute=30, args=["Time Lapse Generation"])

scheduler.add_job(wirelessSensors.readSensors)  # run in background

scheduler.print_jobs()

# start scheduler
scheduler.start()
print("-----------------")
print("Scheduled Jobs")
print("-----------------")
scheduler.print_jobs()
print("-----------------")



# Main Loop

while True:

    time.sleep(1.0)

