#
# wireless sensor routines


import config

import json
import random

import sys
from subprocess import PIPE, Popen, STDOUT
from threading  import Thread
import datetime
import MySQLdb as mdb
import traceback
import state

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------

cmd = [ '/usr/local/bin/rtl_433', '-q', '-F', 'json', '-R', '146', '-R','147', '-R', '148','-R', '150', '-R', '151']

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
#   A few helper functions...

def nowStr():
    return( datetime.datetime.now().strftime( '%Y-%m-%d %H:%M:%S'))

#stripped = lambda s: "".join(i for i in s if 31 < ord(i) < 127)


#   We're using a queue to capture output as it occurs
try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x
ON_POSIX = 'posix' in sys.builtin_module_names

def enqueue_output(src, out, queue):
    for line in iter(out.readline, b''):
        queue.put(( src, line))
    out.close()

def randomadd(value, spread):

    return round(value+random.uniform(-spread, spread),2)


# process functions

def processF020(sLine):

    return


# processes Inside Temperature and Humidity
def processF016TH(sLine):
    return

def processWeatherSenseTB(sLine):
    # weathersense protocol 16
    state = json.loads(sLine)
    myProtocol = state['weathersenseprotocol']
    print("weathersenseprotocol=", myProtocol)
    
    if (config.enable_MySQL_Logging == True):	
	    # open mysql database
	    # write log
	    # commit
	    # close
        try:
                myTEST = ""
                myTESTDescription = ""
                print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'WeatherSenseWireless');
                cur = con.cursor()
                batteryPower = 0.0
                loadPower = 0.0
                solarPower = 0.0
                batteryCharge = 0.0
                

                fields = "deviceid, protocolversion, softwareversion, weathersenseprotocol,irqsource, previousinterruptresult, lightninglastdistance, sparebyte, lightningcount, interruptcount,  batteryvoltage, batterycurrent, loadvoltage, loadcurrent, solarvoltage, solarcurrent, auxa, batterycharge, messageID, batterypower, loadpower, solarpower, test, testdescription"
                values = "%d, %d, %d, %d, %d, %d, %d, %d,%d, %d,%6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f,%6.2f,%6.2f,%d,%6.2f, %6.2f, %6.2f,\'%s\', \'%s\'" % (state["deviceid"], state["protocolversion"], state["softwareversion"], state["weathersenseprotocol"],state['irqsource'],state['previousinterruptresult'],state['lightninglastdistance'],state['sparebyte'],state['lightningcount'],state['interruptcount'],
                state["batteryvoltage"], state["batterycurrent"], state["loadvoltage"], state["loadcurrent"], state["solarpanelvoltage"], state["solarpanelcurrent"], state["auxa"],batteryCharge, state["messageid"], batteryPower, loadPower, solarPower, myTEST, myTESTDescription )
                query = "INSERT INTO TB433MHZ (%s) VALUES(%s )" % (fields, values)
                print("query=", query)
                cur.execute(query)
                con.commit()
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

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
    print("weathersenseprotocol=", myProtocol)
    
    if (config.enable_MySQL_Logging == True):	
	    # open mysql database
	    # write log
	    # commit
	    # close
        try:
                myTEST = ""
                myTESTDescription = ""
                print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'WeatherSenseWireless');
                cur = con.cursor()
                batteryPower = 0.0
                loadPower = 0.0
                solarPower = 0.0
                batteryCharge = 0.0
                

                fields = "deviceid, protocolversion, softwareversion, weathersenseprotocol, PM1_0S, PM2_5S, PM10S, PM1_0A, PM2_5A, PM10A, AQI, batteryvoltage, batterycurrent, loadvoltage, loadcurrent, solarvoltage, solarcurrent, auxa, batterycharge, messageID, batterypower, loadpower, solarpower, test, testdescription"
                values = "%d, %d, %d, %d, %d, %d, %d, %d, %d,%d, %d,%6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f,%6.2f,%6.2f,%d,%6.2f, %6.2f, %6.2f,\'%s\', \'%s\'" % (state["deviceid"], state["protocolversion"], state["softwareversion"], state["weathersenseprotocol"],state['PM1.0S'],state['PM2.5S'],state['PM10S'],state['PM1.0A'],state['PM2.5A'],state['PM10S'],state['AQI'], 
                state["batteryvoltage"], state["batterycurrent"], state["loadvoltage"], state["loadcurrent"], state["solarpanelvoltage"], state["solarpanelcurrent"], state["auxa"],batteryCharge, state["messageid"], batteryPower, loadPower, solarPower, myTEST, myTESTDescription )
                query = "INSERT INTO AQI433MHZ (%s) VALUES(%s )" % (fields, values)
                print("query=", query)
                cur.execute(query)
                con.commit()
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()

                del cur
                del con

    return

def processSolarMAX(sLine):

 state = json.loads(sLine)

 # only accept SolarMAX Protocols (8,10,11)
 print("state=", state)
 myProtocol = state['weathersenseprotocol']
 print("weathersenseprotocol=", myProtocol)
 if ((myProtocol == 8) or (myProtocol == 10) or (myProtocol == 11)):
   if (config.enable_MySQL_Logging == True):	
	    # open mysql database
	    # write log
	    # commit
	    # close
        try:
                myTEST = ""
                myTESTDescription = ""
                print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'WeatherSenseWireless');
                cur = con.cursor()
                batteryPower = 0.0
                loadPower = 0.0
                solarPower = 0.0
                batteryCharge = 0.0
                

                fields = "deviceid, protocolversion, softwareversion, weathersenseprotocol, batteryvoltage, batterycurrent, loadvoltage, loadcurrent, solarvoltage, solarcurrent, auxa, internaltemperature,internalhumidity, batterycharge, messageID, batterypower, loadpower, solarpower, test, testdescription"
                values = "%d, %d, %d, %d, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f,%6.2f,%6.2f,%d,%6.2f, %6.2f, %6.2f,\'%s\', \'%s\'" % (state["deviceid"], state["protocolversion"], state["softwareversion"], state["weathersenseprotocol"], state["batteryvoltage"], state["batterycurrent"], state["loadvoltage"], state["loadcurrent"], state["solarpanelvoltage"], state["solarpanelcurrent"], state["auxa"],state["internaltemperature"], state["internalhumidity"], batteryCharge, state["messageid"], batteryPower, loadPower, solarPower, myTEST, myTESTDescription )
                query = "INSERT INTO SolarMax433MHZ (%s) VALUES(%s )" % (fields, values)
                print("query=", query)
                cur.execute(query)
                con.commit()
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

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

    p = Popen( cmd, stdout=PIPE, stderr=STDOUT, bufsize=1, close_fds=ON_POSIX)
    q = Queue()

    t = Thread(target=enqueue_output, args=('stdout', p.stdout, q))
    
    t.daemon = True # thread dies with the program
    t.start()

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    pulse = 0
    print("starting 433MHz scanning")
    print("######")

    while True:
        #   Other processing can occur here as needed...
        #sys.stdout.write('Made it to processing step. \n')



        try:
            src, line = q.get(timeout = 1)
            print(line.decode())
        except Empty:
            pulse += 1
        else: # got line
            pulse -= 1
            sLine = line.decode()
            #   See if the data is something we need to act on...

            if ( sLine.find('F007TH') != -1) or ( sLine.find('FT0300') != -1) or ( sLine.find('F016TH') != -1) or ( sLine.find('FT020T') != -1):
                
                if (( sLine.find('F007TH') != -1) or ( sLine.find('F016TH') != -1)): 
                    processF016TH(sLine)
                if (( sLine.find('FT0300') != -1) or ( sLine.find('FT020T') != -1)): 
                    processF020(sLine)

            if (sLine.find('SolarMAX') != -1):
                processSolarMAX(sLine)

            if (sLine.find('AQI') != -1):
                processWeatherSenseAQI(sLine)

            if (sLine.find('TB') != -1):
                processWeatherSenseTB(sLine)

        sys.stdout.flush()

