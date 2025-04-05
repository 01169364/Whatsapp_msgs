# WhatsApp Birthday Wisher 🎂
A Python script that automatically sends WhatsApp birthday greetings by fetching contacts and their birthdays from Google Contacts.

# Features ✨
* 📅 Fetches birthdays from Google Contacts

* 💌 Sends personalized WhatsApp messages

* 🔒 Secure OAuth token storage (no repeated logins)

* 📊 Detailed logging

* ⏰ Automated scheduling via Windows Task Scheduler

# Prerequisites
* Python 3.7+

* Google account with contacts

* WhatsApp Web access

* Browser installed

# Installation

1. Clone the repository:

```
git clone https://github.com/01169364/whatsapp-birthday-wisher.git
cd whatsapp-birthday-wisher
```

2. Install dependencies:

```
pip install -r requirements.txt
```
## Setup Guide
**1. Google API Configuration**

* Go to [Google Cloud Console](https://console.cloud.google.com/)

* Create a new project and enable **People API**

* Create OAuth credentials (Desktop App type)

* Download ```credentials.json``` and place in project folder

**2. First-Time Authentication**
   
Run the script manually to authenticate:

```
python birthday_wisher.py
```
This will:

* Open a browser for Google login

* Generate ```token.json``` for future automatic runs

**3. Configure Automation**
   
* Create a scheduled task using the included batch file:

* Edit ```run_birthday_wisher.bat``` to set correct paths

* Set up Windows Task Scheduler to run daily

## File Structure
```
📂 whatsapp-birthday-wisher/
├── 📄 birthday_wisher.py      # Main script
├── 📄 run_birthday_wisher.bat # Batch file for scheduling
├── 📄 requirements.txt        # Dependencies
├── 📄 credentials.json        # Google API credentials
├── 📄 token.json              # Auto-generated auth token
└── 📄 log.txt                 # Activity logs
```
## Customization
Edit these variables in birthday_wisher.py:

```
# Customize your birthday message
MESSAGE_TEMPLATE = """🎉 Happy Birthday {name}! 🎂

Wishing you a wonderful year ahead! 🥳"""

# Adjust sending parameters
WAIT_TIME = 30  # Seconds to wait before sending
CLOSE_DELAY = 15 # Seconds to wait after sending
```
## Troubleshooting
| Issue |	Solution |
| --- | --- |
| Browser closes too quickly |	Increase WAIT_TIME and CLOSE_DELAY |
|Emoji display issues	Ensure | UTF-8 encoding in console |
| Authentication errors |	Delete token.json and re-authenticate |
|Messages not sending |	Keep WhatsApp Web logged in |

## License

MIT License - Free for personal and commercial use

## Support

For issues or feature requests, [please open an issue.](https://github.com/01169364/whatsapp-birthday-wisher/issues)

# Happy automating! 🚀

Let your contacts feel special on their birthdays without lifting a finger after setup!
