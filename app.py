import os
import time
import logging
from datetime import timedelta
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from sqlalchemy.exc import OperationalError, IntegrityError
from dotenv import load_dotenv
from models.models import db, User, Slogan

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/postgres')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure JWT
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
CORS(app)


# Connection retry logic
def connect_with_retry(retries=5, delay=5):
    for attempt in range(retries):
        try:
            logger.info(f"Attempting to connect to database (attempt {attempt + 1}/{retries})")
            # Test connection
            with app.app_context():
                db.engine.connect()
                logger.info("Database connection successful!")
                return True
        except OperationalError as e:
            if attempt < retries - 1:
                logger.error(f"Database connection failed: {str(e)}")
                logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logger.error(f"Database connection failed after {retries} attempts")
                raise
    return False


# Authentication routes
@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validate required fields
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    # Create new user
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password,
        pet_name=data.get('pet_name'),
        pet_species=data.get('pet_species')
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Username or email already exists'}), 400
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error during registration: {str(e)}")
        return jsonify({'error': 'Registration failed'}), 500


@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()

    # Validate required fields
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password are required'}), 400

    # Find user by username
    user = User.query.filter_by(username=data['username']).first()

    # Verify user and password
    if user and bcrypt.check_password_hash(user.password, data['password']):
        # Create access token
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            'access_token': access_token,
            'user': user.to_dict()
        }), 200

    return jsonify({'error': 'Invalid credentials'}), 401


# Protected routes
@app.route('/users/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    # Convert back to integer if it's a string representation of an integer
    try:
        if isinstance(current_user_id, str) and current_user_id.isdigit():
            current_user_id = int(current_user_id)
    except:
        pass

    user = User.query.get(current_user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify(user.to_dict()), 200


@app.route('/users/<username>', methods=['GET'])
def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify(user.to_dict()), 200


@app.route('/users/<username>/slogans', methods=['GET'])
def get_user_slogans(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    slogans = Slogan.query.filter_by(user_id=user.id).all()
    return jsonify({
        'user': user.to_dict(),
        'slogans': [slogan.to_dict() for slogan in slogans]
    }), 200


@app.route('/slogans', methods=['POST'])
@jwt_required()
def create_slogan():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    if not data or 'slogan' not in data:
        return jsonify({'error': 'Slogan text is required'}), 400

    new_slogan = Slogan(
        user_id=current_user_id,
        slogan=data['slogan']
    )

    try:
        db.session.add(new_slogan)
        db.session.commit()
        return jsonify({'message': 'Slogan created successfully', 'slogan': new_slogan.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating slogan: {str(e)}")
        return jsonify({'error': 'Failed to create slogan'}), 500


@app.route('/slogans', methods=['GET'])
def get_all_slogans():
    slogans = Slogan.query.all()
    return jsonify([slogan.to_dict() for slogan in slogans]), 200


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200


if __name__ == '__main__':
    logger.info("Waiting for database to be ready...")
    connect_with_retry()
    logger.info("Starting Flask application...")
    app.run(host='0.0.0.0', port=8000, debug=True)