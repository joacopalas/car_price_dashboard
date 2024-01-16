import numpy as np
import pandas as pd
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px
import dash_mantine_components as dmc

# Initialize the app - incorporate a Dash Mantine theme
external_stylesheets = [dmc.theme.DEFAULT_COLORS]
app = Dash(title='Car Price Visualization', external_stylesheets=external_stylesheets)
server = app.server

autos = pd.read_csv("CarPrice.csv")
autos = autos.drop('car_ID', axis = 1)

categorical_columns = autos.select_dtypes(include=['object']).columns
numerical_columns = autos.select_dtypes(exclude=['object']).columns

## Graphs to use:
def create_scatter_graph(x_axis = 'carlength', y_axis = 'price', colortype = 'carbody'):
    graph = px.scatter(autos, x = x_axis, y = y_axis, color = colortype)
    return graph

def create_histogram(x_axis = 'price', colortype = 'carbody'):
    graph = px.histogram(autos, x = x_axis, color = colortype)
    return graph

def create_heatmap():
    graph = px.imshow(autos[numerical_columns].corr())
    return graph

def create_boxplot(x_axis = 'carbody', y_axis = 'price'):
    graph = px.box(autos, x = x_axis, y = y_axis, color = x_axis)
    return graph

## Widgets
scatter_x_dd = dmc.Select(label = 'Attribute for x axis', id='scatter_x_axis', value='carlength',
    clearable = False, data = numerical_columns)
scatter_y_dd = dmc.Select(label = 'Attribute for y axis', id='scatter_y_axis', value='price',
    clearable = False, data = numerical_columns)
scatter_color_dd = dmc.Select(label = 'Category for color', id='scatter_color_axis', value='carbody',
    clearable = False, data = categorical_columns)
numerical_dd = dmc.Select(label = 'Select a numerical attribute to distribute',id='numerical_axis_histbox', value = 'price', 
                            clearable = False, data = numerical_columns)
categorical_dd = dmc.Select(label = 'Select a categorical atribute to divide the data', id='categorical_axis_histbox',value='carbody', 
                            clearable = False, data = categorical_columns)

## Layout
app.layout = dmc.Container([
    dmc.Title('Car Price Visualization', align = 'center'),
    dmc.Text('This is a simple visualization of data from different types of cars, sorted by many properties. This tool is designed to have a deep understanding of the data at hand. Enjoy!'),
    dmc.Text('For the first graphs, I chose to have a scatter plot between the many numerical attributes of each car, acompanied by a heatmap of the correlation of each pair of attributes, so it´s more easy to explore those values.'),
    html.Br(),
    dmc.Grid([
        dmc.Col([
            dmc.Grid([
                dmc.Col([scatter_x_dd], span = 4),
                dmc.Col([scatter_y_dd], span = 4),
                dmc.Col([scatter_color_dd], span = 4)
            ], grow = True),
            dcc.Graph(figure = create_scatter_graph(), id = 'scatter_plot')
        ], span = 6),
        dmc.Col([
            dmc.Text('Correlation between numerical attributes'),
            dcc.Graph(figure = create_heatmap(), id = 'corr_heatmap_plot')
        ], span = 6),
        dmc.Text('Now for this segment I wanted to see how the data is distributed allong the many categories in wich it´s divided, for example are sedans in general termns more costly than hunchbacks? So in this part you have a distribution histogram distributed by a numerical attribute and divided in colors by the category, and for the other part a boxplot chart selected by category' ),
        dmc.Col([categorical_dd], span = 6),
        dmc.Col([numerical_dd], span = 6),
        dmc.Col([
            dcc.Graph(figure = create_histogram(), id = 'histogram_plot')
        ], span = 6),
        dmc.Col([
            dcc.Graph(figure = create_boxplot(), id = 'box_plot')
        ], span = 6)
    ],gutter = 'xl'),
    dmc.Text('Created by Joaquín Palacios. Data extracted from Kaggle', align = 'center')
], fluid=True)
## Callbacks

@callback(Output('scatter_plot','figure'),
          [Input('scatter_x_axis','value'),Input('scatter_y_axis','value'),Input('scatter_color_axis','value')])
def update_scatter(x_axis, y_axis,colortype):
    return create_scatter_graph(x_axis, y_axis,colortype)

@callback(Output('histogram_plot','figure'),
          [Input('numerical_axis_histbox','value'),Input('categorical_axis_histbox','value')])
def update_histogram(x_axis, color_on):
    return create_histogram(x_axis, color_on)

@callback(Output('box_plot','figure'),
          [Input('categorical_axis_histbox','value'), Input('numerical_axis_histbox', 'value')])
def update_boxplot(x_axis,y_axis):
    return create_boxplot(x_axis, y_axis)

## Run the App
if __name__ == '__main__':
    app.run(debug=True)