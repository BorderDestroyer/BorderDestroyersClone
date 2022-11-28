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
                if str(emoji) == "💙":
                    role = get(user.guild.roles, name = "He/Him")
                elif str(emoji) == "💜":
                    role = get(user.guild.roles, name = "She/Her")
                elif str(emoji) == "🧡":
                    role = get(user.guild.roles, name = "They/Them")
                elif str(emoji) == "❤️":
                    role = get(user.guild.roles, name = "Ask Pronouns")
                elif str(emoji) == "🎮":
                    role = get(user.guild.roles, name = "Gaming")     
                elif str(emoji) == "🎨":
                    role = get(user.guild.roles, name = "Art")                                    
                elif str(emoji) == "🎶":
                    role = get(user.guild.roles, name = "Music")
                elif str(emoji) == "⚽":
                    role = get(user.guild.roles, name = "Sports")
                elif str(emoji) == "📕":           
                    role = get(user.guild.roles, name = "Reading")
                elif str(emoji) == "💻":
                    role = get(user.guild.roles, name = "PC")
                elif str(emoji) == "🖥️":
                    role = get(user.guild.roles, name = "Playstation")
                elif str(emoji) == "🖨️":
                    role = get(user.guild.roles, name = "XBox")
                elif str(emoji) == "🖲️":
                    role = get(user.guild.roles, name = "Switch")
                elif str(emoji) == "📱":
                    role = get(user.guild.roles, name = "Mobile")
                elif str(emoji) == "⌨️":
                    role = get(user.guild.roles, name = "Programming")
                elif str(emoji) == "😡":
                    role = get(user.guild.roles, name = "Game Development")
                elif str(emoji) == "🧙":
                    role = get(user.guild.roles, name = "Anime")
                elif str(emoji) == "🏫":
                    role = get(user.guild.roles, name = "Student")
                elif str(emoji) == "⏯️":
                    role = get(user.guild.roles, name = "YouTube")
                elif str(emoji) == "🐦":
                    role = get(user.guild.roles, name = "Twitter")
                elif str(emoji) == "📷":
                    role = get(user.guild.roles, name = "Instagram")
                elif str(emoji) == "👴":
                    role = get(user.guild.roles, name = "FaceBook")
                elif str(emoji) == "⏰":
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
                if str(emoji) == "💙":
                    role = get(user.guild.roles, name = "He/Him")
                elif str(emoji) == "💜":
                    role = get(user.guild.roles, name = "She/Her")
                elif str(emoji) == "🧡":
                    role = get(user.guild.roles, name = "They/Them")
                elif str(emoji) == "❤️":
                    role = get(user.guild.roles, name = "Ask Pronouns")
                elif str(emoji) == "🎮":
                    role = get(user.guild.roles, name = "Gaming")     
                elif str(emoji) == "🎨":
                    role = get(user.guild.roles, name = "Art")                                    
                elif str(emoji) == "🎶":
                    role = get(user.guild.roles, name = "Music")
                elif str(emoji) == "⚽":
                    role = get(user.guild.roles, name = "Sports")
                elif str(emoji) == "📕":           
                    role = get(user.guild.roles, name = "Reading")
                elif str(emoji) == "💻":
                    role = get(user.guild.roles, name = "PC")
                elif str(emoji) == "🖥️":
                    role = get(user.guild.roles, name = "Playstation")
                elif str(emoji) == "🖨️":
                    role = get(user.guild.roles, name = "XBox")
                elif str(emoji) == "🖲️":
                    role = get(user.guild.roles, name = "Switch")
                elif str(emoji) == "📱":
                    role = get(user.guild.roles, name = "Mobile")
                elif str(emoji) == "⌨️":
                    role = get(user.guild.roles, name = "Programming")
                elif str(emoji) == "😡":
                    role = get(user.guild.roles, name = "Game Development")
                elif str(emoji) == "🧙":
                    role = get(user.guild.roles, name = "Anime")
                elif str(emoji) == "🏫":
                    role = get(user.guild.roles, name = "Student")
                elif str(emoji) == "⏯️":
                    role = get(user.guild.roles, name = "YouTube")
                elif str(emoji) == "🐦":
                    role = get(user.guild.roles, name = "Twitter")
                elif str(emoji) == "📷":
                    role = get(user.guild.roles, name = "Instagram")
                elif str(emoji) == "👴":
                    role = get(user.guild.roles, name = "FaceBook")
                elif str(emoji) == "⏰":
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
                        💙 - He/Him
                        💜 - She/Her
                        🧡 - They/Them
                        ❤️ - Ask""", inline=True)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("💙")
        await msg.add_reaction("💜")
        await msg.add_reaction("🧡")
        await msg.add_reaction("❤️")
        
        embed = discord.Embed(title="Platforms", color = Color.dark_magenta())
        embed.add_field(name="- * - * - * -", value="""
                        
                        💻 - PC
                        🖥️ - Playstation
                        🖨️ - XBox
                        🖲️ - Switch
                        📱 - Mobile""")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("💻")
        await msg.add_reaction("🖥️")
        await msg.add_reaction("🖨️")
        await msg.add_reaction("🖲️")
        await msg.add_reaction("📱")
        
        embed = discord.Embed(title="Interests/Hobbies", color = Color.teal())
        embed.add_field(name="- * - * - * -", value="""
                        🎮 - Gaming
                        🎨 - Art
                        🎶 - Music
                        ⚽ - Sports
                        📕 - Reading
                        ⌨️ - Programming
                        😡 - Game Development
                        🧙 - Anime
                        🏫 - Student""", inline=True)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("🎮")
        await msg.add_reaction("🎨")
        await msg.add_reaction("🎶")
        await msg.add_reaction("⚽")
        await msg.add_reaction("📕")
        await msg.add_reaction("⌨️")
        await msg.add_reaction("😡")
        await msg.add_reaction("🧙")
        await msg.add_reaction("🏫")
        
        embed = discord.Embed(title="Socials", color = Color.gold())
        embed.add_field(name="- * - * - * -", value="""
                        ⏯️ - YouTube
                        🐦 - Twitter
                        📷 - Instagram
                        👴 - Facebook
                        ⏰ - TikTok""")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("⏯️")
        await msg.add_reaction("🐦")
        await msg.add_reaction("📷")
        await msg.add_reaction("👴")
        await msg.add_reaction("⏰")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#ERRORS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
#what allows the cog to run
def setup(client):
    client.add_cog(AutoRole(client))