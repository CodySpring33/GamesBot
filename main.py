from discord.ext.commands import Bot
import discord
import os
import requests
import json
import random
# Create an instance of the API class
bot = Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def game(ctx, arg = None):
    await ctx.channel.send(embed=games(arg))

def games(arg):
  if(arg == None):
    url = 'https://www.freetogame.com/api/games?platform=pc'
    response = requests.request("GET", url)
    json_data = json.loads(response.text)
    lst = list(json_data)
    choice = random.choice(lst)
    embed = discord.Embed(description=choice["short_description"],
      title=choice["title"],
      url=(choice["game_url"]))
    embed.set_image(url=choice["thumbnail"])
    return embed
  else:
    url = f'https://www.freetogame.com/api/games?category={arg}'
    response = requests.request("GET", url)
    json_data = json.loads(response.text)
    lst = list(json_data)
    choice = random.choice(lst)
    embed = discord.Embed(description=choice["short_description"],
      title=choice["title"],
      url=(choice["game_url"]))
    embed.set_image(url=choice["thumbnail"])
    return embed


bot.run(os.getenv('TOKEN'))
