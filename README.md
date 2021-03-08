SwitchDoc Labs WeatherSense Open Source Protocol Monitor

Program monitors the SwitchDoc Labs SDR on Pi for all WeatherSense instruments and records to database

And publishes to MQTT topic "weathersense/#"

config.py contains all the support information

Supports:<BR>

- WeatherSense WeatherRack2<BR>
- WeatherSense Indoor T/H Sensor<BR>
- WeatherSense Lightning Detector<BR>
- WeatherSense Air Quality Index<BR>
- SolarMAX Solar Panel System<BR>

Supporting in the future:<BR>
- WeatherSense Generic <BR>
- WeatherSense Camera <BR>


Version 1.1 March 2021 - Added Power calculations <BR>
Version 1.0 February 2021<BR>

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
sudo -u root -p < WeatherSenseWireless.sql
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
