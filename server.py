from flask import Flask
from threading import Thread
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time
from cachelib.simple import SimpleCache
from random import randint
from scrape import get_all_free_games, get_game_data

app = Flask('')
cache = SimpleCache()
free_games_url = "https://store.steampowered.com/search/results/?query=&start={}&count=500&dynamic_data=&force_infinite=1&maxprice=free&category1=998&snr=1_7_7_230_7&infinite=1"
discounted_games_url = "https://store.steampowered.com/search/results/?query=&start={}&count=50&dynamic_data=&force_infinite=1&specials=1&snr=1_7_7_230_7&infinite=1"


@app.route('/')
def home():
    return "Hello. I am alive!"


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    now = datetime.utcnow()
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=get_all_games,
                      trigger="interval",
                      seconds=86400,
                      next_run_time=now)
    scheduler.start()
    t = Thread(target=run)
    t.start()


def get_all_games():
    print("getting free games list...")
    exec_time = -time.time()
    free_games = get_all_free_games(free_games_url)
    exec_time += time.time()
    print("Done, execution time: {:.2f}".format(exec_time))
    print("Total number of games: ", len(free_games))
    cache.set('free_games', free_games, timeout=86400)


def get_game(user_request):
    if user_request == "free":
        free_games = cache.get('free_games')
        sug = randint(0, len(free_games) - 1)
        game = free_games[sug]
        # sysreq1, sysreq2
        return game

    