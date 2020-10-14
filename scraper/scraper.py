import requests
import time
from bs4 import BeautifulSoup
import smtplib

# index of URLs corresponds to index of card_prices
URLs = ['https://www.shenronslair.com/Cards/Card/BT11-154',  # Vegito SCR
        'https://www.shenronslair.com/Cards/Card/BT11-112',  # Eis shenron
        'https://www.shenronslair.com/Cards/Card/BT10-088']  # Dormant potential
card_prices = [70, 1, 40]
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}


def check_card_price():
    for URL in URLs:
        desc_page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(desc_page.content, 'html.parser')

        name = soup.select_one('h1').get_text().strip()   # name of card
        price = soup.select_one('table>tbody>tr>td>span.text-success').get_text().strip()   # price of card - tcglow
        numeric_price = float(price.split('$')[-1])

        if numeric_price <= card_prices[URLs.index(URL)]:
            send_email(name, price)


def send_email(name, price):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('keyfeula1214@gmail.com', 'triaubdeatsmmkdz')
    subject = "Price dropped for " + name
    body = "The tcg low price for " + name + " has dropped to " + price
    email_msg = f"Subject: {subject} \n\n {body}"
    server.sendmail(
        'keyfeula1214@gmail.com',   # from
        'keyfeula1214@gmail.com',   # to
        email_msg                   # message
    )
    server.quit()


while True:
    check_card_price()
    time.sleep(60*60*8)   # run every 8 hours
