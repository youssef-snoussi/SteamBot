import os
import discord as ds
from server import keep_alive, get_game

client = ds.Client()


def format_msg(game):
    return "**Title**: {} \n **Price**: {} \n **Release date**: {} \n  {}".format(
        game['title'], game['price'], game['release_date'], game['link'])


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == "!free_game":
        try:
            game = get_game("free")
            msg = format_msg(game)
        except:
            msg = "Server busy, try later!"
        await message.channel.send(msg)

keep_alive()
Token = os.environ['_TOKEN']
client.run(Token)
