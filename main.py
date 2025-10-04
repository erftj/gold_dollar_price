import telebot
from telebot.types import ReplyKeyboardMarkup
import requests
from bs4 import BeautifulSoup

TEL_TOKEN = "8345323390:AAFgXaeKqJjAbst09MW4R2Ye8cTlzSTp-N8"
bot = telebot.TeleBot(TEL_TOKEN)
GOLD_URL = "https://www.tgju.org/profile/geram18"
DOLLAR_URL = "https://www.tgju.org/profile/price_dollar_rl"

reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
reply_keyboard.add("gold_price","dollar_price")


def get_gold_price():
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(GOLD_URL, headers=headers, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    el = soup.find("span", {"data-col": "info.last_trade.PDrCotVal"})
    if not el:
        raise ValueError("قیمت پیدا نشد!")

    gold_price = el.get_text(strip=True).replace(",", "")
    return int(gold_price)


gold_price1 = get_gold_price()
gold_price1 = gold_price1 / 10
gold_price1 = int(gold_price1)


def get_dollar_price():
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(DOLLAR_URL, headers=headers, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    el = soup.find(name="span", attrs={"data-col": "info.last_trade.PDrCotVal"})
    if not el:
        raise ValueError("قیمت پیدا نشد!")

    dollar_price = el.get_text(strip=True).replace(",", "")
    return int(dollar_price)


dollar_price1 = get_dollar_price()
dollar_price1 = dollar_price1 / 10
dollar_price1 = int(dollar_price1)


@bot.message_handler(commands=['start'])
def say_hello(message):
    first_name = message.from_user.first_name
    bot.reply_to(message, text=f"سلام {first_name}")
    bot.reply_to(message, text=
    "این ربات برای گرفتن سریع قیمت طلا و دلار اماده شده است از دکمه های زیر استفاده کنین", reply_markup=reply_keyboard)



@bot.message_handler(func=lambda message: True)
def check_btn(message):
    if message.text == "gold_price":
        bot.reply_to(message, text=f"{gold_price1}")
    elif message.text == "dollar_price":
        bot.reply_to(message, text=f"{dollar_price1}")



bot.polling()
