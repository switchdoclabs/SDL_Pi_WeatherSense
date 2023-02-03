#
# wireless sensor routines


import config

import json
import random

import sys
from subprocess import PIPE, Popen, STDOUT
from threading import Thread
import datetime
import MySQLdb as mdb
import traceback
import state
import os
import util

import updateWeb

from paho.mqtt import publish

import aqi


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------

#cmd = [ '/usr/local/bin/rtl_433', '-q', '-F', 'json', '-R', '154', '-R', '155']
cmd = ['/usr/local/bin/rtl_433', '-q', '-F', 'json', '-R', '146', '-R', '147', '-R', '148', '-R', '150', '-R', '151', '-R', '152', '-R', '153', '-R', '154', '-R', '155']


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
#   A few helper functions...

def nowStr():
    return (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


# stripped = lambda s: "".join(i for i in s if 31 < ord(i) < 127)


#   We're using a queue to capture output as it occurs
try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x
ON_POSIX = 'posix' in sys.builtin_module_names


def enqueue_output(src, out, queue):
    for line in iter(out.readline, b''):
        queue.put((src, line))
    out.close()


def randomadd(value, spread):
    return round(value + random.uniform(-spread, spread), 2)


# MQTT Publish Line
def mqtt_publish_single(message, topic):
    topic = '{0}/{1}'.format("weathersense", topic)
    return
    try:
        publish.single(
            topic=topic,
            payload=message,
            hostname=config.MQTThost,
            port=config.MQTTport,
            qos=config.MQTTqos
        )
    except:
        traceback.print_exc()
        print('Mosquitto not available')


# process functions
import gpiozero

# WeatherRack3

def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is


def processWeatherRack3(sLine, lastWeatherRack3TimeStamp, ReadingCount):
    if (config.SWDEBUG):
        sys.stdout.write("processing WeatherRack3 Weather Data\n")
        sys.stdout.write('This is the raw data: ' + sLine + '\n')
        sys.stdout.write('ReadingCount=: ' + str(ReadingCount) + '\n')

    var = json.loads(sLine)

    if (config.enable_MQTT == True):
        mqtt_publish_single(sLine, "WeatherRack3")

    if (lastWeatherRack3TimeStamp == var["time"]):
        # duplicate
        if (config.SWDEBUG):
            sys.stdout.write("duplicate found\n")

        return ""
    lastWeatherRack3TimeStamp = var["time"]


    # outside temperature and Humidity

    lastMainReading = nowStr()
    MessageID = var["messageid"];
    SerialNumber = var["deviceid"]
    wTemp = var["temperature"]
    #wTemp = twos_comp(var["temperature"], 16);

    ucHumi = var["humidity"]

    wTemp = wTemp / 10.0
    # deal with error condtions
    if (wTemp > 140.0):
        # error condition from sensor
        if (config.SWDEBUG):
            sys.stdout.write("error--->>> Temperature reading from WeatherRack3\n")
            sys.stdout.write('This is the raw temperature: ' + str(wTemp) + '\n')
        # put in previous temperature 
        wtemp = state.currentOutsideTemperature
        # print("wTemp=%s %s", (str(wTemp),nowStr() ));
    if (ucHumi > 1000.0):
        # bad humidity
        # put in previous humidity
        ucHumi = state.currentOutsideHumidity

    OutdoorTemperature = wTemp
    #OutdoorTemperature = round(wTemp, 2)
    OutdoorHumidity = round(ucHumi/10.0, 1)

    WindSpeed = round(var["windspeed"] / 10.0, 1)
    WindDirection = var["winddirectiondegrees"]
    WindForce = var["windforce"]
    Noise = round(var["noise"]/10.0, 1)
    TotalRain = round(var["rain"] / 10.0, 1)
    Rain60Minutes = 0.0

    PM2_5 = var["PM2_5"]
    PM10 = var["PM10"]
    SunlightVisible = var["hwlux"] *256*256 + var["lwlux"] 
    VisibleLightLux100 = var["lightvalue20W"]
    myaqi = aqi.to_aqi([
        (aqi.POLLUTANT_PM25, var['PM2_5']),
        (aqi.POLLUTANT_PM10, var['PM10'])
        ])
    if (myaqi > 500):
            myaqi = 500
    #print("myaqi=", myaqi)
    AQI = myaqi

    if (config.enable_MySQL_Logging == True):
        # open mysql database
        # write log
        # commit
        # close
        try:

            con = mdb.connect(
                config.MySQL_Host,
                config.MySQL_User,
                config.MySQL_Password,
                config.MySQL_Schema
            )
            cur = con.cursor()

            # calculate AQI 24 Hour
            timeDelta = datetime.timedelta(days=1)
            now = datetime.datetime.now()
            before = now - timeDelta
            before = before.strftime('%Y-%m-%d %H:%M:%S')
            query = "SELECT AQI, TimeStamp FROM WeatherRack3 WHERE (TimeStamp > '%s') ORDER BY TimeStamp " % (before)

            cur.execute(query)
            myAQIRecords = cur.fetchall()
            myAQITotal = 0.0
            if (len(myAQIRecords) > 0):
                for i in range(0, len(myAQIRecords)):
                    myAQITotal = myAQITotal + myAQIRecords[i][0]
                # adapt for current record
                AQI24Hour = (myAQITotal + float(AQI)) / (len(myAQIRecords) + 1)
            else:
                AQI24Hour = 0.0
        except mdb.Error as e:
            traceback.print_exc()
            print("Error %d: %s" % (e.args[0], e.args[1]))
            con.rollback()
            # sys.exit(1)

        finally:
            cur.close()
            con.close()

            del cur
            del con

    AQI24Average = AQI24Hour

    BarometricPressure = var["pressure"] 
    #calculates the pressure at sealevel when given a known altitude in meters
    
         
    BarometricPressureSeaLevel = (BarometricPressure * 100000) / pow(1.0 - config.altitude_m / 44330.0, 5.255)
    BarometricPressureSeaLevel = BarometricPressureSeaLevel / 100000
    if (config.enable_MySQL_Logging == True):
        # open mysql database
        # write log
        # commit
        # close
        try:
            cpu = gpiozero.CPUTemperature()
            CPUTemperature = cpu.temperature

            con = mdb.connect(
                config.MySQL_Host,
                config.MySQL_User,
                config.MySQL_Password,
                config.MySQL_Schema
            )

            cur = con.cursor()

            fields = "MessageID, SerialNumber, OutdoorTemperature, OutdoorHumidity, TotalRain, SunlightVisible, WindSpeed, WindForce, WindDirection, Noise, BarometricPressure, BarometricPressureSeaLevel, AQI, AQI24Average, PM2_5, PM10,  CPUTemperature,VisibleLightLux100"
            values = "%d, %d, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f,%6.2f,%6.2f,%d,%d,%6.2f, %d" % (
            MessageID, SerialNumber, OutdoorTemperature, OutdoorHumidity, TotalRain, SunlightVisible, WindSpeed, WindForce, WindDirection, Noise, BarometricPressure, BarometricPressureSeaLevel, AQI, AQI24Average, PM2_5, PM10, CPUTemperature, VisibleLightLux100)
            query = "INSERT INTO WeatherRack3 (%s) VALUES(%s )" % (fields, values)
            # print("query=", query)
            cur.execute(query)
            con.commit()
        except mdb.Error as e:
            traceback.print_exc()
            print("Error %d: %s" % (e.args[0], e.args[1]))
            con.rollback()
            # sys.exit(1)

        finally:
            cur.close()
            con.close()

            del cur
            del con
    return lastWeatherRack3TimeStamp


def processWeatherRack3Power(sLine, lastWeatherRack3PowerTimeStamp, WeatherRack3PowerCount):
    state = json.loads(sLine)
    if (config.SWDEBUG):
        sys.stdout.write("processing WeatherRack3 Power Data\n")
        sys.stdout.write('This is the raw data: ' + sLine + '\n')

    if (config.enable_MQTT == True):
            mqtt_publish_single(sLine, "WR3Power")
    
    if (lastWeatherRack3PowerTimeStamp == state["time"]):
        # duplicate
        if (config.SWDEBUG):
            sys.stdout.write("duplicate found\n")

        return ""
    lastWeatherRack3PowerTimeStamp = state["time"]

    if (config.enable_MySQL_Logging == True):
            # open mysql database
            # write log
            # commit
            # close
            try:
                myTEST = ""
                myTESTDescription = ""

                con = mdb.connect(
                    config.MySQL_Host,
                    config.MySQL_User,
                    config.MySQL_Password,
                    config.MySQL_Schema
                )

                cur = con.cursor()
                batteryPower =  float(state["batterychargecurrent"])* float(state["batteryvoltage"])
                loadPower  =  float(state["loadcurrent"])* float(state["loadvoltage"])
                solarPower =  float(state["solarpanelcurrent"])* float(state["solarpanelvoltage"])

                fields = "MessageID, SerialNumber, BatteryCapacity, BatteryVoltage, BatteryCurrent, LoadVoltage, LoadCurrent, SolarPanelVoltage, SolarPanelCurrent, AuxA, BatteryPower, LoadPower, SolarPower, WakeCount, Min_Battery_Voltage_Today_Volts, Max_Charge_Current_Today_Amps, Max_Discharge_Current_Today_Amps, Charge_Amp_Hrs_Today_Amp_Hours, Discharge_Amp_Hrs_Today_Amp_Hours, Charge_Watt_Hrs_Today_Watt_Hours,Discharge_Watt_Hrs_Today_Watt_Hours, Controller_Uptime_Days, Total_Battery_Over_Charges_Count, Total_Battery_Full_Charges_Count "
                values = "%d, %d, %d, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f,%6.2f,%6.2f,%d, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f" % (
                state["messageid"], state["deviceid"],state["batterycapacity"],
                state["batteryvoltage"], state["batterychargecurrent"], state["loadvoltage"], state["loadcurrent"],
                state["solarpanelvoltage"], state["solarpanelcurrent"], state["auxa"],
                batteryPower, loadPower, solarPower, state["wakecount"], state["Min_Battery_Voltage_Today_Volts"], state["Max_Charge_Current_Today_Amps"], state["Max_Discharge_Current_Today_Amps"], state["Charge_Amp_Hrs_Today_Amp_Hours"], state["Discharge_Amp_Hrs_Today_Amp_Hours"], state["Charge_Watt_Hrs_Today_Watt_Hours"], state["Discharge_Watt_Hrs_Today_Watt_Hours"], state["Controller_Uptime_Days"], state["Total_Battery_Over_Charges_Count"], state["Total_Battery_Full_Charges_Count"]
                )
                query = "INSERT INTO WeatherRack3Power (%s) VALUES(%s )" % (fields, values)
                #print("query=", query)
                cur.execute(query)
                con.commit()
            except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0], e.args[1]))
                con.rollback()
                # sys.exit(1)

            finally:
                cur.close()
                con.close()

                del cur
                del con

    return lastWeatherRack3PowerTimeStamp





# WeatherRack2

def processFT020T(sLine, lastFT020TTimeStamp, ReadingCount):
    if (config.SWDEBUG):
        sys.stdout.write("processing FT020T Data\n")
        sys.stdout.write('This is the raw data: ' + sLine + '\n')
        sys.stdout.write('ReadingCount=: ' + str(ReadingCount) + '\n')

    var = json.loads(sLine)

    if (config.enable_MQTT == True):
        mqtt_publish_single(sLine, "FT020T")

    if (lastFT020TTimeStamp == var["time"]):
        # duplicate
        if (config.SWDEBUG):
            sys.stdout.write("duplicate found\n")

        return ""
    lastFT0202TTimeStamp = var["time"]

    # now check for adding record

    if ((ReadingCount % config.RecordEveryXReadings) != 0):
        # skip write to database 
        if (config.SWDEBUG):
            sys.stdout.write("skipping write to database \n")

        return ""

    # outside temperature and Humidity

    mainID = var["id"]
    lastMainReading = nowStr()

    wTemp = var["temperature"]

    ucHumi = var["humidity"]

    wTemp = (wTemp - 400) / 10.0
    # deal with error condtions
    if (wTemp > 140.0):
        # error condition from sensor
        if (config.SWDEBUG):
            sys.stdout.write("error--->>> Temperature reading from FT020T\n")
            sys.stdout.write('This is the raw temperature: ' + str(wTemp) + '\n')
        # put in previous temperature 
        wtemp = state.currentOutsideTemperature
        # print("wTemp=%s %s", (str(wTemp),nowStr() ));
    if (ucHumi > 100.0):
        # bad humidity
        # put in previous humidity
        ucHumi = state.currentOutsideHumidity

    # convert temperature reading to Celsius
    OutdoorTemperature = round(((wTemp - 32.0) / (9.0 / 5.0)), 2)
    #OutdoorTemperature = round(wTemp, 2)
    OutdoorHumidity = ucHumi

    WindSpeed = round(var["avewindspeed"] / 10.0, 1)
    WindGust = round(var["gustwindspeed"] / 10.0, 1)
    WindDirection = var["winddirection"]

    TotalRain = round(var["cumulativerain"] / 10.0, 1)
    Rain60Minutes = 0.0

    wLight = var["light"]
    #if (wLight >= 0x1fffa):
    #    wLight = wLight | 0x7fff0000

    wUVI = var["uv"]
    if (wUVI >= 0xfa):
        wUVI = wUVI | 0x7f00

    SunlightVisible = wLight
    SunlightUVIndex = round(wUVI / 10.0, 1)

    if (var['batterylow'] == 0):
        BatteryOK = "OK"
    else:
        BatteryOK = "LOW"

    # SkyWeather2 Compatiblity
    AQI = 0
    Hour24_AQI = 0
    IndoorTemperature = 0
    IndoorHumidity = 0
    BarometricPressure = 0.0
    BarometricPressureSeaLevel = 0.0
    BarometricTemperature = 0.0

    if (config.enable_MySQL_Logging == True):
        # open mysql database
        # write log
        # commit
        # close
        try:
            cpu = gpiozero.CPUTemperature()
            CPUTemperature = cpu.temperature

            con = mdb.connect(
                config.MySQL_Host,
                config.MySQL_User,
                config.MySQL_Password,
                config.MySQL_Schema
            )

            cur = con.cursor()

            fields = "OutdoorTemperature, OutdoorHumidity, IndoorTemperature, IndoorHumidity, TotalRain, SunlightVisible, SunlightUVIndex, WindSpeed, WindGust, WindDirection,BarometricPressure, BarometricPressureSeaLevel, BarometricTemperature, AQI, AQI24Average, BatteryOK, CPUTemperature"
            values = "%6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f,%6.2f,%6.2f,%6.2f,%6.2f,%6.2f, \'%s\',%6.2f" % (
            OutdoorTemperature, OutdoorHumidity, IndoorTemperature, IndoorHumidity, TotalRain, SunlightVisible,
            SunlightUVIndex, WindSpeed, WindGust, WindDirection, BarometricPressure, BarometricPressureSeaLevel,
            BarometricTemperature, float(AQI), Hour24_AQI, BatteryOK, CPUTemperature)
            query = "INSERT INTO WeatherData (%s) VALUES(%s )" % (fields, values)
            # print("query=", query)
            cur.execute(query)
            con.commit()
        except mdb.Error as e:
            traceback.print_exc()
            print("Error %d: %s" % (e.args[0], e.args[1]))
            con.rollback()
            # sys.exit(1)

        finally:
            cur.close()
            con.close()

            del cur
            del con
    return lastFT0202TTimeStamp


# processes Inside Temperature and Humidity
def processF016TH(sLine, ReadingCountArray):
    if (config.SWDEBUG):
        sys.stdout.write('Processing F016TH data' + '\n')
        sys.stdout.write('This is the raw data: ' + sLine + '\n')
        if config.SWDEBUG:
        
            print(ReadingCountArray)

    var = json.loads(sLine)

    if (config.enable_MQTT == True):
        mqtt_publish_single(sLine, "F016TH")

    lastIndoorReading = nowStr()

    # check for reading count per device
    # indoor T/H sensors support channels 1-8
    # the sensor channel needs to be lowered by one
    chan_array_pos = var['channel'] - 1

    #if ((ReadingCountArray[var["channel"]] % config.IndoorRecordEveryXReadings) != 0):
    if (ReadingCountArray[chan_array_pos] % config.IndoorRecordEveryXReadings) != 0:
        if config.SWDEBUG:
            print("skipping write to database for channel=", var["channel"])
        # increment ReadingCountArray
        # ReadingCountArray[var["channel"]] = ReadingCountArray[var["channel"]] + 1
        ReadingCountArray[chan_array_pos] += 1
        return ""
    # increment ReadingCountArray
    # ReadingCountArray[var["channel"]] = ReadingCountArray[var["channel"]] + 1
    ReadingCountArray[chan_array_pos] += 1

    IndoorTemperature = round(((var["temperature_F"] - 32.0) / (9.0 / 5.0)), 2)
    #IndoorTemperature = var["temperature_F"]

    if (config.enable_MySQL_Logging == True):
        # open mysql database
        # write log
        # commit
        # close
        try:

            con = mdb.connect(
                config.MySQL_Host,
                config.MySQL_User,
                config.MySQL_Password,
                config.MySQL_Schema
            )

            cur = con.cursor()

            fields = "DeviceID, ChannelID, Temperature, Humidity, BatteryOK, TimeRead"

            values = "%d, %d, %6.2f, %6.2f, \"%s\", \"%s\"" % (
            var["device"], var["channel"], IndoorTemperature, var["humidity"], var["battery"], var["time"])
            query = "INSERT INTO IndoorTHSensors (%s) VALUES(%s )" % (fields, values)
            # print("query=", query)
            cur.execute(query)
            con.commit()
        except mdb.Error as e:
            traceback.print_exc()
            print("Error %d: %s" % (e.args[0], e.args[1]))
            con.rollback()
            # sys.exit(1)

        finally:
            cur.close()
            con.close()

            del cur
            del con
    return




# processes Generic Packets 
def processWeatherSenseGeneric(sLine):
    if (config.SWDEBUG):
        sys.stdout.write("processing Generic Data\n")
        sys.stdout.write('This is the raw data: ' + sLine + '\n')

    if (config.enable_MQTT == True):
        mqtt_publish_single(sLine, "WSGeneric")

    return

# processes Radiation Detector Packets 
def processWeatherSenseRadiation(sLine):
    # WeatherSense Protocol 19
    state = json.loads(sLine)
    myProtocol = state['weathersenseprotocol']
    if (config.SWDEBUG):
        sys.stdout.write("processing Radiation Data\n")
        sys.stdout.write('This is the raw data: ' + sLine + '\n')

    if (config.enable_MQTT == True):
        mqtt_publish_single(sLine, "WSRadiation")


    if (config.enable_MySQL_Logging == True):
        # open mysql database
        # write log
        # commit
        # close
        try:

            con = mdb.connect(
                config.MySQL_Host,
                config.MySQL_User,
                config.MySQL_Password,
                config.MySQL_Schema
            )
            
            # calculate Radiation 24 Hour
            timeDelta = datetime.timedelta(days=1)
            now = datetime.datetime.now()
            before = now - timeDelta
            before = before.strftime('%Y-%m-%d %H:%M:%S')
            query = "SELECT uSVh, TimeStamp FROM RAD433MHZ WHERE (TimeStamp > '%s') ORDER BY TimeStamp " % (before)

            cur = con.cursor()
            cur.execute(query)
            myRADRecords = cur.fetchall()
            myRADTotal = 0.0
            if (len(myRADRecords) > 0):
                for i in range(0, len(myRADRecords)):
                    myRADTotal = myRADTotal + myRADRecords[i][0]

                RAD24Hour = (myRADTotal + float(state['uSVh'])) / (len(myRADRecords) + 1)
            else:
                RAD24Hour = 0.0

            batteryPower =  float(state["batterycurrent"])* float(state["batteryvoltage"])
            loadPower  =  float(state["loadcurrent"])* float(state["loadvoltage"])
            solarPower =  float(state["solarpanelcurrent"])* float(state["solarpanelvoltage"])
            batteryCharge = util.returnPercentLeftInBattery(state["batteryvoltage"], 4.2)

            fields = "uSVh24Hour, deviceid, protocolversion, softwareversion, weathersenseprotocol, CPM, nSVh, uSVh, batteryvoltage, batterycurrent, loadvoltage, loadcurrent, solarvoltage, solarcurrent, auxa, solarpresent, radiationpresent, keepalivemessage, lowbattery, batterycharge, messageID, batterypower, loadpower, solarpower "
            values = "%6.2f, %d, %d, %d, %d, %d,%d,  %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %d, %d, %d,%d,%d,%6.2f, %d,%6.2f, %6.2f, %6.3f" % ( RAD24Hour, state["deviceid"], state["protocolversion"], state["softwareversion"], state["weathersenseprotocol"],
            state['CPM'], state['nSVh'], state['uSVh'], 
            state["batteryvoltage"], state["batterycurrent"], state["loadvoltage"], state["loadcurrent"],
            state["solarpanelvoltage"], state["solarpanelcurrent"], state["auxa"],state["solarpresent"],state["radBoardPresent"],state["keepalivemessage"],state["lowbattery"],     batteryCharge, state["messageid"],
            batteryPower, loadPower, solarPower )
            query = "INSERT INTO RAD433MHZ (%s) VALUES(%s )" % (fields, values)
            # print("query=", query)
            cur.execute(query)
            con.commit()
        except mdb.Error as e:
            traceback.print_exc()
            print("Error %d: %s" % (e.args[0], e.args[1]))
            con.rollback()
            # sys.exit(1)

        finally:
            cur.close()
            con.close()

            del cur
            del con
            
            CPM = state['CPM']
            uSVh = state['uSVh']
            # update web maps
            updateWeb.update_SafeCast(CPM, uSVh)
            updateWeb.update_RadMon(CPM)
            updateWeb.update_GMCMap(CPM, uSVh)

            



    return

# processes AfterShock Packets 
def processWeatherSenseAfterShock(sLine):

    # weathersense protocol 18
    state = json.loads(sLine)
    myProtocol = state['weathersenseprotocol']
    if (config.SWDEBUG):
        sys.stdout.write("processing AfterShock Data\n")
        sys.stdout.write('This is the raw data: ' + sLine + '\n')

    if (config.enable_MQTT == True):
        mqtt_publish_single(sLine, "WSAfterShock")


    if (config.enable_MySQL_Logging == True):
        # open mysql database
        # write log
        # commit
        # close
        try:
            myTEST = ""
            myTESTDescription = ""

            con = mdb.connect(
                config.MySQL_Host,
                config.MySQL_User,
                config.MySQL_Password,
                config.MySQL_Schema
            )

            cur = con.cursor()
            batteryPower =  float(state["batterycurrent"])* float(state["batteryvoltage"])
            loadPower  =  float(state["loadcurrent"])* float(state["loadvoltage"])
            solarPower =  float(state["solarpanelcurrent"])* float(state["solarpanelvoltage"])
            batteryCharge = util.returnPercentLeftInBattery(state["batteryvoltage"], 4.2)

            fields = "deviceid, protocolversion, softwareversion, weathersenseprotocol, eqcount, finaleq_si, finaleq_pga, instanteq_si, instanteq_pga, batteryvoltage, batterycurrent, loadvoltage, loadcurrent, solarvoltage, solarcurrent, auxa, solarpresent, aftershockpresent, keepalivemessage, lowbattery, batterycharge, messageID, batterypower, loadpower, solarpower, test, testdescription"
            values = "%d, %d, %d, %d, %d,%6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f,%6.2f,%6.2f, %d, %d, %d, %d,%d,%6.2f, %6.2f, %6.2f,\'%s\', \'%s\'" % (
            state["deviceid"], state["protocolversion"], state["softwareversion"], state["weathersenseprotocol"],
            state['eqcount'], state['finaleq_si'], state['finaleq_pga'], state['instanteq_si'],
            state['instanteq_pga'], 
            state["batteryvoltage"], state["batterycurrent"], state["loadvoltage"], state["loadcurrent"],
            state["solarpanelvoltage"], state["solarpanelcurrent"], state["auxa"],state["solarpresent"],state["aftershockpresent"],state["keepalivemessage"],state["lowbattery"],     batteryCharge, state["messageid"],
            batteryPower, loadPower, solarPower, myTEST, myTESTDescription)
            query = "INSERT INTO AS433MHZ (%s) VALUES(%s )" % (fields, values)
            # print("query=", query)
            cur.execute(query)
            con.commit()
        except mdb.Error as e:
            traceback.print_exc()
            print("Error %d: %s" % (e.args[0], e.args[1]))
            con.rollback()
            # sys.exit(1)

        finally:
            cur.close()
            con.close()

            del cur
            del con

    return



def processWeatherSenseTB(sLine):
    # weathersense protocol 16
    state = json.loads(sLine)
    myProtocol = state['weathersenseprotocol']
    if (config.SWDEBUG):
        sys.stdout.write("processing Lightning TB Data\n")
        sys.stdout.write('This is the raw data: ' + sLine + '\n')

    if (config.enable_MQTT == True):
        mqtt_publish_single(sLine, "WSLightning")

    if (config.enable_MySQL_Logging == True):
        # open mysql database
        # write log
        # commit
        # close
        try:
            myTEST = ""
            myTESTDescription = ""

            con = mdb.connect(
                config.MySQL_Host,
                config.MySQL_User,
                config.MySQL_Password,
                config.MySQL_Schema
            )

            cur = con.cursor()
            batteryPower =  float(state["batterycurrent"])* float(state["batteryvoltage"])
            loadPower  =  float(state["loadcurrent"])* float(state["loadvoltage"])
            solarPower =  float(state["solarpanelcurrent"])* float(state["solarpanelvoltage"])
            batteryCharge = util.returnPercentLeftInBattery(state["batteryvoltage"], 4.2)

            fields = "deviceid, protocolversion, softwareversion, weathersenseprotocol,irqsource, previousinterruptresult, lightninglastdistance, sparebyte, lightningcount, interruptcount,  batteryvoltage, batterycurrent, loadvoltage, loadcurrent, solarvoltage, solarcurrent, auxa, batterycharge, messageID, batterypower, loadpower, solarpower, test, testdescription"
            values = "%d, %d, %d, %d, %d, %d, %d, %d,%d, %d,%6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f,%6.2f,%6.2f,%d,%6.2f, %6.2f, %6.2f,\'%s\', \'%s\'" % (
            state["deviceid"], state["protocolversion"], state["softwareversion"], state["weathersenseprotocol"],
            state['irqsource'], state['previousinterruptresult'], state['lightninglastdistance'], state['sparebyte'],
            state['lightningcount'], state['interruptcount'],
            state["batteryvoltage"], state["batterycurrent"], state["loadvoltage"], state["loadcurrent"],
            state["solarpanelvoltage"], state["solarpanelcurrent"], state["auxa"], batteryCharge, state["messageid"],
            batteryPower, loadPower, solarPower, myTEST, myTESTDescription)
            query = "INSERT INTO TB433MHZ (%s) VALUES(%s )" % (fields, values)
            # print("query=", query)
            cur.execute(query)
            con.commit()
        except mdb.Error as e:
            traceback.print_exc()
            print("Error %d: %s" % (e.args[0], e.args[1]))
            con.rollback()
            # sys.exit(1)

        finally:
            cur.close()
            con.close()

            del cur
            del con

    return


def processWeatherSenseAQI(sLine):
    # weathersense protocol 15
    state = json.loads(sLine)
    myProtocol = state['weathersenseprotocol']
    if (config.SWDEBUG):
        sys.stdout.write("processing AQI Data\n")
        sys.stdout.write('This is the raw data: ' + sLine + '\n')

    if (config.enable_MQTT == True):
        mqtt_publish_single(sLine, "WSAQI")

    if (config.enable_MySQL_Logging == True):
        # open mysql database
        # write log
        # commit
        # close
        try:
            myTEST = ""
            myTESTDescription = ""

            con = mdb.connect(
                config.MySQL_Host,
                config.MySQL_User,
                config.MySQL_Password,
                config.MySQL_Schema
            )

            cur = con.cursor()
            batteryPower =  float(state["batterycurrent"])* float(state["batteryvoltage"])
            loadPower  =  float(state["loadcurrent"])* float(state["loadvoltage"])
            solarPower =  float(state["solarpanelcurrent"])* float(state["solarpanelvoltage"])
            batteryCharge = util.returnPercentLeftInBattery(state["batteryvoltage"], 4.2)
            
            # calculate AQI 24 Hour
            timeDelta = datetime.timedelta(days=1)
            now = datetime.datetime.now()
            before = now - timeDelta
            before = before.strftime('%Y-%m-%d %H:%M:%S')
            query = "SELECT AQI, TimeStamp FROM AQI433MHZ WHERE (TimeStamp > '%s') ORDER BY TimeStamp " % (before)

            cur.execute(query)
            myAQIRecords = cur.fetchall()
            myAQITotal = 0.0
            if (len(myAQIRecords) > 0):
                for i in range(0, len(myAQIRecords)):
                    myAQITotal = myAQITotal + myAQIRecords[i][0]

                AQI24Hour = (myAQITotal + float(state['AQI'])) / (len(myAQIRecords) + 1)
            else:
                AQI24Hour = 0.0
            # HOTFIX for AQI problem from the wireless AQI sensor
            # recalculate AQI from RAW values and write in database

            myaqi = aqi.to_aqi([
                (aqi.POLLUTANT_PM25, state['PM2.5A']),
                (aqi.POLLUTANT_PM10, state['PM10A'])
                ])
            if (myaqi > 500):
                myaqi = 500
            #print("myaqi=", myaqi)
            state['AQI'] = myaqi

            fields = "deviceid, protocolversion, softwareversion, weathersenseprotocol, PM1_0S, PM2_5S, PM10S, PM1_0A, PM2_5A, PM10A, AQI, AQI24Hour, batteryvoltage, batterycurrent, loadvoltage, loadcurrent, solarvoltage, solarcurrent, auxa, batterycharge, messageID, batterypower, loadpower, solarpower, test, testdescription"
            values = "%d, %d, %d, %d, %d, %d, %d, %d, %d,%d, %d, %6.2f,%6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f,%6.2f,%6.2f,%d,%6.2f, %6.2f, %6.2f,\'%s\', \'%s\'" % (
            state["deviceid"], state["protocolversion"], state["softwareversion"], state["weathersenseprotocol"],
            state['PM1.0S'], state['PM2.5S'], state['PM10S'], state['PM1.0A'], state['PM2.5A'], state['PM10S'],
            state['AQI'], AQI24Hour,
            state["batteryvoltage"], state["batterycurrent"], state["loadvoltage"], state["loadcurrent"],
            state["solarpanelvoltage"], state["solarpanelcurrent"], state["auxa"], batteryCharge, state["messageid"],
            batteryPower, loadPower, solarPower, myTEST, myTESTDescription)
            query = "INSERT INTO AQI433MHZ (%s) VALUES(%s )" % (fields, values)
            cur.execute(query)
            con.commit()
        except mdb.Error as e:
            traceback.print_exc()
            print("Error %d: %s" % (e.args[0], e.args[1]))
            con.rollback()
            # sys.exit(1)

        finally:
            cur.close()
            con.close()

            del cur
            del con

    return


def processSolarMAX(sLine):
    state = json.loads(sLine)
    if (config.SWDEBUG):
        sys.stdout.write("processing SolarMAX Data\n")
        sys.stdout.write('This is the raw data: ' + sLine + '\n')

    # only accept SolarMAX Protocols (8,10,11)
    myProtocol = state['weathersenseprotocol']
    if ((myProtocol == 8) or (myProtocol == 10) or (myProtocol == 11)):

        if (config.enable_MQTT == True):
            mqtt_publish_single(sLine, "WSSolarMAX")

        if (config.enable_MySQL_Logging == True):
            # open mysql database
            # write log
            # commit
            # close
            try:
                myTEST = ""
                myTESTDescription = ""

                con = mdb.connect(
                    config.MySQL_Host,
                    config.MySQL_User,
                    config.MySQL_Password,
                    config.MySQL_Schema
                )

                cur = con.cursor()
                batteryPower =  float(state["batterycurrent"])* float(state["batteryvoltage"])
                loadPower  =  float(state["loadcurrent"])* float(state["loadvoltage"])
                solarPower =  float(state["solarpanelcurrent"])* float(state["solarpanelvoltage"])
                batteryCharge = util.returnPercentLeftInBattery(state["batteryvoltage"], 13.2)

                fields = "deviceid, protocolversion, softwareversion, weathersenseprotocol, batteryvoltage, batterycurrent, loadvoltage, loadcurrent, solarvoltage, solarcurrent, auxa, internaltemperature,internalhumidity, batterycharge, messageID, batterypower, loadpower, solarpower, test, testdescription"
                values = "%d, %d, %d, %d, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f,%6.2f,%6.2f,%d,%6.2f, %6.2f, %6.2f,\'%s\', \'%s\'" % (
                state["deviceid"], state["protocolversion"], state["softwareversion"], state["weathersenseprotocol"],
                state["batteryvoltage"], state["batterycurrent"], state["loadvoltage"], state["loadcurrent"],
                state["solarpanelvoltage"], state["solarpanelcurrent"], state["auxa"], state["internaltemperature"],
                state["internalhumidity"], batteryCharge, state["messageid"], batteryPower, loadPower, solarPower,
                myTEST, myTESTDescription)
                query = "INSERT INTO SolarMax433MHZ (%s) VALUES(%s )" % (fields, values)
                cur.execute(query)
                con.commit()
            except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0], e.args[1]))
                con.rollback()
                # sys.exit(1)

            finally:
                cur.close()
                con.close()

                del cur
                del con

    return


# main read 433HMz Sensor Loop
def readSensors():
    print("")
    print("######")
    print("Read Wireless Sensors")
    print("######")
    #   Create our sub-process...
    #   Note that we need to either ignore output from STDERR or merge it with STDOUT due to a limitation/bug somewhere under the covers of "subprocess"
    #   > this took awhile to figure out a reliable approach for handling it...

    p = Popen(cmd, stdout=PIPE, stderr=STDOUT, bufsize=1, close_fds=ON_POSIX)
    q = Queue()

    t = Thread(target=enqueue_output, args=('stdout', p.stdout, q))

    t.daemon = True  # thread dies with the program
    t.start()

    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    pulse = 0
    print("starting 433MHz scanning")
    print("######")
    # last timestamp for WeatherRack3 to remove duplicates
    lastWeatherRack3TimeStamp = ""
    WeatherRack3Count = 0
    lastWeatherRack3PowerTimeStamp = ""
    WeatherRack3PowerCount = 0
    # last timestamp for FT020T to remove duplicates
    lastFT020TTimeStamp = ""
    FT020Count = 0
    IndoorReadingCountArray = [0, 0, 0, 0, 0, 0, 0, 0]
    # temp value
    #config.SWDEBUG = False

    while True:
        #   Other processing can occur here as needed...
        # sys.stdout.write('Made it to processing step. \n')
        
        try:
            src, line = q.get(timeout=1)
            # print(line.decode())
        except Empty:
            pulse += 1
        else:  # got line
            pulse -= 1
            sLine = line.decode()
            #   See if the data is something we need to act on...

            if (sLine.find('F007TH') != -1) or (sLine.find('FT0300') != -1) or (sLine.find('F016TH') != -1) or (
                    sLine.find('FT020T') != -1):

                if ((sLine.find('F007TH') != -1) or (sLine.find('F016TH') != -1)):
                    processF016TH(sLine, IndoorReadingCountArray)
                if ((sLine.find('FT0300') != -1) or (sLine.find('FT020T') != -1)):
                    lastFT020TTimeStamp = processFT020T(sLine, lastFT020TTimeStamp, FT020Count)
                    FT020Count = FT020Count + 1

            if (sLine.find('SolarMAX') != -1):
                processSolarMAX(sLine)

            if (sLine.find('AQI') != -1):
                processWeatherSenseAQI(sLine)

            if (sLine.find('TB') != -1):
                processWeatherSenseTB(sLine)

            if (sLine.find('Generic') != -1):
                processWeatherSenseGeneric(sLine)

            if (sLine.find('AfterShock') != -1):
                processWeatherSenseAfterShock(sLine)

            if (sLine.find('Radiation') != -1):
                processWeatherSenseRadiation(sLine)

            if (sLine.find('WeatherRack3') != -1):
                processWeatherRack3(sLine, lastWeatherRack3TimeStamp, WeatherRack3Count)
                WeatherRack3Count = WeatherRack3Count + 1

            if (sLine.find('WR3 Power') != -1):
                processWeatherRack3Power(sLine, lastWeatherRack3PowerTimeStamp, WeatherRack3PowerCount)
                WeatherRack3PowerCount = WeatherRack3PowerCount + 1

        sys.stdout.flush()




