# Import necessary libraries
from dash import Dash, dash_table, dcc, callback, Output, Input
import pandas as pd  # Importing pandas for data manipulation
import plotly.express as px  # Importing Plotly Express for creating visualizations
import dash_mantine_components as dmc
from sqlalchemy import create_engine  # Import SQLAlchemy's create_engine
from datetime import datetime

# Step 1: Create a SQLAlchemy engine
db_config = {
    'user': 'root',
    'password': 'ZAJDlxblTEhBCDhOsvxwwQDXjWWCfPoR',
    'host': 'autorack.proxy.rlwy.net',
    'port': 22542,
    'database': 'railway'
}
# Create the connection string
connection_string = f"mysql+mysqlconnector://{db_config['user']}:{
    db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
engine = create_engine(connection_string)

# Step 2: Query the table
query = "SELECT * FROM sensor_data"  # Replace with your table name
df = pd.read_sql(query, engine)  # Use the SQLAlchemy engine

# Step 3: Close the engine connection (optional, as it is managed by SQLAlchemy)
engine.dispose()

# Step 4: Convert the timestamp column to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Initialize the Dash application
app = Dash()

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
        start_date=df['timestamp'].min().date(),
        end_date=df['timestamp'].max().date(),
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
], fluid=True)  # Set the container to be fluid

# Define a callback function to update the graph and table based on user input


@callback(
    Output(component_id='graph-placeholder', component_property='figure'),
    Output(component_id='data-table', component_property='data'),
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
