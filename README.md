# Flask Based Web-Application

Building a Flask-based RESTful API for user authentication, inventory management, and reporting dashboard

## Table of Contents

- [Installations](#installations)
- [User-Authentication](#user-authentication)
- [Inventory-Management](#inventory-management)
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
## Data 
The sales and inventory data I used for testing was from the following Kaggle database - [Bhanu Pratap Biswas - Inventory Analysis Case Study](https://www.kaggle.com/datasets/bhanupratapbiswas/inventory-analysis-case-study?select=BegInvFINAL12312016.csv) 
For the purpose of testing, I used only relevant parts of the dataset. I imported the csv's into tables in our schema
![image](https://github.com/Nikita-thomas/tyroo-flask-application/assets/97882049/3e8d9898-f947-4cbd-a27c-6b698ef51393)
*Snapshot of sales data*
The sales and inventory data had a cumulative of 10,000 entries. 

### Connecting MySQL with flask-application 
with the following package 
```bash
from flask_sqlalchemy import SQLAlchemy
```
## User-Authentication 
I mainted a User table to store and check user information like username, password, account creation dates etc. Used bcrypt for hashing passwords 
and generating access tokens with the help of flask_jwt_extended 
![image](https://github.com/Nikita-thomas/tyroo-flask-application/assets/97882049/b9aeeac8-5025-4ff0-bac4-90b1cef80563)
*User information stored in our database. this would also allow for blacklisting of certain logins.*

@jwt_required was used in the CRUD operations to ensure valid tokens for performing any operations.  
![image](https://github.com/Nikita-thomas/tyroo-flask-application/assets/97882049/b533f72e-ebef-4f14-ab7d-66ee7d557432)
*access token generated and returned for successful registeration*

![image](https://github.com/Nikita-thomas/tyroo-flask-application/assets/97882049/fb712643-f1cc-4369-9e35-e09831d28e93)
*successful login*
![image](https://github.com/Nikita-thomas/tyroo-flask-application/assets/97882049/5cf1dc6f-79b8-4c23-b4ec-c05fb6a0218d)
*401 error given for invalid credentials*

## Inventory-Management 
creating methods for PUT, GET, POST, DELETE to Update, Read, Create and Delete elemnets in the inventory database respetively. 
This was done by creating a MySQL instance for the schema and executing different queries and fetching the response. For each method, an appropriate response (such as - "item created successfully") or the appropriate error code was displayed. 

In order to test different API methods and feed JSON responses, POSTMAN was used. 
![image](https://github.com/Nikita-thomas/tyroo-flask-application/assets/97882049/0a1e163f-a869-462d-93cc-a723236589bb)
*GET Method* 
![image](https://github.com/Nikita-thomas/tyroo-flask-application/assets/97882049/40300555-93a0-48b7-955e-6235ccb6afcc)
*to get a specific iventory item*
![image](https://github.com/Nikita-thomas/tyroo-flask-application/assets/97882049/3011dff7-7ffa-4fc3-9dc0-27593bf74ed4)
*creating a new inventory item*
![image](https://github.com/Nikita-thomas/tyroo-flask-application/assets/97882049/8f2fd948-e7d0-49cb-9034-79e49ec16ef2)
*which subsequently gets updated in the SQL schema*

![image](https://github.com/Nikita-thomas/tyroo-flask-application/assets/97882049/525af292-2434-49a2-a0ce-f68efe761270)
*Updating specific inventory items* 
![image](https://github.com/Nikita-thomas/tyroo-flask-application/assets/97882049/ae4564e3-da57-41bf-b70b-d601d0d710a5)
*and Deleting it as well*

## Dashboard 
The dashboard features an interactive date picker. It uses the Dash framework and establishes a connection with the 'sales' table of our schema for updated information. 
![image](https://github.com/Nikita-thomas/tyroo-flask-application/assets/97882049/7badbeeb-ab38-4fb9-b066-8481ace742ad)
*The bar chart provides an overall sales summary, while the line chart displays sales quantity over time for a selected product.*
![image](https://github.com/Nikita-thomas/tyroo-flask-application/assets/97882049/65a2f7c1-619d-41cd-878e-2fd4c29e3ff9)
all plots on the dashboard are interactive

