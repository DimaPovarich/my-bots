#импорты
import telebot
from telebot import types

#получаем доступ к боту через код
bot = telebot.TeleBot('6969959924:AAFsK9gl7AC_AI_-4w15lz0hKS0hucfx3ws')

#нужные нам переменные
parametrs = [1, 2, 3, 4]
name = ''


#формула расчета нормы каллорий
def formula(mass, height, years, gender):
    if gender == 'woman':
        return mass*10 + height*6.25 - years*5 - 161
    else:
        return mass * 10 + height * 6.25 - years * 5 + 5

#функция для форматирования данных в нужный нам формат и записание их в список parametrs
def info(message):
    info = message.text
    info = list(info.split(' '))
    print(info)
    try:
        if int(info[3]) == 1 or int(info[3]) == 3:
            parametrs[3] = 'man'
        else:
            parametrs[3] = 'woman'

        parametrs[0], parametrs[1], parametrs[2] = info[0], info[1], info[2]
        name = info[4]
        bot.send_message(message.chat.id, f'Спасибо {name}, данные успешно приняты')
    except IndexError:
        bot.send_message(message.chat.id, 'Данные введены неправильно!!')

def reset_info(message):
    info = message.text
    info = list(info.split(' '))
    try:
        parametrs[0], parametrs[1], parametrs[2] = info[0], info[1], info[2]
        bot.send_message(message.chat.id, f'Спасибо {name}, данные успешно изменены!')
    except IndexError:
        bot.send_message(message.chat.id, 'Данные введены неверно!')


#две основные функции /start и /help
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Привет! Я бот который посчитает сколько каллорий тебе рекомендуется употреблять, чтобы узнать что я могу напиши /help')
    bot.send_message(message.chat.id, 'Но.. сначала введите свои параметры используя /first_set_setting')

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, 'Мои возможности: \n/reset_settings - перенастроить параметры расчета\n/colories - узнать мою норму колорий\n/first_set_setting - ввести свои данные\n')
#####################


#можно сказать регистрация себя в бота, ввод физических данных
@bot.message_handler(commands=['first_set_setting'])
def get_info(message):
    if parametrs == [1, 2, 3, 4]:
        msg = bot.send_message(message.chat.id, 'Введите свои данные в таком порядке через пробел: вес, рост, возраст, ваш пол(1 - мужской, 2 - женский, 3 - ламинат), ваше имя')
        bot.register_next_step_handler(msg, info)
    else:
        bot.send_message(message.chat.id, 'Вы уже вводили данные о себе, если вы хотите изменить их, то напишите /reset_settings')


#главная функция для расчета каллорий по формуле
@bot.message_handler(commands=['colories'])
def colories(message):
    if parametrs != [1, 2, 3, 4]:
        bot.reply_to(message, f'ваша норма колорий: {formula(int(parametrs[0]), int(parametrs[1]), int(parametrs[2]), parametrs[3])} ккал')
    else:
        bot.send_message(message.chat.id, 'Вы еще не ввели свои параметры или ввели их неверно😥!!')

@bot.message_handler(commands=['reset_settings'])
def reset(message):
    msg = bot.send_message(message.chat.id,'Введите свои обновленные данные в таком порядке через пробел: вес, рост, возраст')
    bot.register_next_step_handler(msg, reset_info)


#если бот не распознал команду, то он говорит что такой команды пока не знает
@bot.message_handler(content_types=['text'])
def test(message):
    bot.reply_to(message, "Извини, но я пока не знаю такую команду😪")


bot.polling()