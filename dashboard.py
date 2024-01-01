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
app.config['MYSQL_DB'] = 'INVENTORY'

# Create MySQL instance
mysql = MySQL(app)

# Define layout
server.layout = html.Div(children=[
    html.H1(children='Inventory Dashboard'),

    dcc.DatePickerRange(
        id='date-picker-range',
        start_date='2022-01-01',
        end_date='2022-12-31',
        display_format='YYYY-MM-DD'
    ),

    dcc.Graph(
        id='inventory-chart',
        figure={}
    ),
])

# Callback to update the chart based on date range
@server.callback(
    Output('inventory-chart', 'figure'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_chart(start_date, end_date):
    # Get data from MySQL database
    cur = mysql.connection.cursor()
    query = f"SELECT * FROM Inventory WHERE Date BETWEEN '{start_date}' AND '{end_date}'"
    cur.execute(query)
    data = cur.fetchall()
    cur.close()

    # Create a DataFrame
    df = pd.DataFrame(data, columns=['ProductID', 'ProductName', 'QuantityInAtock', 'UnitPrice', 'Date'])

    # Create a bar chart
    fig = {
        'data': [
            {'x': df['ProductName'], 'y': df['QuantityInAtock'], 'type': 'bar', 'name': 'Quantity'},
        ],
        'layout': {
            'title': f'Inventory Overview ({start_date} to {end_date})',
            'xaxis': {'title': 'Product'},
            'yaxis': {'title': 'Quantity'},
        }
    }

    return fig

if __name__ == '__main__':
    server.run_server(debug=True)
