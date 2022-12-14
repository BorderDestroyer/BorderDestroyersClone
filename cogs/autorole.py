#imports libraries used for the bot
import discord
from discord.ext import commands, tasks
import random
from itertools import cycle
import os
import sqlite3
from discord import Color
from discord.utils import get

class AutoRole(commands.Cog):
    #initializes the cog for use
    def __init__(self, client):
        self.client = client

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#EVENTS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = discord.utils.get(self.client.guilds, name='TheBDLounge')
        role = get(member.guild.roles, name="OG")
        await member.add_roles(role, False)
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = discord.utils.get(self.client.guilds, name='TheBDLounge')
        user = guild.get_member(payload.user_id)
        if str(user) != "BorderDestroyer Clone#3440":
            print(user.name)
            emoji = payload.emoji
            channel = await self.client.fetch_channel(payload.channel_id)
            rolesChannel = await self.client.fetch_channel(1007262952174391356)
            
            if channel != rolesChannel:
                canPass = False
            else:
                canPass = True
                
            if canPass:
                msg = await rolesChannel.fetch_message(payload.message_id)
                role = ""
                if str(emoji) == "๐":
                    role = get(user.guild.roles, name = "He/Him")
                elif str(emoji) == "๐":
                    role = get(user.guild.roles, name = "She/Her")
                elif str(emoji) == "๐งก":
                    role = get(user.guild.roles, name = "They/Them")
                elif str(emoji) == "โค๏ธ":
                    role = get(user.guild.roles, name = "Ask Pronouns")
                elif str(emoji) == "๐ฎ":
                    role = get(user.guild.roles, name = "Gaming")     
                elif str(emoji) == "๐จ":
                    role = get(user.guild.roles, name = "Art")                                    
                elif str(emoji) == "๐ถ":
                    role = get(user.guild.roles, name = "Music")
                elif str(emoji) == "โฝ":
                    role = get(user.guild.roles, name = "Sports")
                elif str(emoji) == "๐":           
                    role = get(user.guild.roles, name = "Reading")
                elif str(emoji) == "๐ป":
                    role = get(user.guild.roles, name = "PC")
                elif str(emoji) == "๐ฅ๏ธ":
                    role = get(user.guild.roles, name = "Playstation")
                elif str(emoji) == "๐จ๏ธ":
                    role = get(user.guild.roles, name = "XBox")
                elif str(emoji) == "๐ฒ๏ธ":
                    role = get(user.guild.roles, name = "Switch")
                elif str(emoji) == "๐ฑ":
                    role = get(user.guild.roles, name = "Mobile")
                elif str(emoji) == "โจ๏ธ":
                    role = get(user.guild.roles, name = "Programming")
                elif str(emoji) == "๐ก":
                    role = get(user.guild.roles, name = "Game Development")
                elif str(emoji) == "๐ง":
                    role = get(user.guild.roles, name = "Anime")
                elif str(emoji) == "๐ซ":
                    role = get(user.guild.roles, name = "Student")
                elif str(emoji) == "โฏ๏ธ":
                    role = get(user.guild.roles, name = "YouTube")
                elif str(emoji) == "๐ฆ":
                    role = get(user.guild.roles, name = "Twitter")
                elif str(emoji) == "๐ท":
                    role = get(user.guild.roles, name = "Instagram")
                elif str(emoji) == "๐ด":
                    role = get(user.guild.roles, name = "FaceBook")
                elif str(emoji) == "โฐ":
                    role = get(user.guild.roles, name = "TikTok")
                else:
                    await msg.remove_reaction(str(emoji), user)
                    return

                if role != "":
                    await user.add_roles(role, False)
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = discord.utils.get(self.client.guilds, name='TheBDLounge')
        user = guild.get_member(payload.user_id)
        if str(user) != "BorderDestroyer Clone#3440":
            emoji = payload.emoji
            channel = await self.client.fetch_channel(payload.channel_id)
            rolesChannel = await self.client.fetch_channel(1007262952174391356)
            
            if channel != rolesChannel:
                canPass = False
            else:
                canPass = True
            
            if canPass:
                msg = await rolesChannel.fetch_message(payload.message_id)
                print(user.name)
                if str(emoji) == "๐":
                    role = get(user.guild.roles, name = "He/Him")
                elif str(emoji) == "๐":
                    role = get(user.guild.roles, name = "She/Her")
                elif str(emoji) == "๐งก":
                    role = get(user.guild.roles, name = "They/Them")
                elif str(emoji) == "โค๏ธ":
                    role = get(user.guild.roles, name = "Ask Pronouns")
                elif str(emoji) == "๐ฎ":
                    role = get(user.guild.roles, name = "Gaming")     
                elif str(emoji) == "๐จ":
                    role = get(user.guild.roles, name = "Art")                                    
                elif str(emoji) == "๐ถ":
                    role = get(user.guild.roles, name = "Music")
                elif str(emoji) == "โฝ":
                    role = get(user.guild.roles, name = "Sports")
                elif str(emoji) == "๐":           
                    role = get(user.guild.roles, name = "Reading")
                elif str(emoji) == "๐ป":
                    role = get(user.guild.roles, name = "PC")
                elif str(emoji) == "๐ฅ๏ธ":
                    role = get(user.guild.roles, name = "Playstation")
                elif str(emoji) == "๐จ๏ธ":
                    role = get(user.guild.roles, name = "XBox")
                elif str(emoji) == "๐ฒ๏ธ":
                    role = get(user.guild.roles, name = "Switch")
                elif str(emoji) == "๐ฑ":
                    role = get(user.guild.roles, name = "Mobile")
                elif str(emoji) == "โจ๏ธ":
                    role = get(user.guild.roles, name = "Programming")
                elif str(emoji) == "๐ก":
                    role = get(user.guild.roles, name = "Game Development")
                elif str(emoji) == "๐ง":
                    role = get(user.guild.roles, name = "Anime")
                elif str(emoji) == "๐ซ":
                    role = get(user.guild.roles, name = "Student")
                elif str(emoji) == "โฏ๏ธ":
                    role = get(user.guild.roles, name = "YouTube")
                elif str(emoji) == "๐ฆ":
                    role = get(user.guild.roles, name = "Twitter")
                elif str(emoji) == "๐ท":
                    role = get(user.guild.roles, name = "Instagram")
                elif str(emoji) == "๐ด":
                    role = get(user.guild.roles, name = "FaceBook")
                elif str(emoji) == "โฐ":
                    role = get(user.guild.roles, name = "TikTok")
                else:
                    await msg.remove_reaction(str(emoji), user)
                    return
                
                if role != "":
                    await user.remove_roles(role, False)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#COMMANDS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    

#allows the mods to initialize the messages for the autorole
    @commands.command()
    @commands.has_role("Mod")
    async def init_roles(self, ctx):       
        embed = discord.Embed(title = "Pronouns", color = Color.purple())
        embed.add_field(name="- * - * - * -", value="""
                        ๐ - He/Him
                        ๐ - She/Her
                        ๐งก - They/Them
                        โค๏ธ - Ask""", inline=True)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("๐")
        await msg.add_reaction("๐")
        await msg.add_reaction("๐งก")
        await msg.add_reaction("โค๏ธ")
        
        embed = discord.Embed(title="Platforms", color = Color.dark_magenta())
        embed.add_field(name="- * - * - * -", value="""
                        
                        ๐ป - PC
                        ๐ฅ๏ธ - Playstation
                        ๐จ๏ธ - XBox
                        ๐ฒ๏ธ - Switch
                        ๐ฑ - Mobile""")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("๐ป")
        await msg.add_reaction("๐ฅ๏ธ")
        await msg.add_reaction("๐จ๏ธ")
        await msg.add_reaction("๐ฒ๏ธ")
        await msg.add_reaction("๐ฑ")
        
        embed = discord.Embed(title="Interests/Hobbies", color = Color.teal())
        embed.add_field(name="- * - * - * -", value="""
                        ๐ฎ - Gaming
                        ๐จ - Art
                        ๐ถ - Music
                        โฝ - Sports
                        ๐ - Reading
                        โจ๏ธ - Programming
                        ๐ก - Game Development
                        ๐ง - Anime
                        ๐ซ - Student""", inline=True)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("๐ฎ")
        await msg.add_reaction("๐จ")
        await msg.add_reaction("๐ถ")
        await msg.add_reaction("โฝ")
        await msg.add_reaction("๐")
        await msg.add_reaction("โจ๏ธ")
        await msg.add_reaction("๐ก")
        await msg.add_reaction("๐ง")
        await msg.add_reaction("๐ซ")
        
        embed = discord.Embed(title="Socials", color = Color.gold())
        embed.add_field(name="- * - * - * -", value="""
                        โฏ๏ธ - YouTube
                        ๐ฆ - Twitter
                        ๐ท - Instagram
                        ๐ด - Facebook
                        โฐ - TikTok""")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("โฏ๏ธ")
        await msg.add_reaction("๐ฆ")
        await msg.add_reaction("๐ท")
        await msg.add_reaction("๐ด")
        await msg.add_reaction("โฐ")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#ERRORS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
#what allows the cog to run
def setup(client):
    client.add_cog(AutoRole(client))