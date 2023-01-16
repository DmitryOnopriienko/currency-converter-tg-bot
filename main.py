import requests
import telebot
import config
from Currency import Privat24Currency, NbuCurrency
from NbuCurrencyConverter import NbuCurrencyConverter

bot = telebot.TeleBot(config.bot_token)

currencies = ("USD", "EUR")

keyboard_action_chooser = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_action_chooser.row("Convert UAH to ...")
keyboard_action_chooser.row("Convert currency")
keyboard_action_chooser.row("Check currency price")

keyboard_currency_chooser = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_currency_chooser.row("USD", "EUR")
keyboard_currency_chooser.row("Back to menu")

keyboard_amount_chooser = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_amount_chooser.row("10", "100", "200")
keyboard_amount_chooser.row("500", "1000", "5000")


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hello, choose the option", reply_markup=keyboard_action_chooser)
    bot.register_next_step_handler(message, action_chooser)


# @bot.message_handler(commands=["help"])
# def send_help(message):
#     response = "Press /start and choose the option you want"
#     bot.reply_to(message, response)


def action_chooser(message):
    if message.text == "Convert UAH to ...":
        bot.send_message(message.chat.id, "Choose the currency", reply_markup=keyboard_currency_chooser)
        bot.register_next_step_handler(message, uah_convert)
    elif message.text == "Convert currency":
        bot.send_message(message.chat.id, "Choose base currency", reply_markup=keyboard_currency_chooser)
        bot.register_next_step_handler(message, choose_base_currency)
    elif message.text == "Check currency price":
        bot.send_message(message.chat.id, "Choose the currency", reply_markup=keyboard_currency_chooser)
        bot.register_next_step_handler(message, currency_price_privat24)
    else:
        bot.send_message(message.chat.id, "Choose the correct action")
        bot.register_next_step_handler(message, action_chooser)


def currency_price_privat24(message):
    if message.text == "Back to menu":
        return_to_main_menu(bot, message)
    else:
        currency = parse_privat24_currency(message.text)
        if not currency:
            bot.send_message(message.chat.id, "Choose the correct option")
            bot.register_next_step_handler(message, currency_price_privat24)
            return
        bot.reply_to(message, str(currency))
        bot.register_next_step_handler(message, currency_price_privat24)

    # elif message.text not in currencies:
    #     bot.send_message(message.chat.id, "Choose the correct option")
    #     bot.register_next_step_handler(message, currency_chooser)
    # else:
    #     resp = requests.get(config.privat_bank_api).json()
    #     print(resp)
    #     reply = currency_price_message_former(resp, message.text)
    #     bot.reply_to(message, reply)
    #     bot.register_next_step_handler(message, currency_chooser)


def parse_privat24_currency(ccy):
    currencies_json = requests.get(config.privat_bank_api).json()
    for elem in currencies_json:
        if elem["ccy"] == ccy:
            currency = Privat24Currency(ccy)
            currency.buy_price = elem["buy"]
            currency.sale_price = elem["sale"]
            return currency
    return None


def uah_convert(message):
    if message.text == "Back to menu":
        return_to_main_menu(bot, message)
    else:
        if message.text not in currencies:
            bot.send_message(message.chat.id, "Choose the correct option")
            bot.register_next_step_handler(message, uah_convert)
            return
        currency = parse_nbu_currency(message.text)
        if not currency:
            bot.send_message(message.chat.id, "Something went wrong, try again", reply_markup=keyboard_currency_chooser)
            bot.register_next_step_handler(message, uah_convert)
            return
        bot.send_message(message.chat.id, "Enter amount to convert", reply_markup=keyboard_amount_chooser)
        bot.register_next_step_handler(message, convert_uah_amount, currency)


def convert_uah_amount(message, currency: NbuCurrency):
    try:
        amount = float(message.text)
    except:
        bot.send_message(message.chat.id, "Enter correct amount to convert", reply_markup=keyboard_amount_chooser)
        bot.register_next_step_handler(message, convert_uah_amount, currency)
        return
    bot.send_message(message.chat.id, f"{amount} UAH:\n{amount / currency.price:.2f} {currency.cc}", reply_markup=keyboard_action_chooser)
    bot.register_next_step_handler(message, action_chooser)


def parse_nbu_currency(cc):
    currencies_json = requests.get(config.nbu_api_url).json()
    for elem in currencies_json:
        if elem["cc"] == cc:
            currency = NbuCurrency(cc)
            currency.name = elem["txt"]
            currency.price = elem["rate"]
            return currency
    return None


def choose_base_currency(message):
    if message.text == "Back to menu":
        return_to_main_menu(bot, message)
    else:
        if message.text not in currencies:
            bot.send_message(message.chat.id, "Choose the correct option")
            bot.register_next_step_handler(message, choose_base_currency)
            return
        converter = NbuCurrencyConverter()
        converter.base_cc = parse_nbu_currency(message.text)
        if not converter.base_cc:
            bot.send_message(message.chat.id, "Something went wrong, try again", reply_markup=keyboard_currency_chooser)
            bot.register_next_step_handler(message, choose_base_currency)
            return
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row("UAH", "USD", "EUR")
        keyboard.row("Back")
        keyboard.row("Back to menu")
        bot.send_message(message.chat.id, "Choose currency to convert to", reply_markup=keyboard)
        bot.register_next_step_handler(message, choose_cc_to, converter)


def choose_cc_to(message, converter: NbuCurrencyConverter):
    if message.text == "Back":
        bot.send_message(message.chat.id, "Choose base currency", reply_markup=keyboard_currency_chooser)
        bot.register_next_step_handler(message, choose_base_currency)
        return
    if message.text == "Back to menu":
        return_to_main_menu(bot, message)
        return
    if message.text == "UAH":
        converter.cc_to = init_uah_currency()
    else:
        converter.cc_to = parse_nbu_currency(message.text)
    if not converter.cc_to:
        bot.send_message(message.chat.id, "Something went wrong, try again", reply_markup=keyboard_currency_chooser)
        bot.register_next_step_handler(message, choose_cc_to, converter)
        return
    bot.send_message(message.chat.id, "Enter amount to convert", reply_markup=keyboard_amount_chooser)
    bot.register_next_step_handler(message, convert_amount, converter)


def init_uah_currency():
    currency = NbuCurrency("UAH")
    currency.name = "Гривня"
    currency.price = 1
    return currency


def convert_amount(message, converter: NbuCurrencyConverter):
    try:
        amount = float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Enter correct amount to convert", reply_markup=keyboard_amount_chooser)
        bot.register_next_step_handler(message, convert_uah_amount, converter)
        return
    converter.base_amount = amount
    bot.send_message(message.chat.id, str(converter), reply_markup=keyboard_action_chooser)
    bot.register_next_step_handler(message, action_chooser)


def return_to_main_menu(bot: telebot.TeleBot, message: telebot.types.Message):
    bot.send_message(message.chat.id, "Choose the option you want", reply_markup=keyboard_action_chooser)
    bot.register_next_step_handler(message, action_chooser)


bot.infinity_polling()
