from flask import Flask
from threading import Thread
from replit import db
from apscheduler.schedulers.background import BackgroundScheduler
import time
from datetime import datetime
from random import choice
from scraper import get_all_free_games, get_game_requirements


free_games_url = "https://store.steampowered.com/search/results/?query=&start={}&count=500&dynamic_data=&force_infinite=1&maxprice=free&category1=998&snr=1_7_7_230_7&infinite=1"
discounted_games_url = "https://store.steampowered.com/search/results/?query=&start={}&count=50&dynamic_data=&force_infinite=1&specials=1&snr=1_7_7_230_7&infinite=1"



app = Flask('')

@app.route('/')
def home():
    return "Hello. I am alive!"


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=get_free_games, trigger="interval", seconds=86400)
    scheduler.start()
    t = Thread(target=run)
    t.start()


def get_free_games():
    print("getting free games list...")
    exec_time = -time.time()
    free_games = get_all_free_games(free_games_url)
    exec_time += time.time()
    print("games' list updated on {}".format(datetime.now()))
    print("Done, execution time: {:.2f}".format(exec_time))
    print("Total number of games: ", len(free_games))
    db["free_games"] = free_games


def get_game(user_request):
    if user_request == "free":
        free_games = db["free_games"]
        game = choice(free_games)
        return game 

def get_game_reqs(game):
    return get_game_requirements(game)

def save_game(user, game):
    try:
        saved_games = db[str(user)]
        saved_games.append(game['title'])
        db[user] = saved_games
    except:
        db[user] = [game['title']]

def get_saved_games(user):
    try:
        saved_games = db[str(user)]
        return saved_games
    except:
        return False

def clear_saved_games(user):
    try:
        del db[str(user)]
    except:
        pass