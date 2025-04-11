import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Configuration class to access environment variables
class Config:
    # API Credentials
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    
    # Database Configuration
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', '5432'))
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    
    # AWS Credentials
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    
    # Other Services
    SMTP_SERVER = os.getenv('SMTP_SERVER')
    SMTP_USER = os.getenv('SMTP_USER')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
    
    @classmethod
    def validate_config(cls):
        """Validate that all required environment variables are set."""
        required_vars = [
            'API_KEY', 
            'API_SECRET',
            'DB_NAME', 
            'DB_USER', 
            'DB_PASSWORD'
        ]
        
        missing_vars = [var for var in required_vars if getattr(cls, var) is None]
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}. "
                            "Please check your .env file.")

# Example usage
if __name__ == "__main__":
    try:
        Config.validate_config()
        print("Configuration validated successfully!")
        print(f"API Key: {Config.API_KEY[:4]}..." if Config.API_KEY else "API Key not found")
        print(f"Database: {Config.DB_NAME} on {Config.DB_HOST}")
    except ValueError as e:
        print(f"Configuration error: {e}")