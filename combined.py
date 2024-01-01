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
app.config['MYSQL_DB'] = 'INVENTORY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:sahajmarg@localhost/INVENTORY'
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
    @jwt_required()
    def get(self):
        # Get all inventory items
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Inventory")
        inventory_items = cur.fetchall()
        cur.close()
        return jsonify([{'ProductID': item[0], 'ProductName': item[1], 'QuantityInStock': item[2], 'UnitPrice': item[3]} for item in inventory_items])

    @jwt_required()
    def post(self):
        # Create a new inventory item
        data = request.get_json()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Inventory (ProductName, QuantityInStock, UnitPrice) VALUES (%s, %s, %s)", (data['ProductName'], data['QuantityInStock'], data['UnitPrice']))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Item created successfully'})

class InventoryItemResource(Resource):
    @jwt_required()
    def get(self, item_id):
        # Get a specific inventory item by ID
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Inventory WHERE ProductID = %s", (item_id,))
        item = cur.fetchone()
        cur.close()
        return jsonify({'ProductID': item[0], 'ProductName': item[1], 'QuantityInStock': item[2], 'UnitPrice': item[3]})

    @jwt_required()
    def put(self, item_id):
        # Update a specific inventory item by ID
        data = request.get_json()
        cur = mysql.connection.cursor()
        cur.execute("UPDATE Inventory SET ProductName = %s, QuantityInStock = %s, UnitPrice = %s WHERE ProductID = %s", (data['ProductName'], data['QuantityInStock'], data['UnitPrice'], item_id))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Item updated successfully'})

    @jwt_required()
    def delete(self, item_id):
        # Delete a specific inventory item by ID
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Inventory WHERE ProductID = %s", (item_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Item deleted successfully'})
    
@app.route('/register', methods= ['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
    new_user = User(username=request.form['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity={'username': request.form['username']})
    return jsonify(access_token=access_token)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        user = User.query.filter_by(username=request.form['username']).first()

        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            login_user(user)
            access_token = create_access_token(identity={'username': user.username})
            response = jsonify(access_token=access_token, redirect= url_for('inventory'))
            response.status_code = 200
            return redirect(url_for('inventory_dashboard'))
        else:
            response = jsonify({'message': 'Invalid credentials'})
            response.status_code = 401
            return response
        '''
        user = User.query.filter_by(username=request.form['username']).first()

        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('inventory_dashboard'))
        '''
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
