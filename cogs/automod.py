#imports libraries used for the bot
import discord
from discord.ext import commands, tasks
import random
from itertools import cycle
import os
import sqlite3

banned_words = ["dyke", "fag", "faggot", "fagg", "retard", "r-word", "r word", "retarded", "n-word", "n word", " homo ", "nigger", "nigga", "queer", "slut", "whore", "nig"]

class AutoMod(commands.Cog):
    #initializes the cog for use
    def __init__(self, client):
        self.client = client

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#COMMANDS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    

#checks messages to see if they contain the banned words listed above
    @commands.Cog.listener()
    async def on_message(self, message):
        channel = message.channel
        memberReportChannel = await self.client.fetch_channel(1008397235421188167)
        if message.author.name != "BorderDestroyer Clone#3440" and channel != memberReportChannel:
            content = str(message.content).lower()
            content_broken = content.split()
            for u in range(len(content_broken)):
                for i in range(len(banned_words)):
                    if banned_words[i] in content_broken[u]:
                        if len(banned_words[i]) == len(content_broken[u]):
                            await message.delete()
                            
                            await channel.send(f"{message.author.mention} Your message has been removed for innapropriate language, if you think this was a mistake, please use `bd report bug <description>`")
                            await memberReportChannel.send(f"""{message.author} Has had a message removed in {channel.mention}, message content:
**"{message.content}"**""")
                            
                            break


                
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
#what allows the cog to run
def setup(client):
    client.add_cog(AutoMod(client))