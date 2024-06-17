import dash
from dash import html, dcc, callback, Output, Input, State, ctx
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import datetime
from sklearn.model_selection import train_test_split
from sklearn import linear_model, tree, neighbors
import assets.components as cp

parks_name = ["墾丁", "雪霸", "太魯閣", "陽明山", "玉山"]
models = {'Regression': linear_model.LinearRegression,
          'Decision Tree': tree.DecisionTreeRegressor,
          'k-NN': neighbors.KNeighborsRegressor}

# import dataframe
parks_folder = "national_park_animal"
df = pd.read_csv(f'{parks_folder}/All_5parks.csv')
df.date = pd.to_datetime(df['date'], format='%Y%m%d')
df_year_month_amount=df.groupby([df.date.dt.year.rename('year'),df.date.dt.month.rename('month'),df.park]).agg({'amount':'size'}).reset_index()
df_monthly_count=df.groupby([df.date.dt.strftime("%Y%m"),df.park]).agg({'amount':'size'}).reset_index()

dash.register_page(__name__)

layout = html.Div([
    html.H1("回歸"),
    cp.Dropdown(
        id='regression_model_dropdown',
        options=["Regression", "Decision Tree", "k-NN"],
        value='Decision Tree',
        clearable=False
    ),
    cp.Dropdown(
        id='regression_park_dropdown',
        options=parks_name,
        value='玉山',
        clearable=False
    ),
    dcc.DatePickerSingle(
        id='regression_date_picker',
        min_date_allowed=datetime.date(2020, 8, 1),
        max_date_allowed=datetime.date(2025, 8, 1),
        initial_visible_month=datetime.date(2024, 8, 1),
        date=datetime.date(2024, 8, 1)
    ),
    dcc.Graph(id='linear_regression_plot1'),
    dcc.Graph(id='linear_regression_plot2'),
])


@callback(
    Output('linear_regression_plot1', 'figure'),
    Input('regression_model_dropdown', "value"),
    Input('regression_park_dropdown', "value"),
    Input('regression_date_picker', 'date'))
def update_output(name, chosen_park, date_value):
    # park_to_remove = parks_name.copy()
    # park_to_remove.remove('玉山')
    filtered_df=df_monthly_count[df_monthly_count['park']==chosen_park]
    filtered_df["jdate"]=pd.DatetimeIndex(pd.to_datetime(filtered_df.date,format="%Y%m")).strftime("%y%j").astype(int)
    X=filtered_df.jdate.values.reshape(-1, 1)
    model = models[name]()
    model.fit(X, filtered_df.amount)
    x_range = pd.date_range(
                start=datetime.datetime.strptime(filtered_df.date.min(), '%Y%m').date(),
                end=date_value,
                periods=100).strftime("%y%j").astype(int)
    y_range = model.predict(x_range.values.reshape(-1, 1))
    normal_date = lambda x: datetime.datetime.strptime("{:0>5d}".format(x), '%y%j').strftime("%Y%m")
    x_range=[normal_date(x) for x in x_range]

    fig = px.scatter(
        filtered_df,
        x='date' ,y='amount', color='park', opacity=0.65)
    fig.add_traces(go.Scatter(x=x_range, y=y_range, name='Regression Fit'))
    fig.update_xaxes(categoryorder='category ascending')
    return fig


@callback(
    Output('linear_regression_plot2', 'figure'),
    Input('regression_model_dropdown', "value"),
    Input('regression_park_dropdown', "value"))
def update_output(name, chosen_park):
    # park_to_remove = parks_name.copy()
    # park_to_remove.remove('玉山')
    filtered_df=df_year_month_amount[df_year_month_amount['park']==chosen_park]
    X=filtered_df.month.values.reshape(-1, 1)
    model = models[name]()
    model.fit(X, filtered_df.amount)
    x_range = np.linspace(X.min(), X.max(), 100)
    y_range = model.predict(x_range.reshape(-1, 1))

    fig = px.scatter(
        filtered_df,
        x='month' ,y='amount', color='park', opacity=0.65)
    fig.add_traces(go.Scatter(x=x_range, y=y_range, name='Regression Fit'))
    # fig.for_each_trace(lambda trace: trace.update(visible="legendonly") 
                #    if trace.name in park_to_remove else ())
    return fig
