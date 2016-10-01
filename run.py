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
    print('Query: ' + query) #Debug
    with open('list.txt') as f:
        for num, line in enumerate(f, 1):
            if query.lower() in line.lower():
                #await bot.send_message(message.channel, 'Found at line ' + str(num)) #Debug
                error = False
                break
            else:
                error = True
        print(error) #Debug
        #There must be a better way than a bool check, but fuck it
        if error is True:
            await bot.say('Not found! Try an exact show name or use ``$listshows``')
        elif error is False:
            print(num) #Debug
            print(line) #Debug
            show = arg
            files = int(line.rstrip('\n').split('|')[1])
            #await bot.send_message(message.channel, 'Number of files: ' + str(files)) #Debug
            f=open('list.txt')
            lines=f.readlines()
            i = num
            choice = 1
            p = 1
            await bot.say('Show found, check your DMs!')
            await bot.send_message(ctx.message.author, 'Found ``' + str(files) + '`` doujinshi')
            await bot.send_typing(ctx.message.author)
            pages = (int(files / 11)) + 1
            await bot.send_message(ctx.message.author, '[DEBUG] Pages: ' + str(pages))
            if pages == 1:
                print('inside 1 page condition')
                while i < num + files:
                    print(i)
                    currentline = lines[i]
                    name = currentline.rstrip('\n').split(':')[0]
                    doujinshifiles = currentline.rstrip('\n').split(':')[2]
                    await bot.send_message(ctx.message.author, '``' +str(choice) + '``) ' + name + ' (``' + doujinshifiles + '`` pages)')
                    await bot.send_typing(ctx.message.author)
                    #await bot.send_message(message.channel, currentline) #Debug
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
                print('inside +1 page condition!')
                choice = 1
                currentpage = 1
                while currentpage <= pages:
                    print(currentpage)
                    while choice < currentpage * 10 + 1:
                        await bot.send_message(ctx.message.author, 'Page number ``' + str(currentpage) + '``/``' + str(pages) + '``:')
                        while i < num + files: #for kill la kill is "i < 68 + 13" (which is 81, last line) so this is :ok_hand:
                            print('i: ' + str(i))
                            print('choice: ' + str(choice))
                            print('files; ' + str(files))
                            currentline = lines[i] #starts at index 0, be careful!
                            name = currentline.rstrip('\n').split(':')[0]
                            doujinshifiles = currentline.rstrip('\n').split(':')[2]
                            await bot.send_message(ctx.message.author, '``' +str(choice) + '``) ' + name + ' (``' + doujinshifiles + '`` pages)')
                            await bot.send_typing(ctx.message.author)
                            #await bot.send_message(message.channel, currentline) #Debug
                            choice = choice + 1
                            i = i + 1
                            pagesleft = pages - currentpage
                            print('currentpage: ' + str(currentpage * 10 + 1))
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
    await bot.say('Shows in my database:')
    i = 0
    with open('list.txt') as f:
        lines=f.readlines()
        num_lines = file_len('list.txt')
        l = 0
        i = 1
        print(num_lines)
        while l < num_lines + 1:
            await bot.send_typing(ctx.message.channel)
            currentline = lines[l]
            print(currentline)
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
            print('i is: ' + str(i))
            print('pages is: ' + str(pages))
            print('howdoicallthis is: ' + str(howdoicallthis))
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
    #await bot.send_message(message.channel, '[DEBUG] howdoicallthis value: ' + str(howdoicallthis))
    #await bot.send_message(message.channel, '[DEBUG] pages value: ' + str (pages))
    #await bot.send_message(message.channel, '[DEBUG] i value: ' + str(i))
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
    #await bot.send_message(message.channel, 'Show name: ``' + show + '``\nDoujinshi name: ``' + name + '``') #Debug
    showquery = '~' + show_name + '|'
    with open('list.txt') as f:
        lines=f.readlines()
        num_lines = file_len('list.txt')
        l = 0
        while l < num_lines:
            currentline = lines[l]
            #print(currentline) #Debug
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
            await bot.say('Show found!')
            #await bot.send_message(message.channel, 'Current line: ``' + currentline + '``') #Debug
            #await bot.send_message(message.channel, '[DEBUG] Max: ' + str(showline + files - 1))
            while l <= showline + files - 1:
                currentline = lines[l]
                await bot.send_typing(ctx.message.channel)
                if name.lower() in currentline.lower():
                    await bot.say('Doujinshi found too!')
                    await dump_doujinshi(l, ctx.message, lines, showline)
                    return
                else:
                    #await bot.send_message(message.channel, '[DEBUG] Not found, current line is ``' + currentline + '`` and l is ``' + str(l) + '``')
                    l = l + 1
                    error = True
            if error == True:
                await bot.say('Doujinshi not found, check ``$search ' + show + '``!')


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
    print(currentline)
    show = currentline.split('~')[1]
    show = show.split('|')[0]
    #await bot.send_message(message.author, '[DEBUG] Line number: ' + str(num))
    #await bot.send_message(message.author, '[DEBUG] Full line: ' + line)
    #await bot.send_message(message.author, 'Show: ``' + show + '``')
    #await bot.send_message(message.author, 'Doujinshi name: ``' + name + '``')
    #await bot.send_message(message.author, 'Pages: ``' + str(pages) + '``')
    await bot.send_message(message.author, '''Show: ``{}``\nDoujinshi name: ``{}``\nPages: ``{}``'''.format(show, name, str(pages)))
    i = 1
    while i < pages + 1:
        path = "{}/{}/{}{}.{}".format(show, name, filename, str(i), extension)
        #await asyncio.sleep(1) #lib handles ratelimits
        #await bot.send_message(message.author, 'Page number ``' + str(i) + '``')
        #await bot.send_file(message.author, show + '/' + name + '/' + filename + str(i) + '.' + extension)
        content = "Page ``{}``/``{}``".format(str(i), str(pages))
        await bot.send_file(message.author, path, content=content)
        print('Sent file ' + str(i))
        i = i + 1
    await bot.send_message(message.author, 'Dump finished! :ok_hand:')
    print('Dump finished!')

            
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

@bot.event
async def on_command_error(err, ctx):
    print('Error ' + str(err) + ' catched!')
    await bot.send_message(ctx.message.channel, 'Error! ``' + str(err) + '``\nContact @TheGooDFeelinG#4615 for help!')

token = os.getenv('TOKEN')
bot.run(token)
