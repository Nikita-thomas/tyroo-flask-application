from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_restful import Resource, Api


app = Flask(__name__)

# Configure MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sahajmarg'
app.config['MYSQL_DB'] = 'tyroo'

# Create MySQL instance
mysql = MySQL(app)
api = Api(app)

class InventoryResource(Resource):
    def get(self):
        # Get all inventory items
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM tyroo.inventory")
        inventory_items = cur.fetchall()
        cur.close()
        return jsonify([{'InventoryID': item[0], 'Store': item[1], 'City': item[2], 'Brand': item[3], 'Description':item[4], 'Size':item[5], 'onHand':item[6], 'Price':item[7], 'startDate':item[8]} for item in inventory_items])

    def post(self):
        # Create a new inventory item
        data = request.get_json()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tyroo.inventory (InventoryID, Store, City, Brand, Description, Size, onHand, Price,startDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (data['InventoryID'], data['Store'], data['City'], data['Brand'], data['Description'], data['Size'], data['onHand'], data['Price'], data['startDate']))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Item created successfully'})

class InventoryItemResource(Resource):
    def get(self, item_id):
        # Get a specific inventory item by ID
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM tyroo.inventory WHERE InventoryID = %s", (item_id,))
        item = cur.fetchone()
        cur.close()
        return jsonify({'InventoryID': item[0], 'Store': item[1], 'City': item[2], 'Brand': item[3], 'Description':item[4], 'Size':item[5], 'onHand':item[6], 'Price':item[7], 'startDate':item[8]})

    def put(self, item_id):
        # Update a specific inventory item by ID
        data = request.get_json()
        cur = mysql.connection.cursor()
        cur.execute("UPDATE tyroo.inventory SET Store=%s, City=%s, Brand=%s, Description=%s, Size=%s, onHand=%s, Price=%s,startDate=%s WHERE InventoryID = %s", (data['Store'], data['City'], data['Brand'], data['Description'], data['Size'], data['onHand'], data['Price'], data['startDate'], item_id))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Item updated successfully'})

    def delete(self, item_id):
        # Delete a specific inventory item by ID
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM tyroo.inventory WHERE InventoryID = %s", (item_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Item deleted successfully'})

api.add_resource(InventoryResource, '/inventory')
api.add_resource(InventoryItemResource, '/inventory/<path:item_id>')

app.run()
