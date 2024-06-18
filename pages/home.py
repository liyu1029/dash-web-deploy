import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')
teammate_card = dbc.Card(
    [
        dbc.CardImg(src="assets/pic/bird.jpg", top=True),
        dbc.CardBody(
            [
                html.H3('組員'),
                dbc.ListGroup(
                    [
                        dbc.ListGroupItem("陳O妤"),
                        dbc.ListGroupItem("洪O悌"),
                        dbc.ListGroupItem("顏O羽"),            
                    ]
                ),
            ]
        ),
    ],
    style={"width": "20rem"},
)
source_card = dbc.Card(
    [
        dbc.CardImg(src="assets/pic/bird.jpg", top=True),
        dbc.CardBody([
                html.H3('資料來源'),
                html.Label('主要資料：'),
                dbc.ListGroupItem('臺灣國家公園生物多樣性資料庫', href='https://npgis.nps.gov.tw/newpublic/', target="_blank"),
                html.Br(),
                html.Label('輔助資料：'),
                dbc.ListGroup(
                    [
                        dbc.ListGroupItem("台灣物種名錄", href="https://taicol.tw/zh-hant/", target="_blank"),
                        dbc.ListGroupItem('CODiS氣候資料服務系統', href='https://codis.cwa.gov.tw/Home', target="_blank"),
                        dbc.ListGroupItem('(氣象資料開放平臺)', href='https://opendata.cwa.gov.tw/index', target="_blank"),            
                    ]
                ),
        ]),
    ],
    style={"width": "20rem"},
)
park_card = dbc.Card(
    [
        dbc.CardImg(src="assets/pic/bird.jpg", top=True),
        dbc.CardBody([
            html.H3('資料來源')]+[
            dbc.ListGroup([
                dbc.ListGroupItem(f" {park}")
            ]) for park in ["玉山", "雪霸", "陽明山", "太魯閣", "墾丁"]
        ]),
    ],
    style={"width": "20rem"},
)
layout = html.Div([
    html.H1('臺灣國家公園的生物分佈分析'),
    dbc.Row([
        teammate_card,
        source_card,
        page_card
    ], justify="around")
])

