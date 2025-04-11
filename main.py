import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time
from datetime import datetime
from tgtg import TgtgClient
from config import Config

# Global dictionary to track item states
item_states = {}

def send_email(subject, body):
    """Send email notification using SMTP."""
    msg = MIMEMultipart()
    msg['From'] = Config.EMAIL_FROM
    msg['To'] = Config.EMAIL_TO
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
        server.starttls()
        server.login(Config.SMTP_USER, Config.SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"Email sent successfully at {datetime.now()}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def check_available_items():
    """Check for available items and send notifications only on state changes."""
    try:
        # Initialize TGTG client
        client = TgtgClient(
            email=Config.TGTG_EMAIL,
            access_token=Config.TGTG_ACCESS_TOKEN,
            refresh_token=Config.TGTG_REFRESH_TOKEN,
            cookie=Config.TGTG_COOKIE
        )

        # Get items from favorite stores
        items = client.get_items(favorites_only=True)
        
        # Check for state changes
        available_items = []
        for item in items:
            item_id = item['item_id']
            is_available = item['items_available'] > 0
            
            # Check if state has changed
            if item_id not in item_states:
                item_states[item_id] = is_available
                if is_available:
                    available_items.append(item)
            elif item_states[item_id] != is_available:
                item_states[item_id] = is_available
                if is_available:
                    available_items.append(item)

        if available_items:
            # Prepare email content
            subject = "🚨 Too Good To Go - Items Available!"
            body = "The following items are now available:\n\n"
            
            for item in available_items:
                body += f"🏪 {item['display_name']}\n"
                body += f"📍 {item['pickup_location']['address']['address_line']}\n"
                body += f"💰 {item['price_including_taxes']['minor_units'] / 100} {item['price_including_taxes']['code']}\n"
                body += f"📦 Available: {item['items_available']}\n"
                body += f"⏰ Pickup: {item['pickup_interval']['start']} - {item['pickup_interval']['end']}\n\n"

            # Send email notification
            send_email(subject, body)
            print(f"Found {len(available_items)} newly available items at {datetime.now()}")
        else:
            print(f"No state changes detected at {datetime.now()}")

        return True
    except Exception as e:
        # Check if it's a CAPTCHA error (usually contains '403' or 'captcha' in the error)
        error_str = str(e).lower()
        if '403' in error_str or 'captcha' in error_str:
            print("CAPTCHA detected. Terminating the script.")
            print("To get new credentials, run a separate script like:")
            print("from tgtg import TgtgClient")
            print("client = TgtgClient(email='your_email@example.com')")
            print("credentials = client.get_credentials()")
            print("print(credentials)")
            os._exit(1)  # Force terminate the script
        
        print(f"Error checking items: {e}")
        return False

def main():
    """Main function to run the monitoring service."""
    try:
        # Validate configuration
        Config.validate_config()
        
        print("Starting Too Good To Go monitoring service...")
        
        if not Config.TGTG_ACCESS_TOKEN or not Config.TGTG_REFRESH_TOKEN:
            print("No credentials found in .env file.")
            print("Please run a separate script to get credentials:")
            print("from tgtg import TgtgClient")
            print("client = TgtgClient(email='your_email@example.com')")
            print("credentials = client.get_credentials()")
            print("print(credentials)")
            return
        
        # Schedule regular checks
        schedule.every(Config.CHECK_INTERVAL_MINUTES).minutes.do(check_available_items)
        
        # Run immediately on startup
        check_available_items()
        
        # Keep the script running
        while True:
            schedule.run_pending()
            time.sleep(1)
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please check your .env file and restart the application.")

if __name__ == "__main__":
    main() 