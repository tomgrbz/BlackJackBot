import discord
from discord.ext import commands
from bj_disc import BlackJackDisc

bot = commands.Bot(command_prefix='.')
blkjck = BlackJackDisc()

@bot.event
async def on_ready():
    game = discord.Game("with cards")
    await bot.change_presence(status=discord.Status.online, activity=game)
    print('bot is online')

@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await bot.close()

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        return

    channel = ctx.channel
    print(ctx.content)
    if '.bj' in ctx.content:
        blkjck.create_embed(True)
        embed_init = blkjck.embed
        await channel.send(embed=embed_init)
    
    elif "hit" in ctx.content:
        blkjck.play_game("hit")
        await channel.send(embed=blkjck.embed)

    elif "stand" in ctx.content:
        blkjck.play_game("stand")
        await channel.send(embed=blkjck.embed)

    elif "r" in ctx.content:
        blkjck.create_embed(False)
        await channel.send(embed=blkjck.embed)

    return
        

@bot.command()
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount)

with open('token.txt') as f:
    TOKEN = f.readline()

bot.run(TOKEN)



