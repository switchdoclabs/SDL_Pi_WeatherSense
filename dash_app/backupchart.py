import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import MySQLdb as mdb
import datetime

import plotly.graph_objs as go
from dash.dependencies import Input, Output, MATCH, ALL, State





def build_graphAQI_figure():
    con = mdb.connect('localhost', 'root', 'password', 'WeatherSenseWireless');
    #last 7 days 
    timeDelta = datetime.timedelta(days=7)
    now = datetime.datetime.now()
    before = now - timeDelta
    before = before.strftime('%Y-%m-%d %H:%M:%S')
    
    
    query = "SELECT timestamp, AQI FROM AQI433MHZ WHERE (TimeStamp > '%s') ORDER BY timestamp"% (before) 
    df = pd.read_sql(query, con )
    trace1 = go.Scatter(x=df.timestamp, y=df.AQI, name='AQI')

    figure={
    'data': [trace1 ],
    'layout':
    go.Layout(title='WeatherSense AQI') }
    con.close()

    return figure

def build_graph1_figure():
    con = mdb.connect('localhost', 'root', 'password', 'WeatherSenseWireless');
    #last 7 days 
    timeDelta = datetime.timedelta(days=7)
    now = datetime.datetime.now()
    before = now - timeDelta
    before = before.strftime('%Y-%m-%d %H:%M:%S')
    
    
    query = "SELECT timestamp, solarvoltage, batteryvoltage, loadvoltage, batterycurrent, solarcurrent, loadcurrent, auxa FROM AQI433MHZ WHERE (TimeStamp > '%s') AND (deviceid = '1') ORDER BY timestamp"% (before) 
    df = pd.read_sql(query, con )
    trace1 = go.Scatter(x=df.timestamp, y=df.batteryvoltage, name='battery voltage')
    trace2 = go.Scatter(x=df.timestamp, y=df.solarvoltage, name='solar voltage')
    trace3 = go.Scatter(x=df.timestamp, y=df.loadvoltage, name='load voltage')
    trace4 = go.Scatter(x=df.timestamp, y=df.auxa, name='Aux State')

    figure={
    'data': [trace1, trace2, trace3, trace4],
    'layout':
    go.Layout(title='WeatherSenseAQI Solar Voltages') }
    con.close()

    return figure

def build_graph2_figure():
    con = mdb.connect('localhost', 'root', 'password', 'WeatherSenseWireless');
    #last 7 days 
    timeDelta = datetime.timedelta(days=7)
    now = datetime.datetime.now()
    before = now - timeDelta
    before = before.strftime('%Y-%m-%d %H:%M:%S')
    
    query = "SELECT timestamp, solarvoltage, batteryvoltage, loadvoltage, batterycurrent, solarcurrent, loadcurrent, auxa FROM AQI433MHZ WHERE (TimeStamp > '%s') AND (deviceid = '1') ORDER BY timestamp"% (before) 
    df = pd.read_sql(query, con )
    trace1c = go.Scatter(x=df.timestamp, y=df.batterycurrent, name='battery current')
    trace2c = go.Scatter(x=df.timestamp, y=df.solarcurrent, name='solar current')
    trace3c = go.Scatter(x=df.timestamp, y=df.loadcurrent, name='load current')
    figure={
    'data': [trace1c, trace2c, trace3c],
    'layout':
    go.Layout(title='WeatherSenseAQI Currents') }

    con.close()

    return figure

def build_graph3_figure():
    con = mdb.connect('localhost', 'root', 'password', 'WeatherSenseWireless');
    dfSW = pd.read_sql("SELECT timestamp, solarvoltage, batteryvoltage, loadvoltage, batterycurrent, solarcurrent, loadcurrent, auxa FROM SolarMax433MHZ WHERE deviceid = '1'", con )
    SWtrace1 = go.Scatter(x=dfSW.timestamp, y=dfSW.batteryvoltage, name='battery voltage')
    SWtrace2 = go.Scatter(x=dfSW.timestamp, y=dfSW.solarvoltage, name='solar voltage')
    SWtrace3 = go.Scatter(x=dfSW.timestamp, y=dfSW.loadvoltage, name='load voltage')
    SWtrace4 = go.Scatter(x=dfSW.timestamp, y=dfSW.auxa, name='Aux State')
    figure={
    'data': [SWtrace1, SWtrace2, SWtrace3, SWtrace4],
    'layout':
    go.Layout(title='ID 1 Solar Max Voltages') }
    con.close()

    return figure

def build_graph4_figure():
    con = mdb.connect('localhost', 'root', 'password', 'WeatherSenseWireless');
    dfSW = pd.read_sql("SELECT timestamp, solarvoltage, batteryvoltage, loadvoltage, batterycurrent, solarcurrent, loadcurrent, auxa FROM SolarMax433MHZ WHERE deviceid = '1'", con )
    SWtrace1c = go.Scatter(x=dfSW.timestamp, y=dfSW.batterycurrent, name='battery current')
    SWtrace2c = go.Scatter(x=dfSW.timestamp, y=dfSW.solarcurrent, name='solar current')
    SWtrace3c = go.Scatter(x=dfSW.timestamp, y=dfSW.loadcurrent, name='load current')
    figure={
    'data': [SWtrace1c, SWtrace2c, SWtrace3c] ,
    'layout':
    go.Layout(title='ID 1 Solar Max Currents') }
    con.close()

    return figure

def build_graph5_figure():
    con = mdb.connect('localhost', 'root', 'password', 'WeatherSenseWireless');
    #last 48 hours 
    timeDelta = datetime.timedelta(hours=48)
    now = datetime.datetime.now()
    before = now - timeDelta
    before = before.strftime('%Y-%m-%d %H:%M:%S')
    query = "SELECT timestamp, solarvoltage, batteryvoltage, loadvoltage, batterycurrent, solarcurrent, loadcurrent, auxa FROM SolarMax433MHZ WHERE (TimeStamp > '%s') AND (deviceid= '2') ORDER BY timestamp"% (before) 
    dfSW = pd.read_sql(query, con )
    SWtrace1 = go.Scatter(x=dfSW.timestamp, y=dfSW.batteryvoltage, name='battery voltage')
    SWtrace2 = go.Scatter(x=dfSW.timestamp, y=dfSW.solarvoltage, name='solar voltage')
    SWtrace3 = go.Scatter(x=dfSW.timestamp, y=dfSW.loadvoltage, name='load voltage')
    SWtrace4 = go.Scatter(x=dfSW.timestamp, y=dfSW.auxa, name='Aux State')
    figure={
    'data': [SWtrace1, SWtrace2, SWtrace3, SWtrace4],
    'layout':
    go.Layout(title='ID #2 Solar Max Voltages 48 Hours') }
    con.close()

    return figure
def build_graph6_figure():
    con = mdb.connect('localhost', 'root', 'password', 'WeatherSenseWireless');
    #last 8 hours 
    timeDelta = datetime.timedelta(hours=48)
    now = datetime.datetime.now()
    before = now - timeDelta
    before = before.strftime('%Y-%m-%d %H:%M:%S')
    query = "SELECT timestamp, solarvoltage, batteryvoltage, loadvoltage, batterycurrent, solarcurrent, loadcurrent, auxa FROM SolarMax433MHZ WHERE (TimeStamp > '%s') AND (deviceid = '2') ORDER BY timestamp"% (before) 
    dfSW = pd.read_sql(query, con )
    SWtrace1c = go.Scatter(x=dfSW.timestamp, y=dfSW.batterycurrent, name='battery current')
    SWtrace2c = go.Scatter(x=dfSW.timestamp, y=dfSW.solarcurrent, name='solar current')
    SWtrace3c = go.Scatter(x=dfSW.timestamp, y=dfSW.loadcurrent, name='load current')
    figure={
    'data': [SWtrace1c, SWtrace2c, SWtrace3c],
    'layout':
    go.Layout(title='ID #2 Solar Max Currents 48 Hours') }
    con.close()

    return figure

def AQIPage():

    layout = html.Div(children=[

    html.H1("AQI Charts", style={'textAlign': 'center'}),
    
    dcc.Graph(
    id={'type' : 'graph', 'index' : "1"},
    figure = build_graphAQI_figure(),
    ),

     html.H1("433MHz Charts", style={'textAlign': 'center'}),
    dcc.Graph(
    id={'type' : 'graph', 'index' : "3"},
    figure = build_graph3_figure(),
    ),

    dcc.Graph(
    id={'type' : 'graph', 'index' : "4"},
    figure = build_graph4_figure(),
    ) ,
    dcc.Graph(
    id={'type' : 'graph', 'index' : "5"},
    figure = build_graph5_figure(),
    ) ,
    dcc.Graph(
    id={'type' : 'graph', 'index' : "6"},
    figure = build_graph6_figure(),
    ) ,
    html.H1("WeatherSenseAQI Charts", style={'textAlign': 'center'}),
    
    dcc.Graph(
    id={'type' : 'graph', 'index' : "7"},
    figure = build_graph1_figure(),
    ),

    dcc.Graph(
    id={'type' : 'graph', 'index' : "8"},
    figure = build_graph2_figure(),
    ) ,

    dcc.Interval(
            id='interval-component',
            interval=10*1000, # in milliseconds
            n_intervals=0
        ),

    ], className="container" )


# callbacks

@app.callback(
	      [
	      Output({'type' : 'graph', 'index' : MATCH}, 'figure' ),
              ],
              [Input('interval-component','n_intervals'),
              Input({'type' : 'graph', 'index' : MATCH}, 'id' )],
              [State({'type' : 'graph', 'index' : MATCH}, 'value'  )]
              )

def update_metrics(n_intervals, id, value):
    print("n_intervals=", n_intervals)
    myIndex = id['index']
    # build figures
    if (myIndex == '1'):
        print("GraphAQI figure")
        figure = build_graphAQI_figure()
    if (myIndex == '2'):
        print("GraphAQI Solar Currents")
        figure = build_graph3_figure()
    if (myIndex == '3'):
        print("GraphAQI Solar Voltages")
        figure = build_graph4_figure()



    return [figure]

