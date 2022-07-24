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

    # if message.content == "!free_game":
    #     await message.channel.send(
    #         "Wait a moment please while I find a free game for you...")
    #     game = get_game("free")
    #     msg = format_msg(game)
    #     await message.channel.send(msg)

    # if message.content == "!discounted_games":
    #     await message.channel.send(
    #         "Wait a moment please while I find a free game for you...")
    #     game = get_game("discounted")
    #     msg = format_msg(game)
    #     await message.channel.send(msg)

    # if message.content.startswith('!free'):
    #     await message.channel.send(
    #         "Wait a moment please, I'm looking for a game for you!")
    #     number = random.randint(0, 8000)
    #     data = sc.get_data(
    #         f"https://store.steampowered.com/search/results/?query=&start={number}&count=500&dynamic_data=&force_infinite=1&maxprice=free&category1=998&snr=1_7_7_230_7&infinite=1"
    #     )
    #     parsed_data = sc.parse_data(data)
    #     suggestion = parsed_data[sc.get_random_suggestion(parsed_data)]
    #     msg = "**Title**: {} \n **Release date**: {} \n **Price**: {} \n {}".format(
    #         suggestion['title'], suggestion['release_date'],
    #         suggestion['price'], suggestion['link'])
    #     await message.channel.send(msg)


keep_alive()
Token = os.environ['_TOKEN']
client.run(Token)
