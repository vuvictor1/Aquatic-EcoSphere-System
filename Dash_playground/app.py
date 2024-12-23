# app.py
from dash import Dash, dash_table, dcc, callback, Output, Input
import pandas as pd  # Importing pandas for data manipulation
import plotly.express as px  # Importing Plotly Express for creating visualizations
import dash_mantine_components as dmc
# Import functions from database.py
from database import get_database_connection, fetch_sensor_data

# Initialize the Dash application
app = Dash()

# Create a database connection
engine = get_database_connection()

# Fetch initial data
df = fetch_sensor_data(engine)

# Get the earliest and latest timestamps
earliest_timestamp = df['timestamp'].min().date()
latest_timestamp = df['timestamp'].max().date()

# Set the end date to the day after the latest timestamp
end_date = latest_timestamp + pd.Timedelta(days=1)

# Define the layout of the app
app.layout = dmc.Container([  # Create a container for the app layout
    dmc.Title('Sensor Data Visualization',  # Title of the app
              color="blue", size="h3"),  # Set title color and size
    dmc.RadioGroup(  # Create a radio button group for user input
        [dmc.Radio('Turbidity', value='turbidity'),
         dmc.Radio('Temperature', value='temperature'),
         dmc.Radio('Total Dissolved Solids', value='total dissolved solids')],
        id='sensor-type-radio',  # Unique ID for the radio group
        value='turbidity',  # Default selected value
        size="sm"  # Size of the radio buttons
    ),
    dcc.DatePickerRange(  # Date picker for selecting date range
        id='date-picker-range',
        start_date=earliest_timestamp,  # Set to the earliest timestamp
        end_date=end_date,  # Set to the day after the latest timestamp
        display_format='YYYY-MM-DD'  # Format for displaying the date
    ),
    dmc.Grid([  # Create a grid layout for organizing components
        dmc.Col([  # First column for the data table
            dash_table.DataTable(
                id='data-table',  # Add ID for the data table
                data=df.to_dict('records'),
                page_size=12,  # Set the number of rows per page
                style_table={'overflowX': 'auto'}
            )
        ], span=6),  # This column will take up 6 out of 12 grid spaces
        dmc.Col([  # Second column for the graph
            dcc.Graph(figure={}, id='graph-placeholder')
        ], span=6),  # This column will also take up 6 out of 12 grid spaces
    ]),
    dcc.Interval(  # Interval component for automatic updates
        id='interval-component',
        interval=5*1*1000,  # Refresh every 15 minutes (in milliseconds)
        n_intervals=0  # Initial value
    ),
    # Button for manual refresh
    dmc.Button("Refresh Data", id='refresh-button')
], fluid=True)  # Set the container to be fluid

# Define a callback function to update the graph and table based on user input


@callback(
    Output(component_id='graph-placeholder', component_property='figure'),
    Output(component_id='data-table', component_property='data'),
    Input(component_id='sensor-type-radio', component_property='value'),
    Input(component_id='date-picker-range', component_property='start_date'),
    Input(component_id='date-picker-range', component_property='end_date'),
    Input('interval-component', 'n_intervals'),  # Input from the interval
    Input('refresh-button', 'n_clicks'))  # Input from the refresh button
def update_graph(selected_sensor, start_date, end_date, n_intervals, n_clicks):
    # Re-fetch data from the database
    df = fetch_sensor_data(engine)  # Use the function from database.py

    # Convert start and end dates to datetime objects
    start_date_dt = pd.to_datetime(start_date)
    end_date_dt = pd.to_datetime(end_date)

    # Filter the DataFrame for the selected sensor type and date range
    filtered_df = df[(df['sensor_type'] == selected_sensor) &
                     (df['timestamp'] >= start_date_dt) &
                     (df['timestamp'] < end_date_dt)]

    # Create a line plot using Plotly Express
    fig = px.line(filtered_df, x='timestamp', y='value', title=f'{
                  selected_sensor.capitalize()} Over Time')

    # Return the figure and the filtered data for the data table
    return fig, filtered_df.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)  # Run the application in debug mode
