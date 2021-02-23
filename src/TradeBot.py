import requests
import json
import discord
from discord.ext import commands
import time


with open("secrets.json") as f:
  data = json.load(f)

token = data["bot_token"]
key = data["api_key"]
client = commands.Bot(command_prefix = "/")

notification_channel = client.get_channel(768396626825183252)

base_url = "http://politicsandwar.com/api/"


resource_list = ["coal",
                 "oil",
                 "uranium",
                 "lead",
                 "iron",
                 "bauxite",
                 "gasoline",
                 "munitions",
                 "steel",
                 "aluminum",
                 "food"
                ]


async def check_prices():
    print("checking prices")
    for resource in resource_list:
        r =requests.get(f"{base_url}/tradeprice/?resource={resource}&key={key}")
        if r.status_code == 200:
            info = r.json()
            
            highest_buy_offer = int(info["highestbuy"]["price"])
            lowest_sell_offer = int(info["lowestbuy"]["price"])
            if highest_buy_offer > lowest_sell_offer:
                print(resource)
                difference = highest_buy_offer - lowest_sell_offer
                await client.get_channel(768396626825183252).send(f"{resource} is selling for {difference} profit ppu. Link: https://politicsandwar.com/index.php?id=90&display=world&resource1={resource}&buysell=sell&ob=price&od=DEF&maximum=50&minimum=0&search=Go")
            
        else:
            print(resource)
            print(r.status_code)
    time.sleep(90)
    await check_prices()



@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    prices_coroutine = check_prices()
    await prices_coroutine

client.run(token)






print("finished")
