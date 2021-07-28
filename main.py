from discord.ext.commands import Bot
from discord.ext import tasks
import discord
import os
import requests
import json
import random
import math
# Create an instance of the API class
bot = Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    xpEmbed.start()

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
  f.close()
  await ctx.channel.send(response)

@bot.command()
async def stats(ctx, arg=None):
  if not arg:
    user = str(ctx.author)
  else:
    disallowed_characters = "<@!>"
    for character in disallowed_characters:
	    arg = arg.replace(character, "")
    user = str(await bot.fetch_user(arg))
  with open('users.json', "r") as f:
    data = json.load(f)
    if user in data.keys():
      if not arg:
        pic = ctx.author.avatar_url
        pfp = ctx.author
      else:
        pfp = await bot.fetch_user(arg)
        pic = pfp.avatar_url
      embed=discord.Embed(title="Stats", description=pfp.mention + " You are level " + str(data[user]['level']) + " and have " + str(data[user]['xp']) + " xp", color=0xecce8b)
      embed.set_thumbnail(url=(pic))
      await ctx.channel.send(embed=embed)
    else:
      await ctx.channel.send(ctx.author.mention + " no data available.")


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

@bot.event
async def on_message(ctx):
  file = None
  if ctx.author == bot.user:
    return
  else:
    user = str(ctx.author)
    with open('users.json', "r") as f:
      data = json.load(f)
      if user in data.keys():
        data[user]["xp"] += 1
        oldlvl = data[user]["level"]
        data[user]["level"] = math.floor(math.sqrt(data[user]["xp"])/5)
        file = json.dumps(data)
        if oldlvl != data[user]["level"]:
          await ctx.channel.send(str(ctx.author.mention) + " you have leveled up to level " + str(data[user]["level"]) +"!")
      else:
        data[user] = { "xp" : 1 , "level" : 0}
        file = json.dumps(data)
    with open('users.json', "w") as f:
      f.write(file)
  await bot.process_commands(ctx)

@tasks.loop(minutes=10)
async def xpEmbed():
  check = random.randint(0, 25)
  if check % 5 == 0:
    print("sending")
    messageChannel = bot.get_channel(715026731576197122)
    embed = discord.Embed(description="React to this message to gain 25xp!",
        title="Free XP",
        url=("https://www.twitch.tv/cjspring"))
    message = await messageChannel.send(embed=embed)
    await message.add_reaction('🙌')

@bot.event
async def on_reaction_add(reaction, user):
  embed = reaction.message.embeds[0]
  emoji = reaction.emoji
  if user.bot:
    return
  reactor = user
  user = str(user)
  if embed.title == "Free XP":
    if emoji == "🙌":
      with open('users.json', "r") as f:
        data = json.load(f)
        if str(user) in data.keys():
          oldlvl = data[user]["level"]
          data[user]["xp"] += 25
          data[user]["level"] = math.floor(math.sqrt(data[user]["xp"])/5)
          file = json.dumps(data)
          if oldlvl != data[user]["level"]:
            await reaction.message.channel.send(str(reactor.mention) + " you have leveled up to level " + str(data[user]["level"]) +"!")
          with open('users.json', "w") as f:
            f.write(file)
  else:
    return

bot.run(os.getenv('TOKEN'))
