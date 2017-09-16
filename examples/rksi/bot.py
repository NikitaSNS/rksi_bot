import telebot

import config
from examples.rksi.Repositories.TimetableRepository import TimetableRepository

bot = telebot.TeleBot(config.token)

timetable = TimetableRepository().get_timetable('ПОКС-42')

commands = {  # command description used in the "help" command
    'start': 'Get used to the bot',
    'help': 'Gives you information about the available commands',
    'sendLongText': 'A test using the \'send_chat_action\' command',
    'getImage': 'A test using multi-stage messages, custom keyboard, and media sending'
}


@bot.message_handler(commands=['start'])
def handle_text(message):
    # Эти параметры для клавиатуры необязательны, просто для удобства
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = telebot.types.KeyboardButton(text='ПОКС-42')
    keyboard.add(button)
    bot.send_message(message.chat.id, 'Укажите номер группы', reply_markup=keyboard)


# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    if message.text == 'ПОКС-42':
        response = '_______________________\n'
        for lesson in timetable.lessons:
            response += lesson.name + " - " + lesson.time
    else:
        response = message.text
    bot.send_message(message.chat.id, response)


if __name__ == '__main__':
    print(vars(timetable))
    bot.polling(none_stop=True)
