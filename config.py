import os
from dotenv import load_dotenv
from pathlib import Path
from typing import Optional

# Load environment variables from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Configuration class to access environment variables
class Config:
    # TGTG Configuration
    TGTG_EMAIL: str = os.getenv('TGTG_EMAIL', '')
    TGTG_ACCESS_TOKEN: Optional[str] = os.getenv('TGTG_ACCESS_TOKEN', None)
    TGTG_REFRESH_TOKEN: Optional[str] = os.getenv('TGTG_REFRESH_TOKEN', None)
    TGTG_COOKIE: Optional[str] = os.getenv('TGTG_COOKIE', None)
    
    # Email Configuration
    SMTP_SERVER: str = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT: int = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USER: str = os.getenv('SMTP_USER', '')
    SMTP_PASSWORD: str = os.getenv('SMTP_PASSWORD', '')
    EMAIL_FROM: str = os.getenv('EMAIL_FROM', '')
    EMAIL_TO: str = os.getenv('EMAIL_TO', '')
    
    # Application Configuration
    CHECK_INTERVAL_MINUTES: int = 10
    
    @classmethod
    def validate_config(cls):
        """Validate that all required environment variables are set."""
        required_vars = [
            'TGTG_EMAIL',
            'SMTP_SERVER', 
            'SMTP_USER', 
            'SMTP_PASSWORD',
            'EMAIL_FROM',
            'EMAIL_TO'
        ]
        
        missing_vars = [var for var in required_vars if not getattr(cls, var)]
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}. "
                            "Please check your .env file.")

# Example usage
if __name__ == "__main__":
    try:
        Config.validate_config()
        print("Configuration validated successfully!")
        print(f"TGTG Email: {Config.TGTG_EMAIL}")
        print(f"SMTP Server: {Config.SMTP_SERVER}:{Config.SMTP_PORT}")
        print(f"Email From: {Config.EMAIL_FROM}")
        print(f"Email To: {Config.EMAIL_TO}")
        print(f"Check Interval: {Config.CHECK_INTERVAL_MINUTES} minutes")
    except ValueError as e:
        print(f"Configuration error: {e}")