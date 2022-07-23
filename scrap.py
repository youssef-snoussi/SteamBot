import requests
from bs4 import BeautifulSoup
import random


def format_url(url, number):
    return url.format(str(number))


def total_count(url):
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
        title = game.find('span', {'class': 'title'}).text
        price = game.find('div', {'class': 'search_price'}).text
        release_date = game.find('div', {'class': 'search_released'}).text
        games_data.append({
            'link': game['href'],
            'title': title,
            'price': price,
            'release_date': release_date
        })
    return games_data


def get_random_suggestion(data):
    l = len(data) - 1
    sug = random.randint(0, l)
    return sug
