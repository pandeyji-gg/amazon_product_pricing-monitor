from playwright.async_api import async_playwright
import re
import asyncio
import smtplib
import ssl
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


async def check_price(page):
    await page.wait_for_load_state("load")
    price = await page.locator("span.a-price span.a-price-whole").first.inner_text()
    price = re.sub(r"[^\d]", "", price)
    return int(price)


def send_email(actual_price, target_price):
    smtp_server = "smtp.gmail.com"
    port = 465
    sender = os.environ.get("EMAIL_SENDER", "sushantpandey940@gmail.com")
    password = os.environ.get("EMAIL_PASSWORD")
    recipient = os.environ.get("EMAIL_RECIPIENT", "sushantpandey0792@gmail.com")

    msg = EmailMessage()
    msg["Subject"] = f"Price Alert: Amazon Product dropped to ₹{actual_price:,}"
    msg["From"] = sender
    msg["To"] = recipient
    msg.set_content(
        f"""Hello,

This is an automated price alert.

Product price has dropped below your target.

Current Price:  ₹{actual_price:,}
Target Price:   ₹{target_price:,}
Savings:        ₹{target_price - actual_price:,}

Act fast — prices may change.

— Price Monitor Bot
"""
    )

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender, password)
        server.send_message(msg)


async def scraping():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        page = await browser.new_page()
        target_price = int(input("please enter the price you wanna compare with: "))
        while True:
            try:
                await page.goto(
                    "https://www.amazon.com/Apple-iPhone-Version-Desert-Titanium/dp/B0DPJMKJTC?crid=3LRUR21U6UDBE&dib=eyJ2IjoiMSJ9.zgjXFK020cWpt3eB2Mn6Qo595U5ckNwiLSnDBOvj2Ukv7UkhtkyW1qOe83zFF0FcsdMbD4IUMTnYMJ7e7gTzYaoqWHPs8WcoRdqnusxP6roMOnPX7zx4ge_PHra395i3C-F5FgSgO9eSbwY7SLQLucKBjiI6KA8XWC6kTpgUZ2KWaAZ7xeToILPUGj7krUla79Jv7WxFXb-qKMLV_2yK1dTMsK9u0nM3j_Xrgwy0Myw.bHOWGNvgBIhS9VvBcYNjp7YAL-qIgcXLTs_V8uuUWKM&dib_tag=se&keywords=iphone%2B17%2Bpro%2Bmax&qid=1772701806&sprefix=iphon%2Caps%2C288&sr=8-1&th=1"
                )
                title = await page.locator("#productTitle").first.inner_text()
                print(title)
                actual_price = await check_price(page)
            except Exception as e:
                print(f"Error fetching page: {e}")
                await asyncio.sleep(60)
                continue

            print(f"Current price: ₹{actual_price:,} | Target: ₹{target_price:,}")
            if actual_price < target_price:
                send_email(actual_price, target_price)
                print("Price dropped! Email sent.")
                break

            await asyncio.sleep(3600)


asyncio.run(scraping())
