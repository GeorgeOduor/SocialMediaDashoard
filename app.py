import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
from data_models import engagement_summary, impression_day_month, comentary, top_bottom_plots, ctr, plot_en, top_fb, \
    major_fb_engagements,homepage
import plotly.express as px

fa = 'https://use.fontawesome.com/releases/v5.8.1/css/all.css'
df = pd.read_csv('E:/nvida/dashboard/data/Company_A_data.csv')
df2 = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

# globals =======
engagements = ['Impressions', 'Click-Through-Rate', 'Retweets/Shares', 'Likes', 'Video Views', 'Link Clicks',
               'Detail Expands', 'Hashtag Clicks', 'User Profile Clicks', 'Media Engagements', 'Total Engagements',
               'Engagements', 'Follows', 'Replies']
# analyses
infobox_data = engagement_summary(df)

fig = px.bar(df2, x="Fruit", y="Amount", color="City", barmode="group")
fig5,fig51 = major_fb_engagements(df),major_fb_engagements(df,sub="LinkedIn")
top_5_tweets,bottom_5_tweets = top_bottom_plots(df),top_bottom_plots(df,False)
best_format,best_format_val,worst_format,worst_format_val = ctr(df)

app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP, fa],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
)
app.css.config.serve_locally = False
# we use the Row and Col components to construct the sidebar header
# it consists of a title, and a toggle, the latter is hidden on large screens
sidebar_header = dbc.Row(
    [
        dbc.Col(html.H4("Company A", className="display-5")),
        dbc.Col(
            html.Button(
                html.Span(className="navbar-toggler-icon"),
                className="navbar-toggler",
                style={
                    "color": "rgba(0,0,0,.5)",
                    "border-color": "rgba(0,0,0,.1)",
                },
                id="toggle",
            ),
            width="auto",
            align="center",
        ),
    ]
)

sidebar = html.Div(
    [
        sidebar_header,
        html.Div(
            [
                html.Hr(),
                html.P(
                    "Social Media Admin",
                    className="p-1",
                ),
            ],
            id="blurb",
        ),
        dbc.Collapse(
            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/", active="exact"),
                    dbc.NavLink("Twitter", href="/twitter", active="exact"),
                    dbc.NavLink("Facebook", href="/facebook", active="exact"),
                    dbc.NavLink("LinkedIn", href="/linkedin", active="exact"),
                ],
                vertical=True,
                pills=True,
            ),
            id="collapse",
        ),
    ],
    id="sidebar",
)
# twitter layout ===========
tab1_content = dbc.Card(
    dbc.CardBody(
        [html.H4("Top 5 Tweets by Impression"),
            dcc.Graph(
                id='top_5_tweets',figure=top_5_tweets
            )
        ]
    ),
    className="mt-3 col-12", style={'width': '100%'}
)
tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Bottom 5 Tweets by Impression"),
            dcc.Graph(
                id='top_5_tweets', figure=bottom_5_tweets
            ),
        ], style={'width': '100%'}
    ),
    className="mt-3 col-12", style={'width': '100%'}
)

top_bottom = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Top 5 tweets", style={'width': '100%'}),
        dbc.Tab(tab2_content, label="Bottom 5 tweets", style={'width': '100%'})
    ]
)
mode_select = dcc.Dropdown(
    id="dropdown",
    options=[
        {"label": "By Month", "value": "Month_"},
        {"label": "By Day", "value": "Day_"},
    ], value="Month_",
)
engagements_select = dcc.Dropdown(
    id='engagement_sel',
    options=[
        {'label': 'Impressions', 'value': 'Impressions'},
        {'label': 'Click-Through-Rate', 'value': 'Click-Through-Rate'},
        {'label': 'Retweets/Shares', 'value': 'Retweets/Shares'},
        {'label': 'Likes', 'value': 'Likes'},
        {'label': 'Video Views', 'value': 'Video Views'},
        {'label': 'Link Clicks', 'value': 'Link Clicks'},
        {'label': 'Detail Expands', 'value': 'Detail Expands'},
        {'label': 'Hashtag Clicks', 'value': 'Hashtag Clicks'},
        {'label': 'User Profile Clicks', 'value': 'User Profile Clicks'},
        {'label': 'Media Engagements', 'value': 'Media Engagements'},
        {'label': 'Total Engagements', 'value': 'Total Engagements'},
        {'label': 'Engagements', 'value': 'Engagements'},
        {'label': 'Follows', 'value': 'Follows'},
        {'label': 'Replies', 'value': 'Replies'}
    ], value='Impressions'
)
engagements_plot_type = dcc.Dropdown(
    id='plot_type',
    options=[
        {"label": "Plot type:Line", "value": "line"},
        {"label": "Plot type:Bar", "value": "bar"},
    ], value="line"
)
@app.callback(
    dash.dependencies.Output('engagement_trend_graph', 'figure'),
    [
        dash.dependencies.Input('engagement_sel', 'value'),
        dash.dependencies.Input('dropdown', 'value'),
        dash.dependencies.Input('plot_type', 'value'),
    ]
)
def update_engagement_chart(engagement_type, mode, plot_type):
    fig2 = impression_day_month(df, plot_type, mode, engagement_type)
    return fig2
# twitter comments ==============
@app.callback(
    Output(component_id='commentaries', component_property='children'),
    [Input(component_id='engagement_sel', component_property='value'),
    Input(component_id='dropdown', component_property='value')]
)
def update_commentaries(engagement_type, mode):
    return comentary(df=df, mode=mode, engagement=engagement_type)

# Facebook settings=========
@app.callback(
    dash.dependencies.Output('engagement_trend_graph2', 'figure'),
    [
        dash.dependencies.Input('engagement_sel', 'value'),
        dash.dependencies.Input('dropdown', 'value'),
        dash.dependencies.Input('plot_type', 'value'),
    ]
)
def update_engagement_chart2(engagement_type, mode, plot_type):
    fig3 = impression_day_month(df, plot_type, mode, engagement_type,viz = "FaceBook")
    return fig3

# === facebook comments=======
@app.callback(
    Output(component_id='commentaries2', component_property='children'),
    [Input(component_id='engagement_sel', component_property='value'),
    Input(component_id='dropdown', component_property='value')]
)
def update_commentaries2(engagement_type, mode):
    return comentary(df=df, mode=mode, engagement=engagement_type,sub='Facebook')
# facebook plot 2 post type========
@app.callback(
    dash.dependencies.Output('post_format_vis', 'figure'),
    [
        dash.dependencies.Input('engagement_sel', 'value'),
        dash.dependencies.Input('dropdown', 'value'),
        dash.dependencies.Input('plot_type', 'value'),
    ]
)
def update_engagement_chart2_(engagement_type, mode, plot_type):
    fig4 = plot_en(df,engagement=engagement_type,sub='Facebook')
    return fig4
# linked in settings ===
@app.callback(
    dash.dependencies.Output('engagement_trend_graph3_', 'figure'),
    [
        dash.dependencies.Input('engagement_sel', 'value'),
        dash.dependencies.Input('dropdown', 'value'),
        dash.dependencies.Input('plot_type', 'value'),
    ]
)
def update_chart_linkeIn(engagement_type, mode, plot_type):
    fig3_1 = impression_day_month(df, plot_type, mode, engagement_type,viz = "LinkedIn")
    return fig3_1
# linked in commentaries
@app.callback(
    Output(component_id='commentaries3', component_property='children'),
    [Input(component_id='engagement_sel', component_property='value'),
    Input(component_id='dropdown', component_property='value')]
)
def update_commentaries3(engagement_type, mode):
    return comentary(df=df, mode=mode, engagement=engagement_type,sub='LinkedIn')
# linked in plot 2 post type========
@app.callback(
    dash.dependencies.Output('post_format_vis2', 'figure'),
    [
        dash.dependencies.Input('engagement_sel', 'value'),
        dash.dependencies.Input('dropdown', 'value'),
        dash.dependencies.Input('plot_type', 'value'),
    ]
)
def update_engagement_chart2_1(engagement_type, mode, plot_type):
    fig4 = plot_en(df,engagement=engagement_type,sub="LinkedIn")
    return fig4


twitter_layout = html.Div(children=[
    dbc.CardDeck(
        [
            dbc.Card(
                [dbc.CardHeader("Channel : Twitter"),
                 dbc.CardBody(
                     [
                         html.H5("Contents Shared", className="card-title"),
                         html.P(
                             infobox_data[6],
                             className="card-text",
                         ),
                     ]
                 )], style={"height": '10em', 'font-color': 'black'}, color="light"
            ),
            dbc.Card(
                [dbc.CardHeader([html.I(className="fas fa-users mr-2"), html.Span("Average Engagement Rate")]),
                 dbc.CardBody(
                     [
                         html.H5("{} %".format(infobox_data[0]), className="card-title"),
                         html.P(["You have had an average engagement rate of {}% per day and {}% per Tweet".format(
                             infobox_data[0], infobox_data[1])], style={'font-size': '12px'})
                     ]
                 )
                 ], style={"height": '10em'}, color="success", inverse=True
            ),
            dbc.Card(
                [dbc.CardHeader([html.I(className="fas fa-hand-point-up mr-2"), html.Span("Link Clicks")]),
                 dbc.CardBody(
                     [
                         html.H5("{} ".format(infobox_data[2]), className="card-title"),
                         html.P(["On average you've earned {} Link Clicks per Tweet and {} Clicks per day".format(
                             infobox_data[3], infobox_data[4])], style={'font-size': '12px'}),
                     ]
                 )], style={"height": '10em'}, color="warning", inverse=True
            ),
            dbc.Card(
                [dbc.CardHeader([html.I(className="fas fa-thumbs-up mr-2"), html.Span("Likes")]),
                 dbc.CardBody(
                     [
                         html.H5("{} ".format(infobox_data[5]), className="card-title"),
                         html.P(["On average you've earned {} Likes per Tweet and {} Likes per day".format(
                             infobox_data[6], infobox_data[7])], style={'font-size': '12px'}),
                     ]
                 )], style={"height": '10em'}, color="info", inverse=True
            ),
        ]),
    html.Hr(),
    dbc.Row(
        [
            dbc.Col(html.Div([
                #     sub info boxes
                dbc.CardDeck([
                    dbc.Card(
                        [
                            dbc.CardBody([
                                "Impressions",
                                html.Div([html.H4(infobox_data[9])], style={'align': 'center', "fontWeight": "500"})
                            ], style={'align': 'center', "fontWeight": "500"}),

                        ], outline=True),
                    dbc.Card(
                        [
                            dbc.CardBody(["Tweets", html.Div([html.H4(infobox_data[8])],
                                                             style={'align': 'center', "fontWeight": "500"})],
                                         style={'align': 'center', "fontWeight": "800"}),

                        ], outline=True),
                    dbc.Card(
                        [
                            dbc.CardBody(["Follows", html.Div([html.H4(infobox_data[10])],
                                                              style={'align': 'center', "fontWeight": "500"})],
                                         style={'align': 'center', "fontWeight": "800"}),

                        ], outline=True),
                ]), html.Hr(),
                dbc.Card([
                    dbc.CardHeader([
                        dbc.Row([
                            dbc.Col("Engagements", width=3),
                            dbc.Col(engagements_plot_type, width=3),
                            dbc.Col(engagements_select, width=3),
                            dbc.Col(mode_select, width=3),
                        ]),
                    ]),
                    dbc.CardBody([
                        dcc.Graph(
                            id='engagement_trend_graph'
                        )
                    ]),
                    dbc.CardFooter(html.Div(id='commentaries'))
                ], outline=True, style={'height': '510px', "width": "100%"})
            ]), width=7),
            dbc.Col(html.Div([
                top_bottom,
                html.Br(),
                dbc.CardDeck(
                    [dbc.Card([
                        dbc.CardHeader(html.H5('Content Format Performance(Impression Rate)')),
                        dbc.CardBody(html.H5("Best : {} : {}% | Worst : {} : {}%".format(best_format,best_format_val,worst_format,worst_format_val)))
                    ], body=True, outline=True)
                    # dbc.Card([
                    #     html.H5('Worst Performing Content Format')
                    # ], body=True, outline=True)
                    ]
                )
            ]), width=5),
        ]
    )

])
# facebook layout
facebook_layout = html.Div(children=[
    dbc.CardDeck(children=[
        dbc.Card(children=[
            dbc.CardHeader('Chanell : Facebook'),
            dbc.CardBody([
                dbc.Col(engagements_select, width=12),
            ]),
        ]),
        dbc.Card(children=[
            dbc.CardHeader("Average Impressions Per Post"),
            dbc.CardBody(html.H4("{}".format(engagement_summary(df,sma="Facebook")[12]))),
        ]),
        dbc.Card(children=[
            dbc.CardHeader("Average Engagement Rate"),
            dbc.CardBody(html.H4("{} %".format(engagement_summary(df,sma="Facebook")[11]))),
        ]),
        dbc.Card(children=[
            dbc.CardHeader("Average Click Through Rate"),
            dbc.CardBody(
                html.H4("{} %".format(engagement_summary(df,sma="Facebook")[0]))
            ),
        ]),

    ]),
    html.Hr(),
    dbc.CardDeck(children=[
        # dbc.Card(children=[
        dbc.Card([
                    dbc.CardHeader([
                        dbc.Row([
                            dbc.Col("Engagements", width=3),
                            dbc.Col(engagements_plot_type, width=3),
                            # dbc.Col(engagements_select, width=3),
                            dbc.Col(mode_select, width=3),
                        ]),
                    ]),
                    dbc.CardBody([
                        dcc.Graph(
                            id='engagement_trend_graph2'
                        )
                    ]),
                    dbc.CardFooter(html.Div(id='commentaries2'))
                ], outline=True, style={'height': '510px', "width": "100%"}),
        # ]),
        dbc.Card(children=[
            dbc.CardHeader([
                html.H6("Facebook Engagements Vs Post Format Analysis")
            ]),
            dbc.CardBody([
                dcc.Graph(
                    id='post_format_vis',
                )
            ])
        ])
    ]),html.Hr(),
    dbc.CardDeck(children=[
        dbc.Card([
            dbc.CardHeader(html.H6('Top 3 Posts By CTR')),
            dbc.CardBody([
                dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in top_fb(df).columns],
                    data=top_fb(df).to_dict('records'),
                )
            ],),
        ]),
        dbc.Card([
            dcc.Graph(
                id="major_engagements",figure=fig5,
            )
        ],color='success')
    ])
],style={'background':'azure'})
# linked in layout
linkedIn_layout  = html.Div(children=[
    dbc.CardDeck(children=[
        dbc.Card(children=[
            dbc.CardHeader('Channel : LinkedIn'),
            dbc.CardBody([
                dbc.Col(engagements_select, width=12),
            ]),
        ]),
        dbc.Card(children=[
            dbc.CardHeader("Average Impressions Per Post"),
            dbc.CardBody(html.H4("{}".format(engagement_summary(df,sma="LinkedIn")[12]))),
        ]),
        dbc.Card(children=[
            dbc.CardHeader("Average Engagement Rate"),
            dbc.CardBody(html.H4("{} %".format(engagement_summary(df,sma="LinkedIn")[11]))),
        ]),
        dbc.Card(children=[
            dbc.CardHeader("Average Click Through Rate"),
            dbc.CardBody(
                html.H4("{} %".format(engagement_summary(df,sma="LinkedIn")[0]))
            ),
        ]),

    ]),
    html.Hr(),
    dbc.CardDeck(children=[
        # dbc.Card(children=[
        dbc.Card([
                    dbc.CardHeader([
                        dbc.Row([
                            dbc.Col("Engagements", width=3),
                            dbc.Col(engagements_plot_type, width=3),
                            # dbc.Col(engagements_select, width=3),
                            dbc.Col(mode_select, width=3),
                        ]),
                    ]),
                    dbc.CardBody([
                        dcc.Graph(
                            id='engagement_trend_graph3_',
                        )
                    ]),
                    dbc.CardFooter(html.Div(id='commentaries3'))
                ], outline=True, style={'height': '510px', "width": "100%"}),
        # ]),
        dbc.Card(children=[
            dbc.CardHeader([
                html.H6("LinkedIn Engagements Vs Post Format Analysis")
            ]),
            dbc.CardBody([
                dcc.Graph(
                    id='post_format_vis2',
                )
            ])
        ])
    ]),html.Hr(),
    dbc.CardDeck(children=[
        dbc.Card([
            dbc.CardHeader(html.H6('Top 3 Posts By CTR')),
            dbc.CardBody([
                dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in top_fb(df,sub="LinkedIn").columns],
                    data=top_fb(df,sub="LinkedIn").to_dict('records'),
                )
            ],),
        ]),
        dbc.Card([
            dcc.Graph(
                id="major_engagements",figure=fig51,
            )
        ],color='success')
    ])
],style={'background':'azure'})
content = html.Div(id="page-content")

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return homepage
    elif pathname == "/twitter":
        return twitter_layout
    elif pathname == "/facebook":
        return facebook_layout
    elif pathname == "/linkedin":
        return linkedIn_layout
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

@app.callback(
    Output("collapse", "is_open"),
    [Input("toggle", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run_server(debug=False)
