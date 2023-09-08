# name is app.py so api can be start with `flask run` command without `--app <api name>`
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

print(f'=={__name__}==')
app = Flask(__name__)
CORS(app)  # enables CORS for all routes
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/dbname'
db = SQLAlchemy(app)


class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    details = db.Column(db.Text)


@app.route('/api/test')
def test_api():
    return '<p>Test successful!</p>'


@app.route('/api/businesses', methods=['POST'])
def create_businesses():
    # get data from db for location of business markers
    data = request.get_json()
    new_business = Business(
        name=data['name'],
        latitude=data['longitude'],
        details=data['details'],
    )
    db.session.add(new_business)
    db.session.commit()

    return jsonify({'message': 'business created', 'id': new_business.id}), 201


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
