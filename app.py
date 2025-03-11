import os
import time
import logging
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

import models.models as models
from models.models import db

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db.init_app(app)

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


# Routes
@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the SQLAlchemy PostgreSQL API'})


@app.route('/users', methods=['GET'])
def get_users():
    users = models.User.query.all()
    return jsonify([user.to_dict() for user in users])

@app.route('/slogans/<int:user_id>', methods=['GET'])
def get_slogans(user_id):
    slogans = models.Slogan.query.filter_by(user_id=user_id).all()
    return jsonify([slogan.to_dict() for slogan in slogans])

@app.route('/health')
def health():
    try:
        db.session.execute('SELECT 1')
        return jsonify({'status': 'healthy', 'database': 'connected'})
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'database': str(e)}), 500


if __name__ == '__main__':
    logger.info("Waiting for database to be ready...")
    connect_with_retry()
    logger.info("Starting Flask application...")
    app.run(host='0.0.0.0', port=8000, debug=True)