#imports libraries used for the bot
import discord
from discord.ext import commands, tasks
import random
from itertools import cycle
import os
import psycopg2

con = psycopg2.connect('postgres://rdmzqeqchqmaxa:32a505f2159c2f43b17585a19b646452eab0a6ea01243aa87ac255f8be331dbe@ec2-44-205-112-253.compute-1.amazonaws.com:5432/d9uof29k60cnp1', sslmode='require')
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS curHelpPrompts
            (name text, message text, page real)''')




class HelpCommands(commands.Cog):
    #initializes the cog for use
    def __init__(self, client):
        self.client = client

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#EVENTS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~      
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        pUser = payload.member
        if str(pUser) != "BorderDestroyer Clone#3440":        
            cur.execute("""SELECT name
                        FROM curHelpPrompts
                        WHERE name=%s""",
                        [str(pUser),])
            user = str(cur.fetchone()[0])
            
            if user:
                cur.execute("""SELECT message
                            FROM curHelpPrompts
                            WHERE name=%s""",
                            [str(pUser),])
                messageID = str(cur.fetchone()[0])
                
                if messageID == str(payload.message_id):
                    cur.execute("""SELECT page
                                FROM curHelpPrompts
                                WHERE name=%s""",
                                [str(pUser),])
                    page = int(cur.fetchone()[0])
                    
                    pEmoji = payload.emoji
                    Channel = self.client.get_channel(payload.channel_id)
                    msg = await Channel.fetch_message(messageID)
                    
                    page1 = discord.Embed(title="Help Prompt!", color=discord.Color.dark_purple())
                    page1.add_field(name="Default Commands:", value="""
            `bd ping` - Used to see the latency of the bot""")
                    
                    page2 = discord.Embed(title="Help Prompt!", color=discord.Color.dark_purple())
                    page2.add_field(name="Currency Commands: ", value="""
            `bd currency show <user>` - shows the currency held by specified user
            `bd currency destroy <amount>` - destroys specified currency
            `bd bal` - shows how much money you own
            `bd pay <amount> <user>` - pays the specified user""")

                    
                    page3 = discord.Embed(title="Help Prompt!", color=discord.Color.dark_purple())
                    page3.add_field(name="Music Commands:", value="""
            `bd join` - Makes the bot join the voice channel you are in
            `bd play <url>` - adds the url to the queue for the bot to play
            `bd skip` - skips the current song (needs 3 votes)
            `bd queue` - shows the queue for the bot to play""")
                            
                    page4 = discord.Embed(title="Help Prompt!", color=discord.Color.dark_purple())
                    page4.add_field(name="Game Commands:", value="""
            `bd bj <bet>` - Starts a blackjack game, the bet is not required
            `bd cf <choice> <bet>` - Does a coinflip, the bet is not required
            `bd rps <bet>` - Plays Rock Paper Scissors, the bet is not required
            `bd 8ball <question>` - Replies to your question""")
                    
                    page5 = discord.Embed(title="Help Prompt!", color=discord.Color.dark_purple())
                    page5.add_field(name="Report Commands:", value="""
            `bd report bug <description>` - Sends a bug report
            `bd report member <reason>` - Sends a report about a player""")
                    
                    if str(pEmoji) == "◀️":
                        await msg.remove_reaction("◀️", payload.member)
                        page = page - 1
                        
                        while page > 5:
                            page -= 5
                        while page < 1:
                            page += 5
                                                
                        if page == 1:
                            await msg.edit(embed=page1)
                        elif page == 2:
                            await msg.edit(embed=page2)
                        elif page == 3:
                            await msg.edit(embed=page3)
                        elif page == 4:
                            await msg.edit(embed=page4)
                        elif page == 5:
                            await msg.edit(embed=page5)
                            
                        cur.execute("""UPDATE curHelpPrompts
                            SET page=%s, message=%s
                            WHERE name=%s""",
                            [page, msg.id, str(pUser)])
                        
                    elif str(pEmoji) == "▶️":
                        await msg.remove_reaction("▶️", payload.member)
                        page = page + 1
                        
                        while page > 5:
                            page -= 5
                        while page < 0:
                            page += 5
                                                
                        if page == 1:
                            await msg.edit(embed=page1)
                        elif page == 2:
                            await msg.edit(embed=page2)
                        elif page == 3:
                            await msg.edit(embed=page3)
                        elif page == 4:
                            await msg.edit(embed=page4)
                        elif page == 5:
                            await msg.edit(embed=page5)
                            
                        cur.execute("""UPDATE curHelpPrompts
                            SET message=%s, page=%s
                            WHERE name=%s""",
                            [msg.id, page, user])
                    else:
                        await msg.remove_reaction(str(payload.emoji), payload.member)
                else:
                    await msg.remove_reaction(str(payload.emoji), payload.member)
            else:
                await msg.remove_reaction(str(payload.emoji), payload.member) 
            
            con.commit()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#COMMANDS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    

#sends the initial help command
    @commands.command()
    async def help(self, ctx, page=1):
        page1 = discord.Embed(title="Help Prompt!", color=discord.Color.dark_purple())
        page1.add_field(name="Default Commands:", value="""
`bd ping` - Used to see the latency of the bot""")
        
        page2 = discord.Embed(title="Help Prompt!", color=discord.Color.dark_purple())
        page2.add_field(name="Currency Commands: ", value="""
`bd currency show <user>` - shows the currency held by specified user
`bd currency destroy <amount>` - destroys specified currency
`bd bal` - shows how much money you own
`bd pay <amount> <user>` - pays the specified user""")

        
        page3 = discord.Embed(title="Help Prompt!", color=discord.Color.dark_purple())
        page3.add_field(name="Music Commands:", value="""
`bd join` - Makes the bot join the voice channel you are in
`bd play <url>` - adds the url to the queue for the bot to play
`bd skip` - skips the current song (needs 3 votes)
`bd queue` - shows the queue for the bot to play""")
                
        page4 = discord.Embed(title="Help Prompt!", color=discord.Color.dark_purple())
        page4.add_field(name="Game Commands:", value="""
`bd bj <bet>` - Starts a blackjack game, the bet is not required
`bd cf <bet>` - Does a coinflip, the bet is not required
`bd rps <bet>` - Plays Rock Paper Scissors, the bet is not required
`bd 8ball <question>` - Replies to your question""")
        
        page5 = discord.Embed(title="Help Prompt!", color=discord.Color.dark_purple())
        page5.add_field(name="Report Commands:", value="""
`bd report bug <description>` - Sends a bug report
`bd report member <reason>` - Sends a report about a player""")
        
        cur.execute("""SELECT name
                    FROM curHelpPrompts
                    WHERE name=%s""",
                    [str(ctx.author),])
        result = cur.fetchone()
        
        while page > 5:
            page -= 5
        while page < 0:
            page += 5           

        if page == 1:
            helpMSG = await ctx.send(embed=page1)
        elif page == 2:
            helpMSG = await ctx.send(embed=page2)
        elif page == 3:
            helpMSG = await ctx.send(embed=page3)
        elif page == 4:
            helpMSG = await ctx.send(embed=page4)
        elif page == 5:
            helpMSG = await ctx.send(embed=page4)
        
        await helpMSG.add_reaction("◀️")
        await helpMSG.add_reaction("▶️")
        
        if not result:
            cur.execute(f'''INSERT INTO curHelpPrompts VALUES
                        ('{str(ctx.author)}', {str(helpMSG.id)}, '{int(page)}')''')
            con.commit()
        else:
            cur.execute('''UPDATE curHelpPrompts
                        SET message=%s, page=%s
                        WHERE name=%s''',
                        [str(helpMSG.id), int(page), str(ctx.author),])
            con.commit()
                   
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#ERRORS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
#what allows the cog to run
def setup(client):
    client.add_cog(HelpCommands(client))