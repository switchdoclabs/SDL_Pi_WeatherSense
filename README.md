SwitchDoc Labs WeatherSense Open Source Protocol Monitor

For webupdate<BR>

pip install SafecastPy



Program monitors the SwitchDoc Labs SDR on Pi for all WeatherSense instruments and records to database

And publishes to MQTT topic "weathersense/#"


Version V017 December 10,2022 - WeatherRack3 Added<BR>
Version V016 April 30,2022 - local updateWeb Logic Added<BR>
Version V015 April 16,2022 - WR2 Light update and database<BR>
Version V014 April 11,2022 - Added fixSkyCamRemote.py for setting MQTT addresses<BR>
Version V013 March 23,2022 - Added Radiation Detector Support<BR>


Before starting V008 or greater, do: <BR>
sudo pip3 install python-aqi<BR>
sudo pip3 install ffmpeg<BR>

<BR>
if you are updating from an older database version do the following:
<pre>
sudo mysql -u root -p WeatherSenseWireless < updateWeatherSenseWireless.sql
</pre>

Version V012 August 23,2021 - Check for Database existance<BR>
Version V011 August 22,2021 - TimeLapse Error Fix<BR>
Version V010 August 21,2021 - Lightning Formatting<BR>
Version V009 August 13,2021 - Fix for TimeLapse date sorting<BR>
Version V008 August 2,2021 - Fix for AQI Values from Solar AQI<BR>
Version V007 August 2,2021 - Fix for Timelapse display<BR>
Version V006 August 1,2021 - Added SkyCam Solar support and Timelapses<BR>
Version V005 June 9,2021 - Fixed Lightning Typos <BR>
Version V004 June 2021 - Finished AfterShock Support. Y Axis labels. <BR>
Version V003 April 2021 - Added AfterShock Support.  Fixed timestamps<BR>


--------------------<BR>
config.py contains all the support information<BR>
Supports:<BR>

- WeatherSense WeatherRack2<BR>
- WeatherSense Indoor T/H Sensor<BR>
- WeatherSense Lightning Detector<BR>
- WeatherSense Air Quality Index<BR>
- SolarMAX2 Solar Panel System<BR>
- AfterShock Earthquake Detector System<BR>
- WeatherSense SkyCam <BR>
- WeatherSense Radiation Detector <BR>

Supporting in the future:<BR>
- WeatherSense Generic <BR>

Previous Versions:

Version V002 March 2021 - Added Power calculations <BR
Version V001 February 2021<BR>

As always, we recommend using the 32GB SDL SDCard with all the software installed.<BR>

https://shop.switchdoc.com/products/16gb-sd-card-with-stretch-smart-garden-system-groveweatherpi<BR>

Installation:

You need to have the following SDL libraries installed: <BR>

<pre>
cd
git clone https://github.com/switchdoclabs/rtl_433
</pre>
Follow the install instructions.

And you need to install mariadb: <BR>
https://pimylifeup.com/raspberry-pi-mysql/

and

<pre>
sudo apt-get install python3-dev libmysqlclient-dev
sudo pip3 install mysqlclient
</pre>

Next:

<pre>
sudo mysql -u root -p < WeatherSenseWireless.sql
</pre>

Now to run:

<pre>
cd
cd SDL_Pi_WeatherSenseWireless
sudo python3 WeatherSenseMonitor.py

</pre>
and in a different windwow

<pre>
cd SDL_Pi_WeatherSenseWireless
cd dash_app
sudo python3 index.py 
</pre>


Then you can access the web pages on your Pi by:

http://localhost:8050/

Or on any computer in your local network:

http://<your IP Number>:8050/

Use "hostname -I" to your your Raspberry Pi IP Number.

Example:  http://192.168.1.32:8050/
