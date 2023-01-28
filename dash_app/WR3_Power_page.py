# import os
import sys
# import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import MySQLdb as mdb
import datetime

import plotly.graph_objs as go

# build the path to import config.py from the parent directory
sys.path.append('../')
import config

# from dash.dependencies import Input, Output, MATCH, ALL, State

# WeatherRack3 solar power system currents
WR3ID = 0

def build_graph1_figure():
    con = mdb.connect(
        config.MySQL_Host,
        config.MySQL_User,
        config.MySQL_Password,
        config.MySQL_Schema
    )
    # get device ID (Last reporting)
    
    query = "SELECT SerialNumber FROM WeatherRack3Power ORDER BY timestamp LIMIT 1" 

    df = pd.read_sql(query, con)
    WR3ID = df.SerialNumber
    WR3ID = WR3ID[0]
    print("WR3ID=", WR3ID)
    # last 7 days
    timeDelta = datetime.timedelta(days=7)
    now = datetime.datetime.now()
    before = now - timeDelta
    before = before.strftime('%Y-%m-%d %H:%M:%S')

    nowTime = now.strftime('%Y-%m-%d %H:%M:%S')

    #query = "SELECT timestamp, SolarPanelVoltage, BatteryVoltage, LoadVoltage, BatteryCurrent, SolarPanelCurrent, LoadCurrent, AuxA FROM WeatherRack3Power WHERE (TimeStamp > '%s') AND (deviceid = %d ) ORDER BY timestamp" % (
    #     before, WR3ID)
    query = "SELECT timestamp, SolarPanelVoltage, BatteryVoltage, LoadVoltage, BatteryCurrent, SolarPanelCurrent, LoadCurrent, AuxA FROM WeatherRack3Power WHERE (TimeStamp > '%s') ORDER BY timestamp" % (
         before)
    # print("query=", query)
    df = pd.read_sql(query, con)

    trace1 = go.Scatter(x=df.timestamp, y=df.BatteryVoltage, name='battery voltage')
    trace2 = go.Scatter(x=df.timestamp, y=df.SolarPanelVoltage, name='solar voltage')
    trace3 = go.Scatter(x=df.timestamp, y=df.LoadVoltage, name='load voltage')

    figure = {
        'data': [trace1, trace2, trace3 ],
        'layout':
            go.Layout(title=' WeatherRack3 Solar Voltages', xaxis_title="ID=0x%X Updated at: "%WR3ID + nowTime, yaxis_title="Voltage (V)")
            
            }
    con.close()

    #figure.update_yaxes(title_text="<b>primary</b> yaxis title (V)", secondary_y=False)
    return figure


def build_graph3_figure():
    con = mdb.connect(
        config.MySQL_Host,
        config.MySQL_User,
        config.MySQL_Password,
        config.MySQL_Schema
    )

    # get device ID (Last reporting)
 
    query = "SELECT SerialNumber FROM WeatherRack3Power ORDER BY timestamp LIMIT 1" 

    df = pd.read_sql(query, con)
    WR3ID = df.SerialNumber
    WR3ID = WR3ID[0]
    # last 7 days
    timeDelta = datetime.timedelta(days=7)
    now = datetime.datetime.now()
    before = now - timeDelta
    before = before.strftime('%Y-%m-%d %H:%M:%S')

    nowTime = now.strftime('%Y-%m-%d %H:%M:%S')

    query = "SELECT timestamp, BatteryCapacity, SolarPanelVoltage, BatteryVoltage, LoadVoltage, BatteryCurrent, SolarPanelCurrent, LoadCurrent, AuxA FROM WeatherRack3Power WHERE (TimeStamp > '%s') ORDER BY timestamp" % (
        before)
    #query = "SELECT timestamp, SolarPanelVoltage, BatteryVoltage, LoadVoltage, BatteryCurrent, SolarPanelCurrent, LoadCurrent, AuxA FROM WeatherRack3Power WHERE (TimeStamp > '%s') AND (deviceid = %d) ORDER BY timestamp" % (
    #    before, WR3ID)
    df = pd.read_sql(query, con)
    trace1c = go.Scatter(x=df.timestamp, y=df.BatteryCapacity, name='battery capacity')
    figure = {
        'data': [trace1c ],
        'layout':
            go.Layout(title='WeatherRack3 Battery Capacity', xaxis_title="ID=0x%X Updated at: "%WR3ID + nowTime, yaxis_title="%",yaxis_range=[0,100])
            }

    con.close()

    return figure



def build_graph2_figure():
    con = mdb.connect(
        config.MySQL_Host,
        config.MySQL_User,
        config.MySQL_Password,
        config.MySQL_Schema
    )

    # get device ID (Last reporting)
 
    query = "SELECT SerialNumber FROM WeatherRack3Power ORDER BY timestamp LIMIT 1" 

    df = pd.read_sql(query, con)
    WR3ID = df.SerialNumber
    WR3ID = WR3ID[0]
    # last 7 days
    timeDelta = datetime.timedelta(days=7)
    now = datetime.datetime.now()
    before = now - timeDelta
    before = before.strftime('%Y-%m-%d %H:%M:%S')

    nowTime = now.strftime('%Y-%m-%d %H:%M:%S')

    query = "SELECT timestamp, SolarPanelVoltage, BatteryVoltage, LoadVoltage, BatteryCurrent, SolarPanelCurrent, LoadCurrent, AuxA FROM WeatherRack3Power WHERE (TimeStamp > '%s') ORDER BY timestamp" % (
        before)
    #query = "SELECT timestamp, SolarPanelVoltage, BatteryVoltage, LoadVoltage, BatteryCurrent, SolarPanelCurrent, LoadCurrent, AuxA FROM WeatherRack3Power WHERE (TimeStamp > '%s') AND (deviceid = %d) ORDER BY timestamp" % (
    #    before, WR3ID)
    df = pd.read_sql(query, con)
    trace1c = go.Scatter(x=df.timestamp, y=df.BatteryCurrent, name='battery current')
    trace2c = go.Scatter(x=df.timestamp, y=df.SolarPanelCurrent, name='solar current')
    trace3c = go.Scatter(x=df.timestamp, y=df.LoadCurrent, name='load current')
    figure = {
        'data': [trace1c, trace2c, trace3c],
        'layout':
            go.Layout(title='WeatherRack3 Battery Capacity', xaxis_title="ID=0x%X Updated at: "%WR3ID + nowTime, yaxis_title="Current (A)") 
            }

    con.close()

    return figure


def WR3PowerPage():
    layout = html.Div(children=[

        html.H1("WeatherRack3 Solar Power Charts", style={'textAlign': 'center'}),

        dcc.Graph(
            id={'type': 'WR3SolarMAXgraph', 'index': "4"},
            figure=build_graph3_figure(),
        ),

        dcc.Graph(
            id={'type': 'WR3SolarMAXgraph', 'index': "2"},
            figure=build_graph1_figure(),
        ),

        dcc.Graph(
            id={'type': 'WR3SolarMAXgraph', 'index': "3"},
            figure=build_graph2_figure(),
        ),

    ], className="container")

    return layout
