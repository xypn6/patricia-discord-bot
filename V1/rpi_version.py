#rpi version rewritten twice now

# Source code maintained and developed by Sam Pearson
# contact xypn6business@gmail.com for support and issues


# ==== MUST ADD A MAX-SERVER CAP, OTHERWISE IT COULD FILL UP THE RPI SD CARD ====
# Need to rewrite balance algorithm to accept new users.
# will need to get all users in a server then create a new file for each server


# imports all the required modules
import discord
import logging
import random
import sys
import asyncio
import time
import datetime
import os
import pafy
import re
from discord.voice_client import VoiceClient
from discord.ext import commands
from discord.ext.commands import Bot
from pytube import *
from discord import FFmpegPCMAudio, PCMVolumeTransformer
import pymongo

bot_id = ""

sudo_users = ["deathlord730#6438"]
standard_balance = 100

FFMPEG_OPTIONS = {"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", "options": "-vn"}

description = "cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum cum "
help_command = commands.DefaultHelpCommand(no_category = 'help')

activity = discord.Activity()
allowed_mentions = discord.AllowedMentions()
intents = discord.Intents()
client = discord.Client()
messages = discord.Message
voice_client = discord.VoiceClient
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="$", description=description, help_command=help_command, intents=intents)
DBdatabase = pymongo.MongoClient("mongodb://localhost:27017/")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

current_balance = open(r"RPI rewrite 2\current_balance.txt","r+")
balances = current_balance.read()
size = len(current_balance.readlines())
placeholder_balances = balances.split(":")
print(placeholder_balances)
user_balance = dict({})
for i in range(10):
    user_balance[placeholder_balances[i * 2]] = int(placeholder_balances[(i * 2) - 1])
user_balance_2 = user_balance
current_balance.close()

now = datetime.datetime.now()
start_year = now.year
start_month = now.month
start_day = now.day
start_hour = now.hour
start_minute = now.minute 
start_sec = now.second
runTime = "Current Time: "+str(start_hour)+":"+str(start_minute)+":"+str(start_sec)+" "+str(start_day)+"/"+str(start_month)+"/"+str(start_year)
print(runTime)

active_polls = {}

@bot.command(pass_context=True)
async def hi(ctx):
    with open('users.txt','w', encoding='utf-8') as f:
        async for member in ctx.guild.fetch_members(limit=None):
            print("{}:{}".format(member,standard_balance), file=f,)
    print("done")

class Useful(commands.Cog):
    """Commands that provide some sort of usefullness"""
    @commands.command(pass_context=True)
    async def ranInt(self, ctx):
        """Generates a random Integer in a given range"""
        givenRange = str(ctx.message.content[8:])
        intergers = givenRange.split(",")
        print(intergers)
        OutputInt = str("Randomly generated Interger: "+ str(random.randint(int(intergers[0]), int(intergers[1]))))
        await ctx.send(OutputInt)

        
    @commands.command(pass_context=True)
    async def choice(self, ctx):
        """Makes a random choice based on given options.Syntax: '$choice sam,tom'"""
        givenRange = str(ctx.message.content[8:])
        Choices = givenRange.split(",")
        ElementChoice = random.randint(0, int(len(Choices) - 1))
        await ctx.send(Choices[ElementChoice])


    @commands.command(pass_context=True)
    async def time(self, ctx):
        """Displays current time and date"""
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute
        sec = now.second
        print("Current Time: "+str(sec)+":"+str(minute)+":"+str(hour)+" "+str(day)+"/"+str(month)+"/"+str(year))
        current_time = "Current Time: "+str(hour)+":"+str(minute)+":"+str(sec)+" "+str(day)+"/"+str(month)+"/"+str(year)
        await ctx.send(current_time)

    @commands.command(pass_context=True)
    async def poll(self, ctx):
        """Creates a poll people can vote on. Currently can not vote on them"""
        options = ctx.message.content.split()
        creator = str(ctx.message.author)
        if options[1] == "create":
            poll_name = options[2]
            poll_hour = 1
            vote_options = ctx.message.content.split(":")


            await ctx.send("Poll created with name: "+poll_name+"")

        if options[1] == "delete" and str(ctx.message.author) == "deathlord730#6438":
            poll_search = options[2]
            poll_names = list(active_polls.keys())
            for i in range(len(active_polls)):
                if poll_names[i] == poll_search:
                    active_polls.pop(poll_search)
                else:
                    pass

        if options[1] == "query":
            searching = options[2]
            poll_names = list(active_polls.keys())
            for i in range(len(active_polls)):
                if poll_names[i] == searching:
                    found = True
                    await ctx.send("Poll found. Created: "+active_polls[poll_names[i]])
                else:
                    pass
            if found == False:
                await ctx.send("Poll not found")

    @commands.command(pass_context=True)
    async def vote(self, ctx):
        """Votes on a poll. Syntax: $Vote <poll name> <option> <vote (depends on option)>"""
        querys = ctx.message.content.split(" ")
        option = querys[1]
        if option == "list":
            if len(list(active_polls.keys())) != 0:
                await ctx.send("Available polls:"+list(active_polls.keys()))
            else:
                await ctx.send("No available polls")

        elif option == "vote":
            poll = querys[2]
            vote = querys[3]


        elif option == "query":
            pass

        else:
            await ctx.send("Please give a valid response. you can check responses using '$Help $Vote' or '$Help $Poll'")
    
    @commands.command(pass_context=True)
    async def besh(self, ctx):
        with open("besh.png", "rb") as fh:
            f = discord.File(fh, filename="besh.png")
        await ctx.send(file=f)
        await ctx.send('''
        
        Armour Piercing Fin Stabilised Discarding Sabot
        Armour Piercing High Explosive
        Armour Piercing High Explosive Fin Stabilised Discarding Sabot
        Armour Piercing High Explosive Fin Stabilised Discarding Sabot High Explosive Capped Ballisitic Capped
        Armour Piercing High Explosive Fin Stabilised Discarding Sabot High Explosive Anti Tank High Explosive Capped Ballisitic Capped
        :b: :regional_indicator_e: :regional_indicator_s: :regional_indicator_h: 

        ''')

    @commands.command(pass_context=True)
    async def bdays(self, ctx):
        names = ["Sam", "Allie", "Tom", "Millie", "Louie", "Lu", "Eleanor", "Katelyn", "Jodie", "Nate", "Ciaran", "Stu"]
        birthdays =[16/10/2004, 29/10/2004, 22/12/2004, 17/4/2005, "", "", 12/7/2005, "", "", "", "", "", ]
        today_now = datetime.datetime.now()
        today_year = today_now.year
        today_month = today_now.month
        today_day = today_now.day
        today_hour = today_now.hour
        today_minute = today_now.minute 
        today_sec = today_now.second
        bday_string = f'''
        Sam - 16/10/2004
        Allie - 29/10/2004
        Tom - 22/12/2004
        Louie - 26/2/2005
        Millie - 17/4/2004
        Lu - 
        Eleanor - 
        Jodie - 
        Nate - 
        Ciaran - 
        Stu - 
        Katelyn - 12/7/2005
        '''
        await ctx.send(bday_string)

class Fun(commands.Cog):
    """Functions added for a bit of fun"""

    @commands.command(pass_context=True)
    async def repeat(self, ctx):
        """Repeats any message afterwards. Example: '$Repeat Hello!'"""
        variables = ctx.message.content.split(" ")
        await ctx.send(variables[1])


    @commands.command(pass_context=True)
    async def funFact(self, ctx):
        """Displays a randomised fun fact."""
        FunFacts = ["Fuck You"]
        FunString = str("Fun Fact: "+ FunFacts[int(random.randint(0, int(len(FunFacts) - 1)))])
        await ctx.send(FunString)

    @commands.command(pass_context=True)
    async def quote(self, ctx):
        """Returns a random quote"""
        with open('quotes.txt') as quotes_file:
            quotes = [line.rstrip() for line in quotes_file]
        quote = str(quotes[random.randint(0,len(quotes))])
        await ctx.send(quote)

    @commands.command(pass_context=True)
    async def addQuote(self, ctx):
        """Adds a quote to the file."""
        quote = ctx.message.content[10:]
        banned_users = ["Rapid_Rocket#9934"]
        for i in range(len(banned_users)):
            if str(ctx.message.author) == banned_users[i]:
                await ctx.send("Unable to complete this action at this time")
            else:
                if len(quote) < 120:
                    quote_file  = open("quotes.txt", "a")
                    quote_file.write("\n")
                    quote_file.write(quote)
                    quote_file.close()

                    quote_submit_now = datetime.datetime.now()
                    quote_submit_year = quote_submit_now.year
                    quote_submit_month = quote_submit_now.month
                    quote_submit_day = quote_submit_now.day
                    quote_submit_hour = quote_submit_now.hour
                    quote_submit_minute = quote_submit_now.minute
                    quote_submit_sec = quote_submit_now.second
                    quote_submit_time = str(quote_submit_hour)+":"+str(quote_submit_minute)+":"+str(quote_submit_sec)+" "+str(quote_submit_day)+"/"+str(quote_submit_month)+"/"+str(quote_submit_year)

                    await ctx.send("Quote submitted: "+quote+" | By user: "+str(ctx.message.author)+" @ "+quote_submit_time)
                else:
                    await ctx.send("Quote is too long, please submit a shorter")


    @commands.command(pass_context=True)
    async def newTopic(self, ctx):
        """Returns a random question to start a new conversation."""
        topics = ["Whats your favourite instrument?", "Where's your favourite holiday desination and why?", "Who do you think is most likely to become a millionaire?"]
        topic_number = random.randint(0,len(topics))
        await ctx.send(topics[topic_number])


    @commands.command(pass_context=True)
    async def gif(self, ctx):
        """Returns a random gif"""
        with open('gif_file.txt') as gif_file:
            gifs = [line.rstrip() for line in gif_file]
        print(gifs)
        gif_link = str(gifs[random.randint(0,len(gifs))])
        await ctx.send(gif_link)

    @commands.command(pass_context=True)
    async def addGif(self, ctx):
        """Adds a gif from 'https://tenor.com/' or 'https://c.tenor.com/' to the list of gifs"""
        msg_content = ctx.message.content.split(" ")
        gif_link = msg_content[1]

        with open('gif_file.txt') as gif_file:
            gifs = [line.rstrip() for line in gif_file]
        for i in range(len(gifs)):
            if gifs[i] == gif_link:
                already_exists = True
                await ctx.send("Gif already exists")
                break
            else:
                pass
                already_exists = False

        if already_exists == False:

            if gif_link[:18] == "https://tenor.com/" or gif_link[:20] == "https://c.tenor.com/":
                gif_file = open("gif_file.txt", "a")
                gif_file.write("\n")
                gif_file.write(gif_link)
                gif_file.close()

                gif_submit_now = datetime.datetime.now()
                gif_submit_year = gif_submit_now.year
                gif_submit_month = gif_submit_now.month
                gif_submit_day = gif_submit_now.day
                gif_submit_hour = gif_submit_now.hour
                gif_submit_minute = gif_submit_now.minute 
                gif_submit_sec = gif_submit_now.second
                gif_submit_time = str(gif_submit_hour)+":"+str(gif_submit_minute)+":"+str(gif_submit_sec)+" "+str(gif_submit_day)+"/"+str(gif_submit_month)+"/"+str(gif_submit_year)
                print("Gif submitted: "+gif_link+" | By user: "+str(ctx.message.author)+" @ "+gif_submit_time)
                await ctx.send("Gif submitted: "+gif_link+" | By user: "+str(ctx.message.author)+" @ "+gif_submit_time)
            else:
                await ctx.send("Not a 'https://tenor.com/'  or 'https://c.tenor.com/' gif, wont work otherwise")
        else:
            pass

    @commands.command(pass_context=True)
    async def onlineTime(self, ctx):
        """Returns how long the bot has been online."""
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute
        sec = now.second
        online_year = year - start_year
        online_month = month - start_month
        online_day = day - start_day
        online_hour = hour - start_hour
        online_minute = start_minute - minute
        online_sec = sec - start_sec
        online_time = "Online Time: "+str(online_hour)+":"+str(online_minute)+":"+str(online_sec)+" "+str(online_day)+"/"+str(online_month)+"/"+str(online_year)
        await ctx.send(online_time)

class Bank(commands.Cog):
    """Currency based commands"""

    @commands.command(pass_context=True)
    async def balance(self, ctx):
        """Shows your balance in '£'"""
        balance_keys = list(user_balance.keys())
        print(balance_keys)
        for i in range(len(user_balance)):
            if str(balance_keys[i]) == str(ctx.message.author):
                print("Correct user")
                user_balances = str("Your balance is: £"+str(user_balance[balance_keys[i]])+", "+str(ctx.message.author))
                await ctx.send(user_balances)
                break
            else:
                print("Not correct user")

    @commands.command(pass_context=True)
    async def transfer(self, ctx):
        """Send money to another user (%Transfer <recpient>:<amount) - Example: '%Transfer rapid_rocket#9938:10'"""
        balance_keys = list(user_balance_2.keys())
        balance_values = list(user_balance_2.items())
        print(balance_keys)
        for i in range(len(user_balance_2)):
            if str(balance_keys[i]) == str(ctx.message.author):
                print("Correct user")
                contents = str(ctx.message.content)
                recpient = str(contents).split(" ")
                recpient = str(recpient[1]).split(":")
                sent_amount = contents.split(":")
                if int(sent_amount[1]) < 0:
                    await ctx.send("Can not transfer negative value")
                elif int(sent_amount[1]) == 0:
                    await ctx.send("Unable to transfer nil amount")
                else:
                    user_balance = user_balance_2[balance_keys[i]]
                    user_transfer = ctx.message.content[10:]
                    transfer_destination_balance = user_balance_2[str(recpient[0])]
                    user_balance = int(user_balance) - int(sent_amount[1])
                    transfer_destination_balance = transfer_destination_balance + int(sent_amount[1])
                    user_balance_2.update({str(recpient[0]): transfer_destination_balance})
                    user_balance_2.update({str(ctx.message.author): user_balance})

                    transfer_message = str("Transferred £"+str(sent_amount[1])+" to "+str(recpient[0])+", "+str(ctx.message.author))
                    await ctx.send(transfer_message)
                break
            else:
                print("Not correct user")


    print("")

class Admin(commands.Cog):
    """Admin commands"""
    @commands.command(pass_context=True)
    async def kill(self, ctx):
        """Shuts down the bot"""
        if str(ctx.message.author) == "deathlord730#6438":
            await ctx.send("Shutting down...")
            sys.exit()

    @commands.command(pass_context=True)
    async def kick(self, ctx):
        """Kicks a specified user"""
        if str(ctx.message.author) == "deathlord730#6438":
            kick_user = ctx.message.content.split(" ")
            await discord.Member.kick(kick_user[1])
        else:
            pass

class Voice(commands.Cog):
    """Commands for the bot in voice channels"""
    @commands.command(pass_context=True)
    async def join(self, ctx):
        """Joins the bot to the voice channel. Currently, the bot can't do anything in the channel."""
        channel = ctx.message.author.voice.channel
        await channel.connect()

    @commands.command(pass_context=True)
    async def p(self, ctx):
        """Currently doesn't do anything. Just throws up an error"""
        await ctx.send('''
            Traceback (most recent call last):
            File "C:\\Users\diamo\AppData\Local\Programs\Python\Python38\lib\site-packages\discord\ext\commands\bot.py", line 939, in invoke
                await ctx.command.invoke(ctx)
            File "C:\\Users\diamo\AppData\Local\Programs\Python\Python38\lib\site-packages\discord\ext\commands\core.py", line 863, in invoke
                await injected(*ctx.args, **ctx.kwargs)
            File "C:\\Users\diamo\AppData\Local\Programs\Python\Python38\lib\site-packages\discord\ext\commands\core.py", line 94, in wrapped
                raise CommandInvokeError(exc) from exc
            discord.ext.commands.errors.CommandInvokeError: Command raised an exception: AttributeError: 'str' object has no attribute 'guild'
            Ignoring exception in command p:
            Traceback (most recent call last):
            File "C:\\Users\diamo\AppData\Local\Programs\Python\Python38\lib\site-packages\discord\ext\commands\core.py", line 85, in wrapped
                ret = await coro(*args, **kwargs)
            File "d://Coding resources/Python/Discord Bots/discord-bot/rpi_version_rewrite.py", line 439, in p
                link = options[1]
            IndexError: list index out of range

            The above exception was the direct cause of the following exception:

            Traceback (most recent call last):
            File "C:\\Users\diamo\AppData\Local\Programs\Python\Python38\lib\site-packages\discord\ext\commands\bot.py", line 939, in invoke
                await ctx.command.invoke(ctx)
            File "C:\\Users\diamo\AppData\Local\Programs\Python\Python38\lib\site-packages\discord\ext\commands\core.py", line 863, in invoke
                await injected(*ctx.args, **ctx.kwargs)
            File "C:\\Users\diamo\AppData\Local\Programs\Python\Python38\lib\site-packages\discord\ext\commands\core.py", line 94, in wrapped
                raise CommandInvokeError(exc) from exc
            discord.ext.commands.errors.CommandInvokeError: Command raised an exception: IndexError: list index out of range
            ''')
        options = ctx.message.content.split(" ")
        link = options[1]
        converted_link = YouTube(link)
        link_stream = converted_link.streams.get_audio_only()
        link_stream.download()
        file_path = "D:\Coding resources\Python\Discord Bots"+str(converted_link.title)
        channel = ctx.message.author.voice.channel
        if bot.is_connected() == True:
            if bot.is_playing() == False:
                bot.play(file_path)

            else:
                pass

        else:
            channel = ctx.message.author.voice.channel
            await bot.join_voice_channel(channel)

class Testing(commands.Cog):
    """Commands that aren't full emplemented or just dont work (yet)"""

    @commands.command(pass_context=True)
    async def testEmbeds(self, ctx):
        embed = discord.Embed(color=discord.Color.blurple(), description="Test")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def DBdatabaseTest(self,ctx):
        print("")


bot.add_cog(Useful())
bot.add_cog(Fun())
bot.add_cog(Bank())
bot.add_cog(Admin())
bot.add_cog(Voice())
bot.add_cog(Testing())

bot.run(bot_id)


