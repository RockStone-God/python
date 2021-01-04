import discord
from discord.ext import commands
import random
import asyncio
import os
import sqlite3
import aiohttp
import http.client
import json

var = "pls "

variable = "Pls "

client = commands.Bot(command_prefix = commands.when_mentioned_or(var, variable), case_insensitive = True, intents = discord.Intents.all())

@client.event
async def on_ready():
    print("""<------------------------->
    Me is online B)
<------------------------->""")

@client.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.CommandOnCooldown):
        m, s = divmod(error.retry_after, 60)
        h, m = divmod(m, 60)
        if int(h) == 0 and int(m) == 0:
            e = discord.Embed(title=f'Woah stop!',description = f" You must wait {int(s)} seconds to use this command! For further help you can join my support server --> https://discord.gg/6SRNBQv !",color=discord.Colour.red())
            await ctx.send(embed = e)
           
        elif int(h) == 0 and int(m) != 0:
            e = discord.Embed(title=f'Woah stop!',description = f" You must wait {int(s)} seconds to use this command! For further help you can join my support server --> https://discord.gg/6SRNBQv !",color=discord.Colour.red())
            await ctx.send(embed = e)

        else:
            e = discord.Embed(title=f"Woah stop!", description = f"You must wait {int(h)} hours , {int(m)} minutes to use this command! For further help you can join my support server --> https://discord.gg/6SRNBQv !",color=discord.Colour.red())
            await ctx.send(embed = e)

    elif isinstance(error, commands.CheckFailure):
        emb = discord.Embed(title = None, color = discord.Colour.red())
        emb.add_field(name = "** <a:redcross:781023853807271946> You dont have permissions to use this command!!**", value = "If you are still having issues, you can join my support server --> https://discord.gg/6SRNBQv !")
        await ctx.send(embed = emb)

    elif isinstance(error, commands.MissingRequiredArgument):
        em = discord.Embed(title = None, color = discord.Colour.red())
        em.add_field(name = "** <a:redcross:781023853807271946> You are missing the required arguements. Please check if your command requires an addition arguement.**", value = "If you are still having issues, you can join my support server --> https://discord.gg/6SRNBQv !")
        await ctx.send(embed = em)

    elif isinstance(error, commands.RoleNotFound):
        em = discord.Embed(title = None, color = discord.Colour.red())
        em.add_field(name = "** <a:redcross:781023853807271946> This role was not found, please mention a valid role!**", value = "If you are still having issues, you can join my support server --> https://discord.gg/6SRNBQv !")
        await ctx.send(embed = em)

@client.event
async def on_guild_join(guild):
    user = client.get_user(639048582531383307)

    guildchannel = guild.system_channel

    invite = await guildchannel.create_invite(max_uses = 100, unique = True)

    await user.send(f"I have been invited to **{guild.name}** which has **{guild.member_count} members** and invite link is {invite}")

@client.command()
async def meme(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://www.reddit.com/r/dankmemes/top.json") as response:
            j = await response.json()

    data = j["data"]["children"][random.randint(0, 25)]["data"]
    image_url = data["url"]
    title = data["title"]
    em = discord.Embed(title=title, color = discord.Color.blurple())
    em.set_image(url=image_url)
    em.set_footer(text = f"Requested by {ctx.message.author}", icon_url = ctx.message.author.avatar_url)
    await ctx.send(embed=em)

@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f"Cogs.{extension}")
    await ctx.send(f"Loaded {extension}.py")

@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f"Cogs.{extension}")
    await ctx.send(f"Unloaded {extension}.py")

@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    client.unload_extension(f"Cogs.{extension}")
    client.load_extension(f"Cogs.{extension}")
    await ctx.send(f"Reloaded {extension}.py")

for filename in os.listdir("./Cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"Cogs.{filename[:-3]}")

client.run("YOUR_TOKEN_HERE")

