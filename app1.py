import base64
import io

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objs as go

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.Div([
        # Calibration file upload
        dcc.Upload(
            id='upload-calibration',
            children=html.Button('Calibration'),
            multiple=False
        ),
        # Sample file upload
        dcc.Upload(
            id='upload-sample',
            children=html.Button('Sample'),
            multiple=False
        ),
    ], style={'width': '30%', 'float': 'left', 'display': 'inline-block'}),

    html.Div([
        # Plot area
        dcc.Graph(id='output-data-upload'),
    ], style={'width': '70%', 'display': 'inline-block', 'float': 'right'}),
])


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
    Output('output-data-upload', 'figure'),
    [Input('upload-calibration', 'contents'),
     Input('upload-sample', 'contents')],
    [State('upload-calibration', 'filename'),
     State('upload-sample', 'filename')]
)
def update_output(calib_contents, sample_contents, calib_filename, sample_filename):
    """Update the output plot area based on the uploaded file."""
    ctx = dash.callback_context
    if not ctx.triggered:
        # No file uploaded yet
        return go.Figure()

    # Determine which button was clicked
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    df = None
    if button_id == 'upload-calibration' and calib_contents is not None:
        df = parse_contents(calib_contents, calib_filename)
    elif button_id == 'upload-sample' and sample_contents is not None:
        df = parse_contents(sample_contents, sample_filename)

    if df is not None:
        # Create a Plotly figure
        fig = go.Figure(data=[
            go.Scatter(x=df[df.columns[0]], y=df[df.columns[1]], mode='markers')
        ])
        fig.update_layout(title='Uploaded Data Visualization')
        return fig
    else:
        return go.Figure()


if __name__ == '__main__':
    app.run_server(debug=True)
