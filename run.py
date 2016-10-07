import discord
from discord.ext import commands
import asyncio
import subprocess
import os

client = discord.Client()
bot = commands.Bot(command_prefix='$', description="Ero-bot is a lewd h-manga and doujinshi bot!")


@bot.command(pass_context=True)
async def search(ctx, *, show_name : str):
    """Searches for a show and lists all related doujinshi."""
    arg = show_name
    query = "~" + arg + "|"
    with open('list.txt') as f:
        for num, line in enumerate(f, 1):
            if query.lower() in line.lower():
                error = False
                break
            else:
                error = True
        #There must be a better way than a bool check, but fuck it
        if error is True:
            await bot.say('Not found! Try an exact show name or use ``$listshows``')
        elif error is False:
            show = arg
            files = int(line.rstrip('\n').split('|')[1])
            f=open('list.txt')
            lines=f.readlines()
            i = num
            choice = 1
            p = 1
            await bot.send_message(ctx.message.author, 'Found ``' + str(files) + '`` doujinshi')
            await bot.send_typing(ctx.message.author)
            pages = (int(files / 11)) + 1
            if pages == 1:
                while i < num + files:
                    currentline = lines[i]
                    name = currentline.rstrip('\n').split(':')[0]
                    doujinshifiles = currentline.rstrip('\n').split(':')[2]
                    await bot.send_message(ctx.message.author, '``' +str(choice) + '``) ' + name + ' (``' + doujinshifiles + '`` pages)')
                    await bot.send_typing(ctx.message.author)
                    if choice == files:
                        await bot.send_message(ctx.message.author, '**Last page reached.**\nType a selection to continue or type ``exit`` to cancel')
                        pick = await bot.wait_for_message(timeout=20.0, author=ctx.message.author)
                        if pick is None:
                            await bot.send_message(ctx.message.author, 'Timed out, try again!')
                            return
                        if pick.content.lower() == 'exit':
                            await bot.send_message(ctx.message.author, 'Dump cancelled')
                            return
                        if int(pick.content) <= files:
                            doujinshiline = num + int(pick.content) - 1
                            await dump_doujinshi(doujinshiline, ctx.message, lines, num)
                            return
                    i = i + 1
                    choice = choice + 1
            else: #when there is more than one page
                choice = 1
                currentpage = 1
                while currentpage <= pages:
                    while choice < currentpage * 10 + 1:
                        await bot.send_message(ctx.message.author, 'Page number ``' + str(currentpage) + '``/``' + str(pages) + '``:')
                        while i < num + files: #for kill la kill is "i < 68 + 13" (which is 81, last line) so this is :ok_hand:
                            currentline = lines[i] #starts at index 0, be careful!
                            name = currentline.rstrip('\n').split(':')[0]
                            doujinshifiles = currentline.rstrip('\n').split(':')[2]
                            await bot.send_message(ctx.message.author, '``' +str(choice) + '``) ' + name + ' (``' + doujinshifiles + '`` pages)')
                            await bot.send_typing(ctx.message.author)
                            choice = choice + 1
                            i = i + 1
                            pagesleft = pages - currentpage
                            if choice > currentpage * 10:
                                await bot.send_message(ctx.message.author, '**Page end reached** (``' + str(pagesleft) + '`` pages left).\nType a selection to continue.\nIf you want to countinue type ``next``. If you want to stop, type ``exit`` instead!')
                                pick = await bot.wait_for_message(timeout=20.0, author=ctx.message.author)
                                if pick is None:
                                    await bot.send_message(ctx.message.author, 'Timed out, try again!')
                                    return
                                if pick.content.lower()  == "exit":
                                    await bot.send_message(ctx.message.author, 'Dump cancelled')
                                    return
                                if pick.content.lower() == "next":
                                    currentpage = currentpage + 1
                                    break
                                if int(pick.content) <= files:
                                        doujinshiline = num + int(pick.content) - 1
                                        await dump_doujinshi(doujinshiline, ctx.message, lines, num)
                                        return
                            if choice > currentpage * 10 or choice == files + 1 and pagesleft == 0:
                                await bot.send_message(ctx.message.author, '**Last page reached.**\nType a selection to continue or type ``exit`` to cancel')
                                pick = await bot.wait_for_message(timeout=20.0, author=ctx.message.author)
                                if pick is None:
                                    await bot.send_message(ctx.message.author, 'Timed out, try again!')
                                    return
                                if pick.content  == "exit":
                                    await bot.send_message(ctx.message.author, 'Dump cancelled')
                                    return
                                if int(pick.content) <= files:
                                        doujinshiline = num + int(pick.content) - 1
                                        await dump_doujinshi(doujinshiline, ctx.message, lines, num)
                                        return

@bot.command(pass_context=True)
async def listshows(ctx):
    """Lists every show in the database."""
    print('User ' + str(ctx.message.author) + ' used $listshows on channel "' + str(ctx.message.channel) +'"')
    await bot.say('Shows in my database:')
    i = 0
    with open('list.txt') as f:
        lines=f.readlines()
        num_lines = file_len('list.txt')
        l = 0
        i = 1
        while l < num_lines + 1:
            await bot.send_typing(ctx.message.channel)
            currentline = lines[l]
            name = currentline.rstrip('\n').split('|')[0]
            name = name.split('~')[1]
            files = currentline.rstrip('\n').split('|')[1]
            await bot.say("**·** ``" + name + '`` (``' + files + '`` doujinshis!)')
            l = l + int(files) + 2
            i = i + 1
            try:
                howdoicallthis = int(str(i)[:-1]) + 1
            except ValueError:
                howdoicallthis = 0
            pages = (int(i / 11)) + 1
            if howdoicallthis > pages:
                await bot.say('**Page end reached**.\nIf you want to countinue type ``next``. If you want to stop, type ``exit`` instead!')
                pick = await bot.wait_for_message(timeout=20.0, author=(ctx.message.author))
                if pick.content.lower() == "exit":
                    await bot.say('If you want a show added, use ``$suggest <show name>``')
                    return
                if pick.content == None:
                    await bot.say('Timed out, automatically exited!')
                    return
                if pick.content.lower() == "next":
                    continue
            else:
                pass
    await bot.say('If you want a show added, use ``$suggest <show name>``')

@bot.command(pass_context=True)
async def suggest(ctx, *, show_name: str):
    """Adds a show to the database."""
    await bot.say('Running script, searching for ``' + show_name + '``...')
    try:
        subprocess.run(["bash", "/media/ero-bot/unpack.bash", show_name], cwd="/media/ero-bot", check=True)
    except subprocess.CalledProcessError:
        print('error on script')
        await bot.say("Bash script error: Couldn't find ``" + show_name + '`` Or there was a problem extracting. Try another show name.')
    else:
        await bot.say('Doujinshi ``' + show_name + '`` successfully added!')

@bot.command(pass_context=True)
async def exact(ctx, show_name : str, name : str):
    """Dumps a doujinshi by providing the show and the exact name."""
    showquery = '~' + show_name + '|'
    with open('list.txt') as f:
        lines=f.readlines()
        num_lines = file_len('list.txt')
        l = 0
        while l < num_lines:
            currentline = lines[l]
            files = int(currentline.split('|')[1])
            await bot.send_typing(ctx.message.channel)
            if showquery.lower() in currentline.lower():
                show = currentline.split('~')[1]
                show = show.split('|')[0]
                error = False
                break
            else:
                l += files + 2
                error = True
        if error == True:
            await bot.say('Show not found, check show names using ``!listshows``')
            return
        if error == False:
            l = l + 1
            showline = l
            await bot.say('Show found! Searching for the doujinshi...')
            while l <= showline + files - 1:
                currentline = lines[l]
                await bot.send_typing(ctx.message.channel)
                if name.lower() in currentline.lower():
                    await dump_doujinshi(l, ctx.message, lines, showline)
                    return
                else:
                    l = l + 1
                    error = True
            if error == True:
                await bot.say('Doujinshi not found, check ``$search ' + show + '``!')

@bot.command()
async def travis(command : str="none", ):
    if travis is None:
        if command.lower() == "uptime":
            await bot.say("The **local** system uptime is: ``" + uptime() + "``")
        if command.lower() == "stop":
            await bot.say("``On a local enviroment. Ignoring stop command``")
        if command.lower() == "none":
            await bot.say("``Currently on a local enviroment!``\nCommands aviable: ``uptime``")
    else:
        if command.lower() == "stop":
            await bot.say("``Stoping Travis build with exit code 0``")
            exit(0)
        if command.lower() == "uptime":
            await bot.say("The **Travis CI** system uptime is:`` " + uptime() + "``")
        if command.lower() == "none":
            await bot.say("``Currently on a Travis CI build!``\nCommands aviable: ``stop``, ``uptime``")


def uptime():
     try:
         f = open( "/proc/uptime" )
         contents = f.read().split()
         f.close()
     except:
        return "Cannot open uptime file: /proc/uptime"

     total_seconds = float(contents[0])

     # Helper vars:
     MINUTE  = 60
     HOUR    = MINUTE * 60
     DAY     = HOUR * 24

     # Get the days, hours, etc:
     days    = int( total_seconds / DAY )
     hours   = int( ( total_seconds % DAY ) / HOUR )
     minutes = int( ( total_seconds % HOUR ) / MINUTE )
     seconds = int( total_seconds % MINUTE )

     # Build up the pretty string (like this: "N days, N hours, N minutes, N seconds")
     string = ""
     if days > 0:
         string += str(days) + " " + (days == 1 and "day" or "days" ) + ", "
     if len(string) > 0 or hours > 0:
         string += str(hours) + " " + (hours == 1 and "hour" or "hours" ) + ", "
     if len(string) > 0 or minutes > 0:
         string += str(minutes) + " " + (minutes == 1 and "minute" or "minutes" ) + ", "
     string += str(seconds) + " " + (seconds == 1 and "second" or "seconds" )

     return string;

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

async def dump_doujinshi(doujinshiline, message, lines, num):
    currentline = lines[doujinshiline]
    name = currentline.rstrip('\n').split(':')[0]
    await bot.send_message(message.author, 'Dumping doujinshi ``' + name + '``! :wink:')
    filename = currentline.rstrip('\n').split(':')[1]
    pages = int(currentline.rstrip('\n').split(':')[2])
    extension = currentline.rstrip('\n').split(':')[3]
    currentline = lines[num - 1]
    show = currentline.split('~')[1]
    show = show.split('|')[0]
    await bot.send_message(message.author, '''Show: ``{}``\nDoujinshi name: ``{}``\nPages: ``{}``'''.format(show, name, str(pages)))
    i = 1
    while i < pages + 1:
        path = "{}/{}/{}{}.{}".format(show, name, filename, str(i), extension)
        content = "Page ``{}``/``{}``".format(str(i), str(pages))
        await bot.send_file(message.author, path, content=content)
        print('Sent file ' + str(i) + ' of doujinshi "' + name + '" to user ' + str(message.author))
        i = i + 1
    await bot.send_message(message.author, 'Dump finished! :ok_hand:')
    print('Dump finished for user ' + str(message.author))

            
@bot.event
async def on_ready():
    print('Logged in as ' + bot.user.name + ' (id: ' + bot.user.id + ')')
    print('------')
    await bot.change_status(discord.Game(name='with doujinshi!'))
    if travis is None:
        print('Running on local enviroment.')
    else:
        print('Running in a Travis enviroment')
        await bot.change_status(discord.Game(name='with doujinshi! [TRAVIS CI]')) #debug
        i = 1
        while True:
            print("Run number " + str(i) + ". Waiting 9 minutes")
            i = i + 1
            await asyncio.sleep(540)

@bot.event
async def on_command_error(err, ctx):
    print('Error ' + str(err) + ' catched!')
    await bot.send_message(ctx.message.channel, 'Error! ``' + str(err) + '``\nContact TheGooDFeelinG#4615 for help!')

token = os.getenv('TOKEN')
travis = os.getenv('TRAVIS')
bot.run(token)
