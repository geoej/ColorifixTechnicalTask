import base64
import io

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objs as go
import dash_table

# Initialize the Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the app layout with two columns
app.layout = html.Div([
    # Column for data upload with a title
    dbc.Col([
        html.H3('Upload Data'),
        dcc.Upload(
            id='upload-calibration',
            children=html.Button('Calibration'),
            multiple=False
        ),
        dcc.Upload(
            id='upload-sample',
            children=html.Button('Sample'),
            multiple=False
        ),
    ], width=3, style={'padding': '20px'}),

    # Column for output graphs and data table arranged in Bootstrap tabs
    dbc.Col([
        dbc.Tabs([
            dbc.Tab(label="Modelling", children=[
                html.Div(
                    [dcc.Graph(id=f'output-data-upload-{i}', style={'width': '25%', 'display': 'inline-block'}) 
                     for i in range(8)],
                    style={'display': 'flex', 'flex-wrap': 'wrap'}
                ),
            ]),
            dbc.Tab(label="Output", children=[
                dash_table.DataTable(id='calibration-table'),
            ]),
        ]),
    ], width=9, style={'padding': '20px'}),
], className='row')


def parse_contents(contents, filename):
    """Parse CSV file contents uploaded by the user."""
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    if 'csv' in filename:
        # Assume that the user uploaded a CSV file
        return pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    else:
        raise ValueError('File format not supported')


@app.callback(
    [Output(f'output-data-upload-{i}', 'figure') for i in range(8)] +
    [Output('calibration-table', 'data'),
     Output('calibration-table', 'columns')],
    [Input('upload-calibration', 'contents')],
    [State('upload-calibration', 'filename')]
)
def update_output(calib_contents, calib_filename):
    """Update the output plot area and table based on the uploaded file."""
    if calib_contents is not None:
        # Read the calibration file 
        calib = parse_contents(calib_contents, calib_filename)
        
        # Isolating the triplets based on dilusion level and averaging the absorbance
        calib_avg = calib.groupby(['Sample', 'Dilution']).mean(numeric_only=True)
        
        # Calculating the Coeficient of absorption (E)
        calib_coef = calib_avg.mul(2.302585)
        
        # Getting the value of E that maximizes the absorption
        calib_coef_max = calib_coef.max(axis = 1)
        calib_coef_max = calib_coef_max.to_frame()
        print(type(calib_coef_max))

        # Getting representative wavelength for each dilution
        calib_coef_idmax = calib_coef_max.idxmax(axis=1)
        
        # Create multiple figures
        figures = []
        for i in range(9):
            fig = go.Figure(data=[
                go.Scatter(x=list(calib_coef.columns), y=calib_coef.iloc[i,], mode='lines')
            ])
            fig.update_layout(margin=dict(l=20, r=20, t=20, b=20), title=f'Chart {str(calib_coef.index[i])}')
            figures.append(fig)

        # Prepare data for the table
        data = calib.to_dict('records')
        columns = [{'name': col, 'id': col} for col in calib.columns]
        return figures + [data, columns]
    else:
        # Return empty figures and data if no file is uploaded
        return [go.Figure() for _ in range(8)] + [[], []]


if __name__ == '__main__':
    app.run_server(debug=True)
