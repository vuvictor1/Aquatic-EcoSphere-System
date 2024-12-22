# Dash Data Visualization App

## Overview
This Dash application visualizes data from the Gapminder dataset, allowing users to explore various metrics such as population, life expectancy, and GDP per capita across different continents. The app features an interactive layout with radio buttons for user input and a data table for displaying the dataset.

## Features
- **Interactive Graphs**: Users can select different metrics to visualize through a histogram.
- **Data Table**: Displays the Gapminder dataset with pagination.
- **Responsive Design**: The layout adjusts to different screen sizes.

## Technologies Used
- **Dash**: A Python framework for building web applications.
- **Pandas**: A library for data manipulation and analysis.
- **Plotly Express**: A library for creating interactive visualizations.
- **Dash Mantine Components**: A library for enhanced UI components in Dash applications.

## Installation
To run this application, ensure you have the following libraries installed. You can install them using pip:

```bash
pip install -r requirements.txt
```

## Usage
1. Clone the repository or download the app.py script.
2. Run the application using the following command:
```bash
python app.py
```
3. Open a web browser and navigate to `http://127.0.0.1:8050


## Code Explanation
 - Data Loading: The dataset is loaded from a public URL usingPandas.
 - App Initialization: The Dash app is initialized and the layout is defined using Dash Mantine components.
 - User Input: A radio button group allows users to select which metric to visualize.
 - Data Table: Displays the dataset with a specified number of rows per page.
 - Graph Update: A callback function updates the graph based on the selected metric.

 ```python
# Load the dataset
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# Initialize the Dash application
app = Dash()

# Define the layout
app.layout = dmc.Container([
    dmc.Title('My First App with Data, Graph, and Controls', color="blue", size="h3"),
    dmc.RadioGroup([...]),  # Radio buttons for user input
    dmc.Grid([...]),  # Grid layout for data table and graph
], fluid=True)

# Callback to update the graph
@callback(
    Output(component_id='graph-placeholder', component_property='figure'),
    Input(component_id='my-dmc-radio-item', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
    return fig
 ```