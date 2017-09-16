import telebot
import config
from database import *

bot = telebot.TeleBot(config.token)

with db_session:
    all_groups = Group.select()[:]

commands = {  # command description used in the "help" command
    'start': 'Get used to the bot',
    'help': 'Gives you information about the available commands',
    'sendLongText': 'A test using the \'send_chat_action\' command',
    'getImage': 'A test using multi-stage messages, custom keyboard, and media sending'
}

@bot.message_handler(commands=['start'])
def handle_text(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    groups = []
    for group in all_groups:
        groups.append(group.name)

    keyboard.add(*[telebot.types.KeyboardButton(name) for name in groups])
    # for group in all_groups:
    #     keyboard.add(telebot.types.KeyboardButton(group.name))

    bot.send_message(message.chat.id, 'Укажите номер группы', reply_markup=keyboard)


# # help page
# @bot.message_handler(commands=['help'])
# def command_help(m):
#     cid = m.chat.id
#     help_text = "The following commands are available: \n"
#     for key in commands:  # generate help text out of the commands dictionary defined at the top
#         help_text += "/" + key + ": "
#         help_text += commands[key] + "\n"
#     bot.send_message(cid, help_text)  # send the generated help page


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):

    #next_handler - отличная идея чтобы не писать кучу условий

    group = [g for g in all_groups if g.name == message.text]
    if len(group) != 0:
        group = group[0]
        response = ''
        with db_session:
            lessons = Lesson.select(lambda l: l.group.name == group.name).order_by(Lesson.date)[:]

        day = lessons[-1].date

        for lesson in lessons:
            if day != lesson.date:
                day = lesson.date
                response += '<b>' + str(day) + '</b>\n'
            response += lesson.time + '\n' + lesson.name + '\n' \
                        + lesson.lecturer + ', ' + 'ауд. ' + lesson.audience + '\n\n'

        bot.send_message(message.chat.id, response, parse_mode='html')
        pass

    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    bot.polling(none_stop=True)
