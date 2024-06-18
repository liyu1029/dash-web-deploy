import dash
from dash import html, dcc, callback, Output, Input, State, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from bs4 import BeautifulSoup
import requests
import assets.components as cp
from assets.plot_templates import map_layout

# import dataframe and define variables
parks_folder = "national_park_animal"
df = pd.read_csv(f'{parks_folder}/All_5parks.csv')
df.date = pd.to_datetime(df['date'], format='%Y%m%d')
click_pic="assets/pic/click_pic.png"
not_found="assets/pic/not_found.png"
parks_name = ["墾丁", "雪霸", "太魯閣", "陽明山", "玉山"]
weathers = ['PS01', 'TX01', 'RH01', 'WD01', 'WD02', 'WD07', 'WD08', 'PP01']
map_styles = ['open-street-map', 'white-bg', 'carto-positron', 'carto-darkmatter']
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

# define DBSCAN function
def DBSCAN_predict(location_df):
    location_matrix=location_df.to_numpy()
    clus=DBSCAN(eps=0.01,min_samples=10).fit(location_matrix)
    data3_df= pd.DataFrame(location_df, columns=['longitude','latitude'])
    data3_df['location_cluster']=clus.labels_
    return clus.labels_+1

dash.register_page(__name__)

layout = html.Div([
    html.H1("DBSCAN 網站"),
    html.Div([
        html.Div(children=[
            html.Label('選擇年分'),
            cp.Dropdown(df.date.dt.year.unique(),
                        df.date.dt.year.unique(),
                        multi=True,
                        id = 'DBSCAN-year-dropdown'),
            html.Br(),
            html.Label('選擇國家公園'),
            cp.Dropdown(parks_name, ['墾丁'], multi=True,
                        id = 'DBSCAN-park_dropdown'),
            html.Br(),
            # html.Label('選擇物種'),
            # cp.Dropdown(df.中文俗名.unique(), ['白鼻心'], multi=True,
            #             id = 'DBSCAN-class_dropdown'),
            # html.Br(),
            html.Label('選擇物種'),
            cp.Dropdown(df.分類名稱.unique(), ["哺乳綱"], multi=True,
                        id = 'DBSCAN-class_dropdown'),
            html.Br(),
            html.Label('選擇前幾大群'),
            dcc.Slider(2, 20, 1, value=10, id="DBSCAN-cluster-slider",
                       marks={2:"2", 10:"10", 20:"20"},
                       tooltip={"placement": "top", "always_visible": True}),
            dash_table.DataTable(id='DBSCAN-container-output-text'),
        ], style={'width': "17%"}),

        html.Div(children=[
            html.Div([cp.Dropdown(map_styles, map_styles[0],
                         id = 'DBSCAN-mapStyle_dropdown', clearable=False)],
                         style={'width':'20%'}),
            dcc.Graph(figure=go.Figure(layout=map_layout), id='DBSCAN_map_plot'),
        ], style={'width': "52%"}),

        html.Div(children=[
            html.Div(html.Img(src=click_pic, style={'height':'100%', 'width':'100%'}, id="DBSCAN-pic")),
            dcc.Markdown("""
                **Click Data**

                Click on points in the graph.
            """),
            dash_table.DataTable(id='DBSCAN-click-data'),
        ], style={'width': "22%"}),
    ], style={'display': 'flex', 'flexDirection': 'row', 'justify-content': 'space-between'}),
])

# show clicked data & img
@callback(
    Output('DBSCAN-pic', 'src'),
    Output('DBSCAN-click-data', 'data'),
    Output('DBSCAN-click-data', 'style_table'),
    Input('DBSCAN_map_plot', 'clickData'),
    prevent_initial_call=True,
    running=[(Output('DBSCAN-click-data', 'children'), "running...", ""),
             (Output('DBSCAN-pic', 'src'), "", "")])
def display_click_data(clickData):
    input_image = clickData['points'][0]['hovertext']
    response = requests.get(f"https://taicol.tw/zh-hant/taxon/{input_image}")
    soup = BeautifulSoup(response.text, "lxml")
    div = soup.find("div", {"class": "posa"})
    results = div.find_all("img")
    image_links = [result.get("src") for result in results]
    point_info=clickData['points'][0]
    del point_info["bbox"]
    if len(image_links)==0:
        # return "", json.dumps(clickData, indent=2)
        # return "", [point_info], {'overflowY': 'scroll'}
        return not_found, [{"":i, "val":point_info[i]}for i in point_info.keys()], {'overflowY': 'scroll'}
    else:
        # return image_links[0], json.dumps(clickData, indent=2)
        # return image_links[0], [point_info], {'overflowY': 'scroll'}
        return image_links[0], [{"":i, "val":point_info[i]}for i in point_info.keys()], {'overflowY': 'scroll'}


# plot map
@callback(
    Output('DBSCAN_map_plot', 'figure'),
    Output('DBSCAN-container-output-text', 'data'),
    Input('DBSCAN-year-dropdown', 'value'),
    Input('DBSCAN-park_dropdown', 'value'),
    Input('DBSCAN-class_dropdown', 'value'),
    Input('DBSCAN-cluster-slider', 'value'),
    Input('DBSCAN-mapStyle_dropdown', 'value'),
    State('DBSCAN_map_plot', 'figure'),
    running=[(Output('DBSCAN-container-output-text', 'children'), "running...", "Done")])
    # prevent_initial_call=True)
def update_figure(selected_year, selected_park, selected_class, clusters, map_style, old_fig):
    filtered_df = df[(df.date.dt.year.isin(selected_year))&(df.park.isin(selected_park))&(df.分類名稱.isin(selected_class))]
    location_df = filtered_df[["longitude", "latitude"]]
    if len(location_df.index) >= 1:
        filtered_df['location_cluster']=DBSCAN_predict(location_df)
        top_cluster = filtered_df['location_cluster'].value_counts().sort_values(ascending=False).head(clusters).index
        filtered_df = filtered_df[filtered_df.location_cluster.isin(top_cluster)]
        filtered_df['location_cluster']='cluster '+filtered_df['location_cluster'].astype(str)
        cluster_count_table = pd.DataFrame(filtered_df['location_cluster'].value_counts())
        text = cluster_count_table.reset_index().to_dict('records')
    else:
        filtered_df['location_cluster']=""
        text = pd.DataFrame(["樣本不足"]).to_dict('records')
    fig = px.scatter_mapbox(filtered_df, lat="latitude", lon="longitude",
                            color="location_cluster", hover_name="TaiCoL")
    fig.update_layout(old_fig['layout'])
    fig.update_layout(mapbox_style=map_style)
    return fig, text
