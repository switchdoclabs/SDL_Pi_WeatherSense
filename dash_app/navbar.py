
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html

from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc



################
# Navbar
################
def Navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("AQI", href="/aqi_page")),
            dbc.NavItem(dbc.NavLink("Lightning", href="/lightning_page")),
            dbc.NavItem(dbc.NavLink("Weather", href="/weather_page")),
            dbc.NavItem(dbc.NavLink("Indoor T/H", href="/indoorth_page")),
            dbc.NavItem(dbc.NavLink("SolarMAX", href="/solarmax_page")),
            dbc.NavItem(dbc.NavLink("Generic", href="/generic_page")),
                ],
                id='navbar',
                brand="WeatherSense Logging",
                brand_href="#",
                color="primary",
                dark=True,

    )
    return navbar

def Logo(app):
    logo = html.Img(src=app.get_asset_url('WSLogo.png'), height=100, style={'margin' :'20px'})
    return logo



