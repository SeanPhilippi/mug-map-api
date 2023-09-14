# name is app.py so api can be start with `flask run` command without `--app <api name>`
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

# load .env which specifies to put the app in debug mode, helpful for development phase
load_dotenv()

print(f'=={__name__}==')
app = Flask(__name__)
CORS(app)  # enables CORS for all routes

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)


class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    details = db.Column(db.Text)


@app.route('/api/test')
def test_api():
    return jsonify({'success': True, 'data': 'some test data'}), 200


@app.route('/api/businesses', methods=['POST'])
def create_business():
    # get data from db for location of business markers
    data = request.get_json()
    print(f'==data {data}')
    # new_business = Business(
    #     name=data['name'],
    #     latitude=data['longitude'],
    #     details=data['details'],
    # )
    # db.session.add(new_business)
    # db.session.commit()

    # return jsonify({'message': 'business created', 'id': new_business.id}), 201
    # return jsonify(data), 200
    return data, 200


@app.route('/api/businesses', methods=['GET'])
def get_businesses():
    # get data from db for location of business markers
    businesses = Business.query.all()
    return jsonify([{
        'id': b.id,
        'name': b.name,
        'latitude': b.latitude,
        'longitude': b.longitude,
    } for b in businesses
    ]), 200


@app.route('/api/business/<int:id>', methods=['GET'])
def get_business_data(id):
    # get data from db for a specific business for details card
    business = Business.query.get_or_404(id)
    return jsonify({
        'id': business.id,
        'name': business.name,
        'latitude': business.latitude,
        'longitude': business.longitude,
        'details': business.details,
    }), 200
