from dash import Input, Output, State, callback, no_update
import pandas as pd
import plotly.express as px
import numpy as np
from .data import get_dataset, list_indicators, YEAR_MIN, YEAR_MAX


def _filter_df(df, indicator, countries, year_range, per_capita):
    dff = df[df["indicator"] == indicator].copy()
    if countries:
        dff = dff[dff["country"].isin(countries)]
    dff = dff[(dff["year"] >= year_range[0]) & (dff["year"] <= year_range[1])]
    if per_capita and "population" in dff.columns:
        dff["value"] = dff["value"] / dff["population"]
    return dff


@callback(
    Output("timeseries", "figure"),
    Output("choropleth", "figure"),
    Output("ranking", "figure"),
    Output("scatter-energy-co2", "figure"),
    Input("indicator", "value"),
    Input("countries", "value"),
    Input("year-range", "value"),
    Input("scale-log", "value"),
    Input("per-capita", "value"),
)
def update_graphs(indicator, countries, year_range, scale_log, per_capita):
    df = get_dataset()
    per_capita_flag = "PC" in (per_capita or [])
    dff = _filter_df(df, indicator, countries, year_range, per_capita_flag)

    if dff.empty:
        empty = px.scatter(title="Aucune donnée")
        return empty, empty, empty, empty

    fig_ts = px.line(dff, x="year", y="value", color="country", markers=True,
                     title=f"{indicator} ({'par habitant' if per_capita_flag else 'total'})")
    if "LOG" in (scale_log or []):
        fig_ts.update_yaxes(type="log")

    last_year = dff['year'].max()
    last = dff[dff['year'] == last_year]
    fig_map = px.choropleth(last, locations="iso_code", color="value",
                            hover_name="country", color_continuous_scale="Viridis",
                            title=f"{indicator} - {last_year}")

    top = last.sort_values("value", ascending=False).head(15)
    fig_rank = px.bar(top, x="value", y="country", orientation='h',
                      title=f"Top 15 {indicator} - {last_year}", text="value")
    fig_rank.update_yaxes(autorange="reversed")

    energy_total = _filter_df(df, "Primary Energy Consumption (TWh)", None, year_range, False)
    co2_total = _filter_df(df, "CO2 Emissions (Mt)", None, year_range, False)
    energy_last = energy_total[energy_total.year == last_year][["country", "value"]].rename(columns={"value": "energy"})
    co2_last = co2_total[co2_total.year == last_year][["country", "value"]].rename(columns={"value": "co2"})
    merged = energy_last.merge(co2_last, on="country", how="inner")
    fig_scatter = px.scatter(merged, x="energy", y="co2", hover_name="country",
                             trendline="ols", title=f"Energy vs CO2 ({last_year})")
    fig_scatter.update_layout(xaxis_title="Primary Energy (TWh)", yaxis_title="CO2 (Mt)")

    return fig_ts, fig_map, fig_rank, fig_scatter


@callback(
    Output("datatable", "figure"),
    Input("indicator", "value"),
    Input("countries", "value"),
    Input("year-range", "value"),
    Input("per-capita", "value"),
)
def update_table(indicator, countries, year_range, per_capita):
    df = get_dataset()
    per_capita_flag = "PC" in (per_capita or [])
    dff = _filter_df(df, indicator, countries, year_range, per_capita_flag)
    if dff.empty:
        return px.imshow([[0]], labels=dict(color="value"), title="Aucune donnée")

    pivot = dff.pivot_table(index="country", columns="year", values="value")
    fig = px.imshow(pivot, aspect="auto", color_continuous_scale="Blues",
                    title=f"Table {indicator}")
    return fig
