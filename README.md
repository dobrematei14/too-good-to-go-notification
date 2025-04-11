# Too Good To Go Notification System 🍽️

A Python-based notification system that monitors your favorite restaurants on Too Good To Go and alerts you via email when packages become available. Built using the official `tgtg` Python client.

## Features ✨

- 🔍 Monitors favorite restaurants for available packages
- 📧 Sends real-time email notifications when packages are available
- 🔒 Secure credential management using environment variables
- ⚡ Fast and efficient API integration using official tgtg client
- 🔄 Automatic token refresh and session management

## Prerequisites 📋

- Python 3.9 or higher
- pip (Python package manager)
- SMTP server access (for email notifications)
- Too Good To Go account

## Installation 🚀

1. Clone the repository:
```bash
git clone https://github.com/dobrematei14/too-good-to-go-notification.git
cd too-good-to-go-notification
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration ⚙️

1. Create your environment file:
```bash
cp .env.template .env
```

2. Configure your environment variables in `.env`:
   - TGTG Credentials
   - SMTP Settings (for email)

## Environment Variables 📝

### TGTG Configuration
- `TGTG_EMAIL`: Your Too Good To Go account email
- `TGTG_ACCESS_TOKEN`: (Optional) Your access token if you already have one
- `TGTG_REFRESH_TOKEN`: (Optional) Your refresh token if you already have one
- `TGTG_COOKIE`: (Optional) Your cookie if you already have one

### Email Configuration
- `SMTP_SERVER`: SMTP server address
- `SMTP_USER`: SMTP username
- `SMTP_PASSWORD`: SMTP password
- `EMAIL_FROM`: Your email address
- `EMAIL_TO`: Recipient email address

## Usage Example 📝

```python
from tgtg import TgtgClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize TGTG client
client = TgtgClient(
    email=os.getenv("TGTG_EMAIL"),
    access_token=os.getenv("TGTG_ACCESS_TOKEN"),
    refresh_token=os.getenv("TGTG_REFRESH_TOKEN"),
    cookie=os.getenv("TGTG_COOKIE")
)

# Get available items from favorite stores
items = client.get_items(favorites_only=True)

# Process and send notifications for available items
for item in items:
    if item["items_available"] > 0:
        # Send email notification
        send_notification(item)
```

## Security 🔒

- Never commit your `.env` file to version control
- Keep your API keys and credentials secure
- Regularly rotate your credentials
- Use environment-specific configuration files

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.