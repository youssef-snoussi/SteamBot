import os
import discord as ds
import scrap as sc
import random

client = ds.Client()
url = "https://store.steampowered.com/search/results/?query=&start={}&count=500&dynamic_data=&force_infinite=1&maxprice=free&category1=998&snr=1_7_7_230_7&infinite=1"


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!free'):
        await message.channel.send(
            "Wait a moment please, I'm looking for a game for you!")
        number = random.randint(0, 8000)
        data = sc.get_data(
            f"https://store.steampowered.com/search/results/?query=&start={number}&count=500&dynamic_data=&force_infinite=1&maxprice=free&category1=998&snr=1_7_7_230_7&infinite=1"
        )
        parsed_data = sc.parse_data(data)
        suggestion = parsed_data[sc.get_random_suggestion(parsed_data)]
        msg = "**Title**: {} \n **Release date**: {} \n **Price**: {} \n {}".format(
            suggestion['title'], suggestion['price'],
            suggestion['release_date'], suggestion['link'])
        await message.channel.send(msg)


Token = os.environ['_TOKEN']
client.run(Token)
