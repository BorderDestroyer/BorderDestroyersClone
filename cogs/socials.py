#imports libraries used for the bot
import discord
from discord.ext import commands, tasks
import random
from itertools import cycle
import os
import sqlite3
from discord import Color
from discord.utils import get
from googleapiclient.discovery import build
import tweepy
import psycopg2

peopleToSellout = ["BorderDestroyer", "ChiefOfBricks"]

#initializes twitter api
twitterApiKey = 'hMLEzhaBHeq1OdKjugIUmHzQA'
twitterSecretKey = 'oL1oJEMQnsmsv8ERpaUuKWhztjYIGPf4A7rj3328LDBMWojBcW'
twitterBearerKey = 'AAAAAAAAAAAAAAAAAAAAANcDgAEAAAAAppGIUHWXETzPVBaBQoE5ipds5nU%3DkodryiFUC2FtEEyUmLJFnbxzxdGJS4iV4NZf13fSsfF9Dfh0X9'
twitterAccessToken = '1379616063999119361-WHZzpLx3QS205HqIBJoH7W6xclni33'
twitterAccessTokenSecret = 'Nm1ngqzdcTdgOZ4utZpZAtEt2l9rwgbr4QRUmPeslwwnJ'

auth = tweepy.OAuthHandler(twitterApiKey, twitterSecretKey)
auth.set_access_token(twitterAccessToken, twitterAccessTokenSecret)

api = tweepy.API(auth)

twitterHandles = ["border_game"]

#initializes YouTube api
youtube = build('youtube', 'v3', developerKey='AIzaSyANT73U7GE7w_KYNGkAQ6-6VFkTF_QH5Mo')
YouTubersID = ['UCKeSimtpEbtM1ZsA-Dqs6zg', "UCFdxznUIgXCUzk6wfbk6KyQ"]

#creates database for storing latest content data
con = psycopg2.connect('postgres://rdmzqeqchqmaxa:32a505f2159c2f43b17585a19b646452eab0a6ea01243aa87ac255f8be331dbe@ec2-44-205-112-253.compute-1.amazonaws.com:5432/d9uof29k60cnp1', sslmode='require')
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS sellout
            (name text, youtube text, twitter text, instagram text, tiktok text)''')

class Socials(commands.Cog):
    #initializes the cog for use
    def __init__(self, client):
        self.client = client
        self.YouTubeUpdates.start()
        self.TwitterUpdates.start()
        

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#tasks
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    

#posts new youtube uploads into the YoutubeUpdates channel in the server
    @tasks.loop(minutes=60)
    async def YouTubeUpdates(self):
        DiscordYouTubeChannel = await self.client.fetch_channel(1008813817800708146)
        for i in range(len(YouTubersID)):
            cur.execute("""SELECT name
                        FROM sellout
                        WHERE name=%s""",
                        [peopleToSellout[i],])
            result = cur.fetchone()
            
            if not result:
                cur.execute(f'''INSERT INTO sellout VALUES
                            ('{peopleToSellout[i]}', 'N/A', 'N/A', 'N/A', 'N/A')''')
            
            request = youtube.search().list(
            part='id',
            channelId = YouTubersID[i],
            type='video',
            order='date',
            maxResults=1
            )
            
            response = request.execute()
            
            video_link_array = [f"https://www.youtube.com/watch?v={video['id']['videoId']}" \
                for video in response['items']]
            
            cur.execute("""SELECT youtube
                        FROM sellout
                        WHERE name=%s""",
                        [peopleToSellout[i],])
            lastURL = str(cur.fetchone()[0])
            
            if lastURL != video_link_array[0]:
                cur.execute("""UPDATE sellout
                            SET youtube=%s
                            WHERE name=%s""",
                            [video_link_array[0], peopleToSellout[i],])
                
                await DiscordYouTubeChannel.send(f"""**{peopleToSellout[i]} Upload!**
{peopleToSellout[i]} Has Uploaded A New YouTube Video!
{video_link_array[0]}""")
                
            con.commit()
            
#posts new Twitter posts into the TwitterUpdates channel in the server
    @tasks.loop(minutes=1)
    async def TwitterUpdates(self):
        DiscordTwitterChannel = await self.client.fetch_channel(1008845475035746444)
        for i in range(len(twitterHandles)):
            cur.execute("""SELECT name
                        FROM sellout
                        WHERE name=%s""",
                        [peopleToSellout[i],])
            result = cur.fetchone()
            
            if not result:
                cur.execute(f'''INSERT INTO sellout VALUES
                            ('{peopleToSellout[i]}', 'N/A', 'N/A', 'N/A', 'N/A')''')
                
            tweet_list= api.user_timeline(user_id=twitterHandles[i], count=5)
            tweet= tweet_list[0]
            
            url = f"https://twitter.com/{twitterHandles[i]}/statuses/{tweet.id}"
            
            cur.execute("""SELECT twitter
                        FROM sellout
                        WHERE name=%s""",
                        [peopleToSellout[i],])
            lastURL = str(cur.fetchone()[0])
            
            if lastURL != url:
                cur.execute("""UPDATE sellout
                            SET twitter=%s
                            WHERE name=%s""",
                            [url, peopleToSellout[i],])
                
                await DiscordTwitterChannel.send(f"""**{peopleToSellout[i]} Tweeted!**
{peopleToSellout[i]} Has Made A New Tweet!
{url}""")
            con.commit()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#ERRORS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
#what allows the cog to run
def setup(client):
    client.add_cog(Socials(client))