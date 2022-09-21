from concurrent.futures import process
from email import message
from hashlib import new
from random import random
from urllib import request
from discord.ext import commands
import discord
import random
from discord import Permissions
from discord import Status
from discord import Message

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True
bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True, # Commands aren't case-sensitive
    intents = intents # Set up basic permissions
)

bot.author_id = "224206372668047360"  # Change to your discord id

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier

@bot.command()
async def pong(ctx):
    await ctx.send('pong')

#the bot create an Admin role (if it doesn't exists) on your server   
@bot.command()    
async def admin(ctx, member : discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="AdminCristophe")
    if role is None:
    # Doesn't exist, create the role here
        role = await ctx.guild.create_role(name="AdminCristophe", permissions=Permissions.all())
    await member.add_roles(role)
    
#the bot ban that member from the server (Test with caution)
@bot.command()    
async def ban(ctx, member : discord.Member):
    await member.ban()

#the bot write back for each possible status
@bot.command()
async def count(ctx):
    online = 0
    idle = 0
    off = 0
    for member in ctx.guild.members:
        if member.status== Status.online:
            online+=1
        if member.status==Status.idle:
            idle+=1
        if member.status==Status.offline:
            off+=1
    await ctx.send(str(online) + " members are online, " + str(idle) + " are idle and " + str(off) + " are off")

#your bot post a @here mention followed by a Yes/No question.
# The bost will then write the question again in another message and
# add one 👍 and one 👎 emoji reaction to its message
@bot.command()
async def poll(ctx, question):
    await ctx.send(question + ' YES or NO ?' + ctx.author.mention)
    react_message = await ctx.send(question)
    await react_message.add_reaction('👍')
    await react_message.add_reaction('👎')

#the post post a random comic from https://xkcd.com
@bot.command()
async def xkcd(ctx,num=None): #async func to get comic
    comicnumber = random.randint(1,100)
    request.get(f'https://xkcd.com/{comicnumber}/info.0.json')
    #response = requests.get(f'https://xkcd.com/{comicnumber}/info.0.json')
    #response = bot.get(f'https://xkcd.com/{comicnumber}/info.0.json')
    await ctx.send(response['img'])

@bot.event
async def on_message(message):
    
    #the bot don't reply to himself
    if message.author == bot.user:
        return
    
    #the bot write back the name of the user typing the command !name
    if message.content.startswith('!name'):
        await message.channel.send(message.author.name)
        
    #the bot answer with a value between 1 and 6
    if message.content.startswith('!d6'):
        await message.channel.send(random.randint(1,6))
    
    #the bot should say "Salut tout seul" and ping the original author of the message
    if message.content.startswith('Salut tout le monde'):
        await message.channel.send('Salut tout seul ' + message.author.mention)
    
    else:
        await bot.process_commands(message)
    #if message.content.startswith('!admin')
    # user = ctx.message.author
    # role = discord.utils.get(user.server.roles, name="role to add name")
    # await client.add_roles(user, role)

token = "MTAyMjExNTM1MDg3NzMyMzMxNA.GlvOUf.yvWwL3egv2U3agT8zIzPXbF_jNPFcG8khsT_5Q"
bot.run(token)  # Starts the bot