#rpi version rewritten twice now

# Source code maintained and developed by Sam Pearson
# contact xypn6business@gmail.com for support and issues


# ==== MUST ADD A MAX-SERVER CAP, OTHERWISE IT COULD FILL UP THE RPI SD CARD ====
# Need to rewrite balance algorithm to accept new users.
# will need to get all users in a server then create a new file for each server


#discord-intergration based imports
import discord
from discord.voice_client import VoiceClient
from discord.ext import commands
from discord.ext.commands import Bot
from pytube import *
from discord import FFmpegPCMAudio, PCMVolumeTransformer

#other imports
import logging
import random
import sys
import asyncio
import time
import datetime
import os
import pafy
import re
import pymongo
import re

sudo_users = ["deathlord730#6438"]

bot_id = ""

standard_balance = 100
FFMPEG_OPTIONS = {"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", "options": "-vn"}
description = "IF YOU DONT UNDERSTAND HOW A COMMAND WORKS, USE FUCKING .help <command>."

help_command = commands.DefaultHelpCommand(no_category = 'help')
activity = discord.Activity()
intents = discord.Intents.all()
client = discord.Client()
messages = discord.Message
voice_client = discord.VoiceClient
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="$", description=description, help_command=help_command, intents=intents)
DBdatabase = pymongo.MongoClient("mongodb://localhost:27017/")
allowed_mentions = discord.AllowedMentions(everyone = True)

now = datetime.datetime.now()
start_year = now.year
start_month = now.month
start_day = now.day
start_hour = now.hour
start_minute = now.minute 
start_sec = now.second
runTime = "Current Time: "+str(start_hour)+":"+str(start_minute)+":"+str(start_sec)+" "+str(start_day)+"/"+str(start_month)+"/"+str(start_year)
print(runTime)
version = "2.0.7"

with open(r"current_balance.txt", "r", encoding='utf-8') as balance_file:
    balance_dict = {}
    balance_read = balance_file.read()
    balance_list = balance_read.split(":")
    user_list = []
    values_list = []
    user_number = int((len(balance_list)))
    for a in range(user_number):
        if (a % 2) == 0 or a == 0:
            user_list.append(str(balance_list[a])[1:])
        else:
            values_list.append(int(balance_list[a]))
    user_list.pop(len(user_list) - 1)
    for i in range(len(user_list)):
        balance_dict[user_list[i]] = values_list[i]
    # balances are stored in balance_dict


def get_user_balance(user):
    for i in range(len(user_list)):
        try:
            user_balance = balance_dict.get(user)
            passed = True
            return user_balance
            break
        except KeyError:
            passed = False
            string = "Unfortunately, You dont have a balance. Creating one now, try again and it should've worked. If you think this an error, Message deathlord730#6438"
            with open(r"current_balance.txt", "a", encoding='utf-8') as balance_file:
                balance_file.write("\n")
                username = user
                add_user = str(username + ":100:")
                balance_file.write(add_user)
                user_list.append(user)
                values_list.append(100)
                balance_dict[user] = 100

def update_file(condition, value, player):
    # win = True, loss = False
    # value = winnings/losses after bet + after multipier if won
    user_balance = get_user_balance(player)
    if condition == True:
        user_balance += int(value)
    else:
        user_balance -= int(value)

    balance_dict.update({player:user_balance})
    updated_user_list = list(balance_dict.keys()) # gets all users in a list
    update_balance_list = list(balance_dict.values())# gets all user values in a list
    updated_dict = []
    for i in range(len(updated_user_list)):
        updated_dict.append(str(str(updated_user_list[i])+":"+str(update_balance_list[i])+":"))
    with open(r"current_balance.txt", "w", encoding='utf-8') as balance_file: # backend file handling for updating balance file
        for i in range(len(updated_dict)):
            balance_file.write("\n")
            balance_file.write(updated_dict[i])

def og_member(username):
    og_members = ["Nathan_#1385", "Rapid_Rocket#9934", "deathlord730#6438", "ciarannn#8722", r"Saggy eyelids😝🤌🏼#5484", "Lucifertherockhoarder#8900", "TheSugarPuffBitch#8010", "alliegatorskinboots#7258", "stu_of_the_art67#6315", "doveflapstick#9555", "Fosshss#5571", "jodierichards#5282"]
    for i in range(len(og_members)):
        if og_members[i] == username:
            confirmed = True
        else:
            pass
    
    if confirmed == True:
        return True
    else:
        return False

def sudo_user(username):
    sudo_users = ["Xypn6#6438"]
    for i in range(len(sudo_users)):
        if sudo_users[i] == username:
            confirmed = True
        else:
            pass
    
    if confirmed == True:
        return True
    else:
        return False

@bot.event
async def on_ready():
    user_id = bot.user.id
    total_member_count = 0
    guild_count = 0
    guild_string = ""
    for g in bot.guilds:
        guild_string += f"{g.name} - {g.id} - Members: {g.member_count}\n"
        total_member_count += g.member_count
        guild_count += 1

    with open(r"guild_file", "w", encoding="utf-8") as guild_file:
        guild_file.write(guild_string)

    print(guild_string)

    activity_name = "over " + str(guild_count) + " guilds."
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=activity_name))


@bot.event
async def on_guild_join(guild):
    join_message = "Thanks for adding me to the server. My prefix is $. Use $help for more information!"
    await guild.text_channels[0].send(join_message)
    user_id = bot.user.id
    total_member_count = 0
    guild_count = 0
    guild_string = ""
    for g in bot.guilds:
        guild_string += f"{g.name} - {g.id} - Members: {g.member_count}\n"
        total_member_count += g.member_count
        guild_count += 1

    with open(r"guild_file", "w", encoding="utf-8") as guild_file:
        guild_file.write(guild_string)

    activity_name = "over " + str(guild_count) + " guilds."
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=activity_name))
    print("Joined new server.")
    print("Updated guild list:")
    print(guild_string)
    print("============")


@bot.event
async def get_all_users(ctx):
    if str(ctx.message.author) == "deathlord730#6438":
        with open(r"user.txt", "w", encoding="utf-8") as f:
            async for member in ctx.guild.fetch_members(limit=None):
                print("{}:{}".format(member, standard_balance), file=f)
        print("done")
    else:
        pass
    
        
@bot.event
async def kill(ctx):
    if str(ctx.message.author) == "deathlord730#6438":
        await ctx.send("Shutting down...")
        sys.exit()
    else:
        pass

@bot.command(pass_context=True)
async def adminBalance(ctx):
    """<recip> <amount>"""
    if str(ctx.message.author) == "deathlord730#6438":
        recip = str((ctx.message.content.split(" ")[1]))
        amount = str((ctx.message.content.split(" ")[2]))
        user_balance = get_user_balance(recip)
        user_balance += int(amount)

        balance_dict.update({recip:user_balance})
        updated_user_list = list(balance_dict.keys()) # gets all users in a list
        update_balance_list = list(balance_dict.values())# gets all user values in a list
        updated_dict = []
        for i in range(len(updated_user_list)):
            updated_dict.append(str(str(updated_user_list[i])+":"+str(update_balance_list[i])+":"))
        with open(r"current_balance.txt", "w", encoding='utf-8') as balance_file: # backend file handling for updating balance file
            for i in range(len(updated_dict)):
                balance_file.write("\n")
                balance_file.write(updated_dict[i])
        
        await ctx.send(f"Added £{amount} to {recip}")
    else:
        pass
    

class Useful(commands.Cog):
    """Commands that provide some sort of usefullness"""
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
        await ctx.send(random.choice(Choices))


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
    async def roadmap(self, ctx):
        """Shows a roadmap for features that are currently in development"""
        ctx.send('''
        Name:                      |  Progress:
        Updated version 2.1        | In progress
        adding non-prefix commands | On hold
        voice commands             | On hold
        ''')
    
    @commands.command(pass_context=True)
    async def validateLu(self, ctx):
        await ctx.send("<@703216469231665195>ILY LU!!!")
        await ctx.message.delete()

    @commands.command(pass_context=True)
    async def submitMod(self, ctx):
        """must be a curseforge mod"""
        msg = str(ctx.message.content)
        print(msg)
        msg = msg[11:]
        print(msg)
        print(msg[:-45])
        msg_list = list(msg)

        msg_str = ""
        for i in range(45):
            msg_str += msg_list[i]
        print(msg_str)
        if msg_str != "https://www.curseforge.com/minecraft/mc-mods/":
            await ctx.send("Not a curse forge mod link. Should start with 'https://www.curseforge.com/minecraft/mc-mods/'")
        else:
            with open('minecraft_mods.txt') as modfile:
                mods = [line.rstrip() for line in modfile]
            print(mods)
            for i in range(len(mods)):
                if mods[i] == msg:
                    await ctx.send("Mod already requested")
                else:
                    with open("minecraft_mods.txt", "a") as mod_file:
                        mod_file.write(msg)
                        mod_file.write("\n")
                        await ctx.send("Mod requested")
                        break

class Fun(commands.Cog):
    """commands added for a bit of cheeky fun"""

    @commands.command(pass_context=True)
    async def repeat(self, ctx):
        """Repeats any message afterwards. Example: '$Repeat Hello!'"""
        await ctx.send(str(ctx.message.content)[8:])

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
        banned_users = [""]
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

    @commands.command(pass_context=True)
    async def funFact(self, ctx):
        """Displays a randomised fun fact."""
        with open('fun_facts.txt') as fact_file:
            facts = [line.rstrip() for line in fact_file]
        fact = str(facts[random.randint(0,len(facts))])
        await ctx.send(fact)
    
    @commands.command(pass_context=True)
    async def addFact(self, ctx):
        """Adds a fun fact"""
        options = ctx.message.split[" "]
        options.pop[0]
        fact = ""
        for i in range(len(options)):
            fact = fact + options[i] + " "
        if len(fact) < 120:
            with open("fun_facts.txt", "a") as fact_file:
                fact_file.write("\n")
                fact_file.write(fact)
            ctx.send("Fact submitted: "+fact)
        else:
            ctx.send("Fact is too long. I only have limited space, please be conservative")

    @commands.command(pass_context=True)
    async def topic(self, ctx):
        """Gets a random topic to talk about"""
        with open(r"topics.txt", "r") as topic_file:
            topics = [line.rstrip() for line in topic_file]
        topic = random.randint(1, len(topics))
        await ctx.send(topics[topic])

    @commands.command(pass_context=True)
    async def addTopic(self, ctx):
        """Adds a topic to talk about"""
        options = ctx.message.content.split(" ")
        options.pop(0)
        topic = ""
        print(options)
        for i in range(len(options)):
            topic = topic + options[i] + " "
        with open(r"topics.txt", "a") as topic_file:
            topic_file.write(topic)
            topic_file.write("\n")

    @commands.command(pass_context=True)
    async def letsGo(self, ctx):
        """LETS GO"""
        await ctx.send("https://tenor.com/view/daceegee-dacg-dababy-less-go-gif-20851407")

    @commands.command(pass_context=True)
    async def activityStatus(self, ctx):
        """
        Allows everyone to change the activity status of the bot
        syntax: $activityStatus <type (playing, watching, listening, streaming)> <text>
        """
        username = str(ctx.message.author)
        og_status = og_member(username)

        if og_status == True:
            options = ctx.message.content.split(" ")
            change_text = ctx.message.content.split(" ")
            change_text.pop(0)
            change_text.pop(0)
            act_type = str(options[1]).lower()
            status_text = ""
            
            for i in range(len(change_text)):
                status_text += change_text[i] + " "
        
            if act_type == "watching":
                    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status_text))

            elif act_type == "listening":
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status_text))

            elif act_type == "streaming":
                await bot.change_presence(activity=discord.Streaming(name=status_text, url="https://www.twitch.tv/xypn6"))

            elif act_type == "playing":
                await bot.change_presence(activity = discord.Game(name=status_text))

            else:
                await ctx.send("Invalid type. Must be either 'Playing', 'Watching', 'Streaming' or 'Listening'")

        else:
            await ctx.send("You do not have permission to use this command")
    
    @commands.command(pass_context=True)
    async def version(self, ctx):
        """a """
        version_number = "2.0.1"
        developer = "Sam Pearson"
        language = "python"
        email = "xypn6business@gmail.com"
        await ctx.send(f'''
            Version: {version_number}
        Developer/s: {developer}
        Language: {language}
        Contact info: {email}''')

    @commands.command(pass_context=True)
    async def goodMorning(self, ctx):
        """Returns a goodmorning message"""
        with open('morning_messages.txt') as morning:
            morning_msg = [line.rstrip() for line in morning]
        msg = str(morning_msg[random.randint(0,len(morning_msg))])
        await ctx.send(msg)

    @commands.command(pass_context=True)
    async def goodMorning(self, ctx):
        """Returns a goodnight message"""
        with open('evening_messages.txt') as evening:
            evening_msg = [line.rstrip() for line in evening]
        msg = str(evening_msg[random.randint(0,len(evening_msg))])
        await ctx.send(msg)

    @commands.command(pass_context=True)
    async def server(self, ctx):
        """server website"""
        await ctx.send("https://xypn6.github.io/")

    @commands.command(pass_context=True)
    async def generateDate(self, ctx):
        """Generate a location, time and idea for a date"""
        places = ["park", "field", "your house", "their house", "pub/restaurant"]
        times = ["sunrise", "early morning", "Mid morning", "early afternoon", "mid afternoon", "late afternoon", "early evening", "mid evening", "late evening", "sunset", "midnight", "11:11"]
        ideas = ["drinks", "drinks and food", "food", "picnic", "dancing", "cake-date", "afternoon tea", "fuckin sex or some shit", "movie night", "just a good ol chat", "some cute shit idk"]

        place = places[(random.randint(0, (len(places))))]
        time = times[(random.randint(0, (len(times))))]
        idea = ideas[(random.randint(0, (len(ideas))))]
        await ctx.send(f"place: {place}")
        await ctx.send(f"time: {time}")
        await ctx.send(f"idea: {idea}")

class Bank(commands.Cog):
    """Commands added to help build an economy"""
    @commands.command(pass_context=True)
    async def balance(self, ctx):
        """Shows your balance in '£'"""
        user = str(ctx.message.author)
        for i in range(len(user_list)):
            try:
                user_balance = balance_dict.get(user)
                passed = True
                break
            except KeyError:
                passed = False
        
        if str(user_balance) != "None":
            string = "Your balance is: £" + str(user_balance)

        elif str(user_balance) == "None" or passed == False:
            string = "Unfortunately, You dont have a balance. Creating one now, try again and it should've worked. If you think this an error, Message Xypn6#6438"
            with open(r"current_balance.txt", "a", encoding='utf-8') as balance_file:
                balance_file.write("\n")
                username = str(ctx.message.author)
                add_user = str(username + ":100:")
                balance_file.write(add_user)
                user_list.append(user)
                values_list.append(100)
                balance_dict[user] = 100

        await ctx.send(string)

    @commands.command(pass_context=True)
    async def transfer(self, ctx):
        """Transfers X amount to another user in the server. $transfer <target user#0000>:<amount>"""
        author = str(ctx.message.author)
        splits = ctx.message.content.split(":")
        recip = splits[0].split(" ")
        recip = str(recip[1])
        amount = int(splits[1])
        #recip = target user
        #amount = transfer amount
        # balances are stored in balance_dict
        passed = False
        for i in range(len(user_list)):
            if user_list[i] == recip:
                passed = True
                print("passed")
            else:
                pass
        if passed == True:
            pass
        else:
            print("not passed")
            await ctx.send("recipient user does not exist / does not have a balance")

        for i in range(len(user_list)): # gets author balance
            if author == user_list[i]:
                author_balance = balance_dict.get(author)
                break
            else:
                pass
        for i in range(len(user_list)): # gets recipient balance
            if recip == user_list[i]:
                recip_balance = balance_dict.get(recip)
                break
            else:
                pass
        
        if author_balance < amount:
            string = f"You have insufficient funds. You tried to transfer £{amount}, but you only have £{author_balance}"
            await ctx.send(string)

        elif amount == "0" or amount == 0:
            await ctx.send("Can not transfer nil value")

        elif author == recip:
            await ctx.send("Can not transfer money to self")

        elif passed != True:
            pass

        else:
            new_balance = author_balance - amount
            recip_new_balance = recip_balance + amount
            balance_dict.update({author:new_balance})
            balance_dict.update({recip:recip_new_balance})
            confirm_string = f"You have transferred £{amount} to '{recip}'. Your balance is now £{new_balance}"
            await ctx.send(confirm_string)# end of front-end code

            updated_user_list = list(balance_dict.keys()) # gets all users in a list
            update_balance_list = list(balance_dict.values())# gets all user values in a list
            updated_dict = []
            for i in range(len(updated_user_list)):
                updated_dict.append(str(str(updated_user_list[i])+":"+str(update_balance_list[i])+":"))

            with open(r"current_balance.txt", "w", encoding='utf-8') as balance_file: # backend file handling for updating balance file
                for i in range(len(updated_dict)):
                    balance_file.write("\n")
                    balance_file.write(updated_dict[i])

class Gambling(commands.Cog):
    """Appears theres nothing here, check back later"""
    @commands.command(pass_context=True)
    async def coinToss(self, ctx):
        """(2x multipler) heads or tails, 50/50. $coinToss <h/t> <amount>"""
        bet_amount = str((ctx.message.content.split(" ")[2]))
        user_choice = str((ctx.message.content.split(" ")[1])).lower()
        ht = random.randint(1,2)
        username = str(ctx.message.author)
        user_balance = get_user_balance(username)
        if user_balance < int(bet_amount):
            await ctx.send("You do not have enough.")
        else:
            if user_choice == "heads" or user_choice == "h":
                user_choice = 1
            elif user_choice == "tails" or user_choice == "t":
                user_choice = 2
            else:
                await ctx.send(f"{user_choice} not valid. enter heads, h, tails or t")

            if user_choice == ht:
                cond = True
                update_file(cond, bet_amount, username)
                username = str(ctx.message.author)
                user_balance = get_user_balance(username)
                await ctx.send(f"You won. Your balance is now £{user_balance}")
            else:
                cond = False
                update_file(cond, bet_amount, username)
                username = str(ctx.message.author)
                user_balance = get_user_balance(username)
                await ctx.send(f"You lost. Your balance is now £{user_balance}")
    
    @commands.command(pass_context=True)
    async def slots(self, ctx):
        """Bet an amount and let the fates decide your winnings. $slots <bet amount>"""
        slot_1 = random.randint(1,6)
        slot_2 = random.randint(1,6)
        slot_3 = random.randint(1,6)
        slot_numbers = []
        slot_numbers.append(slot_1)
        slot_numbers.append(slot_2)
        slot_numbers.append(slot_3)
        combo = ""
        for i in range(3):
            slot_number = slot_numbers[i]
            if slot_number == 1:
                combo += "x"
            elif slot_number == 2:
                combo += "o"
            elif slot_number == 3:
                combo += "?"
            elif slot_number == 4:
                combo += "!"
            elif slot_number == 5:
                combo += "$"
            elif slot_number == 6:
                combo += "£"
        print(combo)
        slot_list = list(combo)
        for i in range(1):
            if slot_list[i] == "£" and slot_list[i+1] == "£" and slot_list[i+2] == "£":
                multiplier = 10
            elif slot_list[i] == "$" and slot_list[i+1] == "$" and slot_list[i+2] == "$":
                multiplier = 5
            elif slot_list[i] == "!" and slot_list[i+1] == "!" and slot_list[i+2] == "!":
                multiplier = 3
            elif slot_list[i] == "?" and slot_list[i+1] == "?" and slot_list[i+2] == "?":
                multiplier = 2
            elif slot_list[i] == "o" and slot_list[i+1] == "o" and slot_list[i+2] == "o":
                multiplier = 1.75
            elif slot_list[i] == "x" and slot_list[i+1] == "x" and slot_list[i+2] == "x":
                multiplier = 1.3
            elif slot_list[i] == "x" and slot_list[i+1] == "x":
                multiplier = 1.1
            elif slot_list[i] == "x" and slot_list[i+2] == "x":
                multiplier = 1.1
            elif slot_list[i+1] == "x" and slot_list[i+2] == "x":
                multiplier = 1.1
            elif slot_list[i] == "x" or slot_list[i+1] == "x" or slot_list[i+2] == "x":
                multiplier = 1
            else:
                multiplier = 0
        bet_amount = int((ctx.message.content.split(" ")[1]))
        user_balance = get_user_balance(str(ctx.message.author))
        if bet_amount > user_balance:
            await ctx.send(f"Your balance is {user_balance}. Bet less")
        else:
            user = str(ctx.message.author)
            user_balance -= bet_amount
            cond2 = False
            update_file(cond2, bet_amount, user)
            print(user_balance)
            winnings = bet_amount * multiplier
            print(winnings)
            cond = True
            update_file(cond, winnings, user)
            await ctx.send("Spinning...")
            time.sleep(2)
            slot_string = str("| "+slot_list[0]+" | "+slot_list[1]+" | "+slot_list[2]+" |")
            await ctx.send(f"{slot_string} = {winnings}")

    @commands.command(pass_context=True)
    async def blackjack(self, ctx):
        print("")
    
    @commands.command(pass_context=True)
    async def roulette(self, ctx):
        print("")
    
    @commands.command(pass_context=True)
    async def pontoon(self, ctx):
        """Also known as 'first to 21'. Rules: start with 2 cards, then draw until you think you've beat the dealer, daren't go anymore, got 21 or gone 'bust'. Jack, queen and king = 10. ace = 1 or 11. """
        # if anyones reading this, ik its not the most efficient method, buts it 4 am, im on 2 hours sleep and ive had enough caffiene to floor an elephant. cut me a fuckin break.

        #    msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        #    if msg.content.lower() == <message>:
        
        # if <card> in <list>:
        #   does this
        # else:
        #   does this
        
        #cards: ace = 1/11 (ask user), jack=10, queen=10, king = 10
        #pos: ace=1, 1 = 2, 2=3, 3=4, 4=5, 5=6, 6=7, 7=8, 8=9, 9=10, 10=11, jack=12, queen=13, king=14

        jack = 10
        queen = 10
        king = 10 
        bet_amount = str((ctx.message.content.split(" ")[1]))
        
        player_cards = []
        auth = str(ctx.message.author)
        channel = ctx.channel.id
        dealer_value = 0 # either going to be preset value or random / biased value added each "tick"
        for i in range(2):
            player_cards.append(str(random.randint(1,14)))
            for i in range(len(player_cards)):
                if player_cards[i] == "1":
                    ace_value = 2

                elif player_cards[i] == "2" or player_cards[i] == "3" or player_cards[i] == "4" or player_cards[i] == "5" or player_cards[i] == "6" or player_cards[i] == "7" or player_cards[i] == "8" or player_cards[i] == "9" or player_cards[i] == "10" or player_cards[i] == "11":
                    player_cards[i] = int(int(player_cards[i]) - 1) 

                elif player_cards[i] == "12" or player_cards[i] == "13" or player_cards[i] == "14":
                    player_cards[i] = 10

        bust = False
        total = 0
        while bust == False:
            total = 0
            for i in range(len(player_cards)):
                if player_cards[i] == 1:
                    await ctx.send("Ace: 1 or 11")
                    ace_value = await bot.wait_for("message", check=lambda message: str(ctx.message.author) == auth)
                    ace_pass = False
                    while ace_pass == False:
                        if ace_value.content == "1":
                            player_cards[i] = 1
                            ace_pass = True
                        elif ace_value.content == "11":
                            player_cards[i] == 11
                            ace_pass = True
                        else:
                            await ctx.send("Ace: 1 or 11")
                            ace_value = await bot.wait_for("message", check=lambda message: str(ctx.message.author) == auth)

                elif player_cards[i] == "2" or player_cards[i] == "3" or player_cards[i] == "4" or player_cards[i] == "5" or player_cards[i] == "6" or player_cards[i] == "7" or player_cards[i] == "8" or player_cards[i] == "9" or player_cards[i] == "10":
                    player_cards[i] = int(int(player_cards[i]) - 1)
                
                elif player_cards[i] == "11":
                    player_cards[i] = 11

                elif player_cards[i] == "12" or player_cards[i] == "13" or player_cards[i] == "14":
                    player_cards[i] = 10
                
                else:
                    pass
            
            for a in range(len(player_cards)):
                total += player_cards[a]
            await ctx.send(f"Card total: {total}")

            passed = False
            while passed == False:
                await ctx.send("hit(take card) or stick(stay) ")
                next_card = await bot.wait_for("message", check=lambda message: str(ctx.message.author) == auth)
                if next_card.content.lower() == "hit" or next_card.content.lower() == "take card" or next_card.content.lower() == "twist":
                    player_cards.append(str(random.randint(1,14)))
                    if total > 21:
                        bust = False
                        busted = True
                    else:
                        busted = False
                    passed = True
                elif next_card.content.lower() == "stick" or next_card.content.lower() == "stay":
                    if total > 21:
                        busted = True
                    else:
                        busted = False
                    passed = True
                    bust = True
                else:
                    pass

            await ctx.send(player_cards)
        if busted == True:
            await ctx.send(f"You busted.")
        else:
            await ctx.send("placeholder")
        


bot.add_cog(Useful())
bot.add_cog(Fun())
bot.add_cog(Bank())
bot.add_cog(Gambling())


bot.run(bot_id)
