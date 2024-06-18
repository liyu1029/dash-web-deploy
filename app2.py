import dash
from dash import Dash, html, dcc, State, callback, Input, Output
import dash_bootstrap_components as dbc
import assets.plot_templates as plot_templates

# app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
# app = Dash(__name__, use_pages=True)
app = Dash(__name__, use_pages=True, pages_folder="pages2")
server = app.server

navbar = dbc.NavbarSimple(
    children=[
            dbc.NavItem(dbc.NavLink(f" {page['name']}", href=page["relative_path"], active="exact")) for page in dash.page_registry.values()
    ],
    brand="國家公園生物分佈", brand_href="/",
    color="primary", dark=True,
)

nav = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink(f" {page['name']}", href=page["relative_path"], active="exact")) for page in dash.page_registry.values()]+[
        dbc.DropdownMenu(
            [dbc.DropdownMenuItem(f" {page['name']}") for page in dash.page_registry.values()],
            label="More pages",
            nav=True,
        ),
    ],
    horizontal="center",
    pills=True,
    class_name="py-4"
)

app.layout = html.Div([
    # html.Div([
    #     html.Div(
    #         dbc.Button(f" {page['name']}", href=page["relative_path"], class_name='btn3')
    #     ) for page in dash.page_registry.values()
    # ],
    # className="d-flex pb-4"),#space-evenly
    navbar,
    dash.page_container,
    nav
])


if __name__ == '__main__':
    app.run(debug=True)
