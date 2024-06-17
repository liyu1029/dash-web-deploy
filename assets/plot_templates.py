import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go

pio.templates["custom_theme"] = go.layout.Template(
    data=dict(
        scattermapbox=[dict(marker=dict(size=12))]
    ),
    layout=go.Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        mapbox=dict(style="open-street-map"),
        font=dict(family="assets/font/Iansui-Regular.ttf", size=17),
        title_font=dict(family="assets/font/Iansui-Regular.ttf", size=20),
        title={"x": 0.5, "xanchor": "center"}
    )
)
pio.templates.default = 'plotly+custom_theme'


# MAP PLOT SETUP
map_layout = dict(
    margin={"r":0,"t":0,"l":0,"b":0}, height=500,
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))