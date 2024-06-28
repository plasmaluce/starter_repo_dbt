import dash
from dotenv import dotenv_values
import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, types
from sqlalchemy import text  # to be able to pass string
import plotly.express as px
from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc 

# we of course need plotly and pandas
import plotly.express as px
import pandas as pd


config = dotenv_values('token.env')

# define variables for the login
username = config['postgres_user']
password = config['postgres_PW']
host = config['postgres_IP']
port = config['postgres_port']
db_climate = config['postgres_DB_climate']

url = f'postgresql://{username}:{password}@{host}:{port}/climate'

engine = create_engine(url, echo=False) # echo is a type of login or reporting

# check your URL
engine.url # password is hidden

# Defining dataframes from the marts

df_mart_hour = pd.read_sql_query("SELECT * FROM dbt_climate.mart_forecast_hour", url) 

df_mart_day = pd.read_sql_query("SELECT * FROM dbt_climate.mart_forecast_day", url)  

df_mart_week = pd.read_sql_query("SELECT * FROM dbt_climate.mart_conditions_week", url)  
df_mart_week.sort_values('week_of_year',inplace=True)

#instanciate the app
app =dash.Dash(external_stylesheets=[dbc.themes.QUARTZ])


#the general syntax for a table
d_table = dash_table.DataTable(df_mart_day.to_dict('records'),
                                  [{"City": i, "avg_temp_c": i} for i in df_mart_day.columns],
                                  style_data={'color': 'white','backgroundColor': 'teal'},
                              style_header={
                                  'backgroundColor': 'rgb(210, 210, 210)',
                                  'color': 'black','fontWeight': 'bold'}) 

fig = px.bar(df_mart_day[df_mart_day['city'].isin(['Berlin', 'Tripoli', 'Cape Town', 'Bangui', 'New York', 'Tokyo', 'Wellington'])], 
             y='avg_humidity', 
             x='avg_temp_c',  
             color='city',
             orientation='v',
             hover_name="country",
             height=500)

fig = fig.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
    )

graph = dcc.Graph(figure=fig)


app =dash.Dash()

app.layout = html.Div(html.H1(children = 'My First Spicy Dash'))


if __name__ == '__main__':
     app.run_server() 