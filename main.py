import telebot
import config
from telebot import types
import pandas as pd
import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe
bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('/add_new')
    markup.add(item1)

    bot.send_message(message.chat.id, 'Добро пожаловать, нажми /help, чтобы узнать что я умею.', reply_markup=markup)


@bot.message_handler(commands=['help'])
def h(message):
    bot.send_message(message.chat.id, """
/help - мои умения
    """)



@bot.message_handler()
def bo(message):
    global z

    hellenic_message = message.text
    place = hellenic_message[hellenic_message.find('at'):hellenic_message.find('for')]
    place = place[3:len(place) - 2]
    amount = hellenic_message[hellenic_message.find('€') + 1:hellenic_message.find(':') - 4]
    amount = amount.replace(',', '.', 10)

    # Settings
    SPREADSHEET_NAME = 'Hellenic bank messages'

    # Working with df
    gc = gspread.service_account('credentials.json')

    # Open a sheet from a spreadsheet in one go
    wks = gc.open(SPREADSHEET_NAME).sheet1

    existing_df = get_as_dataframe(wks)
    existing_df = existing_df.loc[:, ~existing_df.columns.str.contains('^Unnamed')]
    existing_df.dropna(inplace=True)
    existing_df = existing_df.astype(str)

    df = pd.DataFrame({'Name': [place], 'Category': ['-'], 'Amount (EUR)': [amount]})
    existing_df.dropna(inplace=True)
    # Concatenate 2 DF
    frames = [existing_df, df]
    result_df = pd.concat(frames, ignore_index=True)

    wks.clear()
    set_with_dataframe(wks, result_df)

    bot.send_message(message.chat.id, f'SUCCESSFULLY ADDED: {place}   {amount}')
    # z = bot.send_message(message.chat.id, 'Введите сообщение')
    # bot.register_next_step_handler(z, save)
def save(message):
    global z
    hellenic_message = message.text
    place = hellenic_message[hellenic_message.find('at'):hellenic_message.find('for')]
    place = place[3:len(place) - 2]
    amount = hellenic_message[hellenic_message.find('€') + 1:hellenic_message.find(':') - 4]
    amount = amount.replace(',', '.', 10)

    # Settings
    SPREADSHEET_NAME = 'Networth test'

    # Working with df
    gc = gspread.service_account('credentials.json')

    # Open a sheet from a spreadsheet in one go
    wks = gc.open(SPREADSHEET_NAME).sheet1

    existing_df = get_as_dataframe(wks)
    existing_df = existing_df.loc[:, ~existing_df.columns.str.contains('^Unnamed')]
    existing_df.dropna(inplace=True)
    existing_df = existing_df.astype(str)

    df = pd.DataFrame({'Name': [place], 'Category': ['-'], 'Amount (EUR)': [amount]})
    existing_df.dropna(inplace=True)
    print(existing_df)
    # Concatenate 2 DF
    frames = [existing_df, df]
    result_df = pd.concat(frames, ignore_index=True)

    wks.clear()
    set_with_dataframe(wks, result_df)

    bot.send_message(message.chat.id, f'SUCCESSFULLY ADDED: {place}   {amount}')


bot.polling(none_stop=True)
