import requests
from bs4 import BeautifulSoup
from random import randint


def format_url(url, number):
    return url.format(str(number))


def get_total_count(url):
    req = requests.get(url)
    data = dict(req.json())
    return data['total_count']


def get_data(url):
    req = requests.get(url)
    data = dict(req.json())
    return data['results_html']


def parse_data(data):
    games_data = []
    soup = BeautifulSoup(data, 'html.parser')
    games = soup.find_all('a')
    for game in games:
        title = game.find('span', {'class': 'title'}).text.strip()
        price = game.find('div', {'class': 'search_price'}).text.strip()
        release_date = game.find('div', {
            'class': 'search_released'
        }).text.strip()
        games_data.append({
            'link': game['href'],
            'title': title,
            'price': price,
            'release_date': release_date
        })
    return games_data


def get_random_suggestion(data):
    l = len(data) - 1
    sug = randint(0, l)
    return sug


def get_all_free_games(url):
    games = []
    total_count = get_total_count(url)
    for i in range(0, total_count, 50):
        formatted_url = format_url(url, i)
        data = get_data(formatted_url)
        data = parse_data(data)
        for game in data:
            if game not in games:
                games.append(game)
    return games


def get_free_game(url):
    number = randint(0, get_total_count(url))
    formated_url = format_url(url, number)
    data = get_data(formated_url)
    parsed_data = parse_data(data)
    game = parsed_data[get_random_suggestion(parsed_data)]
    return game
