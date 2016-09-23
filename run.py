import discord
from discord.ext import commands
from time import sleep
import asyncio

client = discord.Client()
bot = commands.Bot(command_prefix='?', description='''Ero-Bot is a +18 h-manga and doujinshi bot!
    Contact: TheGooDFeelinG#4165''')

@bot.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == bot.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Fuck off everyone hates you, {0.author.mention}'.format(message)
        await bot.send_message(message.channel, msg)
	
    if message.content.startswith('!dm'):
        msg = 'test'
        user = message.author
        await bot.send_message(user, msg)

    if message.content.startswith('!picdm'):
        await bot.send_file(message.author, 'test1.png')

    if message.content.startswith('!picture'):
        await bot.send_file(message.channel, 'test1.png')

    if message.content.startswith('!clearall'):
        def my_message(m):
            return m.author == bot.user
        deleted = await bot.purge_from(message.channel)
        await bot.send_message(message.channel, 'Deleted {} messages!'.format(len(deleted)))
        await asyncio.sleep(2)
        await bot.purge_from(message.channel, check=my_message)

    if message.content.startswith('!menu'):
        msg = """```
        What do you want to do?
        1) Kill yourslef
        2) Kill yourself```
        ``Type the number below!``"""
        await bot.send_message(message.channel, msg)
        
        def pick_check(m):
            return m.content.isdigit()
            
        pick = await bot.wait_for_message(timeout=20.0, author=message.author, check=pick_check)
        if pick is None:
            await bot.send_message(message.channel, 'Timed out, try again!')
            return
        if int(pick.content) == 1:
            await bot.send_message(message.channel, 'You picked 1!')
        if int(pick.content) == 2:
            await bot.send_message(message.channel, 'You picked 2!')
    
    if message.content.startswith('!search'):
        await bot.send_message(message.channel, 'wip you fucker')

        for line in f:
            if "test" in line: print(line)
            
    if message.content.startswith('!repeat'):
        await bot.send_message(message.channel, message.content)

    await bot.process_commands(message)
            
@bot.command()
async def mention(ctx):
    """[WIP] Mentions yourself"""
    await bot.say('{ctx.message.author.id}'.format(ctx))

@bot.command()
async def picture(ctx):
    """[WIP] Sends a picture to the current channel"""
    await bot.send_file(ctx.channel, 'test1.png')

@bot.command()
async def clearall(channel : id):
    """[WIP] Clear all the messages in the current channel"""
    def my_message(m):
         return m.author == bot.user
    deleted = await bot.purge_from(channel)
    await bot.send_message(channel, 'Deleted {} messages!'.format(len(deleted)))
    await asyncio.sleep(2)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name + ' (id: ' + bot.user.id + ')')
    print('------')
    #print('Opening list.txt')
    #f = open('list.txt', 'r')
    #print('Everything done!')
    #print('------')
    
    
    await bot.change_status(discord.Game(name='with doujinshi!'))

bot.run('token')
