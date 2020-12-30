import discord
from discord.ext import commands
import asyncio
import datetime
import re
import sqlite3

class ReactionRole(commands.Cog, name = "Reaction Role"):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):
        main = sqlite3.connect("main.sqlite")
        cursor = main.cursor()

        if '<:' in str(reaction.emoji):
            cursor.execute(f"SELECT emoji, role, message_id, channel_id FROM reaction WHERE guild_id = '{reaction.guild_id}' AND message_id = '{reaction.message_id}' AND emoji = '{reaction.emoji.id}'")
            result = cursor.fetchone()
            guild = self.client.get_guild(reaction.guild_id)

            if result is None:
                return

            elif str(reaction.emoji.id) in str(result[0]):
                on = discord.utils.get(guild.roles, id = int(result[1]))
                user = guild.get_member(reaction.user_id)
                await user.add_roles(on)

            else:
                return

        elif '<:' not in str(reaction.emoji):
            cursor.execute(f"SELECT emoji, role, message_id, channel_id FROM reaction WHERE guild_id = '{reaction.guild_id}' AND message_id = '{reaction.message_id}' AND emoji = '{reaction.emoji.id}'")
            result = cursor.fetchone()
            guild = self.client.get_guild(reaction.guild_id)

            if result is None:
                return

            elif result is not None:
                on = discord.utils.get(guild.roles, id = int(result[1]))
                user = guild.get_member(reaction.user_id)
                await user.add_roles(on)

            else:
                return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, reaction):
        main = sqlite3.connect("main.sqlite")
        cursor = main.cursor()

        if '<:' in str(reaction.emoji):
            cursor.execute(f"SELECT emoji, role, message_id, channel_id FROM reaction WHERE guild_id = '{reaction.guild_id}' AND message_id = '{reaction.message_id}' AND emoji = '{reaction.emoji.id}'")
            result = cursor.fetchone()
            guild = self.client.get_guild(reaction.guild_id)

            if result is None:
                return

            elif str(reaction.emoji.id) in str(result[0]):
                on = discord.utils.get(guild.roles, id = int(result[1]))
                user = guild.get_member(reaction.user_id)
                await user.remove_roles(on)

            else:
                return

        elif '<:' not in str(reaction.emoji):
            cursor.execute(f"SELECT emoji, role, message_id, channel_id FROM reaction WHERE guild_id = '{reaction.guild_id}' AND message_id = '{reaction.message_id}' AND emoji = '{reaction.emoji.id}'")
            result = cursor.fetchone()
            guild = self.client.get_guild(reaction.guild_id)

            if result is None:
                return

            elif result is not None:
                on = discord.utils.get(guild.roles, id = int(result[1]))
                user = guild.get_member(reaction.user_id)
                await user.remove_roles(on)

            else:
                return

    @commands.command(aliases = ["rr"])
    async def reactionrole(self, ctx, channel: discord.TextChannel, messageid, emoji, role: discord.Role):
        main = sqlite3.connect('main.sqlite')
        cursor = main.cursor()
        cursor.execute(f"SELECT emoji, role, message_id, channel_id FROM reaction WHERE guild_id = '{ctx.message.guild.id}' AND message_id = '{messageid}'")
        result = cursor.fetchone()

        if "<:" in emoji:
            enm = re.sub(':.*?:', '', emoji).strip('<>')

            if result is None:
                sql = ("INSERT INTO reaction(emoji, role, message_id, channel_id, guild_id) VALUES(?,?,?,?,?)")
                val = (enm, role.id, messageid, channel.id, ctx.guild.id)
                msg = await channel.fetch_message(messageid)
                en = self.client.get_emoji(int(enm))
                await msg.add_reaction(en)
                await ctx.send(f":white_check_mark: Created reaction role in {channel.mention}!")
            
            elif str(messageid) not in str(result[3]):
                sql = ("INSERT INTO reaction(emoji, role, message_id, channel_id, guild_id) VALUES(?,?,?,?,?)")
                val = (enm, role.id, messageid, channel.id, ctx.guild.id)
                msg = await channel.fetch_message(messageid)
                en = self.client.get_emoji(int(enm))
                await msg.add_reaction(en)
                await ctx.send(f":white_check_mark: Created reaction role in {channel.mention}!")
        
        elif '<:' not in emoji:
            if result is None:
                sql = ("INSERT INTO reaction(emoji, role, message_id, channel_id, guild_id) VALUES(?,?,?,?,?)")
                val = (emoji, role.id, messageid, channel.id, ctx.guild.id)
                msg = await channel.fetch_message(messageid)
                await msg.add_reaction(emoji)
                await ctx.send(f":white_check_mark: Created reaction role in {channel.mention}!")
            
            elif str(messageid) not in str(result[3]):
                sql = ("INSERT INTO reaction(emoji, role, message_id, channel_id, guild_id) VALUES(?,?,?,?,?)")
                val = (emoji, role.id, messageid, channel.id, ctx.guild.id)
                msg = await channel.fetch_message(messageid)
                await msg.add_reaction(emoji)
                await ctx.send(f":white_check_mark: Created reaction role in {channel.mention}!")

        cursor.execute(sql, val)
        main.commit()
        cursor.close()
        main.close()

def setup(client):
    client.add_cog(ReactionRole(client))