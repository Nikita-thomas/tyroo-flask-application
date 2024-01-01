from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_mysqldb import MySQL
from flask_restful import Resource, Api
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

# Configure MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sahajmarg'
app.config['MYSQL_DB'] = 'tyroo'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:sahajmarg@localhost/tyroo'
# Create MySQL instance
mysql = MySQL(app)
api = Api(app)

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Initialize Flask-JWT-Extended
jwt = JWTManager(app)

# Initialize Flask extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Mock User class for demonstration
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class InventoryResource(Resource):
    @jwt_required
    def get(self):
        # Get all inventory items
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM tyroo.inventory")
        inventory_items = cur.fetchall()
        cur.close()
        return jsonify([{'InventoryID': item[0], 'Store': item[1], 'City': item[2], 'Brand': item[3], 'Description':item[4], 'Size':item[5], 'onHand':item[6], 'Price':item[7], 'startDate':item[8]} for item in inventory_items])
    @jwt_required
    def post(self):
        # Create a new inventory item
        data = request.get_json()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tyroo.inventory (InventoryID, Store, City, Brand, Description, Size, onHand, Price,startDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (data['InventoryID'], data['Store'], data['City'], data['Brand'], data['Description'], data['Size'], data['onHand'], data['Price'], data['startDate']))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Item created successfully'})

class InventoryItemResource(Resource):
    @jwt_required
    def get(self, item_id):
        # Get a specific inventory item by ID
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM tyroo.inventory WHERE InventoryID = %s", (item_id,))
        item = cur.fetchone()
        cur.close()
        return jsonify({'InventoryID': item[0], 'Store': item[1], 'City': item[2], 'Brand': item[3], 'Description':item[4], 'Size':item[5], 'onHand':item[6], 'Price':item[7], 'startDate':item[8]})

    @jwt_required
    def put(self, item_id):
        # Update a specific inventory item by ID
        data = request.get_json()
        cur = mysql.connection.cursor()
        cur.execute("UPDATE tyroo.inventory SET Store=%s, City=%s, Brand=%s, Description=%s, Size=%s, onHand=%s, Price=%s,startDate=%s WHERE InventoryID = %s", (data['Store'], data['City'], data['Brand'], data['Description'], data['Size'], data['onHand'], data['Price'], data['startDate'], item_id))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Item updated successfully'})

    @jwt_required
    def delete(self, item_id):
        # Delete a specific inventory item by ID
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM tyroo.inventory WHERE InventoryID = %s", (item_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Item deleted successfully'})
    
@app.route('/register', methods= ['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity={'username': data['username']})
    return jsonify(access_token=access_token)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()

        if user and bcrypt.check_password_hash(user.password, data['password']):
            login_user(user)
            access_token = create_access_token(identity={'username': user.username})
            response = jsonify(access_token=access_token)
            response.status_code = 200
            return redirect(url_for('inventoryresource'))
        else:
            response = jsonify({'message': 'Invalid credentials'})
            response.status_code = 401
            return response
    return 

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/inventory_dashboard')
@login_required
def inventory_dashboard():
    return jsonify({'message': 'Welcome to the inventory dashboard!'})

api.add_resource(InventoryResource, '/inventory')
api.add_resource(InventoryItemResource, '/inventory/<int:item_id>')

if __name__ == '__main__':
    app.run(debug=True)
