import discord
from discord.ext import commands
import datetime
import sqlite3

class Welcome(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id FROM main WHERE guild_id = {member.guild.id}")
        result = cursor.fetchone()

        if result is None:
            return

        else:
            cursor.execute(f"SELECT msg FROM main WHERE guild_id = {member.guild.id}")
            result1 = cursor.fetchone()
            members = len(list(member.guild.members))
            mention = member.mention
            user = member.name
            guild = member.guild

            embed = discord.Embed(color = 0x1abc9c, description = str(result1[0]).format(members = members, mention = mention, user = user, guild = guild) , timestamp = datetime.datetime.utcnow())
            embed.set_thumbnail(url = member.avatar_url)
            embed.set_author(name = member.name, icon_url = member.avatar_url)

            channel = self.client.get_channel(id = int(result[0]))

        await channel.send(embed = embed)

    @commands.group(invoke_without_command = True)
    async def welcome(self, ctx):
        em = discord.Embed(color = 0x1abc9c, timestamp = ctx.message.created_at)
        em.add_field(name = '<a:jaguartick:780637693746610238> **Available Welcome Setup Commands:**', value = '```welcome channel <#channel>```\n```welcome text <message>```', inline = False)
        em.add_field(name = "Variables to make your welcome message cooler!", value = "<a:pointer:772736004222091305> {user} -- Displays user's name in the message!\n<a:pointer:772736004222091305> {mention} -- Mentions the user in the message!\n<a:pointer:772736004222091305> {guild} -- Sends the server name in the message.\n<a:pointer:772736004222091305> {members} -- Sends the number of members in the server!")

        await ctx.send(embed = em)

    @welcome.command()
    async def channel(self, ctx, channel: discord.TextChannel):
        if ctx.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT channel_id FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()

            if result is None:
                sql = ("INSERT INTO main(guild_id, channel_id) VALUES(?,?)")
                val = (ctx.guild.id, channel.id)

                em = discord.Embed(color = ctx.author.color, timestamp = ctx.message.created_at)
                em.add_field(name = "<a:jaguartick:780637693746610238> Successful Setup!", value = f"Channel succesfully set to {channel.mention}")

                await ctx.send(embed = em)

            elif result is not None:
                sql = ("UPDATE main SET channel_id = ? WHERE guild_id = ?")
                val = (channel.id, ctx.guild.id)

                em = discord.Embed(color = ctx.author.color, timestamp = ctx.message.created_at)
                em.add_field(name = "<a:jaguartick:780637693746610238> Successful Update!", value = f"Channel succesfully updated to {channel.mention}")

                await ctx.send(embed = em)

            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()    

    @welcome.command()
    async def text(self, ctx, *, text):
        if ctx.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT msg FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()

            if result is None:
                sql = ("INSERT INTO main(guild_id, msg) VALUES(?,?)")
                val = (ctx.guild.id, text)

                em = discord.Embed(color = ctx.author.color, timestamp = ctx.message.created_at)
                em.add_field(name = "<a:jaguartick:780637693746610238> Successful Setup!", value = f"Welcome message succesfully set to `{text}`!")

                await ctx.send(embed = em)

            elif result is not None:
                sql = ("UPDATE main SET msg = ? WHERE guild_id = ?")
                val = (text, ctx.guild.id)

                em = discord.Embed(color = ctx.author.color, timestamp = ctx.message.created_at)
                em.add_field(name = "<a:jaguartick:780637693746610238> Successful Update!", value = f"Welcome message succesfully updated to `{text}`!")

                await ctx.send(embed = em)

            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()              
    
def setup(client):
    client.add_cog(Welcome(client))