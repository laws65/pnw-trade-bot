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

notification_channel = client.get_channel(813894055347486730)

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
        r = requests.get(f"{base_url}/tradeprice/?resource={resource}&key={key}")
        if r.status_code == 200:
            info = r.json()

            highest_buy_offer = int(info["highestbuy"]["price"])
            buy_amount = int(info["highestbuy"]["amount"])
            lowest_sell_offer = int(info["lowestbuy"]["price"])
            sell_amount = int(info["lowestbuy"]["amount"])
            if highest_buy_offer > lowest_sell_offer:
                print(resource)
                difference = highest_buy_offer - lowest_sell_offer
                embed = discord.Embed(title="Trade Alert", description=f"A trade alert for **{resource}**!")
                embed.add_field(name="Buying for", value=f"Selling {buy_amount} {resource} at [${highest_buy_offer:,}](https://politicsandwar.com/index.php?id=90&display=world&resource1={resource}&buysell=sell&ob=price&od=DEF&maximum=50&minimum=0&search=Go) ppu"),
                embed.add_field(name="Selling for", value=f"Buying {sell_amount} {resource} at [${lowest_sell_offer:,}](https://politicsandwar.com/index.php?id=90&display=world&resource1={resource}&buysell=buy&ob=price&od=DEF&maximum=50&minimum=0&search=Go) ppu"),
                embed.add_field(name="Difference", value=f"PPU Difference: ${difference:,}. Maximum profit: ${difference * min(buy_amount, sell_amount):,}")
                await client.get_channel(813894055347486730).send(embed=embed)

        else:
            print(resource)
            print(r.status_code)

@tasks.loop(seconds=90)
async def prices():
    await check_prices()


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    prices.start()


client.run(token)

print("finished")
