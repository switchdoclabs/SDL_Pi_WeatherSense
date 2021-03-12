from __future__ import print_function
# import state
# import sys
# from datetime import datetime
SOFTWAREVERSION = "V003"
import wirelessSensors

import time
from apscheduler.schedulers.background import BackgroundScheduler
import apscheduler.events

# Check for user imports
try:
    import conflocal as config
except ImportError:
    import config

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

scheduler.print_jobs()

# start scheduler
scheduler.start()
print("-----------------")
print("Scheduled Jobs")
print("-----------------")
scheduler.print_jobs()
print("-----------------")
