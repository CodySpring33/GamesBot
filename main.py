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
  response = games(arg)
  try: 
    if response[0] == 'G':
      await ctx.channel.send(response)
  except:
    await ctx.channel.send(embed=response)

@bot.command()
async def tags(ctx):
  f = open("terms.json")
  data = json.load(f)
  response = "The searchable tags are: "
  for x in range(45):
    if x != 44:
      response += data["tags"][x] + ", "
    else:
      response += data["tags"][x]
  await ctx.channel.send(response)


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
    try:
      response = requests.request("GET", url)
      json_data = json.loads(response.text)
      lst = list(json_data)
      choice = random.choice(lst)
      embed = discord.Embed(description=choice["short_description"],
        title=choice["title"],
        url=(choice["game_url"]))
      embed.set_image(url=choice["thumbnail"])
      return embed
    except:
      return f"Game Tag {arg} Not Found."


bot.run(os.getenv('TOKEN'))
