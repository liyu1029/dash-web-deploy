import dash
from dash import html, dcc, callback, Input, Output, dash_table
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import assets.components as cp
parks_folder = "national_park_animal"
df = pd.read_csv(f'{parks_folder}\All_5parks.csv')
df.date = pd.to_datetime(df['date'], format='%Y%m%d')
parks_name = ["墾丁", "雪霸", "太魯閣", "陽明山", "玉山"]
weathers = {'PS01':'測站氣壓', 'TX01':'氣溫', 'RH01':'相對溼度', 'WD01':'風速', 'WD02':'風向', 'WD07':'最大瞬間風速', 'WD08':'最大瞬間風向', 'PP01':'降水量'}
df.rename(columns=weathers, inplace=True)
for weather in weathers.values():
    df[weather] = pd.to_numeric(df[weather], errors='coerce')

fig2 = px.line(df.groupby([df.date.dt.year,df.park]).agg({'amount':'size'}).reset_index(),x='date',y='amount', color='park')
fig2.update_layout(xaxis_title="時間", yaxis_title="觀測數量")
fig3 = px.bar(df.groupby([df.分類名稱,df.park]).agg({'amount':'size'}).sort_values(by='amount',ascending=False).reset_index(),x='分類名稱',y='amount', color='park')
fig3.update_layout(xaxis_title="物種", yaxis_title="觀測數量")
fig4 = px.bar(df.groupby(df.park).size())
fig4.update_layout(xaxis_title="國家公園", yaxis_title="觀測數量")

dash.register_page(__name__)

layout = html.Div([
    html.H1("分析圖表"),
    html.Div([
        dcc.Graph(figure=fig2),
        dcc.Graph(figure=fig4),
    ], style={'display': 'flex', 'flexDirection': 'row', 'justify-content': 'space-between'}),
    dcc.Graph(figure=fig3),
    html.Br(),
    html.Label('選擇年分'),
    cp.Dropdown(list(weathers.values()), ['測站氣壓', '氣溫', '相對溼度', '風速', '風向'],
                multi=True,
                id = 'weather-dropdown'),
    dcc.Graph(id='weather-scatter-plot'),
    cp.Dropdown(list(weathers.values()), '氣溫',id = 'weather-dropdown2'),
    dcc.Graph(id='weather-CDF'),
    cp.Dropdown(list(weathers.values()), '氣溫',id = 'weather-dropdown-X'),
    cp.Dropdown(list(weathers.values()), '相對溼度',id = 'weather-dropdown-Y'),
    cp.Dropdown(parks_name, parks_name, multi=True, id = 'plot-park_dropdown'),
    dcc.Graph(id='weather-amount-heatmap'),
    dash_table.DataTable(id='tbl'),
    dcc.Graph(id='tbl_out'),
    dcc.Graph(id='tbl_out2'),
])


@callback(
    Output('weather-scatter-plot', 'figure'),
    Input('weather-dropdown', 'value')
)
def update_city_selected(chosen_weather):
    # df = df.dropna(subset=chosen_weather)
    # fig = ff.create_scatterplotmatrix(df[chosen_weather], diag='histogram')
    fig = px.scatter_matrix(df, dimensions=chosen_weather, color="park")
    fig.update_layout(
        autosize=False,
        height=1000,
        )
    return fig

@callback(
    Output('weather-CDF', 'figure'),
    Input('weather-dropdown2', 'value')
)
def update_city_selected(chosen_weather):
    fig = px.ecdf(df, x=chosen_weather, color="park", markers=False, lines=True, marginal="histogram")
    return fig

@callback(
    Output('weather-amount-heatmap', 'figure'),
    Input('weather-dropdown-X', 'value'),
    Input('weather-dropdown-Y', 'value'),
    Input('plot-park_dropdown', 'value')
)
def update_city_selected(chosen_weatherX, chosen_weatherY, selected_park):
    filtered_df = df[df.park.isin(selected_park)]
    fig = px.density_heatmap(filtered_df, x=chosen_weatherX, y=chosen_weatherY, marginal_x="violin", marginal_y="violin")
    return fig

@callback(
    Output('tbl', 'data'),
    Input('plot-park_dropdown', 'value')
)
def update_city_selected(selected_park):
    filtered_df = df[df.park.isin(selected_park)]
    a = filtered_df[weathers.values()].describe().apply(lambda s: s.apply('{0:.2f}'.format))
    return a.rename_axis('').reset_index().to_dict('records',index=True)

@callback(
        Output('tbl_out', 'figure'),
        Output('tbl_out2', 'figure'),
        Input('tbl', 'active_cell'),
        Input('plot-park_dropdown', 'value'))
def update_graphs(active_cell, selected_park):
    filtered_df = df[df.park.isin(selected_park)]
    if active_cell:
        selected_weather=str(active_cell["column_id"])
        fig1 = px.histogram(filtered_df, x=selected_weather, color='park', marginal="box")
        fig2 = px.ecdf(filtered_df, x=selected_weather, color="park", markers=False, lines=True, marginal="histogram")
    else:
        fig1 = px.histogram(filtered_df, x="氣溫", color='park', marginal="box")
        fig2 = px.ecdf(filtered_df, x="氣溫", color="park", markers=False, lines=True, marginal="histogram")
    return fig1,fig2
