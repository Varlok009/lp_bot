from copy import copy

import telegram
from clean_string import get_clean_string
from difflib import get_close_matches
from get_cities import get_cities_for_game
from settings import PATH_TO_CITIES


DATA = get_cities_for_game(PATH_TO_CITIES)
USERS_CITY = {}


class Game:
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        if user_id not in USERS_CITY:
            USERS_CITY[self.user_id] = {'cities': copy(DATA), 'last_city': None}
            self.data_cities = USERS_CITY[self.user_id]
        else:
            self.data_cities = USERS_CITY[self.user_id]

    def get_correct_city_from_user_cities(self, user_city: str) -> str:
        """
        Очищает строку от лишних символов, возвращает наиболее вероятное
        совпадение строки с исходным массивом строк
        Если совпадения не найдено - возвращает пустую строку
        """
        user_city = get_clean_string(user_city)
        user_city = get_close_matches(user_city, self.data_cities['cities'])
        return user_city[0] if user_city else ''

    def round_user(self, user_city: str) -> str:
        """
        Проверяет удовлетворяет ли введенное название города
        условиям игры, если да - удаляет город пользователя из
        массива доступных городов и отмечает последний сыгранный город
        Если условия игры не выполнены - возвращает пустую строку,
        иначе возвращает удаленный город
        """
        if not self.data_cities['last_city']:
            self.data_cities['last_city'] = user_city
            self.delite_city(user_city)
            return user_city

        if self.data_cities['last_city'][-1] != user_city[0]:
            return ''

        self.data_cities['last_city'] = user_city
        self.delite_city(user_city)
        return user_city

    def round_bot(self) -> str:
        """
        Возвращает случайный город, удовлетворящий условиям игры.
        Удаляет его из общего массива город пользователя
        """
        for city in self.data_cities['cities']:
            if city[0] == self.data_cities['last_city'][-1]:
                self.data_cities['last_city'] = city
                self.delite_city(city)
                return city
        return ''

    def delite_city(self, city):
        self.data_cities['cities'].remove(city)

    def get_status_game(self) -> bool:
        """
        Проверяет есть ли доступные ходы. Если есть - возвращает True
        Если нет - возращает False и инициализирует новый список городов
        для пользователя.
        """
        if not self.data_cities['cities']:
            self.new_game()
            return False

        for city in self.data_cities['cities']:
            if city[0] == self.data_cities['last_city'][-1]:
                return True

        self.new_game()
        return False

    def new_game(self) -> None:
        USERS_CITY[self.user_id] = {'cities': copy(DATA), 'last_city': None}
        self.data_cities = USERS_CITY[self.user_id]


def round_game(user_id, user_city):
    game = Game(user_id)

    correct_city = game.get_correct_city_from_user_cities(user_city)

    if not correct_city:
        return 'This city cannot be used, try another'

    if not game.round_user(correct_city):
        return 'Your the city does not meet the requirements of the game'

    if not game.get_status_game():
        return 'No cities available, congratulations on the draw'

    bot_city = game.round_bot()

    if not game.get_status_game():
        return (f'{bot_city.capitalize()}. No cities available, congratulations on the draw')

    return (f'Your choice {correct_city.capitalize()} then {bot_city.capitalize()}')


def handle_city(update: telegram.Update, context) -> None:
    if update.effective_user:
        user_id = update.effective_user.id
    if update.message:
        user_city = update.message.text
    if '/city' in user_city:
        user_city = user_city.replace('/city', '')
    if not user_city and update.message:
        update.message.reply_text('You mest enter city name')
    elif update.message:
        answer = round_game(user_id, user_city)
        update.message.reply_text(answer)
