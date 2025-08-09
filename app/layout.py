from dash import html, dcc
import dash_bootstrap_components as dbc
from .data import get_dataset, list_indicators, YEAR_MIN, YEAR_MAX


def build_layout():
    df = get_dataset()
    indicators = list_indicators(df)
    countries = sorted(df['country'].unique())
    default_countries = [c for c in ["France", "Germany", "United States", "China"] if c in countries]
    decade_marks = {y: str(y) for y in range(YEAR_MIN - YEAR_MIN % 10, YEAR_MAX + 1, 10)}

    return dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Explorateur Énergie & CO2"), width=8),
            dbc.Col(html.Div("Demo Dash", className="badge bg-primary mt-3"), width=4, style={"textAlign": "right"})
        ], className="mb-2"),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label("Choisir un indicateur"),
                    dcc.Dropdown(id="indicator", clearable=False,
                                 options=[{"label": v, "value": v} for v in indicators],
                                 value=indicators[0] if indicators else None),
                    html.Label("Sélection pays"),
                    dcc.Dropdown(id="countries", multi=True,
                                 options=[{"label": c, "value": c} for c in countries],
                                 value=default_countries),
                    html.Label("Période"),
                    dcc.RangeSlider(id="year-range", min=YEAR_MIN, max=YEAR_MAX,
                                    value=[YEAR_MIN, YEAR_MAX], step=1, dots=False,
                                    marks=decade_marks,
                                    tooltip={"placement": "bottom", "always_visible": True}),
                    html.Div([
                        dbc.Checklist(id="scale-log", options=[{"label": "Echelle logarithmique", "value": "LOG"}], value=[]),
                        dbc.Checklist(id="per-capita", options=[{"label": "Par habitant", "value": "PC"}], value=["PC"]),
                    ], className="mt-2"),
                ], className="control-panel")
            ], width=3),
            dbc.Col([
                html.Div(dcc.Loading(dcc.Graph(id="timeseries")), className="graph-panel"),
                html.Div(dcc.Loading(dcc.Graph(id="choropleth")), className="graph-panel"),
            ], width=9)
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H4("Tableau détail"),
                    dcc.Loading(dcc.Graph(id="datatable"))
                ], className="graph-panel")
            ], width=6),
            dbc.Col([
                html.Div([
                    html.H4("Top 15 (dernière année)"),
                    dcc.Loading(dcc.Graph(id="ranking"))
                ], className="graph-panel"),
                html.Div([
                    html.H4("Relation Energie vs CO2"),
                    dcc.Loading(dcc.Graph(id="scatter-energy-co2"))
                ], className="graph-panel"),
            ], width=6)
        ], className="mt-2"),
        html.Hr(),
        html.Footer("Source: Our World In Data (energie & emissions)", style={"fontSize": "0.8rem", "textAlign": "center", "marginTop": "1rem"})
    ], fluid=True)
