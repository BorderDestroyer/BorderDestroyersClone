#imports libraries used for the bot
import discord
from discord.ext import commands, tasks
import random
from itertools import cycle
import os
import sqlite3
from discord import Color
from discord.utils import get
import asyncio
import psycopg2

two_cards = ["<:TwoOfSpades:1010650727116460115>", "<:TwoOfClubs:1010650462011281418>", "<:TwoOfHearts:1010650725648433172>", "<:TwoOfDiamonds:1010650463659638875>"]
three_cards = ["<:ThreeOfSpades:1010650578394816632>", "<:ThreeOfClubs:1010650573403602974>", "<:ThreeOfHearts:1010650576297664604>", "<:ThreeOfDiamonds:1010650575022588035>"]
four_cards = ["<:FourOfSpades:1010650495188205579>", "<:FourOfClubs:1010650490201186396>", "<:FourOfHearts:1010650493502107720>", "<:FourOfDiamonds:1010650491849556018>"]
five_cards = ["<:FiveOfSpades:1010650488515067985>", "<:FiveOfClubs:1010650482139746435>", "<:FiveOfHearts:1010650486480846948>", "<:FiveOfDiamonds:1010650484085887149>"]
six_cards = ["<:SixOfSpades:1010650564352299128>", "<:SixOfClubs:1010650550880194651>", "<:SixOfHearts:1010650561646952520>", "<:SixOfDiamonds:1010650558576734238>"]
seven_cards = ["<:SevenOfSpades:1010650547050774639>", "<:SevenOfClubs:1010650540360876185>", "<:SevenOfHearts:1010650543737274468>", "<:SevenOfDiamonds:1010650542139261028>"]
eight_cards = ["<:EightOfSpades:1010650480801751061>", "<:EightOfClubs:1010650472790622278>", "<:EightOfHearts:1010650479094681631>", "<:EightOfDiamonds:1010650474506096790>"]
nine_cards = ["<:NineOfSpades:1010650527333371966>", "<:NineOfClubs:1010650521490685963>", "<:NineOfHearts:1010650525940858930>", "<:NineOfDiamonds:1010650523797569727>"]
ten_face_cards = ["<:TenOfSpades:1010650571704913970>", "<:TenOfClubs:1010650566155845704>", "<:TenOfDiamonds:1010650568093618226>", "<:TenOfHearts:1010650570006204566>", "<:KingOfSpades:1010650518986698852>", "<:KingOfClubs:1010650511223033906>", "<:KingOfHearts:1010650516017131520>", "<:KingofDiamonds:1010650514003861544>", "<:QueenOfSpades:1010650538397941860>", "<:QueenOfClubs:1010650530344865883>", "<:QueenOfHearts:1010650534845362176>", "<:QueenOfDiamonds:1010650532966305892>", "<:JackOfSpades:1010650505887883394>", "<:JackOfClubs:1010650497771905146>", "<:JackOfHearts:1010650502234656848>", "<:JackOfDiamonds:1010650500020047974>"]
ace_cards = ["<:AceOfSpades:1010650470810923088>", "<:AceOfClubs:1010650465534484590>", "<:AceOfDiamonds:1010650467082178652>", "<:AceOfHearts:1010650469032538143>"]
        
cards = [two_cards, three_cards, four_cards, five_cards, six_cards, seven_cards, eight_cards, nine_cards, ten_face_cards, ace_cards]

con = psycopg2.connect('postgres://rdmzqeqchqmaxa:32a505f2159c2f43b17585a19b646452eab0a6ea01243aa87ac255f8be331dbe@ec2-44-205-112-253.compute-1.amazonaws.com:5432/d9uof29k60cnp1', sslmode='require')
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS curBlackjackGames
            (player text, playerCards text, playerEmojis text, dealerCards text, dealerEmojis text, bet real, message text)''')

class Games(commands.Cog):
    #initializes the cog for use
    def __init__(self, client):
        self.client = client
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#FUNCTIONS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#allows you to easily alter the amount of money held by a user
    def currency_change(amount, ctx):
        cur.execute("""SELECT amount
                   FROM currency
                   WHERE name=%s""",
                [str(ctx.author),])
        result = float(cur.fetchone()[0])
        
        newCurrency = result + amount
        
        if newCurrency < 0:
            newCurrency = 0
            
        cur.execute('''UPDATE currency
                        SET amount=%s
                        WHERE name=%s''',
                        [newBalance, str(ctx.author)])
            
        con.commit()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#EVENTS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#checks the message of react and who reacted, and then play the bj game
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        pID = str(payload.message_id)
        pEmoji = payload.emoji
        pReactor = str(payload.member).replace("'", "")
        pMember = payload.member
        
        if str(pMember) != "BorderDestroyer Clone#3440":                           
            cur.execute("""SELECT player
                        FROM curBlackjackGames
                        WHERE player=%s""",
                        [pReactor,])
            result = cur.fetchone()[0]
                    
            if result:
                cur.execute("""SELECT message
                            FROM curBlackjackGames
                            WHERE player=%s""",
                            [pReactor,])
                ID = str(cur.fetchone()[0])
                
                if ID == pID:
                    embed = discord.Embed(title = f"{pMember}'s Blackjack Game", color = Color.purple())
                    pChannel = payload.channel_id
                    Channel = self.client.get_channel(pChannel)
                    msg = await Channel.fetch_message(pID)
                    
                    
                    if str(pEmoji) == "🎯":
                        await msg.remove_reaction("🎯", payload.member)
                        dealerEmojiList = ""
                        playerEmojiList = ""
                        playerNumberSeq = ""
                        
                        cardVal = random.randint(0, 9)
                        newCard = random.choice(cards[cardVal])
                        cardVal += 2
                        
                        cur.execute("""SELECT playerCards
                                    FROM curBlackjackGames
                                    WHERE player=%s""",
                                    [pReactor,])
                        playerCards = cur.fetchone()[0]
                        
                        cur.execute("""SELECT playerEmojis
                                    FROM curBlackjackGames
                                    WHERE player=%s""",
                                    [pReactor,])
                        playerEmojis = cur.fetchone()[0]
                        
                        cur.execute("""SELECT dealerCards
                                    FROM curBlackjackGames
                                    WHERE player=%s""",
                                    [pReactor,])
                        dealerCards = cur.fetchone()[0]
                        
                        cur.execute("""SELECT dealerEmojis
                                    FROM curBlackjackGames
                                    WHERE player=%s""",
                                    [pReactor,])
                        dealerEmojis = cur.fetchone()[0]
                        
                        playerCardList = str(playerCards).split(", ")
                        dealerCardList = str(dealerCards).split(", ")
                        playerEmojiList = playerEmojis.split(", ")
                        dealerEmojiList = dealerEmojis.split(", ")
                        playerCards += f", {cardVal}"
                        
                        playerEmojiList.append(newCard)
                        curPlayerScore = cardVal
                        
                        if curPlayerScore > 21:
                            while "11" in playerCardList:
                                placement = playerCardList.index("11")
                                playerCardList[placement] = "1"
                            for i in range(len(playerCardList)):
                                playerCards += playerCardList[i]

                        
                        for i in range(len(playerCardList)):
                            if i == 0:
                                playerNumberSeq += str(playerCardList[i])
                                curPlayerScore += int(playerCardList[i])
                            else:
                                playerNumberSeq += " + "
                                playerNumberSeq += str(playerCardList[i])
                                curPlayerScore += int(playerCardList[i])
                        
                        playerNumberSeq += f" + {cardVal}"
                        
                        newEmojiList = ""
                        for i in range(len(playerEmojiList)):
                            newEmojiList += playerEmojiList[i]
                            newEmojiList += " "
                            
                        embed = discord.Embed(title = f"{pMember}'s Blackjack Game", color = Color.purple())
                        embed.add_field(name="Dealer's Cards", value=f"""
                                        {dealerEmojis}      ?
                                        {dealerCardList[0]} + ? = {dealerCardList[0]} + ?""", inline=False)
                        embed.add_field(name=f"{pMember}'s Cards", value=f"""
                                        {newEmojiList}
                                        {playerNumberSeq} = {curPlayerScore}""", inline=False)
                        embed.set_footer(text="'🎯' = HIT, '👋' = PASS", icon_url=embed.Empty)
                        
                        await msg.edit(embed=embed)
                                        
                        cur.execute("""UPDATE curBlackjackGames
                                    SET playerCards=%s, playerEmojis=%s, dealerCards=%s, dealerEmojis=%s
                                    WHERE player=%s""",
                                    [playerCards, newEmojiList, dealerCards, dealerEmojis, pReactor])
                        
                    elif str(pEmoji) == "👋":
                        await msg.remove_reaction("👋", payload.member)
                        won = False
                        tie = False
                        dealerEmojiList = ""
                        dealerNumberSeq = ""
                        playerNumberSeq = ""
                        
                        cur.execute("""SELECT playerCards
                                    FROM curBlackjackGames
                                    WHERE player=%s""",
                                    [pReactor,])
                        playerCards = cur.fetchone()[0]
                        
                        cur.execute("""SELECT playerEmojis
                                    FROM curBlackjackGames
                                    WHERE player=%s""",
                                    [pReactor,])
                        playerEmojis = cur.fetchone()[0]
                        
                        cur.execute("""SELECT dealerCards
                                    FROM curBlackjackGames
                                    WHERE player=%s""",
                                    [pReactor,])
                        dealerCards = cur.fetchone()[0]
                        
                        cur.execute("""SELECT dealerEmojis
                                    FROM curBlackjackGames
                                    WHERE player=%s""",
                                    [pReactor,])
                        dealerEmojis = cur.fetchone()[0]
                        
                        curDealerScore = int(dealerCards)
                        dealerCardList = str(dealerCards).split(", ")
                        playerCardList = str(playerCards).split(", ")
                        
                        curPlayerScore = 0
                        for i in range(len(playerCardList)):
                            if i == 0:
                                playerNumberSeq += str(int(float(playerCardList[i])))
                                curPlayerScore += int(float(playerCardList[i]))
                            else:
                                playerNumberSeq += " + "
                                playerNumberSeq += str(playerCardList[i])
                                curPlayerScore += int(playerCardList[i])
                        
                        playerEmojiList = playerEmojis.split(", ")
                        newPlayerEmojiList = ""
                        for i in range(len(playerEmojiList)):
                            newPlayerEmojiList += playerEmojiList[i]
                            newPlayerEmojiList += " "
                
                        while curDealerScore <= 16:
                            dealerEmojiList = ""
                            dealerNumberSeq = ""
                        
                            cardVal = random.randint(0, 9)
                            newCard = random.choice(cards[cardVal])
                            cardVal += 2
                            
                            dealerCardList = str(dealerCards).split(", ")                    
                            dealerEmojiList = dealerEmojis.split(", ")

                            dealerCards = str(dealerCards)
                            dealerCards += f", {cardVal}"  
                            dealerEmojis += f", {newCard}"          
                            dealerEmojiList.append(newCard)
                            curDealerScore = cardVal
                            
                            for i in range(len(dealerCardList)):
                                if i != 0:
                                    dealerNumberSeq += " + "

                                dealerNumberSeq += str(int(dealerCardList[i]))
                                curDealerScore += int(float(dealerCardList[i]))
                            
                            dealerNumberSeq += f" + {cardVal}"         
                            
                            newEmojiList = ""
                            for i in range(len(dealerEmojiList)):
                                newEmojiList += dealerEmojiList[i]
                                newEmojiList += " "
                            
                            embed = discord.Embed(title = f"{pMember}'s Blackjack Game", color = Color.purple())
                            embed.add_field(name="Dealer's Cards", value=f"""
                                            {newEmojiList}
                                            {dealerNumberSeq} = {curDealerScore}""", inline=False)
                            embed.add_field(name=f"{pMember}'s Cards", value=f"""
                                            {newPlayerEmojiList}
                                            {playerNumberSeq} = {curPlayerScore}""", inline=False)
                            embed.set_footer(text="'🎯' = HIT, '👋' = PASS", icon_url=embed.Empty)
                            
                            await msg.edit(embed=embed)
                            
                            cur.execute("""UPDATE curBlackjackGames
                                    SET dealerCards=%s, dealerEmojis=%s
                                    WHERE player=%s""",
                                    [dealerCards, newEmojiList, pReactor])
                        
                        dealerDistance = curDealerScore - 21
                        playerDistance = curPlayerScore - 21
                        
                        if playerDistance == dealerDistance:
                            embed.set_footer(text=f"**We both got {curPlayerScore}, so we tie!**", icon_url=embed.Empty)
                            tie = True
                        elif playerDistance == 0 and dealerDistance != 0:
                            embed.set_footer(text=f"**You Win!**", icon_url=embed.Empty)
                            won = True
                        elif playerDistance != 0 and dealerDistance == 0:
                            embed.set_footer(text=f"**I Win!**", icon_url=embed.Empty)
                            won = False
                        elif playerDistance < 0 and dealerDistance > 0:
                            embed.set_footer(text=f"*You Win!*", icon_url=embed.Empty)
                            won = True
                        elif playerDistance > 0 and dealerDistance < 0:
                            embed.set_footer(text=f"**I Win!**", icon_url=embed.Empty)
                            won = False
                        elif playerDistance < 0 and dealerDistance < 0:
                            if playerDistance < dealerDistance:
                                embed.set_footer(text=f"**I Win!**", icon_url=embed.Empty)
                                won = False
                            elif playerDistance > dealerDistance:
                                embed.set_footer(text=f"*You Win!*", icon_url=embed.Empty)
                                won = True
                        elif playerDistance > 0 and dealerDistance > 0:
                            if playerDistance > dealerDistance:
                                embed.set_footer(text=f"**I Win!**", icon_url=embed.Empty)
                                won = False
                            elif playerDistance < dealerDistance:
                                embed.set_footer(text=f"**You Win**", icon_url=embed.Empty)
                                won = True
                                
                        await msg.edit(embed=embed)      
                        
                        cur.execute("""SELECT bet
                                    FROM curBlackjackGames
                                    WHERE player=%s""",
                                    [pReactor,])
                        bet = float(cur.fetchone()[0])
                        
                        if bet > 0:
                            if won and not tie:
                                cur.execute("""SELECT amount
                                            FROM currency
                                            WHERE name=%s""",
                                            [str(pReactor),])
                                amount = float(cur.fetchone()[0])
                                    
                                newCurrency = amount + bet
                                    
                                if newCurrency < 0:
                                    newCurrency = 0
                                        
                                cur.execute('''UPDATE currency
                                                SET amount=%s
                                                WHERE name=%s''',
                                                [newCurrency, str(pReactor)])
                                
                                await Channel.send(f"{payload.member.mention} You won ${bet}")
                            elif not tie and not won:
                                cur.execute("""SELECT amount
                                            FROM currency
                                            WHERE name=%s""",
                                            [str(pReactor),])
                                amount = float(cur.fetchone()[0])
                                    
                                newCurrency = amount - bet
                                    
                                if newCurrency < 0:
                                    newCurrency = 0
                                        
                                cur.execute('''UPDATE currency
                                                SET amount=%s
                                                WHERE name=%s''',
                                                [newCurrency, str(pReactor)])
                                
                                await Channel.send(f"{pMember.mention} You lost ${bet}")
                        
                        cur.execute("""DELETE FROM curBlackjackGames
                                WHERE player=%s""",
                                [str(pReactor),])
                                    
                    else:
                        await msg.remove_reaction(str(payload.emoji), payload.member)
                
            con.commit()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#COMMANDS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    
#a rock paper scissors command
    @commands.command(aliases=["rps"])
    async def rockpaperscissors(self, ctx, input, bet = 0):     
        userObj = ctx.author
        user = str(userObj).replace("'", "")
           
        cur.execute("""SELECT amount
                    FROM currency
                    WHERE name=%s""",
                    [str(user),])
        result = float(cur.fetchone()[0])
        
        if not result:
            cur.execute(f'''INSERT INTO currency VALUES
                        ('{user}', '500')''')

            con.commit()
            
            cur.execute("""SELECT amount
                    FROM currency
                    WHERE name=%s""",
                    [str(user),])
            result = float(cur.fetchone()[0])
            
        if result < bet:
            check = False
        else:
            check = True
        
        if check:
            if input == "rock" or input == "paper" or input == "scissors":
                choices = ["rock", "paper", "scissors"]
                picked = random.choice(choices)
            
                await ctx.send(f"{ctx.author.mention} Alright, I pick {picked}.")
            
                bot_lost_response = f"{ctx.author.mention} Oh you won, that's dumb, I demand a rematch!"
                bot_won_response = f"{ctx.author.mention} Oh I won, Guess I'm just that lucky!"
            
                if picked == input:
                    await ctx.send("Oh we tied, how boring.")
                elif picked == "rock" and input == "paper" or picked == "scissors" and input == "rock" or picked == "paper" and input == "scissors":
                    await ctx.send(bot_lost_response)
                    if bet > 0:
                        currency_change(bet, ctx)
                        await ctx.send(f"{ctx.author.mention} You gain ${bet}")
                elif picked == "rock" and input == "scissors" or picked == "scissors" and input == "paper" or picked == "paper" and input == "rock":
                    await ctx.send(bot_won_response)
                    if bet > 0:
                        currency_change(-bet, ctx)
                        await ctx.send(f"{ctx.author.mention} You lost ${bet}")
            else:
                await ctx.send(f"{ctx.author.mention} Uh, bud, {input} is not a part of ROCK PAPER SCISSORS.")

#a coin flip command
    @commands.command(aliases=["cf"])
    async def coinflip(self, ctx, input = "dwazdzcsjiocoincianionw", bet = 0):
        cur.execute("""SELECT amount
                    FROM currency
                    WHERE name=%s""",
                    [str(ctx.author),])
        result = float(cur.fetchone()[0])
        
        if not result:
            cur.execute(f'''INSERT INTO currency VALUES
                        ('{member}', '500')''')

            con.commit()
            
            cur.execute("""SELECT amount
                    FROM currency
                    WHERE name=%s""",
                    [str(ctx.author),])
            result = float(cur.fetchone()[0])
            
        if result < bet:
            check = False
        else:
            check = True
            
        if check:
            choices = ["tails", "heads"]
            picked = random.choice(choices)
            
            await ctx.send(f"{ctx.author.mention} The coin landed on {picked}!")
            
            if input != "dwazdzcsjiocoincianionw" and bet > 0:
                if lower(input) == picked:
                    currency_change(bet, ctx)
                    await ctx.send(f"{ctx.author.mention} You won the coinflip! You gained ${bet}!")
                elif lower(input) != picked:
                    currency_change(-bet, ctx)
                    await ctx.send(f"{ctx.author.mention} You did not win the coinflip. You lost ${bet}")
        
#just a snarky 8ball command
    @commands.command(aliases=["8ball", "ask"])
    async def _8ball(self, ctx, *, question):
        responses = ["No",
                     "Yes",
                     "I'll tell you if you bake me cookies!",
                     "Why do you want to know?",
                     "What's in it for me?",
                     "I don't feel like giving an answer right now...",
                     "All signs point to possibly.",
                     "How the **** should I know?",
                     "Only time will tell...",
                     "I don't know, but regardless you'll always be my sunshine!",
                     "Only if you eat 100 jellybeans.",
                     "*Takes out earbuds* Oh, I know these! Mask by Dream! *Puts earbuds back in*",
                     "Go touch some grass.",
                     "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                     "Blame the French",
                     "Maybe... Of course silly!",
                     "'One moment, Karen's at it again' *sigh* What was that?",
                     "33.747252, -112.633853, 4:00 AM at the South West corner",
                     "https://www.youtube.com/watch?v=M5V_IXMewl4",
                     "Don't remove the 'h' from 'watch' in the YouTube url for a video...",
                     "Do remove the 'a' from 'watch' in the YouTube url for a video!",
                     "You will find your answers here - https://www.youtube.com/channel/UCKeSimtpEbtM1ZsA-Dqs6zg",
                     """Like an angel with cruel and merciless intent
Go forth, young boy
And you'll become a legend
In time, this blue of the sky
Will reach out to knock on the door to your heart
You're looking at me
Make it all that you see
Content and we're merely smiling
Once more, the touch you long for
Consumes you in yearning to find that embrace
You're unaware, though-

Oh hi what was that?""",
                    """教えて 教えてよ
その仕組みを
僕の中に誰がいるの？
壊れた 壊れたよ
この世界で
君が笑う
何も見えずに

Oh hi what was that?""",
                    "https://twitter.com/border_game You shall find your answers here!",
                    "balls",
                    "Not really.",
                    "No. Just no.",
                    "Dude, you have google for a reason."]
    
        await ctx.send(f"{ctx.author.mention} {random.choice(responses)}")
        
#A Blackjack command
    @commands.command(aliases=["bj"])
    async def blackjack(self, ctx, bet=0):
        user = str(ctx.author).replace("'", "")
        cur.execute("""SELECT amount
                    FROM currency
                    WHERE name=%s""",
                    [str(user),])
        result = float(cur.fetchone()[0])
        
        if not result:
            cur.execute(f'''INSERT INTO currency VALUES
                        ('{user}', '500')''')

            con.commit()
            
            cur.execute("""SELECT amount
                    FROM currency
                    WHERE name=%s""",
                    [str(user),])
            result = float(cur.fetchone()[0])
            
        if result < bet:
            check = False
        else:
            check = True
            
        if check: 
            cur.execute("""SELECT player
                        FROM curBlackjackGames
                        WHERE player=%s""",
                        [str(user),])
            result = cur.fetchone()
            
            if result:
                cur.execute("""DELETE FROM curBlackjackGames
                            WHERE player=%s""",
                            [str(user),])
            
            con.commit()
            
            dealerOne = random.randint(0, 9)
            playerOne = random.randint(0, 9)
            playerTwo = random.randint(0, 9)
            
            dealerScoreOne = dealerOne + 2
            playerScoreOne = playerOne + 2
            playerScoreTwo = playerTwo + 2
            
            curDealerScore = dealerScoreOne
            curPlayerScore = playerScoreOne + playerScoreTwo
            
            dealerEmojiOne = random.choice(cards[dealerOne])
            playerEmojiOne = random.choice(cards[playerOne])
            playerEmojiTwo = random.choice(cards[playerTwo])
            
            dealerEmojis = f"{dealerEmojiOne}"
            playerEmojis = f"{playerEmojiOne}, {playerEmojiTwo}"
            dealerCounts = f"{dealerScoreOne}"
            playerCounts = f"{playerScoreOne}, {playerScoreTwo}"
            
            if curPlayerScore > 21:
                if playerOne == 9 and playerScoreOne == 11:
                    playerScoreOne = 1
                elif playerTwo == 9 and playerScoreTwo == 11:
                    playerScoreTwo = 1
            
            embed = discord.Embed(title = f"{ctx.author.name}'s Blackjack Game", color = Color.purple())
            embed.add_field(name="Dealer's Cards", value=f"""
                            {dealerEmojiOne}      ?
                            {dealerScoreOne} + ? = {curDealerScore} + ?""", inline=False)
            embed.add_field(name=f"{ctx.author.name}'s Cards", value=f"""
                            {playerEmojiOne}      {playerEmojiTwo}
                            {playerScoreOne} + {playerScoreTwo} = {curPlayerScore}""", inline=False)
            embed.set_footer(text="'🎯' = HIT, '👋' = PASS", icon_url=embed.Empty)
            msg = await ctx.send(embed=embed)
            
            msgID = str(msg.id)
                    
            cur.execute(f'''INSERT INTO curBlackjackGames VALUES
                            ('{user}', '{playerCounts}', '{playerEmojis}', '{dealerCounts}', '{dealerEmojis}', {bet}, '{msgID}') ''')
            
            con.commit()
            
            await msg.add_reaction("🎯")
            await msg.add_reaction("👋")
        else:
            await ctx.send(f"{ctx.author.mention} You do not have enough to gamble that much!")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#ERRORS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#handles errors for the rock paper scissors command
    @rockpaperscissors.error
    async def rps_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(f"{ctx.author.mention} What the heck is that supposed to be? You gotta pick 'rock', 'paper', or 'scissors' man...")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"{ctx.author.mention} So you are aproaching me? Fine! Let us D- D- D- Fight! `use 'bd rps <Your Choice> <bet>'`")

#handles errors for the 8ball command
    @_8ball.error
    async def _8ball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("How- I need a prompt to give advice on... `bd ask <prompt>`")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
#what allows the cog to run
def setup(client):
    client.add_cog(Games(client))