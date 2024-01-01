# Flask Based Web-Application

Building a Flask-based RESTful API for user authentication, inventory management, and reporting dashboard

## Table of Contents

- [Installations](#installations)
- [User Authentication](#userauthentication)
- [Inventory Management](#inventorymanagement)
- [Dashboard](#Dashboard)

## Installations
Creating a virtual environment to allow for isolation and security using the following command 

```bash
# Virtual environment creation command
pip install --user pipenv
pipenv install flask

# to enable virtual environment 
pipenv shell
```
after installing the packages in requirements.txt 

### Connecting MySQL with flask-application 
with the following package 
```bash
from flask_sqlalchemy import SQLAlchemy
```
to store and check user information like username, password, account creation dates etc. Used bcrypt for hashing passwords 
and generating access tokens with the help of flask_jwt_extended 

@jwt_required was used in the CRUD operations to ensure valid tokens for performing any operations.  

## Inventory Management 
creating methods for PUT, GET, POST, DELETE to Update, Read, Create and Delete elemnets in the inventory database respetively. 
This was done by creating a MySQL instance for the schema and executing different queries and fetching the response. For each method, an appropriate response (such as - "item created successfully") or the appropriate error code was displayed. 

In order to test different API methods and feed JSON responses, POSTMAN was used. 

## Dashbooard 



