import dash
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
# import json
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
    }
}

# define Kmeans function
def kmeans_predict(clusters, location_df):
    location_matrix=location_df.to_numpy()
    kmeans=KMeans(n_clusters=clusters)
    dy=kmeans.fit_predict(location_matrix)
    # dlabel=kmeans.labels_
    centers = kmeans.cluster_centers_
    return centers, kmeans.predict(location_df)+1

dash.register_page(__name__)

layout = html.Div([
    html.H1("Kmeans 網站"),
    html.Div([
        html.Div(children=[
            html.Label('選擇年分'),
            cp.Dropdown(df.date.dt.year.unique(),
                        df.date.dt.year.unique(),
                        multi=True,
                        id = 'year-dropdown'),
            html.Br(),
            html.Label('選擇國家公園'),
            cp.Dropdown(parks_name, ['墾丁'], multi=True,
                        id = 'park_dropdown'),
            html.Br(),
            html.Label('選擇物種'),
            cp.Dropdown(df.中文俗名.unique(), np.random.choice(df.中文俗名.unique(), 6), multi=True,
                        id = 'class_dropdown'),
            html.Br(),
            # html.Label('選擇物種'),
            # cp.Dropdown(df.分類名稱.unique(), ['鳥綱', '木蘭綱', "哺乳綱"], multi=True,
            #             id = 'class_dropdown'),
            # html.Br(),
            html.Label('選擇群數'),
            dcc.Slider(2, 20, 1, value=10, id="cluster-slider",
                       marks={2:"2", 10:"10", 20:"20"},
                       tooltip={"placement": "top", "always_visible": True}),
            html.Div(id='container-output-text')
        ], style={'width': "17%"}),

        html.Div(children=[
            html.Div([cp.Dropdown(map_styles, map_styles[0],
                         id = 'mapStyle_dropdown', clearable=False)],
                         style={'width':'20%'}),
            dcc.Graph(figure=go.Figure(layout=map_layout), id='Kmeans_map_plot'),
        ], style={'width': "52%"}),

        html.Div(children=[
            html.Div(html.Img(style={'height':'100%', 'width':'100%'}, id="KM-pic")),
            dcc.Markdown("""
                **Click Data**

                Click on points in the graph.
            """),
            html.Pre(id='click-data', style=styles['pre']),
        ], style={'width': "22%"}),
    ], style={'display': 'flex', 'flexDirection': 'row', 'justify-content': 'space-between'})
])

# show clicked data & img
@callback(
    Output('KM-pic', 'src'),
    Output('click-data', 'children'),
    Input('Kmeans_map_plot', 'clickData'),
    prevent_initial_call=True,
    running=[(Output('click-data', 'children'), "running...", ""),
             (Output('KM-pic', 'src'), "", "")])
def display_click_data(clickData):
    input_image = clickData['points'][0]['hovertext']
    response = requests.get(f"https://taicol.tw/zh-hant/taxon/{input_image}")
    soup = BeautifulSoup(response.text, "lxml")
    # 抓照片
    pic_div = soup.find("div", {"class": "posa"})
    pic_results = pic_div.find_all("img")
    image_links = [result.get("src") for result in pic_results]
    # 抓名字
    name_div = soup.find("div", {"class": "maintxt"})
    name_results = name_div.find_all("h2")
    name = [result.get_text() for result in name_results][1]

    if len(image_links)==0:
        # return "", json.dumps(clickData, indent=2)
        return "assets\\pic\\not_found.jpg", name
    else:
        # return image_links[0], json.dumps(clickData, indent=2)
        return image_links[0], name


# plot map
@callback(
    Output('Kmeans_map_plot', 'figure'),
    Output('container-output-text', 'children'),
    Input('year-dropdown', 'value'),
    Input('park_dropdown', 'value'),
    Input('class_dropdown', 'value'),
    Input('cluster-slider', 'value'),
    Input('mapStyle_dropdown', 'value'),
    State('Kmeans_map_plot', 'figure'),
    running=[(Output('container-output-text', 'children'), "running...", "Done")])
    # prevent_initial_call=True)
def update_figure(selected_year, selected_park, selected_class, clusters, map_style, old_fig):
    filtered_df = df[(df.date.dt.year.isin(selected_year))&(df.park.isin(selected_park))&(df.中文俗名.isin(selected_class))]
    location_df = filtered_df[["longitude", "latitude"]]
    if len(location_df.index) >= clusters:
        center, location_df['location_cluster']= kmeans_predict(clusters, location_df)
        filtered_df['location_cluster']='cluster '+location_df['location_cluster'].astype(str)
        text = f"已分為{clusters}群"
    else:
        filtered_df['location_cluster']=""
        text = f"樣本不足，無法分為{clusters}群"    
    fig = px.scatter_mapbox(filtered_df ,lat="latitude", lon="longitude",
                            color="location_cluster", hover_name="TaiCoL")
    fig.update_layout(old_fig['layout'])
    fig.update_layout(mapbox_style=map_style)

    return fig, text
