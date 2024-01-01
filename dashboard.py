import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL

# Flask app
server = dash.Dash(__name__)
app = server.server  # Get the Flask app from the Dash app

# Configure MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sahajmarg'
app.config['MYSQL_DB'] = 'tyroo'

# Create MySQL instance
mysql = MySQL(app)

# Define layout
server.layout = html.Div(children=[
    html.H1(children='Inventory Dashboard'),

    dcc.DatePickerRange(
        id='date-picker-range',
        start_date='1/1/2016',
        end_date='6/6/2017',
        display_format='DD/MM/YYYY'
    ),

    dcc.Graph(
        id='sales-chart',
        figure={},
        style={'height': '700px', 'width': '1000px'}
    ),
    html.Div([
        dcc.Dropdown(
            id='product-dropdown',
            multi=False,
            placeholder='Select a product'
        ),
        dcc.Graph(
            id='selected-product-sales-chart',
            figure={}
        ),
    ]),
])
# Callback to update the chart based on date range
@server.callback(
    Output('sales-chart', 'figure'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_chart(start_date, end_date):
    # Get data from MySQL database
    cur = mysql.connection.cursor()
    query = f"SELECT sales.Brand,sales.Description,sales.SalesQuantity, sales.SalesDollars, sales.SalesDate, sales.Volume FROM tyroo.sales WHERE SalesDate BETWEEN '{start_date}' AND '{end_date}'"
    cur.execute(query)
    data = cur.fetchall()
    cur.close()

    # Create a DataFrame
    df = pd.DataFrame(data, columns=['Brand','Description', 'SalesQuantity', 'SalesDollars', 'SalesDate', 'Volume'])

    # Create a bar chart
    fig = {
        'data': [
            {'x': df['Description'], 'y': df['SalesDollars'], 'type': 'bar', 'name': 'Sales'},
        ],
        'layout': {
            'title': f'Sales Overview ({start_date} to {end_date})',
            'xaxis': {'title': 'Product', 'automargin': True, 'tickangle': -45},  # Rotate x-axis labels
            'yaxis': {'title': 'Sales in Dollars'},
            'margin': {'l': 50, 'r': 50, 't': 50, 'b': 100},
        }
    }

    return fig

def update_product_dropdown_options(start_date, end_date):
    # Get data from MySQL database
    cur = mysql.connection.cursor()
    query = f"SELECT DISTINCT Description FROM tyroo.sales WHERE SalesDate BETWEEN '{start_date}' AND '{end_date}'"
    cur.execute(query)
    data = cur.fetchall()
    cur.close()

    # Debug print to check the retrieved data
    print("Retrieved data:", data)

    # Create a list of product options for the dropdown
    product_options = [{'label': product[0], 'value': product[0]} for product in data]

    # Debug print to check the generated options
    print("Dropdown options:", product_options)

    return product_options


# Callback to update the second chart based on selected product and date range
@server.callback(
    Output('selected-product-sales-chart', 'figure'),
    [Input('product-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)

def update_selected_product_chart(selected_product, start_date, end_date):
    # Get data for the selected product from MySQL database
    cur = mysql.connection.cursor()
    query = f"SELECT sales.SalesDate, sales.SalesQuantity FROM tyroo.sales WHERE Description = '{selected_product}' AND SalesDate BETWEEN '{start_date}' AND '{end_date}'"
    cur.execute(query)
    data = cur.fetchall()
    cur.close()

    # Create a DataFrame for the selected product
    selected_product_df = pd.DataFrame(data, columns=['SalesDate', 'SalesQuantity'])

    # Create a line chart for the selected product
    selected_product_fig = {
        'data': [
            {'x': selected_product_df['SalesDate'], 'y': selected_product_df['SalesQuantity'], 'type': 'line', 'name': f'Sales - {selected_product}'},
        ],
        'layout': {
            'title': f'Sales Overview for {selected_product} ({start_date} to {end_date})',
            'xaxis': {'title': 'Sales Date'},
            'yaxis': {'title': 'Sales Quantity'},
        }
    }

    return selected_product_fig

if __name__ == '__main__':
    server.run_server(debug=True)
