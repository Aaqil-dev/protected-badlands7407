import discord
from discord.ext import commands
import youtube_dl
import os
import json
import random
import asyncio
import asyncpraw
from discord.ext.commands import cooldown, BucketType

reddit = asyncpraw.Reddit(client_id = "nskrlCP_0ebwfg",
                          client_secret = "	rR5efdbsU1Y8TeR-S4Vm1BKl6boxNg",
                          user_agent = "Epic Memes For You")

os.chdir("C:\\Users\\Ali Aaqil Inaz\\Desktop\\The Anonymous Bot")

client = commands.Bot(command_prefix = "/")
token = os.getenv("NzY5NDYwMTc4NjI5ODIwNDM2.X5PVog.AYYu9LDKfBhpRcHG9exaxthoZ-U")
client.remove_command("help")

@client.event
async def on_ready():
  await client.change_presence(status = discord.Status.idle, activity = discord.Game("/help"))
  print("Bot is ready")


@client.group(invoke_without_command = True)
async def help(ctx):
  em = discord.Embed(title = "Help Command List", description = "All Commands Fall Into The Folowing Categories. \nUse / As The Prefix!",color = discord.Color.red())

  em.add_field(name = ":man_police_officer:Moderation", value = "/help_moderation \n• Use Moderation Commands To Manage Your Server!")
  em.add_field(name = ":joy:Fun", value = "/help_fun \n• Spend Time And Have Fun!")
  em.add_field(name = ":coin:Fun", value = "/help_currency \n• A Bunch Of Fun Currency Commands!")

  await ctx.send(embed = em)

@client.group(invoke_without_command = True)
async def help_moderation(ctx):
  em = discord.Embed(title = "Moderation Commands", description = "Use These Commands To Manage Your Server", color = discord.Color.red())

  em.add_field(name = ":man_police_officer:Moderation", value = "`kick`,`ban`,`unban`,`mute`,`unmute`,`purge`")

  await ctx.send(embed = em)

@client.group(invoke_without_command = True)
async def help_fun(ctx):
  em = discord.Embed(title = "Fun Commands", description = "Use These Commands To Have Fun!", color = discord.Color.red())

  em.add_field(name = ":joy:Fun", value = "`meme`,`8ball`,`userinfo`,`hello`,`lenny`,`invite`,`snipe`,`suggest`,`say`,`dm`,`ping`")

  await ctx.send(embed = em)

@client.group(invoke_without_command = True)
async def help_currency (ctx):
  em = discord.Embed(title = "Currency Commands", description = "Fun Currency Commands!", color = discord.Color.red())

  em.add_field(name = ":coin:Currency", value = "`beg`,`rob`,`leaderboard`,`shop`,`withdraw`,`deposit`,`balance`,`inventory`,`sell`,`buy`")

  await ctx.send(embed = em)

@client.command()
async def hello (ctx):
  await ctx.send("Hi! I'm The Anonymous Bot! To Get Started, Type The Command /help")

@client.command()
async def kill(ctx, user: discord.Member):
  await ctx.send(f"{ctx.author.mention} killed {user.mention}!")

@client.command()
async def lenny(ctx):
  await ctx.send("( ͡° ͜ʖ ͡°)")

@client.command()
async def meme (ctx, subred = "memes"):
  subreddit = reddit.subreddit("memes")
  all_subs = []

  top = subreddit.top(Limit = 500)

  for submission in top:
    all_subs.append(submission)

  random_sub = random.choice(all_subs)

  name = random_sub.title
  url = random_sub.url

  em = discord.Embed(title = name)

  em.set_image(url = url)

  await ctx.send(embed = em)

@client.command()
async def invite(ctx):
  em = discord.Embed(title=f'{ctx.author.name} thanks for supporting The Anonymous Bot', description = "You can support The Anonymous Bot by doing these things", color = discord.Color.red())
  em.add_field(name = "Invite me to your server", value = '[Click here](https://discord.com/api/oauth2/authorize?client_id=769460178629820436&permissions=8&scope=bot)')
  
  await ctx.send(embed=em)

snipe_message_content = None
snipe_message_author = None
snipe_message_id = None

@client.event
async def on_message_delete(message):

    global snipe_message_content
    global snipe_message_author
    global snipe_message_id

    snipe_message_content = message.content
    snipe_message_author = message.author
    snipe_message_id = message.id
    await asyncio.sleep(60)

    if message.id == snipe_message_id:
        snipe_message_author = None
        snipe_message_content = None
        snipe_message_id = None
      
@client.command()
async def snipe(message):
    if snipe_message_content==None:
        await message.channel.send("Theres nothing to snipe!")
    else:
        embed = discord.Embed(description=f"{snipe_message_content}")
        embed.set_footer(text=f"Asked by {message.author.name}#{message.author.discriminator}", icon_url=message.author.avatar_url)
        embed.set_author(name= f"{snipe_message_author}")
        await message.channel.send(embed=embed)
        return

@client.command()
async def ping(ctx) :
    await ctx.send(f"🏓 Pong with {str(round({ctx.author}.latency, 2))}")

@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
  responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."]

  await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@client.command()
@commands.cooldown(1, 15, commands.BucketType.user)
@commands.has_permissions(manage_messages=True)
async def say(ctx, *, arg):
  await ctx.message.delete()
  await ctx.send(arg)

@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def dm(ctx , member:discord.Member , * ,message1):
  if not member:
    await ctx.send("mention a member!")
    return 
  else:
   await ctx.message.delete()  
   await member.send(f"{message1}")
   await ctx.send("Message Has Been Send To The User", delete_after=5)

@client.command(aliases=["whois"])
async def userinfo(ctx, member: discord.Member = None):
    if not member:  # if member is no mentioned
        member = ctx.message.author  # set member as the author
    roles = [role for role in member.roles]
    embed = discord.Embed(colour=discord.Colour.purple(), timestamp=ctx.message.created_at,
                          title=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}")

    embed.add_field(name="ID:", value=member.id) 
    embed.add_field(name="Display Name:", value=member.display_name) 

    embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

    embed.add_field(name="Roles:", value="".join([role.mention for role in roles]))
    embed.add_field(name="Highest Role:", value=member.top_role.mention)
    print(member.top_role.mention)
    await ctx.send(embed=embed)

@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def suggest(ctx, *, value):
    channel = discord.utils.get(ctx.guild.channels, name='〖📜〗chat')
    await ctx.message.delete()
    await ctx.author.send(
        "Your Suggestion Has Been Sent, If Your Suggestion Is Incorrect, Your Suggestion Will Be Deleted")
    em = discord.Embed(title=f"{ctx.message.author}'s Suggestion")
    em.set_thumbnail(url=ctx.author.avatar_url)
    em.add_field(name="Suggestion:", value=f'{value}')
    em.set_footer(text=f"ID: {ctx.author.id}")
    poll_msg = await channel.send(embed=em)
    await poll_msg.add_reaction('👍')
    await poll_msg.add_reaction('👎')

@client.command(aliases=['bal'])
async def balance(ctx):
  await open_account(ctx.author)
  user = ctx.author
  users = await get_bank_data()

  wallet_amt = users[str(user.id)]["wallet"]
  bank_amt = users[str(user.id)]["bank"]

  em = discord.Embed(title = f"{ctx.author.name}'s balance",color = discord.Color.red())
  em.add_field(name = "Wallet balance",value = wallet_amt)
  em.add_field(name = "Bank balance",value = bank_amt)
  await ctx.send(embed = em)

@commands.cooldown(1,3,BucketType.user)
@client.command()
async def beg(ctx):
  await open_account(ctx.author)

  users = await get_bank_data()

  user = ctx.author

  earnings = random.randrange(500)

  users[str(user.id)]["wallet"] += earnings

  with open("mainbank.json", "w") as f:
        json.dump(users,f)

  await ctx.send(f"A Kind Hearted Person Gave You {earnings} Coins!")


async def open_account(user):

  users = await get_bank_data()
  

  if str(user.id) in users:
    return False
  else:
    users[str(user.id)] = {}
    users[str(user.id)]["wallet"] = 0
    users[str(user.id)]["bank"] = 0 


  with open("mainbank.json","w") as f:
    json.dump(users,f)
  return True



async def get_bank_data():
  with open("mainbank.json","r") as f:
    users = json.load(f)

  return users


async def update_bank(user,change = 0,mode = "wallet"):
  users = await get_bank_data()

  users[str(user.id)][mode] += change

  with open("mainbank.json","w") as f:
    json.dump(users,f)

  bal = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"]]
  return bal

@client.command(aliases=['with'])
async def withdraw(ctx,amount = None):
  await open_account(ctx.author)

  if amount == None:
    await ctx.send("Please enter the amount")
    return
  
  bal = await update_bank(ctx.author)

  amount = int(amount)
  if amount>bal[1]:
    await ctx.send("You do not have that much money!")
    return
  if amount<0:
    await ctx.send("Amount must be positive!")
    return

  await update_bank(ctx.author,amount)
  await update_bank(ctx.author,-1*amount,"bank")

  await ctx.send(f"You withdrew {amount} coins!")

@client.command()
async def send(ctx,member:discord.Member,amount = None):
  await open_account(ctx.author)
  await open_account(member)

  if amount == None:
    await ctx.send("Please enter the amount")
    return
  
  bal = await update_bank(ctx.author)

  amount = int(amount)
  if amount>bal[0]:
    await ctx.send("You do not have that much money!")
    return
  if amount<0:
    await ctx.send("Amount must be positive!")
    return

  await update_bank(ctx.author,-1*amount,"bank")
  await update_bank(member,amount,"bank")

  await ctx.send(f"You gave {amount} coins!")

@client.command(aliases=['dep'])
async def deposit(ctx,amount = None):
  await open_account(ctx.author)

  if amount == None:
    await ctx.send("Please enter the amount")
    return
  
  bal = await update_bank(ctx.author)

  amount = int(amount)
  if amount>bal[0]:
    await ctx.send("You do not have that much money!")
    return
  if amount<0:
    await ctx.send("Amount must be positive!")
    return

  await update_bank(ctx.author,-1*amount)
  await update_bank(ctx.author,amount,"bank")

  await ctx.send(f"You deposited {amount} coins!")


@client.command()
async def slots(ctx,amount = None):
  await open_account(ctx.author)

  if amount == None:
    await ctx.send("Please enter the amount")
    return
  
  bal = await update_bank(ctx.author)

  amount = int(amount)
  if amount>bal[0]:
    await ctx.send("You do not have that much money!")
    return
  if amount<0:
    await ctx.send("Amount must be positive!")
    return


  final = []
  for i in range(3):
    a = random.choice(["X","O","Q"])

    final.append(a)

    await ctx.send(str(final))

  if final[0] == final[1] or final[0] == final[2] or final[2] == final[1]:

    await update_bank(ctx.author,2*amount)
    await ctx.send("You won!")
  else:
    await update_bank(ctx.author,-1*amount)
    await ctx.send("You lost!")

@client.command()
async def rob(ctx,member:discord.Member):
  await open_account(ctx.author)
  await open_account(member)

  
  bal = await update_bank(member)

  if bal[0]<100:
    await ctx.send("It's not worth it!")
    return

  earnings = random.randrange(0, bal[0])

  await update_bank(ctx.author,earnings)
  await update_bank(member,-1*earnings)

  await ctx.send(f"You robbed and got {earnings} coins!")

mainshop = [{"name":"Watch","price":100,"description":"Time"},
            {"name":"Laptop","price":1000,"description":"Work"},
            {"name":"PC","price":10000,"description":"Gaming"}]


@client.command()
async def shop(ctx):
    em = discord.Embed(title = "Shop")

    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        em.add_field(name = name, value = f"${price} | {desc}")

    await ctx.send(embed = em)



@client.command()
async def buy(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await buy_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}")
            return


    await ctx.send(f"You just bought {amount} {item}")


@client.command(aliases=['inv'])
async def inventory(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []


    em = discord.Embed(title = "Bag")
    for item in bag:
        name = item["item"]
        amount = item["amount"]

        em.add_field(name = name, value = amount)    

    await ctx.send(embed = em)    
async def buy_this(user,item_name,amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0]<cost:
        return [False,2]


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item":item_name , "amount" : amount}
        users[str(user.id)]["bag"] = [obj]        

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost*-1,"wallet")

    return [True,"Worked"]
    
@client.command()
async def sell(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await sell_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have {amount} {item} in your bag.")
            return
        if res[1]==3:
            await ctx.send(f"You don't have {item} in your bag.")
            return

    await ctx.send(f"You just sold {amount} {item}.")

async def sell_this(user,item_name,amount,price = None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price==None:
                price = 0.9* item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            return [False,3]
    except:
        return [False,3]    

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost,"wallet")

    return [True,"Worked"]

@client.command(aliases = ["lb"])
async def rich(ctx,x = 1):
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["wallet"] + users[user]["bank"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total,reverse=True)    

    em = discord.Embed(title = f"Top {x} Richest People" , description = "This is decided on the basis of raw money in the bank and wallet",color = discord.Color(0xfa43ee))
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = client.get_user(id_)
        name = member.name
        em.add_field(name = f"{index}. {name}" , value = f"{amt}",  inline = False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed = em)

@client.command(aliases = ['clear'])
@commands.has_permissions(manage_messages = True)
async def purge(ctx, amount = 2):
  await ctx.channel.purge(limit = amount)
  await ctx.send(f"Succesfully Cleared {amount} Messages!")

@client.command(aliases = ['k'])
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member,*,reason = "No Reason Provided"):
  guild = ctx.message.guild
  await member.send(member.name + f"Has Been Kicked From {guild.name}")
  await member.kick(reason = reason)

@client.command(aliases = ['b'])
@commands.has_permissions(kick_members = True)
async def ban(ctx, member : discord.Member,*,reason = "No Reason Provided"):
  guild = ctx.message.guild
  await member.send(member.name + f"Has Been Banned From {guild.name}")
  await member.ban(reason = reason)

@client.command(aliases = ['ub'])
@commands.has_permissions(ban_members = True)
async def unban(ctx,*,member):
  banned_users = await ctx.guild.bans()
  member_name, member_disc = member.split('#')

  for banned_entry in banned_users:
    user = banned_entry.user

    if (user.name, user.discriminator)==(member_name,member_disc):

      await ctx.guild.unban(user)
      await ctx.send(member_name +"Has Been Unbanned!")
      return
      
    await ctx.send(member+"Was Not Found")

@client.command(aliases = ['m'])
@commands.has_permissions(kick_members = True)
async def mute(ctx, member : discord.Member):
  muted_role = ctx.guild.get_role(738778396363849768)

  await member.add_roles(muted_role)

  await ctx.send(member.mention +"has been muted!")

@client.command(aliases = ['unmute'])
@commands.has_permissions(kick_members = True)
async def un_mute(ctx, member : discord.Member):
  muted_role = ctx.guild.get_role(738778396363849768)

  await member.remove_roles(muted_role)

  await ctx.send(member.mention +"has been unmuted!")









  





client.run("NzY5NDYwMTc4NjI5ODIwNDM2.X5PVog.AYYu9LDKfBhpRcHG9exaxthoZ-U")

