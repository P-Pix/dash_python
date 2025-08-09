import dash
from dash import Dash
import dash_bootstrap_components as dbc
from .layout import build_layout
import app.callbacks  # noqa: F401

CUSTOM_CSS = "/assets/custom.css"


def create_app():
    external_stylesheets = [dbc.themes.CYBORG]  # thème plus moderne
    app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
    app.title = "Dash Energie & CO2"
    app.layout = build_layout()
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=8050)
