import dash
from dash import html, dcc, callback, Output, Input, State, ctx
import dash_bootstrap_components as dbc
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import joblib
from scipy.stats import kstest
np.set_printoptions(suppress=True)


# import dataframe
parks_folder = "national_park_animal"
df = pd.read_csv(f'{parks_folder}/All_5parks.csv')
df['TX01'] = pd.to_numeric(df['TX01'], errors='coerce')
df['WD01'] = pd.to_numeric(df['WD01'], errors='coerce')
df['WD02'] = pd.to_numeric(df['WD02'], errors='coerce')
df['PP01'] = pd.to_numeric(df['PP01'], errors='coerce')
df = df.dropna(subset=['TX01','WD01','WD02','PP01'])
X_train = df[['TX01','WD01','WD02','PP01']].values
#導入訓練好的模型
clf_dt = joblib.load(f'{parks_folder}/clf_park.pkl')
clf_rf = joblib.load(f'{parks_folder}/clf_spices.pkl')


dash.register_page(__name__)

card_input = dbc.Card([
        dbc.CardBody(
            [
                html.H4("使用模型預測:"),
                html.Label('選擇氣溫(-15~37) : '),
                dcc.Input(id="TX01-input", type="number", min=-15, max=37, value=20, style={'width':'100%'}),
                html.Label('選擇風速(0~37) :   '),
                dcc.Input(id="WD01-input", type="number", min=0, max=37, value=2, style={'width':'100%'}),
                html.Label('選擇風向(0~360) :  '),
                dcc.Input(id="WD02-input", type="number", min=0, max=360, value=360, step=2, style={'width':'100%'}),
                html.Label('選擇降水量(0~1) :  '),
                dcc.Input(id="PP01-input", type="number", min=0, max=1, value=1, step=0.1, style={'width':'100%'}),
                html.Br(),
                html.Button('預測', id="predict_btn", className='btn2 my-4'),
            ],
        ),
    ],style={"width": "15rem"})

card_result = dbc.Card([
        dbc.CardBody(
            [
                dbc.Alert([
                    html.H4(id='pridict_result', className="alert-heading"),
                    html.Div(id='pridict_warning')],
                    color="info"),
                dcc.Graph(figure=px.bar(title="Probability Distribution"),
                          id='decision_tree_plot'),
            ],
        ),
    ],style={"width": "55rem"}, color="info", outline=True)

layout = html.Div([
    html.Div([
        html.H1("決策樹網站"),
        html.Div([
            card_input,
            card_result,
        ], className="d-flex flex-row d-inline-flex"),
    ], className="d-flex flex-column d-inline-flex"),
], className="d-flex justify-content-center")

# layout = html.Div([
#     html.H1("決策樹網站"),
#     html.Div([
#         card_input,
#         card_result,
#     ], className="d-flex flex-row d-inline-flex"),
# ])

@callback(
    Output('pridict_result', 'children'),
    Output('pridict_warning', 'children'),
    Output('decision_tree_plot', 'figure'),
    State('TX01-input', 'value'),
    State('WD01-input', 'value'),
    State('WD02-input', 'value'),
    State('PP01-input', 'value'),
    Input('predict_btn', 'n_clicks'),)
    # prevent_initial_call=True)
def update_output(TX01, WD01, WD02, PP01, n_clicks):
    new_sample = np.array([[TX01, WD01, WD02, PP01]])
    new_sample = new_sample.reshape(1, -1)
    prob_df = pd.DataFrame()
    predicted_park = clf_dt.predict(new_sample)
    文字 = f'預測國家公園類別：{predicted_park[0]}。'
    警告=""
    prob_df["Probability"] = clf_rf.predict_proba(new_sample).flatten()
    prob_df["Categories"] = clf_rf.classes_
    prob_df = prob_df.sort_values(by='Probability', ascending=False)
    fig = px.bar(prob_df,x="Categories", y="Probability", title="預測可能出現的生物機率")

    bad_index=[]
    # 可以判斷輸入的數據是否對模型預測有沒有偏差
    # 對四個天氣特徵做比較分布
    for feature_idx in range(X_train.shape[1]):
        stat, p_value = kstest(new_sample[:, feature_idx], 'norm', args=(np.mean(X_train[:, feature_idx]), np.std(X_train[:, feature_idx])))
        if p_value < 0.05:
            bad_index.append(feature_idx+1)
    if bad_index:
        警告 = f'輸入數據與訓練數據的第 {bad_index} 個特徵的分布不同，可能會影響模型預測。'
    return 文字, 警告, fig


