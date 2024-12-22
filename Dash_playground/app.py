# Import necessary libraries
from dash import Dash, dash_table, dcc, callback, Output, Input
import pandas as pd  # Importing pandas for data manipulation
import plotly.express as px  # Importing Plotly Express for creating visualizations
import dash_mantine_components as dmc
from datetime import datetime

# Load the dataset from a local file or a public URL into a pandas DataFrame
df = pd.read_csv('sensor_data.csv')  # Ensure the path is correct

# Convert the timestamp column to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Initialize the Dash application
app = Dash()

# Define the layout of the app
app.layout = dmc.Container([  # Create a container for the app layout
    dmc.Title('Sensor Data Visualization',  # Title of the app
              color="blue", size="h3"),  # Set title color and size
    dmc.RadioGroup(  # Create a radio button group for user input
        # Create radio buttons for turbidity, temperature, and total dissolved solids
        [dmc.Radio('Turbidity', value='turbidity'),
         dmc.Radio('Temperature', value='temperature'),
         dmc.Radio('Total Dissolved Solids', value='total dissolved solids')],
        id='sensor-type-radio',  # Unique ID for the radio group
        value='turbidity',  # Default selected value
        size="sm"  # Size of the radio buttons
    ),
    dcc.DatePickerRange(  # Date picker for selecting date range
        id='date-picker-range',
        # Set the start date to the minimum date in the dataset
        start_date=df['timestamp'].min().date(),
        # Set the end date to the maximum date in the dataset
        end_date=df['timestamp'].max().date(),
        display_format='YYYY-MM-DD'  # Format for displaying the date
    ),
    dmc.Grid([  # Create a grid layout for organizing components
        dmc.Col([  # First column for the data table
            dash_table.DataTable(
                id='data-table',  # Add ID for the data table
                # Create a data table from the DataFrame
                data=df.to_dict('records'),
                page_size=12,  # Set the number of rows per page
                # Enable horizontal scrolling if needed
                style_table={'overflowX': 'auto'}
            )
        ], span=6),  # This column will take up 6 out of 12 grid spaces
        dmc.Col([  # Second column for the graph
            # Placeholder for the graph, initially empty
            dcc.Graph(figure={}, id='graph-placeholder')
        ], span=6),  # This column will also take up 6 out of 12 grid spaces
    ]),
], fluid=True)  # Set the container to be fluid, allowing it to resize with the window

# Define a callback function to update the graph and table based on user input


@callback(
    Output(component_id='graph-placeholder', component_property='figure'),
    # Output for the data table
    Output(component_id='data-table', component_property='data'),
    # Input from the radio group
    Input(component_id='sensor-type-radio', component_property='value'),
    Input(component_id='date-picker-range',
          component_property='start_date'),  # Start date input
    Input(component_id='date-picker-range',
          component_property='end_date')  # End date input
)
# Function to update the graph and table
def update_graph(selected_sensor, start_date, end_date):
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
