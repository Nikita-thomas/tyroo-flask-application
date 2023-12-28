from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/db_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        new_user = User(username=data['username'], password=data['password'])
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User registered successfully'}

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['username'], password=data['password']).first()
        if user:
            access_token = create_access_token(identity=data['username'])
            return {'access_token': access_token}
        return {'message': 'Invalid credentials'}, 401

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_raw_jwt()['jti']
        # Add the token to the blacklist or perform other token invalidation mechanism
        # For simplicity, let's assume we have a simple set to store the revoked tokens
        revoked_tokens.add(jti)
        return {'message': 'Successfully logged out'}

# Set up the API resources
api = Api(app)
api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
