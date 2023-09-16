# name is app.py so api can be start with `flask run` command without `--app <api name>`
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# load .env which specifies to put the app in debug mode, helpful for development phase
load_dotenv()

print(f'=={__name__}==')
app = Flask(__name__)
CORS(app)  # enables CORS for all routes

# app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
# app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
# app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
# app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'mysql+pymysql://{os.getenv("MYSQL_USER")}:'
    f'{os.getenv("MYSQL_PASSWORD")}@'
    f'{os.getenv("MYSQL_HOST")}/'
    f'{os.getenv("MYSQL_DB")}'
)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# mysql will use plural of this class name as the assumed table to save to
class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address1 = db.Column(db.String(255), nullable=False)
    address2 = db.Column(db.String(255))
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    zip = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(255))
    instagram = db.Column(db.String(100))
    facebook = db.Column(db.String(100))
    x = db.Column(db.String(100))
    website = db.Column(db.String(255))
    offers_mugs = db.Column(db.Boolean())
    wifi = db.Column(db.Boolean())
    work_friendly = db.Column(db.Boolean())
    description = db.Column(db.Text())
    submitter_name = db.Column(db.String(255), nullable=False)
    submitter_email = db.Column(db.String(100), nullable=False)
    message_to_admin = db.Column(db.Text())
    # Assuming latitude and longitude would be floats
    # latitude = db.Column(db.Float())
    # longitude = db.Column(db.Float())


@app.route('/api/test')
def test_api():
    return jsonify({'success': True, 'data': 'some test data'}), 200


@app.route('/api/businesses', methods=['POST'])
def create_business():
    try:
        data = request.get_json()
        print(f'==data {data}')
        new_business = Business(
            name=data['name'],
            address1=data['address1'],
            address2=data['address2'],
            city=data['city'],
            country=data['country'],
            zip=data['zip'],
            phone=data['phone'],
            email=data['email'],
            instagram=data['instagram'],
            facebook=data['facebook'],
            x=data['x'],
            website=data['website'],
            offers_mugs=data['offers_mugs'],
            wifi=data['wifi'],
            work_friendly=data['work_friendly'],
            description=data['description'],
            submitter_name=data['submitter_name'],
            submitter_email=data['submitter_email'],
            message_to_admin=data['message_to_admin'],
            # latitude=data['latitude'],
            # longitude=data['longitude'],
        )
        db.session.add(new_business)
        db.session.commit()
        # return jsonify({'message': 'Record successfully added'}), 200
        return jsonify({'message': 'Business successfully saved', 'business_id': new_business.id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error occurred: {str(e)}'}), 400


@app.route('/api/businesses', methods=['GET'])
def get_businesses():
    try:
        businesses = Business.query.all()
        return jsonify([{
            'id': b.id,
            'name': b.name,
            'address1': b.address1,
            'address2': b.address2,
            'city': b.city,
            'country': b.country,
            'zip': b.zip,
            'phone': b.phone,
            'email': b.email,
            'instagram': b.instagram,
            'facebook': b.facebook,
            'x': b.x,
            'website': b.website,
            'offers_mugs': b.offers_mugs,
            'wifi': b.wifi,
            'work_friendly': b.work_friendly,
            'description': b.description,
            'submitter_name': b.submitter_name,
            'submitter_email': b.submitter_email,
            'message_to_admin': b.message_to_admin,
            # 'latitude': b.latitude,
            # 'longitude': b.longitude,
        } for b in businesses
        ]), 200
    except Exception as e:
        return jsonify({'message': f'Error occurred: {str(e)}'}), 400


@app.route('/api/business/<int:id>', methods=['GET'])
def get_business_data(id):
    # get data from db for a specific business for details card
    try:
        business = Business.query.get_or_404(id)
        return jsonify({
            'id': business.id,
            'name': business.name,
            'address1': business.address1,
            'address2': business.address2,
            'city': business.city,
            'country': business.country,
            'zip': business.zip,
            'phone': business.phone,
            'email': business.email,
            'instagram': business.instagram,
            'facebook': business.facebook,
            'x': business.x,
            'website': business.website,
            'offers_mugs': business.offers_mugs,
            'wifi': business.wifi,
            'work_friendly': business.work_friendly,
            'description': business.description,
            'submitter_name': business.submitter_name,
            'submitter_email': business.submitter_email,
            'message_to_admin': business.message_to_admin,
            # 'latitude': business.latitude,
            # 'longitude': business.longitude,
        }), 200
    except Exception as e:
        return jsonify({'message': f'Error occurred: {str(e)}'}), 400
