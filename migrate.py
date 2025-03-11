import os
import logging
import time
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from alembic.config import Config
from alembic import command
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def wait_for_db(database_url, retries=5, delay=5):
    """Wait for the database to be ready"""
    engine = create_engine(database_url)

    for attempt in range(retries):
        try:
            logger.info(f"Attempting to connect to database (attempt {attempt + 1}/{retries})")
            connection = engine.connect()
            connection.close()
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


def run_migrations():
    """Run database migrations using Alembic"""
    try:
        logger.info("Running database migrations...")

        # Create Alembic config
        alembic_cfg = Config("alembic.ini")

        # Run the migration
        command.upgrade(alembic_cfg, "head")

        logger.info("Database migrations completed successfully!")
    except Exception as e:
        logger.error(f"Error running migrations: {str(e)}")
        raise


if __name__ == "__main__":
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        if wait_for_db(database_url):
            run_migrations()
    else:
        logger.error("DATABASE_URL environment variable not set")
