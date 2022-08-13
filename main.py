import os
import discord as ds
from server import keep_alive, get_game, get_game_reqs, save_game, get_saved_games, clear_saved_games

client = ds.Client()
last_result = False


def format_game(game):
    return "**Title**: {} \n **Price**: {} \n **Release date**: {} \n  {}".format(
        game['title'], game['price'], game['release_date'], game['link'])


def format_reqs(reqs):
    msg = ""
    for d in reqs:
        os = list(d.keys())[0]
        levels = list(d[os].keys())
        msg += "**" + os + "**\n"
        for l in levels:
            msg += "**" + l + "**\n"
            for val in d[os][l]:
                msg += val + "\n"
        msg += "===========\n"
    return msg


def format_saved_games(games):
    msg = "Your saved games: \n"
    for game in games:
        msg += "**Title:** {} \n".format(game)
    return msg


@client.event
async def on_ready():
    print("{0.user} is runing".format(client))


@client.event
async def on_message(message):

    global last_result

    if message.author == client.user:
        return

    if message.content == "!free_game":
        try:
            game = get_game("free")
            last_result = game
            msg = format_game(game)
        except:
            msg = "OOOPS! Server busy, please try later!"
        await message.channel.send(msg)

    if message.content == "!requirements":
        if last_result:
            reqs = get_game_reqs(last_result)
            msg = format_reqs(reqs)
            await message.channel.send(msg)
        else:
            await message.channel.send(
                "You need to search for a game first, try using '!free_game' command!"
            )

    if message.content == "!save":
        save_game(message.author, last_result)
        # user = User(message.author)
        # user.save_game(last_result)
        # save_user(user)
        await message.channel.send('game saved successfully!')

    if message.content == "!saved_games":
        saved_games = get_saved_games(message.author)
        if saved_games == False:
            await message.channel.send("You don't have any saved games!")
        else:
            msg = format_saved_games(saved_games)
            await message.channel.send(msg)
    if message.content == "!clear":
        clear_saved_games(message.author)
        await message.channel.send("Your saved games have been deleted!")

keep_alive()
Token = os.environ['_TOKEN']
client.run(Token)
