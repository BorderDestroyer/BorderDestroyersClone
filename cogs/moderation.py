#imports libraries used for the bot
import discord
from discord.ext import commands, tasks
import random
from itertools import cycle
import os
from datetime import datetime

class Moderation(commands.Cog):
    #initializes the cog for use
    def __init__(self, client):
        self.client = client
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#COMMANDS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    

#used to clear messages from a channel
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=0):
        if amount == 0:
            amount = 9999999999999999
        elif amount < 0:
            await ctx.send(f"{ctx.author.mention} Bud, the amount for the purge can't be a negative number...")
    
        await ctx.channel.purge(limit=amount + 1)

#a simple kick command
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"Kicked {member.mention}, they'll probably be back...")

    
#a simple ban command
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"Banned {member.mention}, have a not so wonderful day!")
        
#a simple unban command
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")
        
        for ban_entry in banned_users:
            user = ban_entry.user
        
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"Unbanned {user.mention}, welcome back!")
                return      

#creates the report group    
    @commands.group(pass_context=True)
    async def report(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"{ctx.author.mention} What about reporting would you like to know? Use `bd report help` to see available options!")

#allows members to report bugs to the bug reports channel
    @report.command(aliases=["bugs", "glitch", "glitches"])
    async def bug(self, ctx, *, description):
        await ctx.send(f"{ctx.author.mention} Your bug report has been submitted!")

        bugReportChannel = await self.client.fetch_channel(1008397261421686964)
        
        await bugReportChannel.send(f"""{ctx.author} reported a bug, Description - 
{description}""")
        
#allows member to report members to the member reports channel
    @report.command(aliases=["user", "player", "mem"])
    async def member(self, ctx, member : discord.Member, *, description):
        await ctx.send(f"{ctx.author.mention} You member report has been submitted!")
        
        memberReportChannel = await self.client.fetch_channel(1008397235421188167)

        await memberReportChannel.send(f"""{ctx.author} reported {member}, Description -
{description}""")
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#ERRORS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#handles errors for the clear command
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error,commands.BadArgument):
            await ctx.send(f"{ctx.author.mention} I- What? What do you want me to clear? Tha- What?")
        elif isinstance(error, commands.MissingPermissions(missing_perms)):
            await ctx.send(f"{ctx.author.mention} What do you think you're trying to pull here?")

#handles errors for the kick command
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(f"{ctx.author.mention} I cannot find who you meant for the life of me...")
        elif isinstance(error, commands.MissingPermissions(missing_perms)):
            await ctx.send(f"{ctx.author.mention} What do you think you're trying to pull here?")

#handles errors for the ban command
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(f"{ctx.author.mention} I cannot find who you meant for the life of me...")
        elif isinstance(error, commands.MissingPermissions(missing_perms)):
            await ctx.send(f"{ctx.author.mention} What do you think you're trying to pull here?")

#handles errors for the unban command
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(f"{ctx.author.mention} I cannot find who you meant for the life of me...")
        elif isinstance(error, commands.MissingPermissions(missing_perms)):
            await ctx.send(f"{ctx.author.mention} What do you think you're trying to pull here?")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#FUNCTIONS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
#what allows the cog to run
def setup(client):
    client.add_cog(Moderation(client))