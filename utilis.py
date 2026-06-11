"""
Utility functions for the project tracker
"""
import logging
from datetime import datetime


def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename='project_tracker.log'
    )
    return logging.getLogger(__name__)


def validate_email(email: str) -> bool:
    """Simple email validation"""
    return '@' in email and '.' in email


def format_date(date_string: str) -> str:
    """Format ISO date string to readable format"""
    try:
        dt = datetime.fromisoformat(date_string)
        return dt.strftime("%Y-%m-%d %H:%M")
    except:
        return date_string


logger = setup_logging()