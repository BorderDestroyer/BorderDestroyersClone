#imports libraries used for the bot
import discord
from discord.ext import commands, tasks
import random
from itertools import cycle
import os
import psycopg2

#database setup

con = psycopg2.connect('postgres://rdmzqeqchqmaxa:32a505f2159c2f43b17585a19b646452eab0a6ea01243aa87ac255f8be331dbe@ec2-44-205-112-253.compute-1.amazonaws.com:5432/d9uof29k60cnp1', sslmode='require')
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS currency
            (name text, amount real)''')


class Currency(commands.Cog):
#initializes the cog for use
    def __init__(self, client):
        self.client = client
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#EVENTS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    

#listens for a new member to join and adds them to the currency database
    @commands.Cog.listener()
    async def on_member_join(self, member):
        member = str(member).replace("'", "")
        
        cur.execute("""SELECT name
                   FROM currency
                   WHERE name=%s""",
                [str(member),])
        result = cur.fetchone()
        
        if not result:
            cur.execute(f'''INSERT INTO currency VALUES
                        ('{member}', '500')''')
            con.commit()
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#COMMANDS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    
#creates the group for the currency commands
    @commands.group(pass_context=True)
    async def currency(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"{ctx.author.mention} What about currency would you like to know? Use `bd help 2` to see available options!")
    
#displays the currency of everyone in the server
    @currency.command(pass_context=True, aliases=["list", "expose"])
    async def show(self, ctx, member : discord.Member = "all"):     
        memberObj = member
        member = str(member).replace("'", "")
        
        if member == "all":
            for row in cur.execute('''SELECT * FROM currency'''):
                await ctx.send(row)
                print(row)
        else:
            cur.execute("""SELECT amount
                       FROM currency
                       WHERE name=%s""",
                    [str(member),])
            result = float(cur.fetchone()[0])
        
            await ctx.send(f"{ctx.author.mention}: {memberObj} has `${result}`")

#adds a member into the currency database
    @currency.command()
    async def add(self, ctx, member : discord.Member):
        memberObj = member
        member = str(member).replace("'", "")
        cur.execute("""SELECT name
                   FROM currency
                   WHERE name=%s""",
                [str(member),])
        result = cur.fetchone()
        
        if result:
            await ctx.send(f"{ctx.author.mention}: {memberObj.mention} is already in the database")
        else:

            cur.execute(f"""INSERT INTO currency VALUES
                        ('{str(member)}', '500')""")

            con.commit()
            
            await ctx.send(f"{memberObj.mention} has been given $500")
            print(f"{memberObj} has been given 500 dollars")

#destroys money held by the user when prompted
    @currency.command()
    async def destroy(self, ctx, amount):
        member = str(ctx.author).replace("'", "")
        memberObj = ctx.author   
        
        cur.execute("""SELECT amount
                   FROM currency
                   WHERE name=%s""",
                [str(member),])
        result = float(cur.fetchone()[0])
        
        if result < float(amount):
            await ctx.send(f"{ctx.author.mention} That would leave you bankrupt...")
        else:
            newBalance = result - float(amount)
            
            cur.execute('''UPDATE currency
                        SET amount=%s
                        WHERE name=%s''',
                        [newBalance, str(member)])
            
            await ctx.send(f"{ctx.author.mention} You destroyed ${amount}! That's a federal offense! You now have `${newBalance}`")
            con.commit()

#sets the amount manually for the specified user
    @currency.command()
    @commands.has_permissions(ban_members=True)
    async def bankgive(self, ctx, amount, member : discord.Member):
        if float(amount) <= 0:
            await ctx.send(f'{ctx.author.mention} Yeah, that would be stealing, please add a positive amount!')
        else:               
            memberObj = member
            member = str(member).replace("'", "")
            
            cur.execute("""SELECT name
                       FROM currency
                       WHERE name=%s""",
                    [str(member),])
            result = cur.fetchone()
        
            if result:
                cur.execute("""SELECT amount
                            FROM currency
                            WHERE name=%s""",
                            [str(member),])
                curAmount = float(cur.fetchone()[0])
            
                newAmount = curAmount + float(amount)
            
                cur.execute('''UPDATE currency
                            SET amount=%s
                            WHERE name=%s''',
                            [newAmount, str(member)])
            
                await ctx.send(f'`${amount}` has been given to {memberObj.mention}!')
                
                con.commit()
            else:
                await ctx.send(f'{ctx.author.mention} that user could not be found')

#checks the currency held by the user
    @commands.command(aliases=["bal"])
    async def balance(self, ctx):
        member = str(ctx.author).replace("'", "")
        memberObj = ctx.author
        
        cur.execute("""SELECT amount
                   FROM currency
                   WHERE name=%s""",
                [str(member),])
        result = cur.fetchone()[0]
        
        await ctx.send(f"{ctx.author.mention} You have `${result}`")

#pays another member from user's amount
    @commands.command()
    async def pay(self, ctx, toPay, member : discord.Member):
        if float(toPay) <= 0:
            await ctx.send(f'{ctx.author.mention} Yeah, that would be stealing, please specify a POSITIVE amount!')
        elif str(member) == str(ctx.author):
            await ctx.send(f"{ctx.author.mention} You gave yourself ${toPay}, you gain nothing, but feel charitable for some reason.")
        else:
            memberObj = member
            member = str(member).replace("'", "")
            
            user = str(ctx.author).replace("'", "")
            
            cur.execute("""SELECT amount
                       FROM currency
                       WHERE name=%s""",
                    [str(user),])
            curAmountSender = float(cur.fetchone()[0])
        
            if curAmountSender < float(toPay):
                await ctx.send(f"{ctx.author.mention} You don't have enough money")
            else:
                cur.execute("""SELECT amount
                           FROM currency
                           WHERE name=%s""",
                        [str(member),])
                curAmountReceiver = cur.fetchone()[0]

                newAmountSender = curAmountSender - float(toPay)
                newAmountReceiver = curAmountReceiver + float(toPay)
        
                cur.execute('''UPDATE currency 
                            SET amount=%s 
                            WHERE name=%s''', 
                            [newAmountSender, str(user)])
        
                cur.execute('''UPDATE currency
                            SET amount=%s
                            WHERE name=%s''',
                            [newAmountReceiver, str(member)])
        
                con.commit()
                await ctx.send(f"{ctx.author.mention} payed {memberObj.mention} ${toPay}!")
        
    @currency.command()
    async def add_all(self, ctx):
        for guild in self.client.guilds:
            for member in guild.members:      
                memberObj = member
                member = str(member).replace("'", "")      
                cur.execute("""SELECT name
                        FROM currency
                        WHERE name=%s""",
                        [str(member),])
                result = cur.fetchone()
                
                if not result:
                    cur.execute(f'''INSERT INTO currency VALUES
                                ('{member}', '500')''')

                    con.commit()
                        
                    await ctx.send(f"{memberObj.mention} has been given $500")
                    print(f"{memberObj} has been given 500 dollars")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#ERRORS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#handles errors for the currency command
    @currency.error
    async def currency_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(f"{ctx.author.mention} I know you want somethign to do with currency, I just don't know what... Use `bd currency help` For a list of commands!")

#handles errors for the show command in the currency group
    @show.error
    async def show_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(f"{ctx.author.mention} I cannot find that person, so either you spelt it wrong, or they're committing tax fraud like a responsible human being!")

#handles errors for the bankgive command
    @bankgive.error
    async def bankgive_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"{ctx.author.mention} You need to specify who to give the money to and how much! Use `bd currency bankgive <amount> <who to give money to>`")
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"{ctx.author.mention} Uh, something went wrong here, but I cannot figure out what... `bd currency bankgive <amount> <who to give money to>`")

  
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
#what allows the cog to run
def setup(client):
    client.add_cog(Currency(client))