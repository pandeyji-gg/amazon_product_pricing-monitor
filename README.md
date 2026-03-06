# Amazon Price Monitor

Monitors an Amazon product's price and sends an email alert when it drops below your target price.

## What it does

- Checks product price every hour
- Sends email notification when price drops below target
- Displays current price vs target price in terminal
- Runs until target price is reached

## Requirements

```bash
pip install playwright python-dotenv
playwright install firefox
```

## Setup

Create a `.env` file in the same folder:
```
EMAIL_PASSWORD=your_gmail_app_password
EMAIL_SENDER=your_email@gmail.com
EMAIL_RECIPIENT=recipient_email@gmail.com
```

Gmail App Password required — not your regular Gmail password. Enable 2FA first, then generate an App Password from myaccount.google.com.

## Usage

Set the product URL in the script, then run:
```bash
python price_monitor.py
```

Enter your target price when prompted:
```
please enter the price you wanna compare with: 70000
```

## Output

```
Current price: ₹68,149 | Target: ₹70,000
Price dropped! Email sent.
```
