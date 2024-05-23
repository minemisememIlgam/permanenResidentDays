import telebot
from datetime import datetime

bot = telebot.TeleBot('6844034324:AAHMvxLQHA8SXFCFe4Eo7vToF4ge4OlW2wY')

ostatni_days = 0
study_days = 0
work_days = 0

def calculate_days(date_ranges):
    total_days = 0
    if date_ranges.strip().lower() == 'нет':
        return 0
    for date_range in date_ranges.split("\n"):
        if date_range.strip():
            start_date_str, end_date_str = date_range.split("-")
            start_date = datetime.strptime(start_date_str, "%d.%m.%Y")
            end_date = datetime.strptime(end_date_str, "%d.%m.%Y")
            total_days += (end_date - start_date).days + 1
    return total_days

@bot.message_handler(commands=['calculatePR'])
def start(message):
    bot.send_message(message.from_user.id, "Od kdy do kdy jsi pobyval v ČR za učelem ostatni? (в формате dd.mm.yyyy-dd.mm.yyyy, можно несколько строк) или напишите 'нет', если не применимо")
    bot.register_next_step_handler(message, get_study)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == "ahoj":
        bot.send_message(message.from_user.id, "Ahoj, jak ti mužu pomoci?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "/calculatePR")
    else:
        bot.send_message(message.from_user.id, "Nerozumim. Napiš /calculatePR.")

def get_study(message):
    global ostatni_days
    ostatni_days = calculate_days(message.text)
    bot.send_message(message.from_user.id, 'Od kdy do kdy jsi pobyval v ČR za učelem studium? (в формате dd.mm.yyyy-dd.mm.yyyy, можно несколько строк) или напишите "нет", если не применимо')
    bot.register_next_step_handler(message, get_work)

def get_work(message):
    global study_days
    study_days = calculate_days(message.text) // 2
    bot.send_message(message.from_user.id, 'Od kdy do kdy jsi pobyval v ČR za učelem zamestnani? (в формате dd.mm.yyyy-dd.mm.yyyy, можно несколько строк) или напишите "нет", если не применимо')
    bot.register_next_step_handler(message, get_result)

need_days = 1825

def get_result(message):
    global work_days
    work_days = calculate_days(message.text)
    total_days = ostatni_days + study_days + work_days
    bot.send_message(message.from_user.id, f"Celkem dní pobytu: {total_days} (ostatni: {ostatni_days}, studium: {study_days}, zamestnani: {work_days})")
    bot.send_message(message.from_user.id, f"Zbyva dnu pobytu: {need_days - total_days}")

bot.polling(none_stop=True, interval=0)
