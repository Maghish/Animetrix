import discord
from discord.ext import commands
import random
from fun_config import *




class economy(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            
            await ctx.send("You have to wait for 00:00:{:.2f}s to use this command".format(error.retry_after))


    @commands.command()
    @commands.cooldown(1, 86400,commands.BucketType.user)
    async def daily(self, ctx):
        amount = random.randint(100, 9999)
        await update_bank(ctx.author, amount, "Wallet")
        await ctx.send(f"You got {amount} Chibucks!")

    @commands.group(aliases = ["balance", "bal"])
    async def balancee(self, ctx):
        user = ctx.author
        users = await get_bank_data()
        if str(user.id) not in users:
                await open_account(ctx.author)
                return False
        else:
            user = ctx.author
            users = await get_bank_data()
            walletamt = users[str(user.id)]["Wallet"]
            em = discord.Embed(
                title= (f"{user.name}'s leftovers"),color= 0xcc00ff)
            em.add_field(name = "Wallet", value = f"{walletamt:,} Chibucks")
            em.set_thumbnail(url = ctx.author.avatar)
            await ctx.send(embed = em)

    @balancee.command()
    async def of(self, ctx , member: discord.Member):
        user = ctx.author
        users = await get_bank_data()
        if str(user.id) not in users:
                return False
        else:
            user = ctx.author
            users = await get_bank_data()
            walletamt = users[str(member.id)]["Wallet"]
            zero = str(0)
            em = discord.Embed(
                title= (f"{member.name}'s leftovers"),color= 0xcc00ff)
            em.add_field(name = "Wallet", value = (f"{walletamt:,}"))
            await ctx.send(embed = em)
    
    @commands.command()
    async def pay(self, ctx,member: discord.Member, amount = None):
        user = ctx.author
        users = await get_bank_data()
        if str(user.id) not in users:
                return False
        else:
            user = ctx.author
            users = await get_bank_data()
            balance = (users[str(user.id)]["Wallet"])
            amount = str(amount)
            result = balance < int(amount)
            print(f'{balance} and {amount} and {result}')
            if amount == None:
                await ctx.send("Enter the amount")
                return 
            if result is True:
                await ctx.send("Insufficient Chibucks")
                return
            if int(amount)<0:
                await ctx.send("Invaild amount")
                return
            await update_bank(ctx.author,-1* int(amount), "Wallet"),
            await update_bank(member, amount, "Wallet")
            await ctx.reply (f'{amount} Chibucks has been transferred from {ctx.author} to {member}!')

    


async def setup(client:commands.Bot) -> None:
   await client.add_cog(economy(client))


