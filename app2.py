import base64
import io
import requests

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
        html.H6('Load Calibration and Sample data:'),
        dcc.Upload(
            id='upload-calibration',
            children=html.Button('Calibration'),
            multiple=False
        ),
        html.H3('Fetching Sample data from Notion API')
    ], width=3, style={'padding': '20px'}),

    # Column for output graphs and data table arranged in Bootstrap tabs
    dbc.Col([
        dbc.Tabs([
            dbc.Tab(label="Modelling", children=[
                html.H6('Absorptivity coefficient as a fuction of wavelengths per each dilusion level'),
                html.Div(
                    [dcc.Graph(id=f'output-data-upload-{i}', 
                               style={'width': '25%', 'display': 'inline-block'}) 
                     for i in range(9)],
                    style={'display': 'flex', 'flex-wrap': 'wrap'}
                ),
            ]),
            dbc.Tab(label="Parsed data", children=[
                dash_table.DataTable(id='parsed-table'),
            ]),
            dbc.Tab(label="Output", children=[
                dash_table.DataTable(id='calibration-table'),
            ])
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
    [Output(f'output-data-upload-{i}', 'figure') for i in range(9)],
    [Output('calibration-table', 'data'), Output('calibration-table', 'columns')],
    [Output('parsed-table', 'data'), Output('parsed-table', 'columns')],
    # Inputs
    [Input('upload-calibration', 'contents')],
    # States
    [State('upload-calibration', 'filename')]
)
def update_output(calib_contents, calib_filename):
    """Update the output plot area and table based on the uploaded file."""
    if calib_contents is not None:
        # Read the calibration file 
        calib = parse_contents(calib_contents, calib_filename)
        
        #print(calib)
        # Getting data from Notion API
        # API Token and Database ID for Samples
        api_token = 'secret_jKETolQ4fuWdOb8pwLBwyV1If01N1UhMbeJz8MBNWkJ'
        database_id = '558261863d3b40d2a2d403748079e37f'

        # The API test URL for querying a database
        url = f'https://api.notion.com/v1/databases/{database_id}/query'

        # Headers for authentication and setting the Notion version
        headers = {
            'Authorization': f'Bearer {api_token}',
            'Notion-Version': '2022-06-28',  
            'Content-Type': 'application/json'
        }

        # Make a POST request to query the database
        response = requests.post(url, headers=headers)

        # Check if the request is successful
        if response.status_code == 200:
            data = response.json()

            # Processing the JSON data into a DataFrame
            rows = []
            for item in data['results']:
                # Extracting and processing the data
                row = {
                    'Download URL': item['properties']['Download URL']['url'],
                    'Sample Type': item['properties']['Sample type']['select']['name'],
                    'Client Name': item['properties']['Client']['select']['name'],
                }
                rows.append(row)

            # Createing a DataFrame
            sample_db = pd.DataFrame(rows)
            #print(sample_db)  # Display the DataFrame
            #print(type(sample_db))
        else:
            print(f'Failed to retrieve data: {response.status_code}')

        
        # Isolating the triplets based on dilusion level and averaging the absorbance
        calib_avg = calib.groupby(['Sample', 'Dilution']).mean(numeric_only=True)
        
        # Calculating the Coeficient of absorption (E)
        calib_coef = calib_avg.mul(2.302585)
        print(calib_coef)

        # Getting the value of E that maximizes the absorption
        calib_coef_max = calib_coef.max(axis = 1)
        print(calib_coef_max)

        # Getting representative wavelength for each dilution
        calib_coef_idmax = calib_coef.idxmax(axis=1)
        print(calib_coef_idmax)
        print(type(calib_coef_idmax))
        
        # Calculating pigment concentration for sample data
        # First we get the effective wavelength for the specific dilution 

        from io import StringIO

        # Get the url of the CSV file
        file_url = sample_db.loc[0][0]

        # Use requests to get the content
        r = requests.get(file_url, verify=False)  
        data = StringIO(r.text)

        # R
        sample = pd.read_csv(data)
        
        # Subset metadata
        sample_results = sample[['Sample', 'Dilution']]
        
        # Empty container for the results
        sample_contents = []
            
        # Calculating the sample contents ---> fails
        #for i in range(len(sample)):
        #    dilution = sample.at[i,'Dilution']
        #    print(dilution)
        #    if sample.at[i,"Sample"] == 'Blank':
                
        #        sample_contents.append(sample.iloc[i, calib_coef_idmax[('Blank', dilution)]] / 
        #                               calib_coef_max.loc[('Blank', dilution)])
        #    else:
        #        print(calib_coef_idmax[('S1', dilution)])
        #        print(sample.at[i, calib_coef_idmax[('S1', dilution)]])
        #        sample_contents.append(sample.iloc[i, calib_coef_idmax[('S1', dilution)]] / calib_coef_max.loc[('S1', dilution)])
        #sample_results = sample_results.assign(Pigment_concentration = sample_contents)
        #print(sample_results)
        #print(sample_contents)


        # Converting coefieicent values to Dataframe for pltting 
        calib_coef_max = calib_coef_max.to_frame()
        calib_coef_idmax = calib_coef_idmax.to_frame()

        # Create multiple figures to show the response of coeficient to wavelength
        figures = []
        for i in range(9):
            fig = go.Figure(data=[
                go.Scatter(x=list(calib_coef.columns), 
                           y=calib_coef.iloc[i,], mode='lines')
            ])
            fig.update_layout(margin=dict(l=20, r=20, t=20, b=20), 
                              title=f'Coeficient of Absorbance (M−1⋅cm−1 ) {str(calib_coef.index[i])}',
                                title_font=dict(size=9))
            figures.append(fig)

        # Prepare data for the table
        calib_data = calib.to_dict('records')
        calib_columns = [{'name': col, 'id': col} for col in calib.columns]

        parsed_data = sample_db.to_dict('records')
        parsed_columns = [{'name': col, 'id': col} for col in sample_db.columns]

        return figures + [calib_data, calib_columns, parsed_data, parsed_columns]
        # Return empty figures and data if no file is uploaded
        return [go.Figure() for _ in range(9)] + [[], []]


if __name__ == '__main__':
    app.run_server(debug=True)
