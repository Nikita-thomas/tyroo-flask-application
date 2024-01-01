from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import secrets

app = Flask(__name__)

# Configure Flask app
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:sahajmarg@localhost/INVENTORY'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = secrets.token_hex(16)

# Initialize Flask extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.username}')"
    
#Creating all columns
with app.app_context():
    db.create_all()

from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token

class UserRegistrationResource(Resource):
    def post(self):
        data = request.get_json()
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        new_user = User(username=data['username'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity={'username': data['username']})
        return jsonify(access_token=access_token)
    
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

class UserLoginResource(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()

        if user and bcrypt.check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity={'username': user.username})
            response = jsonify(access_token=access_token)
            response.status_code = 200
            return response
        else:
            response = jsonify({'message': 'Invalid credentials'})
            response.status_code = 401
            return response

class UserLogoutResource(Resource):
    @jwt_required()
    def post(self):
        jwt_token = request.get_json()
        # You can add more logic for logging out if necessary
        response = jsonify({'message': 'Successfully logged out'})
        response.status_code = 200
        return response
    
from flask_restful import Api

api = Api(app)

# Add resources to the API
api.add_resource(UserRegistrationResource, '/register')
api.add_resource(UserLoginResource, '/login')
api.add_resource(UserLogoutResource, '/logout')

if __name__ == '__main__':
    app.run(debug=True)
