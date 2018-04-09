import discord
from discord.ext import commands
import asyncio
import os
import hw2
import keys

client = discord.Client()
bot  = commands.Bot(command_prefix='/')
tokenid = keys.discordkey()

@bot.listen()
async def on_ready():
    print('logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('Discord Version: ' + discord.__version__)
    print('--------')

@bot.command()
async def logout(ctx):
    await ctx.send('Logging off...')
    bot.close()
    exit()

@bot.command()
async def matchRates(ctx, match):
    
    hw2.matchRates(match)
    imgfile = discord.File('rates.png')
    await ctx.send('',file=imgfile)

#a747b8ee-e081-4288-8cdb-73d17233c5bd

@bot.command()
async def matchBuild(ctx, match, gamertag):
    await ctx.send('Processing..')
    flag = hw2.matchBuild(match, gamertag)
    build = discord.File('build.txt')
        
    if flag == False:
        await ctx.send('',file=build)
    else:
        obj = open('build.txt','r')
        msg = obj.read()
        await ctx.send('```{}```'.format(msg))
        obj.close()

@bot.command()
async def mmr(ctx, *gamertag):
    #conv = list(gamertag)[0]
    gTag = ' '.join(gamertag)

    hw2.mmr(gTag)
    imgfile = discord.File('mmr.png')
    await ctx.send('',file=imgfile)

bot.run(tokenid)
