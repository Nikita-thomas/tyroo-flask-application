
from flask import Flask, jsonify, request

app = Flask(__name__)

movies = [
    {"id": 1, "name": "Product A", "quantity": 100, "price": 25.00},
    {"id": 2, "name": "Product B", "quantity": 50, "price": 40.00},
    {"id": 3, "name": "Product C", "quantity": 200, "price": 15.00},
    {"id": 4, "name": "Product D", "quantity": 75, "price": 30.00},
    {"id": 5, "name": "Product E", "quantity": 120, "price": 20.00}
]

@app.route('/movies')
def hello():
    return jsonify(movies)

@app.route('/movies', methods=['POST'])
def add_movie():
    movie = request.get_json()
    movies.append(movie)
    return {'id': len(movies)}, 200

@app.route('/movies/<int:index>', methods=['PUT'])
def update_movie(index):
    movie = request.get_json()
    movies[index] = movie
    return jsonify(movies[index]), 200

@app.route('/movies/<int:index>', methods=['DELETE'])
def delete_movie(index):
    movies.pop(index)
    return 'None', 200

app.run()