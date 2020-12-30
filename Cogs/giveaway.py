import discord
from discord.ext import commands
import asyncio
import random
import datetime

def convert(time):
    pos = ["s","m","h","d"]

    time_dict = {"s" : 1, "m" : 60, "h" : 3600, "d" : 3600*24}

    unit = time[-1]

    if unit not in pos:
        return -1

    try:
        val = int(time[:-1])
    
    except:
        return -2

    return val * time_dict[unit]

class GiveawayCog(commands.Cog, name = "Giveaway"):
    
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def gcreate(self, ctx):
        def check(m):
            return m.author == ctx.author and m.channel == ctx.message.channel

        color = 0x1abc9c
        em1 = discord.Embed(color = color)
        em1.add_field(name = "Which channel should the giveaway be hosted in?", value = "Mention the `channel`!")
        em1.set_footer(text = "Answer within 30 seconds!")
        await ctx.send(embed = em1)

        try:
            msg1 = await self.client.wait_for('message', check = check, timeout = 30.0)

        except asyncio.TimeoutError:
            await ctx.send("You didnt answer in time!")
            return
        
        else:
            c_id = int(msg1.content[2:-1])
            channel = self.client.get_channel(c_id)

        em2 = discord.Embed(color = color)
        em2.add_field(name = "How much time shall the giveaway last? (s|m|h|d)", value = "Example: 10s, where s = seconds")
        em2.set_footer(text = "Answer within 30 seconds!")
        await ctx.send(embed = em2)

        try:
            msg2 = await self.client.wait_for('message', check = check, timeout = 30.0)

        except asyncio.TimeoutError:
            await ctx.send("You didnt answer in time!")
            return
        
        else:
            time = convert(msg2.content)

        em3 = discord.Embed(color = color)
        em3.add_field(name = "What is the Role requirement if any?", value = "Type `none` for no role requirement!\n> Example: @role")
        em3.set_footer(text = "Answer within 30 seconds!")
        await ctx.send(embed = em3)

        try:
            msg3 = await self.client.wait_for('message', check = check, timeout = 30.0)

        except asyncio.TimeoutError:
            await ctx.send("You didnt answer in time!")
            return
        
        else:
            pass

        em4 = discord.Embed(color = color)
        em4.add_field(name = "What is the prize for the giveaway?", value = "Example: Nitro")
        em4.set_footer(text = "Answer within 30 seconds!")
        await ctx.send(embed = em4)

        try:
            msg4 = await self.client.wait_for('message', check = check, timeout = 30.0)

        except asyncio.TimeoutError:
            await ctx.send("You didnt answer in time!")
            return
        
        else:
            prize = msg4.content

        embed1 = discord.Embed(title = "Giveaway confirmation", description = f"1. `Which channel should giveaway be hosted?`\nAnswer: `#{channel.name}`\n\n2. `How long should the giveaway last?`\nAnswer: `{msg2.content}`\n\n3. `What is the prize for the giveaway?`\nAnswer: {prize}")

        msg = await ctx.send(embed = embed1)
        await msg.add_reaction("<a:jaguartick:780637693746610238>")
        await msg.add_reaction("<a:redcross:781023853807271946>")

        def check(reaction):
            return str(reaction.emoji) in ["<a:jaguartick:780637693746610238>","<a:redcross:781023853807271946>"] and reaction.user_id == ctx.author.id

        reaction = await self.client.wait_for("raw_reaction_add", check = check)

        if str(reaction.emoji) == "<a:jaguartick:780637693746610238>":
            if msg3.content.lower() == "none":
                await ctx.send("<a:jaguartick:780637693746610238> Giveaway created succesfully <:rocktada:786620492176949268>")

                embed = discord.Embed(title = prize, description = f"React with <:rocktada:786620492176949268> to enter\nTime: {msg2.content}\nHosted by: {ctx.author.mention}", color = discord.Color.green())

                my_msg = await channel.send("<:rocktada:786620492176949268> **Giveaway** <:rocktada:786620492176949268>", embed = embed)

                await my_msg.add_reaction("<a:rocktada:786620492176949268>")

                await asyncio.sleep(time)

                new_msg = await channel.fetch_message(my_msg.id)

                users = await new_msg.reactions[0].users().flatten()

                users.pop(users.index(self.client.user))

                if len(users) == 0:
                    await channel.send("No winner could be decided!")
                    return

                winner = random.choice(users)

                emb = discord.Embed(title = prize, description = f"Winner: {winner.mention}\nHosted by {ctx.author.mention}")

                await my_msg.edit(content = "<:rocktada:786620492176949268> **Giveaway Ended** <:rocktada:786620492176949268>", embed = emb)

                await channel.send(f"Congratulations! {winner.mention} won **{prize}**!\nhttps://discord.com/channels/{ctx.guild.id}/{channel.id}/{my_msg.id}")

            else:
                r_id = int(msg3.content[3:-1])
                role = discord.utils.get(ctx.guild.roles, id = r_id)

                embed = discord.Embed(title = prize, description = f"React with <:rocktada:786620492176949268> to enter\nTime: {msg2.content}\nHosted by: {ctx.author.mention}\n\n**Requirements**:\nRole: {role.mention}", color = discord.Color.green())

                my_msg = await channel.send("<:rocktada:786620492176949268> **Giveaway** <:rocktada:786620492176949268>", embed = embed)

                await my_msg.add_reaction("<a:rocktada:786620492176949268>")
                    
                await asyncio.sleep(time)

                new_msg = await channel.fetch_message(my_msg.id)

                users = await new_msg.reactions[0].users().flatten()
            
                users.pop(users.index(self.client.user))

                if len(users) == 0:
                    await channel.send("No winner could be decided!")
                    return

                winner = random.choice(users)

                if role in winner.roles:
                    emb = discord.Embed(title = prize, description = f"Winner: {winner.mention}\nHosted by {ctx.author.mention}")

                    await my_msg.edit(content = "<:rocktada:786620492176949268> **Giveaway Ended** <:rocktada:786620492176949268>", embed = emb)

                    await channel.send(f"Congratulation! {winner.mention} won **{prize}**!\nhttps://discord.com/channels/{ctx.guild.id}/{channel.id}/{my_msg.id}")

                else:
                    em = discord.Embed(description = f"You were missing the role requirement: {role.name}, hence your giveaway will be rerolled!")
                    await winner.send(embed = em)

                    await channel.send("Giveaway will be rerolled automatically since the winner was missing the required role!")

                    new_msg = await channel.fetch_message(my_msg.id)

                    users = await new_msg.reactions[0].users().flatten()

                    users.pop(users.index(self.client.user))

                    winner1 = random.choice(users)

                    if role in winner1.roles:
                        emb = discord.Embed(title = prize, description = f"Winner: {winner1.mention}\nHosted by {ctx.author.mention}")

                        await my_msg.edit(content = "<:rocktada:786620492176949268> **Giveaway Ended** <:rocktada:786620492176949268>", embed = emb)

                        await channel.send(f"Congratulation! {winner1.mention} won the reroll for **{prize}**!\nhttps://discord.com/channels/{ctx.guild.id}/{channel.id}/{my_msg.id}")

                    else:
                        em = discord.Embed(description = f"You were missing the role requirement: {role.name}, hence your rerolled giveaway will be ended now!")
                        await winner.send(embed = em)

                        
                        emb = discord.Embed(title = prize, description = f"Winner: No one won :sob:\nHosted by {ctx.author.mention}")

                        await my_msg.edit(content = "<:rocktada:786620492176949268> **Giveaway Ended** <:rocktada:786620492176949268>", embed = emb)

                        await channel.send("Giveaway ended automatically since the rerolled winner was also missing the required role!")
                        return
                                
        elif str(reaction.emoji) == "<a:redcross:781023853807271946>":
            await ctx.send("The giveaway has been cancelled.......... :sob:")

def setup(client):
    client.add_cog(GiveawayCog(client))
