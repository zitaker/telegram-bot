# будет работать через сайт (https://www.pythonanywhere.com) или надо установить библиотеки на компьютер

from random import choice

import telebot

token = ''
# чтобы проверить нужно созать телеграм бота и вписать свой токен

bot = telebot.TeleBot(token)


RANDOM_TASKS = ['Пойти в магазин', 'апельсины', 'хлеб', 'молоко и творог']

todos = dict()


HELP = '''
Список доступных команд:
/ show  - напечать все задачи на заданную дату
/ add - добавить задачу
/ random - добавить на сегодня случайную задачу
/ help - Напечатать help
'''


def add_todo(date, task):
    date = date.lower()
    if todos.get(date) is not None:
        todos[date].append(task)
    else:
        todos[date] = [task]


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, HELP)


@bot.message_handler(commands=['random'])
def random(message):
    task = choice(RANDOM_TASKS)
    add_todo('сегодня', task)
    bot.send_message(message.chat.id, f'Задача {task} добавлена на сегодня')


@bot.message_handler(commands=['add'])
def add(message):
    _, date, tail = message.text.split(maxsplit=2)
    task = ' '.join([tail])
    add_todo(date, task)
    bot.send_message(message.chat.id, f'Задача {task} добавлена на дату {date}')


@bot.message_handler(commands=['show'])
def print_(message):
    date = message.text.split()[1].lower()
    if date in todos:
        tasks = ''
        for task in todos[date]:
            tasks += f'[ ] {task}\n'
    else:
        tasks = 'Такой даты нет'
    bot.send_message(message.chat.id, tasks)


bot.polling(none_stop=True)
