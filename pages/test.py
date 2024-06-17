import dash
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import json
from sklearn.cluster import KMeans
from bs4 import BeautifulSoup
import requests
import assets.components as cp
from assets.plot_templates import map_layout


# import dataframe and define variables
parks_folder = "national_park_animal"
df = pd.read_csv(f'{parks_folder}\\All_5parks.csv')
df.date = pd.to_datetime(df['date'], format='%Y%m%d')
parks_name = ["墾丁", "雪霸", "太魯閣", "陽明山", "玉山"]
weathers = ['PS01', 'TX01', 'RH01', 'WD01', 'WD02', 'WD07', 'WD08', 'PP01']
map_styles = ['open-street-map', 'white-bg', 'carto-positron', 'carto-darkmatter']
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    },
    'btn':{
        'background-color': 'blue',
    }
}

# initialize map plot
fig = px.scatter_mapbox(df.head(5), lat="latitude", lon="longitude", hover_name="TaiCoL",
                        hover_data=["中文俗名", "學名"], color="分類名稱")
fig.update_layout(map_layout)


# define Kmeans function
def kmeans_predict(clusters, location_df):
    location_matrix=location_df.to_numpy()
    kmeans=KMeans(n_clusters=clusters)
    dy=kmeans.fit_predict(location_matrix)
    # dlabel=kmeans.labels_
    centers = kmeans.cluster_centers_
    return centers, kmeans.predict(location_df)+1

dash.register_page(__name__)

layout0 = html.Div([
    html.H1("TEST--"),
    html.Div([
        html.Div(children=[
            html.Label('選擇年分'),
            cp.Dropdown(df.date.dt.year.unique(),
                        df.date.dt.year.unique(),
                        multi=True),
            # dbc.Card(
            # [
            #     dbc.CardImg(src="/static/images/placeholder286x180.png", top=True),
            #     dbc.CardBody(
            #         [
            #             html.H4("Card title", className="card-title"),
            #             html.P(
            #                 "Some quick example text to build on the card title and "
            #                 "make up the bulk of the card's content.",
            #                 className="card-text",
            #             ),
            #             dbc.Button("Go somewhere", color="primary"),
            #         ]
            #     ),
            # ],
            # style={"width": "18rem"}),
            html.Br(),
            html.Label('選擇國家公園'),
            cp.Dropdown(parks_name, ['墾丁'], multi=True),
            html.Br(),
            html.Label('選擇物種'),
            cp.Dropdown(df.中文俗名.unique(), np.random.choice(df.中文俗名.unique(), 6), multi=True),
            html.Br(),
            html.Label('選擇群數'),
            dcc.Slider(2, 20, 1, value=10,
                       marks={2:"2", 10:"10", 20:"20"},
                       tooltip={"placement": "top", "always_visible": True}),
            html.Div()
        ], style={'width': "17%"}),

        html.Div(children=[
            html.Div([cp.Dropdown(map_styles, map_styles[0],
                         clearable=True),],
                         style={'width':'20%'}),
            dcc.Graph(figure=fig, id='Kmeans_map_plot'),
        ], style={'width': "52%"}),

        html.Div(children=[
            html.Div(html.Img(src="assets\\pic\\not_found.jpg",style={'height':'100%', 'width':'100%'})),
            dcc.Markdown("""
                **Click Data**

                Click on points in the graph.
            """),
            html.Pre(style=styles['pre']),
        ], style={'width': "22%"}),
    ], style={'display': 'flex', 'flexDirection': 'row', 'justify-content': 'space-between'})
])



def layout():
    return layout0