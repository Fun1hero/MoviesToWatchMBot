import requests
import datetime
import telebot
import tmdbsimple as tmdb

tmdb.API_KEY = '30edbbffe90ed13b306393e208d93102'
token = "655354611:AAHI2t21zF57t9UScMMD4GKW4Qh9IJhHhq0"
url = "https://api.telegram.org/bot" + token + "/"
popular = 'https://api.themoviedb.org/3/movie/popular?api_key='+ tmdb.API_KEY + '&language=en-US&page=1'


class BotHandler:

    def __init__(self, _token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(_token)

    def get_updates(self, offset=None, timeout=80):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            print(get_result.__str__() + ' ' + len(get_result).__str__())
            last_update = get_result[-1]
        else:
            print(get_result.__str__() + ' ' + len(get_result).__str__())
            last_update = get_result[len(get_result)]

        return last_update


def get_request_(req, offset=None, timeout=80):
    method = 'get_request_'
    params = {'timeout': timeout, 'offset': offset}
    resp = requests.get(req + method, params)
    result_json = resp.json()['results']
    return result_json


movieMBot = BotHandler(token)
greetings = ('здравствуй', 'привет', 'ку', 'здорово')
now = datetime.datetime.now()


def main():
    new_offset = None
    today = now.day
    hour = now.hour

    while True:
        movieMBot.get_updates(new_offset)

        last_update = movieMBot.get_last_update()

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']

        if last_chat_text.lower() in greetings and today == now.day and 6 <= hour < 12:
            movieMBot.send_message(last_chat_id, 'Доброе утро, {}'.format(last_chat_name))
            today += 1  # can greet once

        elif last_chat_text.lower() in greetings and today == now.day and 12 <= hour < 17:
            movieMBot.send_message(last_chat_id, 'Добрый день, {}'.format(last_chat_name))
            today += 1  # can greet once

        elif last_chat_text.lower() in greetings and today == now.day and 17 <= hour < 23:
            movieMBot.send_message(last_chat_id, 'Добрый вечер, {}'.format(last_chat_name))
            today += 1  # can greet once

        if last_chat_text.lower() == '/популярное':
            popularList = ''
            for i in range(len(get_request_(popular))):
                film = tmdb.Movies().popular()['results'][i]
                popularList += (i+1).__str__() + ') ' + film['title'] + ' – rating: ' + film['vote_average'].__str__() + '\n'
            movieMBot.send_message(last_chat_id, popularList)

        if last_chat_text.lower() == '/жанры':
            genre = tmdb.Genres().movie_list()['genres']
            genLen = len(genre)
            genreList = ''
            for i in range(genLen):
                genreList += genre[i]['name'] + '\t(id: ' + genre[i]['id'].__str__() + ')' + '\n'
            movieMBot.send_message(last_chat_id, genreList)

        if last_chat_text.lower() == '/фильм':
            movie = tmdb.Movies(100)
            responce = movie.info()
            print(tmdb.Movies().lists().__str__())
            # movieMBot.send_message(last_chat_id, '\"' + movie.title + '\",' + ' here you go, {}'.format(last_chat_name))

        new_offset = last_update_id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()