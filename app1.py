from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_restful import Resource, Api


app = Flask(__name__)

# Configure MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sahajmarg'
app.config['MYSQL_DB'] = 'INVENTORY'

# Create MySQL instance
mysql = MySQL(app)
api = Api(app)

class InventoryResource(Resource):
    def get(self):
        # Get all inventory items
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Inventory")
        inventory_items = cur.fetchall()
        cur.close()
        return jsonify([{'ProductID': item[0], 'ProductName': item[1], 'QuantityInAtock': item[2], 'UnitPrice': item[3]} for item in inventory_items])

    def post(self):
        # Create a new inventory item
        data = request.get_json()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Inventory (ProductName, QuantityInStock, UnitPrice) VALUES (%s, %s, %s)", (data['ProductName'], data['QuantityInStock'], data['UnitPrice']))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Item created successfully'})

class InventoryItemResource(Resource):
    def get(self, item_id):
        # Get a specific inventory item by ID
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Inventory WHERE ProductID = %s", (item_id,))
        item = cur.fetchone()
        cur.close()
        return jsonify({'ProductID': item[0], 'ProductName': item[1], 'QuantityInAtock': item[2], 'UnitPrice': item[3]})

    def put(self, item_id):
        # Update a specific inventory item by ID
        data = request.get_json()
        cur = mysql.connection.cursor()
        cur.execute("UPDATE Inventory SET ProductName = %s, QuantityInStock = %s, UnitPrice = %s WHERE ProductID = %s", (data['ProductName'], data['QuantityInStock'], data['UnitPrice'], item_id))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Item updated successfully'})

    def delete(self, item_id):
        # Delete a specific inventory item by ID
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Inventory WHERE ProductID = %s", (item_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Item deleted successfully'})

api.add_resource(InventoryResource, '/inventory')
api.add_resource(InventoryItemResource, '/inventory/<int:item_id>')

app.run()
