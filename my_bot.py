import logging
from tkinter.messagebox import NO

import telegram
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
import settings
import ephem
from datetime import datetime as dt
from clean_string import get_clean_string
from difflib import get_close_matches


planets = [
    planet[2] for planet in ephem._libastro.builtin_planets()
    if planet[1] == 'Planet']


logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')


PROXY = {
    'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {
        'username': settings.PROXY_USERNAME,
        'password': settings.PROXY_PASSWORD
    }
}


def greet_user(update: telegram.Update, context) -> None:
    text = 'call /start'
    logging.info(text)
    update.message.reply_text(text)


def get_correct_planet_name(user_planet_name: str, planets: list[str]) -> str:
    """
    Очищенную от лишних символов и пробелов строку,
    сравнивает со значениями строк в списке.
    При отсутствии прямых совпадений ищет вероятные совпадения.
    Возвращает: строку являющуюся прямым совпадением ->
    наиболее вероятным совпадением -> пустую строку,
    если подходящих вариантов не найдено.
    """
    user_planet_name = get_clean_string(user_planet_name).capitalize()
    if user_planet_name in planets:
        return user_planet_name
    else:
        possible_names = get_close_matches(user_planet_name, planets)
        return possible_names[0] if possible_names else ''


def handle_planet(update: telegram.Update, context) -> None:
    if len(update.message.text.split(' ')) == 1:
        update.message.reply_text('Нou must to use /planet with a name planet')
    else:
        planet = get_correct_planet_name(update.message.text.split()[1], planets)
        if planet:
            object_planet = getattr(ephem, planet)
            constell = ephem.constellation(object_planet(dt.today()))[1]
            update.message.reply_text(f'Today {planet} is in the {constell}')
        else:
            update.message.reply_text('We have not found such a planet')


def get_number_words(user_text: str) -> str:
    """
    Возвращает количество слов в переданной строке,
    исключая символы и цифры
    """
    if not user_text:
        return 'You must enter at least one word'

    if ' ' not in user_text:
        return 'Your message contain 1 word'

    count_words = len(user_text.split())
    return f'Your message contain {count_words} words'


def handle_wordcount(update: telegram.Update, context) -> None:
    """
    Отправляет пользовотелю в чат - сколько слов содержит сообщение
    с командой /wordcount
    """
    user_text = get_clean_string(update.message.text)
    if 'wordcount' in user_text:
        user_text = user_text.replace('wordcount', '')

    answer_to_user = get_number_words(user_text)
    update.message.reply_text(answer_to_user)


def get_date_next_fool_moon() -> str:
    """
    """
    date_next_full_moon = ephem.next_full_moon(dt.today())
    date_next_full_moon = dt.strptime(
                                    str(date_next_full_moon),
                                    '%Y/%m/%d %H:%M:%S'
                                    )
    date_next_full_moon = date_next_full_moon.strftime('%d.%m.%Y %H:%M:%S')

    return date_next_full_moon


def handle_next_fool_moon(update: telegram.Update, context) -> None:
    """
    Отправляют пользователю в чат - дату следующего полнолуния
    """
    # date_next_full_moon = str(get_date_next_fool_moon()).split()
    date_next_full_moon = get_date_next_fool_moon().split()
    update.message.reply_text('The next full moon will be {} at {}'.format(
        date_next_full_moon[0], date_next_full_moon[1]
    ))


def talk_to_me(update: telegram.Update, context) -> None:
    if update.message:
        user_text = update.message.text
        logging.info(user_text)
        if type(user_text) == str:
            update.message.reply_text(user_text)


def main():
    mybot = Updater(settings.TOKEN, request_kwargs=PROXY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", handle_planet))
    dp.add_handler(CommandHandler("wordcount", handle_wordcount))
    dp.add_handler(CommandHandler("next_fool_moon", handle_next_fool_moon))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
