import dash
from dash import html, dcc, callback, Output, Input, State, ctx
import plotly.express as px
import pandas as pd
import numpy as np
import assets.components as cp
# parks_folder = "national_park_animal"
# df = pd.read_csv(f'{parks_folder}/All_5parks.csv')
# similarities_df = pd.read_csv(f'{parks_folder}/jaccard_similarity.csv', index_col=0)
# all_species = df.TaiCoL.unique()
# all_species_name = df[['TaiCoL', '中文俗名']].drop_duplicates().set_index('TaiCoL').T.to_dict('list')
# parks_name = ["墾丁", "雪霸", "太魯閣", "陽明山", "玉山"]
# weathers = ['PS01', 'TX01', 'RH01', 'WD01', 'WD02', 'WD07', 'WD08', 'PP01']
# df.date = pd.to_datetime(df['date'], format='%Y%m%d')

dash.register_page(__name__)

layout = html.Div([
    html.H1("Jaccard similarity"),
    # html.Div([
    #     html.B('選擇物種: '),
    #     html.Button('隨機選擇', id='random_species_btn'),
    #     cp.Dropdown(all_species, np.random.choice(all_species, 10), multi=True,
    #                 id = 'species-dropdown', clearable=False),
    # ]),
    # html.Br(),
    # html.Div([
    #     dcc.Graph(id='jaccard_plot'),
    # ]),
])


# @callback(
#     Output('species-dropdown', 'value'),
#     Input('random_species_btn', 'n_clicks')
# )
# def update_species_selected(n_clicks):
#     return np.random.choice(all_species, 10)

# @callback(
#     Output('jaccard_plot', 'figure'),
#     Input('species-dropdown', 'value'),
#     running=[(Output("random_species_btn", "disabled"), True, False)]
# )
# def update_graph(chosen_species):
#     most_bird = df[df.分類名稱.isin(["鳥綱"])]["TaiCoL"].value_counts()[1:11]
#     if len(chosen_species) >= 1:
#         chosen_similarities = similarities_df.loc[chosen_species,chosen_species]
#         俗名s=list()
#         for 俗名 in chosen_species:
#             俗名s.append(all_species_name[俗名][0])
#         chosen_similarities.index=俗名s
#         chosen_similarities.columns=俗名s
#         fig = px.imshow(chosen_similarities, text_auto=True, aspect="auto", zmin=0, zmax=1, color_continuous_scale="blues")
#         return fig
