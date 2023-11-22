# name is app.py so api can be start with `flask run` command without `--app <api name>`
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
import traceback

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
    state = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    zip = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(255))
    instagram = db.Column(db.String(100))
    facebook = db.Column(db.String(100))
    x = db.Column(db.String(100))
    website = db.Column(db.String(255))
    # additional info
    offers_mugs = db.Column(db.Boolean())
    accepts_personal_mug = db.Column(db.Boolean())
    wifi = db.Column(db.Boolean())
    work_friendly = db.Column(db.Boolean())
    sufficient_outlets = db.Column(db.Boolean())
    description = db.Column(db.Text())
    submitter_name = db.Column(db.String(255), nullable=False)
    submitter_email = db.Column(db.String(100), nullable=False)
    message_to_admin = db.Column(db.Text())
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())


@app.route('/api/test')
def test_api():
    return jsonify({'success': True, 'data': 'some test data'}), 200


@app.route('/api/businesses/', methods=['GET'])
@app.route('/api/businesses/<filters>', methods=['GET'])
def get_businesses(filters=None):
    print(f'==filters {filters}')
    try:
        if filters is not None:
            filters_map = {
                'offersMugs': 'offers_mugs',
                'acceptsPersonalMug': 'accepts_personal_mug',
                'wifi': 'wifi',
                'workFriendly': 'work_friendly',
                'outlets': 'outlets',
            }
            parsed_filters = [filters_map.get(filter_value, filter_value) for filter_value in filters.split(',')]
            filter_conditions = [getattr(Business, filter_column) == 1 for filter_column in parsed_filters]
            # asterisk acts as a spread operator to spread out the filter conditions to be implicitly anded together
            businesses = Business.query.filter(*filter_conditions).all()
        else:
            businesses = Business.query.all()

        return jsonify([{
            'id': b.id,
            'name': b.name,
            'offers_mugs': b.offers_mugs,
            'accepts_personal_mug': b.accepts_personal_mug,
            'wifi': b.wifi,
            'work_friendly': b.work_friendly,
            'sufficient_outlets': b.sufficient_outlets,
            'lat': b.latitude,
            'lng': b.longitude,
        } for b in businesses
        ]), 200
    except Exception as e:
        return jsonify({'message': f'Error occurred: {str(e)}'}), 400


@app.route('/api/businesses/<int:id>', methods=['GET'])
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
            'state': business.state,
            'country': business.country,
            'zip': business.zip,
            'phone': business.phone,
            'email': business.email,
            'instagram': business.instagram,
            'facebook': business.facebook,
            'x': business.x,
            'website': business.website,
            'offers_mugs': business.offers_mugs,
            'accepts_personal_mug': business.accepts_personal_mug,
            'wifi': business.wifi,
            'work_friendly': business.work_friendly,
            'sufficient_outlets': business.sufficient_outlets,
            'description': business.description,
            'lat': business.latitude,
            'lng': business.longitude,
        }), 200
    except Exception as e:
        return jsonify({'message': f'Error occurred: {str(e)}'}), 400


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
            state=data['state'],
            country=data['country'],
            zip=data['zip'],
            phone=data['phone'],
            email=data['email'],
            instagram=data['instagram'],
            facebook=data['facebook'],
            x=data['x'],
            website=data['website'],
            # additional info
            offers_mugs=data['offers_mugs'],
            accepts_personal_mug=data['accepts_personal_mug'],
            wifi=data['wifi'],
            work_friendly=data['work_friendly'],
            sufficient_outlets=data['sufficient_outlets'],
            description=data['description'],
            submitter_name=data['submitter_name'],
            submitter_email=data['submitter_email'],
            message_to_admin=data['message_to_admin'],
            latitude=data['lat'],
            longitude=data['lng'],
        )
        db.session.add(new_business)
        db.session.commit()
        return jsonify({'message': 'Business successfully saved', 'business_name': new_business.name}), 200
    except Exception as e:
        traceback.print_exc()
        db.session.rollback()
        return jsonify({'message': f'Error occurred: {str(e)}'}), 400


@app.route('/api/businesses/<int:id>', methods=['PUT'])
def update_business(id):
    try:
        business = Business.query.get_or_404(id)
        updated_data = request.get_json()
        print(f'==updated_data {updated_data}')
        for key, value in updated_data.items():
            if hasattr(business, key):
                setattr(business, key, value)
        db.session.commit()
        return jsonify({'message': 'Business successfully updated', 'business_name': business.name}), 200
    except Exception as e:
        traceback.print_exc()
        db.session.rollback()
        return jsonify({'message': f'Error occurred: {str(e)}'}), 400
