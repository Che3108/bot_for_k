#!/usr/bin/python

import telebot
import re
import pandas as pd
import load_data # Скрипт обработки файлов базы

# чтение базы
base_path = 'base'
df = load_data.build_base(base_path)

def find_inn(inn):
    try:
        df_inn = df[df.inn==inn]
        send_str = f'ИНН клиента: {df_inn.inn.iloc[0]}\n\n  <Информация о киенте>'
    except IndexError:
        send_str = f'Клиент с ИНН {inn} отсутствует в базе.'
    return send_str

# Создание бота
bot = telebot.TeleBot('API_key')
@bot.message_handler(content_types=['text'])


def get_text_messages(message):
    if bool(re.search( r'\D', message.text)):
        bot.send_message(message.from_user.id, "Вам необходимо ввести ИНН организации (10 или 12 цифр).")
    else:
        if len(message.text) == 10:
            control_num = [2, 4, 10, 3, 5, 9, 4, 6, 8]
            control_sum = 0
            for i in range(len(control_num)):
                control_sum += control_num[i]*int(message.text[i])
            control_sum = control_sum % 11
            if str(control_sum)[-1] == message.text[-1]:
                bot.send_message(message.from_user.id, find_inn(message.text))
            else:
                bot.send_message(message.from_user.id, "Введен ошибочный номер, контрольная сумма не совпала.")
        elif len(message.text) == 12:
            control_num_1 = [7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
            control_num_2 = [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
            control_sum_1 = 0
            control_sum_2 = 0
            for i in range(len(control_num_1)):
                control_sum_1 += control_num_1[i]*int(message.text[i])
            for i in range(len(control_num_2)):
                control_sum_2 += control_num_2[i]*int(message.text[i])
            control_sum_1 = control_sum_1 % 11
            control_sum_2 = control_sum_2 % 11
            if (str(control_sum_1)[-1] == message.text[-2]) and (str(control_sum_2)[-1] == message.text[-1]):
                bot.send_message(message.from_user.id, find_inn(message.text))
            else:
                bot.send_message(message.from_user.id, "Введен ошибочный номер, контрольная сумма не совпала.")
        else:
            bot.send_message(message.from_user.id, "Вам необходимо ввести ИНН организации (10 или 12 цифр).")
        

bot.polling(none_stop=True, interval=0)
