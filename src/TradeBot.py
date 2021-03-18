import discord
from discord.ext import commands, tasks
import time
import aiohttp

token = " "
key = " "
client = commands.Bot(command_prefix = "/")

notification_channel_low = 813894055347486730
notification_channel_high = 822203808921813092


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
        url = f"{base_url}/tradeprice/?resource={resource}&key={key}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                info = await response.json()

        if response.status == 200:
            print(response.status)

            highest_buy_offer = int(info["highestbuy"]["price"])
            buy_amount = int(info["highestbuy"]["amount"])
            lowest_sell_offer = int(info["lowestbuy"]["price"])
            sell_amount = int(info["lowestbuy"]["amount"])

            if highest_buy_offer > lowest_sell_offer:
                difference = highest_buy_offer - lowest_sell_offer
                max_profit = difference * min(buy_amount, sell_amount)
                embed = discord.Embed(title="Trade Alert", description=f"A trade alert for **{resource}**!",
                                      color=discord.Color.orange())
                embed.add_field(name="Selling for", value=f"Amount: {sell_amount:,}"
                                                          f"\n"
                                                          f"PPU:${lowest_sell_offer:,}"
                                                          f"\n"
                                                          f"[CLICK TO BUY](https://politicsandwar.com/index.php?id=90&display=world&resource1={resource}&buysell=sell&ob=price&od=DEF&maximum=50&minimum=0&search=Go)"),
                embed.add_field(name="Buying for", value=f"Amount: {buy_amount:,}"
                                                         f"\n"
                                                         f"PPU: ${highest_buy_offer:,}"
                                                         f"\n"
                                                         f"[CLICK TO SELL](https://politicsandwar.com/index.php?id=90&display=world&resource1={resource}&buysell=buy&ob=price&od=DEF&maximum=50&minimum=0&search=Go)"),
                embed.add_field(name="Difference", value=f"PPU Difference: ${difference:,}."
                                                         f"\n"
                                                         f"Maximum profit: ${max_profit:,}")
                if max_profit < 49999:
                    await client.get_channel(notification_channel_low).send(embed=embed)
                if max_profit > 50000:
                    await client.get_channel(notification_channel_high).send(embed=embed)
                else:
                    pass

        else:
            print(resource)
            print(response.status)
    del highest_buy_offer
    del lowest_sell_offer

@tasks.loop(seconds=90)
async def prices():
    await check_prices()

@client.command(brief="Pong!", pass_context=True)
async def ping(ctx):
    """ Pong! """
    before = time.monotonic()
    message = await ctx.send("Pong!")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"Pong!  `{int(ping)}ms`")
    print(f'Ping {int(ping)}ms')

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    prices.start()

client.run(token)

print("finished")
