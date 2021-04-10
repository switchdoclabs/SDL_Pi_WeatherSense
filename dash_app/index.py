# import os
# import shutil
# import glob
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, MATCH, ALL, State
import dash_bootstrap_components as dbc
# import plotly.express as px
# import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
# import traceback
import datetime
# import base64

# import time

# import threading

from non_impl import NotImplPage

from navbar import Navbar, Logo

# pages

import solarmax_page
import weather_page
import indoorth
import aftershock_page
import aqi_page
import lightning_page

# import generic_page

# state of previous page
previousPathname = ""

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

# print("new navbar=")
nav = Navbar()
logo = Logo(app)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

# print("new navbar=")
nav = Navbar()
logo = Logo(app)

app.config.suppress_callback_exceptions = True

app.layout = html.Div(

    [

        html.Div(id='my-output-interval'),

        dcc.Interval(
            id='main-interval-component',
            interval=10 * 1000,  # in milliseconds - leave as 10 seconds
            n_intervals=0
        ),
        dcc.Interval(
            id='minute-interval-component',
            interval=60 * 1000,  # in milliseconds
            n_intervals=0
        ),
        dcc.Interval(
            id='minute15-interval-component',
            interval=15 * 60 * 1000,  # in milliseconds
            n_intervals=0
        ),

        # dbc.Spinner(id="main-spinner", color="white" ),
        # dcc.Location(id = 'url', refresh = True),
        dcc.Location(id='url', refresh=False),

        html.Div(id='page-content'),
        # html.Div(id = 'wp-placeholder', style={'display':'none'})
    ],

    id="mainpage"

)


@app.server.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    # r.headers["Cache-Control"] = 'no-store'
    # r.headers["Pragma"] = "no-store"
    # r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'must-revalidate, max-age=10'
    return r


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    global previousPathname

    # print("--------------------->>>>>>>>>>>>>>>>new page")
    now = datetime.datetime.now()
    nowString = now.strftime('%Y-%m-%d %H:%M:%S')
    # print("begin=",nowString)

    # print("pathname=", pathname)
    # print("previousPathname=", previousPathname)
    i = [i['prop_id'] for i in dash.callback_context.triggered]
    # print('i=', i)
    # print('TRIGGER(S):', [i['prop_id'] for i in dash.callback_context.triggered ])
    if (i[0] == '.'):
        # print("---no page change--- ['.']")
        raise PreventUpdate
    # if (pathname == previousPathname):
    #    print("---no page change---Equal Pathname")
    #    raise PreventUpdate
    previousPathname = pathname

    #myLayout = NotImplPage()
    myLayout = aqi_page.AQIPage() 
    myLayout2 = ""
    if pathname == '/weather_page':
        myLayout = weather_page.WeatherPage()
        myLayout2 = ""
    if pathname == '/indoorth_page':
        print("before IndoorTHPage")
        myLayout = indoorth.IndoorTHPage()
        # print("myLayout=")
        myLayout2 = ""
    if pathname == '/aqi_page':
        myLayout = aqi_page.AQIPage()
        myLayout2 = ""
    if pathname == '/aftershock_page':
        myLayout = aftershock_page.AfterShockPage()
        myLayout2 = ""
    if pathname == '/lightning_page':
        myLayout = lightning_page.LightningPage()
        myLayout2 = ""
    if pathname == '/solarmax_page':
        myLayout = solarmax_page.SolarMAXPage()
        myLayout2 = ""
    if pathname == '/generic_page':
        # myLayout = log_page.LogPage()
        myLayout2 = ""
    if pathname == '/status_page':
        # myLayout = log_page.LogPage()
        myLayout2 = ""

    # print("myLayout= ",myLayout)
    # print("myLayout2= ",myLayout2)
    # print("page-content= ",app.layout)
    now = datetime.datetime.now()
    nowString = now.strftime('%Y-%m-%d %H:%M:%S')
    # print("end=",nowString)
    return (logo, nav, myLayout, myLayout2)


############
# callbacks
############
# aftershock_page callbacks


@app.callback(
    [
        Output({'type': 'AfterShockgraph', 'index': MATCH}, 'figure'),
    ],
    [Input('minute-interval-component', 'n_intervals'),
     Input({'type': 'AfterShockgraph', 'index': MATCH}, 'id')],
    [State({'type': 'AfterShockgraph', 'index': MATCH}, 'value')]
)
def update_metrics(n_intervals, id, value):
    print("n_intervals=", n_intervals)
    myIndex = id['index']
    # build figures
    if (myIndex == '1'):
        print("GraphAfterShock figure")
        figure = aftershock_page.build_graphAfterShock_figure()
    if (myIndex == '2'):
        print("GraphAfterShock Solar Currents")
        figure = aftershock_page.build_graph1_figure()
    if (myIndex == '3'):
        print("GraphAfterShock Solar Voltages")
        figure = aftershock_page.build_graph2_figure()

    return [figure]


@app.callback(
    [
        Output({'type': 'ASdynamic', 'index': MATCH}, 'children'),
    ],
    [Input('main-interval-component', 'n_intervals'),
     Input({'type': 'ASdynamic', 'index': MATCH}, 'id')],
    [State({'type': 'ASdynamic', 'index': MATCH}, 'value')]
)
def updateAfterShockUpdate(n_intervals, id, value):
    if (True):
        # if ((n_intervals % (1*2)) == 0) or (n_intervals ==0): # 5 minutes -10 second timer

        # if ((n_intervals % (5*6)) == 0) or (n_intervals ==0): # 5 minutes -10 second timer
        print("--->>>updateAfterShockUpdate", datetime.datetime.now(), n_intervals)
        print("updateAfterShockUpdate n_intervals =", n_intervals, id['index'])
        if (id['index'] == "StringTime"):
            # weather_page.CWJSON = weather_page.generateCurrentWeatherJSON()
            # value = str(weather_page.CWJSON[id['index']]) +" "+ weather_page.CWJSON[id['index']+'Units']
            now = datetime.datetime.now()
            nowString = now.strftime('%Y-%m-%d %H:%M:%S')
            value = "AfterShock Updated at:" + nowString
            aftershock_page.updateAfterShockLines()

            return [value]

        value = aftershock_page.ASJSON[id['index']]
    else:
        raise PreventUpdate
    return [value]





# lightning_page callbacks


@app.callback(
    [
        Output({'type': 'Lightninggraph', 'index': MATCH}, 'figure'),
    ],
    [Input('minute-interval-component', 'n_intervals'),
     Input({'type': 'Lightninggraph', 'index': MATCH}, 'id')],
    [State({'type': 'Lightninggraph', 'index': MATCH}, 'value')]
)
def update_metrics(n_intervals, id, value):
    print("n_intervals=", n_intervals)
    myIndex = id['index']
    # build figures
    if (myIndex == '1'):
        print("GraphLightning figure")
        figure = lightning_page.build_graphLightning_figure()
    if (myIndex == '2'):
        print("GraphLightning Solar Currents")
        figure = lightning_page.build_graph1_figure()
    if (myIndex == '3'):
        print("GraphLightning Solar Voltages")
        figure = lightning_page.build_graph2_figure()

    return [figure]


@app.callback(
    [
        Output({'type': 'LPdynamic', 'index': MATCH}, 'children'),
    ],
    [Input('main-interval-component', 'n_intervals'),
     Input({'type': 'LPdynamic', 'index': MATCH}, 'id')],
    [State({'type': 'LPdynamic', 'index': MATCH}, 'value')]
)
def updateLightningUpdate(n_intervals, id, value):
    if (True):
        # if ((n_intervals % (1*2)) == 0) or (n_intervals ==0): # 5 minutes -10 second timer

        # if ((n_intervals % (5*6)) == 0) or (n_intervals ==0): # 5 minutes -10 second timer
        print("--->>>updateLightningUpdate", datetime.datetime.now(), n_intervals)
        print("updateLightningUpdate n_intervals =", n_intervals, id['index'])
        if (id['index'] == "StringTime"):
            # weather_page.CWJSON = weather_page.generateCurrentWeatherJSON()
            # value = str(weather_page.CWJSON[id['index']]) +" "+ weather_page.CWJSON[id['index']+'Units']
            now = datetime.datetime.now()
            nowString = now.strftime('%Y-%m-%d %H:%M:%S')
            value = "Lightning Updated at:" + nowString
            lightning_page.updateLightningLines()

            return [value]

        value = lightning_page.LLJSON[id['index']]
    else:
        raise PreventUpdate
    return [value]


# aqi_page callbacks

@app.callback(
    [
        Output({'type': 'AQIgraph', 'index': MATCH}, 'figure'),
    ],
    [Input('main-interval-component', 'n_intervals'),
     Input({'type': 'AQIgraph', 'index': MATCH}, 'id')],
    [State({'type': 'AQIgraph', 'index': MATCH}, 'value')]
)
def update_metrics(n_intervals, id, value):
    print("n_intervals=", n_intervals)
    myIndex = id['index']
    # build figures
    if (myIndex == '1'):
        print("GraphAQI figure")
        figure = aqi_page.build_graphAQI_figure()
    if (myIndex == '2'):
        print("GraphAQI Solar Currents")
        figure = aqi_page.build_graph1_figure()
    if (myIndex == '3'):
        print("GraphAQI Solar Voltages")
        figure = aqi_page.build_graph2_figure()

    return [figure]


# solarmax_page callbacks

@app.callback(
    [
        Output({'type': 'SolarMAXgraph', 'index': MATCH}, 'figure'),
    ],
    [Input('minute15-interval-component', 'n_intervals'),
     Input({'type': 'SolarMAXgraph', 'index': MATCH}, 'id')],
    [State({'type': 'SolarMAXgraph', 'index': MATCH}, 'value')]
)
def update_metrics(n_intervals, id, value):
    print("n_intervals=", n_intervals)
    myIndex = id['index']
    # build figures
    if (myIndex == '2'):
        print("SolarMAX Solar Currents")
        figure = solarmax_page.build_graph1_figure()
    if (myIndex == '3'):
        print("SolarMAX Solar Voltages")
        figure = solarmax_page.build_graph2_figure()

    return [figure]


# Indoor Temperature Humidity


@app.callback(
    [
        Output({'type': 'WPITHdynamic', 'index': MATCH}, 'figure'),
    ],
    [Input('minute-interval-component', 'n_intervals'),
     Input({'type': 'WPITHdynamic', 'index': MATCH}, 'id')],
    [State({'type': 'WPITHdynamic', 'index': MATCH}, 'value')]
)
def updateIndoorTHUpdate(n_intervals, id, value):
    # if ((n_intervals % (1*6)) == 0) or (n_intervals ==0): # 1 minutes -10 second timer
    # if ((n_intervals % (5*6)) == 0) or (n_intervals ==0): # 5 minutes -10 second timer
    # print("--->>>updateIndoorTHUpdate", datetime.datetime.now(), n_intervals)
    # print("updateIndoorTH  n_intervals =", n_intervals, id['index'])
    if (id['index'] == 'temperature'):
        timeDelta = datetime.timedelta(days=7)
        data = indoorth.generateTHData(timeDelta)
        fig = indoorth.buildTemperatureGraph(data)
        # print(fig)
        return [fig]
    if (id['index'] == 'humidity'):
        timeDelta = datetime.timedelta(days=7)
        data = indoorth.generateTHData(timeDelta)
        fig = indoorth.buildHumidityGraph(data)
        # print(fig)
        return [fig]


# else:
#    raise PreventUpdate
# return [figure]

# weather page callbacks


@app.callback(
    [
        Output({'type': 'WPdynamic', 'index': MATCH}, 'children'),
    ],
    [Input('main-interval-component', 'n_intervals'),
     Input({'type': 'WPdynamic', 'index': MATCH}, 'id')],
    [State({'type': 'WPdynamic', 'index': MATCH}, 'value')]
)
def updateWeatherUpdate(n_intervals, id, value):
    if ((n_intervals % (1 * 6)) == 0) or (n_intervals == 0):  # 5 minutes -10 second timer
        # if ((n_intervals % (5*6)) == 0) or (n_intervals ==0): # 5 minutes -10 second timer
        # print("--->>>updateWeatherUpdateString", datetime.datetime.now(), n_intervals)
        # print("updateWeatherUpdate n_intervals =", n_intervals, id['index'])
        if (id['index'] == "StringTime"):
            weather_page.CWJSON = weather_page.generateCurrentWeatherJSON()
            value = str(weather_page.CWJSON[id['index']]) + " " + weather_page.CWJSON[id['index'] + 'Units']
            value = "Weather Updated at:" + value

            return [value]

        value = str(weather_page.CWJSON[id['index']]) + " " + weather_page.CWJSON[id['index'] + 'Units']
    else:
        raise PreventUpdate
    return [value]


@app.callback(
    [
        Output({'type': 'WPRdynamic', 'index': MATCH}, 'figure'),
    ],
    [Input('main-interval-component', 'n_intervals'),
     Input({'type': 'WPRdynamic', 'index': MATCH}, 'id')],
    [State({'type': 'WPRdynamic', 'index': MATCH}, 'value')]
)
def updateWeatherRosePage(n_intervals, id, value):
    if (n_intervals == 0):  # stop first update
        raise PreventUpdate
    # print("WeatherRose n_intervals=", n_intervals)
    # update every 15 minutes
    # if (True): # 15 minutes -10 second timer
    if ((n_intervals % (15 * 6)) == 0):  # 15 minutes -10 second timer
        # print("--->>>updateCompassRose", datetime.datetime.now(), n_intervals)
        timeDelta = datetime.timedelta(days=7)
        data = weather_page.fetchWindData(timeDelta)
        fig = weather_page.figCompassRose(data)

    else:
        raise PreventUpdate
    return [fig]


@app.callback(
    [
        Output({'type': 'WPGdynamic', 'index': MATCH}, 'figure'),
    ],
    [Input('main-interval-component', 'n_intervals'),
     Input({'type': 'WPGdynamic', 'index': MATCH}, 'id')],
    [State({'type': 'WPGdynamic', 'index': MATCH}, 'value')]
)
def updateWeatherGraphPage(n_intervals, id, value):
    if (n_intervals == 0):  # stop first update
        raise PreventUpdate

    if ((n_intervals % (1 * 6)) == 0):  # 15 minutes -10 second timer
        # if ((n_intervals % (5*6)) == 0): # 15 minutes -10 second timer
        # print("--->>>updateWeatherGraphs", datetime.datetime.now(), n_intervals, id)
        # print("--->>>updateWeatherGraphs:", id['index'])
        if (id['index'] == 'graph-oth'):
            fig = weather_page.buildOutdoorTemperature_Humidity_Graph_Figure()
        if (id['index'] == 'graph-suv'):
            fig = weather_page.buildSunlightUVIndexGraphFigure()
        if (id['index'] == 'graph-aqi'):
            fig = weather_page.buildAQIGraphFigure()
            # print("aqi-fig=",fig)

    else:
        raise PreventUpdate
    return [fig]


if __name__ == '__main__':
    # app.run_server(debug=True, host='0.0.0.0')
    app.run_server(host='0.0.0.0')
