# bot.py
# Michael Scott
# 16 April 2021

import os
import asyncpraw
import discord

from discord.ext import commands, tasks

xpost_names = []

# Logging into Reddit
reddit = asyncpraw.Reddit(client_id = 'dwUjUKN3cyr1-w',
                          client_secret = '7UTKg5wvZX7XllDkwVDTe9GFeFiFlA',
                          user_agent = 'picantemoon',
                          username = 'picante01',
                          password = 'DxFzbxKG-2cGz+#'
                         )

# DISCORD TOKEN
#TOKEN = "BLANK FOR GITHUB"
#GUILD = "picante's server"

client = discord.Client()
bot = commands.Bot(command_prefix = '!')

@tasks.loop(seconds = 60)
async def send_message():
    ostr = " "
    subreddit = await reddit.subreddit("CryptoMoonShots")
    post_names = []
    post_url = []
    xpost_names = []
    badpost_names = []
    message_channel = bot.get_channel(830887323021213718)

# Keywords to look for in post description 
    gmarkers = ["liquidity locked", "Liquidity Locked", "Liquidity locked", "liquidity Locked",
            "locked liquidity", "Locked Liquidity", "Locked liquidity", "locked Liquidity",
            "liquidity is locked", "Liquidity is locked", "Liquidity is Locked", "Liquidity Is Locked",
            "Liquidity has been locked", "Liquidity was locked", "liquidity was locked", "liquidity has been locked",
            "Liquidity will be locked", "Liquidity will be Locked", "liquidity will be locked", "liquidity will be Locked",]

# Going through the 5 most recent posts and appending to list
    async for submission in subreddit.new(limit = 5):
        if any(x in submission.selftext for x in gmarkers):
            post_names.append(submission.title)
            print (submission.title)
            print("\nYes! Locked Liquidity :)")
            post_url.append(submission.url)
            print("----------")

        else:
            badpost_names.append(submission.title)
            print(submission.title)
            print("\nNo! No Locked Liquidity :(")
            print("----------")

# Posts or no posts
#FIX NOT DELETING FROM LIST
    print("here is data")
    print(post_names)
    print(xpost_names)
    post_names = [x for x in post_names if x not in xpost_names]
    print(post_names)

    print(f"Finished")

    Npost_names = set(post_names)
    Nxpost_names = set(xpost_names)

    if (post_names == []):
        await message_channel.send("Nothing new!")
        xpost_names = badpost_names
    elif (Npost_names == Nxpost_names):
        await message_channel.send("Nothing new!")
    else:
        await message_channel.send(ostr.join(post_names))
        xpost_names = post_names

    if (post_url == []):
        await message_channel.send("Nothing new!")
    else:
        await message_channel.send(ostr.join(post_url))
        await message_channel.send("@here")

    print(xpost_names)
    print(post_names)

@send_message.before_loop
async def before():
    await bot.wait_until_ready()
    print("Starting up...")

send_message.start()
bot.run(TOKEN)