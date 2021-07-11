import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from data import countries_df, totals_df
from builders import make_table

stylesheets = [
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.min.css",
    "https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap",
]


app = dash.Dash(__name__, external_stylesheets=stylesheets)

bubble_map = px.scatter_geo(
    countries_df,
    size="Confirmed",
    size_max=40,
    hover_data={
        "Confirmed": ":,",
        "Recovered": ":,",
        "Deaths": ":,2f",
        "Country_Region": False,
    },
    title="Confirmed By Country",
    color_continuous_scale=px.colors.sequential.Oryel,
    hover_name="Country_Region",
    color="Confirmed",
    locations="Country_Region",
    locationmode="country names",
    template="plotly_dark",
)
bubble_map.update_layout(margin=dict(l=0, r=0, t=50, b=50))

bars_graph = px.bar(
    totals_df,
    x="condition",
    y="count",
    template="plotly_dark",
    title="Total Global Cases",
    hover_data={"count": ":,"},
    labels={"condition": "Condition", "count": "Count", "color": "Condition"},
)
bars_graph.update_traces(marker_color=["#e74c3c", "#8e44ad", "#27ae60"])

app.layout = html.Div(
    style={
        "textAlign": "center",
        "minHeight": "100vh",
        "backgroundColor": "black",
        "color": "white",
        "fontFamily": "Open Sans, sans-serif",
    },
    children=[
        html.Header(
            style={"textAlign": "center", "paddingTop": "50px", "marginBottom": 100},
            children=[html.H1("Corona Dashboard", style={"fontSize": 40})],
        ),
        html.Div(
            style={
                "display": "grid",
                "gap": 50,
                "gridTemplateColumns": "repeat(4, 1fr)",
            },
            children=[
                html.Div(
                    style={"grid-column": "span 3"},
                    children=[dcc.Graph(figure=bubble_map)],
                ),
                html.Div(
                    children=[make_table(countries_df)],
                ),
            ],
        ),
        html.Div(
            style={
                "display": "grid",
                "gap": 50,
                "gridTemplateColumns": "repeat(4, 1fr)",
            },
            children=[
                html.Div(children=[dcc.Graph(figure=bars_graph)]),
                html.Div(
                    children=[
                        dcc.Input(placeholder="What is your name?", id="hello-input"),
                        html.H2(children="Hello Anynomous", id="hello-output"),
                    ]
                ),
            ],
        ),
    ],
)


@app.callback(Output("hello-output", "children"), [Input("hello-input", "value")])
def update_hello(value):
    if value is None:
        return "Hello anonymous"
    else:
        return f"Hello {value}"


if __name__ == "__main__":
    app.run_server(debug=True)
