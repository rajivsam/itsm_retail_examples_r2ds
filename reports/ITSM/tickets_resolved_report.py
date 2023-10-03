from dash import Dash, html,dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import numpy as np

fp = "../../data/q2_2016_ticket_resolution_data.csv"
fpdtypes = "../../data/ticket_resolution_dtypes.csv"
dtypes_df = pd.read_csv(fpdtypes)
dtypes_dict = {row["attribute"]: row["type"] for index, row in dtypes_df.iterrows()}

q2_df = pd.read_csv(fp)
q2_df = q2_df.astype(dtypes_dict)
q2_df["resolution_time"] = q2_df["closed_at"] - q2_df["sys_created_at"]
q2_df["resolution_time"] = q2_df["resolution_time"].apply(lambda x: x.total_seconds()/3600)
group_vals = q2_df.assignment_group.unique().tolist()
group_vals = [g.strip() for g in group_vals ]
select_group_10_closing_activity = q2_df["assignment_group"] == "Group 10"
df_g10 = q2_df[select_group_10_closing_activity].copy()
figp =  px.violin(df_g10, y="resolution_time", box=True, points="all", hover_data=df_g10.columns)
fige = px.ecdf(df_g10, x="resolution_time") 
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.layout = dbc.Container([
    dbc.Row(
                dbc.Col(html.H1('ITSM Ticket Resolution Activity Reports for Q2-2010', style={"text-align": 'center', "font-family": 'monospace'}), width=10), justify="center"),            
    dbc.Row([
        dbc.Col(html.Label("Select a support group", style={"text-align":'right',
                                                            "font-family": 'monospace'}),width={"size":2, "offset": 1}),
        dbc.Col(dcc.Dropdown(group_vals,'Group 10', id='demo-dropdown'), width={"size": 2, "offset": 0})], justify="center", align="center"),
        html.Br(),
    dbc.Row( [dbc.Col(html.H6("Ticket Resolution times for the group",
                               style={"text-align":'left', "font-family": 'monospace'}),
                               width=3), 
                               dbc.Col(dcc.Graph(figure=figp, id='q2plot'), width=9)],
                                 justify="center", align="center"),
        html.Br(),
    
    dbc.Row( [dbc.Col(html.H6("Probablistic View of Ticket Resolution Time for the group", style={"text-align":'left', "font-family": 'monospace'}), align="center", width=3), dbc.Col(dcc.Graph(figure=fige, id='q2ecdf'), width=9)], justify="center", align="center"),
        
        ], fluid=True)

@callback(
    Output('q2plot', 'figure'),
    Input('demo-dropdown', 'value')
)
def update_graph(value):
    select_group_closing_activity = q2_df["assignment_group"] == value
    df_sg = q2_df[select_group_closing_activity].copy()

    #fig = px.histogram(df_sg, x="rthrs", labels=dict(rthrs="resolution time in hours"))
    fig =  px.violin(df_sg, y="resolution_time", box=True, points="all", hover_data=df_sg.columns)
    return fig

@callback(
    Output('q2ecdf', 'figure'),
    Input('demo-dropdown', 'value')
)
def update_ecdf(value):
    select_group_closing_activity = q2_df["assignment_group"] == value
    df_sg = q2_df[select_group_closing_activity].copy()
    #fig = px.histogram(df_sg, x="rthrs", labels=dict(rthrs="resolution time in hours"))
    fig = px.ecdf(df_sg, x="resolution_time")
    return fig

if __name__ == '__main__':
    app.run(debug=True)