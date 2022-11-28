#imports libraries used for the bot
import discord
from discord.ext import commands, tasks
import random
from itertools import cycle
import os
from discord import Color
from discord.utils import get

#the token for your bot in the discord dashboard
token ='Nope, you cant have my token'

#sets what the bot is intended for, set to all as default
intents = discord.Intents().all()

#sets the prefix for commands
client = commands.Bot(command_prefix = ["bd ", "Bd ", "bD ", "BD" ], intents=intents) 
client.remove_command('help')

#A list of statuses for the bot to cycle between
status = cycle(['Watching Anime', 'Minecraft', ':D', 'subscribe', 'baking cookies'])

#allows the users specified in the list to load the moderation cog when it has been unloaded due to security breach
canLoadModerationCog = ["BorderDestroyer#7000"]

#channel IDs to use in code for sending messages
spamChannel = client.get_channel(1007001757014048890) 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#EVENTS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#runs when the bot is activated
@client.event
async def on_ready(): 
    change_status.start()
    print("I HAVE BEEN BORNED!")
    
#runs when a member joins the server
@client.event
async def on_member_join(member):
    newPeopleChannel = client.get_channel(1009166982249193493)
    await newPeopleChannel.send(f"Welcome {member.mention} to the server! Please be sure to check out{client.get_channel(1007262952174391356).mention} to get some roles, and {client.get_channel(1007263061121437816).mention} to introduce yourself to everyone here!")

#runs when a member leaves the server
@client.event
async def on_member_remove(member):
    print((f"{member} has left the server"))
      
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#COMMANDS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#used to check the latency of the bot
@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")

#sends all the rules to the channel the message is sent in
@client.command()
@commands.has_role("Mod")
async def init_rules(ctx):
    embed = discord.Embed(title = "Welcome!", color = Color.purple())
    embed.add_field(name="- * - * - * -", value="""
                    **Welcome to The BDLounge!**
                    This is a server not only spread news regarding BorderDestroyer and events, but to also build and interact with this awesome community!
                    
                    - * - * - * -
                    
                    **Rules**
                    Please be sure to read and follow the rules listed below while interacting with the server. I hope you enjoy your time here!
                    
                    - * - * - * -
                    
                    There is one very important rule for while you are here -
                    **Please respect others in the server. Any form of bullying or harrassment will not be tolerated and be punished accordingly. Overall just please use your common sense! If there is someone making you uncomfortable during your stay here, please say so and it will be dealt with accordingly!**
                    """, inline=True)
    await ctx.send(embed=embed)
    
    embed = discord.Embed(color = Color.blurple())
    embed.add_field(name="**RULE  #1: BE RESPECTFUL**", value="""
                    - * - * - * -
                    Please use you common sense on here and don't be a jerk to others. This includes **no hate speach/discriminatory language**, **no toxicity**, and **keep swearing to a minimum** This server is meant to be a nice community getaway for people to have fun and hang out in, so please respect eachother.""", inline=True)
    await ctx.send(embed=embed)
    
    embed = discord.Embed(color = Color.blue())
    embed.add_field(name="**RULE  #2: NO SPAMMING**", value=f"""
                    - * - * - * -
                    Unless it is in {client.get_channel(1007001757014048890).mention}, please keep the **spam to a minimum**. Everyone goes on rants about something every once in a while (I mean take my Twitter for example) but **don't purposefully spam for the sake of being annoying**""", inline=True)
    await ctx.send(embed=embed)
    
    embed = discord.Embed(color = Color.teal())
    embed.add_field(name="**RULE  #3: NO NSFW CONTENT**", value="""
                    - * - * - * -
                    Just don't post it, keep that stuff to yourself. Not everyone wants to see or know what you are into.""", inline=True)
    await ctx.send(embed=embed)
    
    embed = discord.Embed(color = Color.green())
    embed.add_field(name="**RULE  #4: NO MENTION OF POLITICS/RELIGION**", value="""
                    - * - * - * -
                    Politics and religion can very easily become a topic where people get mad at each other and makes it easy for fights to break out, so please refrain from any mention of the subjects.""", inline=True)
    await ctx.send(embed=embed)
    
    embed = discord.Embed(color = Color.dark_green())
    embed.add_field(name="**RULE  #5: DON'T FILE FALSE REPORTS**", value="""
                    - * - * - * -
                    The report system is specifically for cases where someone feels another is not following the rules, so **spamming the report or filing blatantly false reports will not be tolerated**.""", inline=True)
    await ctx.send(embed=embed)
    
    await ctx.send("""Please read the above rules before accessing the server
*Rules can and will be changed overtime*""")

@client.command()
@commands.has_role("Mod")
async def new_rule(ctx):
    embed = discord.Embed(color = Color.dark_orange())
    embed.add_field(name="**RULE #6: NO SCAMMING**", value="""
I feel as though this shouldn't need to be a rule, but this is twice in the last week this has happened. Don't try to scam me or anyone in the server.""")
    await ctx.send(embed=embed)
    
#
@client.command()
@commands.has_role("Mod")
async def init_documentation(ctx):
    embed = discord.Embed(color = Color.purple())
    embed.add_field(name="**DIRECTORY**", value="Here is a list of all the channels in the server and what their purpose is!")
    embed.add_field(name='\u200b', value=f"""
‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿


{client.get_channel(1009166982249193493).mention} - 
Just a channel that shows all the new people who join the server!

{client.get_channel(1007262687484456990).mention} - 
All the rules for the server! Be sure to check them out!

{client.get_channel(1007262952174391356).mention} - 
Go here to get some roles to define who you are!

{client.get_channel(1009182532362834015).mention} - 
It's... It's this... I don't need to explain this...

{client.get_channel(1009184572048683088).mention} - 
Leave your suggestions here! Whether it be for the server, video ideas, anything!""", inline=False)
    embed.add_field(name='\u200b', value=f"""
‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿


{client.get_channel(1009187610683514980).mention} - 
A channel for BorderDestroyer to use to shoutout creators that he likes to watch!

{client.get_channel(1009187685484740708).mention} - 
A channel for you to promote your own content and get yourself out there!

""", inline=False)
    embed.add_field(name='\u200b', value=f"""
‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿


{client.get_channel(1009204112061116527).mention} - 
A channel for you to post job requests for anyone in the server, or to promote commissions that you do!

{client.get_channel(1009204146014015579).mention} - 
A place for you to talk about hel- I mean programming!

{client.get_channel(1010913056064274482).mention} - 
A place for you to talk about you art creations!

{client.get_channel(1010913635138277428).mention} - 
A place for you to talk about your art creations/commissions!""", inline=False)
    embed.add_field(name='\u200b', value=f"""
‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿


{client.get_channel(1007263061121437816).mention} - 
Feel free to introduce yourself here to the rest of the server!

{client.get_channel(1001233995507449909).mention} - 
It's a general chat... Do whatever you want here...

{client.get_channel(1007001757014048890).mention} - 
A place for you to talk about the canned ham product Spam!

{client.get_channel(1008810610399662190).mention} - 
Please send pictures of your animals here, I'm begging you.

{client.get_channel(1009183856500420619).mention} - 
Feel free to post any memes you find funny here!

{client.get_channel(1009184029783887994).mention} - 
Share any music you like to listen to here!

{client.get_channel(1009184324182081536).mention} - 
Whether it's fine art or something I'd make, share it here if you desire!""", inline=False)
    embed.add_field(name='\u200b', value=f"""
‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿


{client.get_channel(1001233995507449910).mention} - 
It's a general voice channel...""", inline=False)
    embed.add_field(name='\u200b', value=f"""
‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿


{client.get_channel(1008813817800708146).mention} - 
This is a channel for notifications for YouTube videos!

{client.get_channel(1008845475035746444).mention} - 
This is a channel for notifications for Twitter posts!""", inline=False)
    embed.add_field(name='\u200b', value=f"""
‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿‿


{client.get_channel(1009182320714072164).mention} - 
Use this channel to play any of the games offered by the bot!""", inline=False)
    await ctx.send(embed=embed)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#TASKS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#changes the bots active status every 10 minutes
@tasks.loop(minutes=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Runs the bot
client.run(token)