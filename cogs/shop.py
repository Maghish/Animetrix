import discord
from discord.ext import commands 
from fun_config import *


class Shop(commands.Cog):
    

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.group(aliases = ["shop", "Shop"])
    async def shopp(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                title= "Marketplace",
                description= "Here you can find various items to enhance your harvestors, defenses and buy potions and various materials. Type `r!shop (page)` to open the page!",
                color= 0x1ea205

            )
            embed.add_field(name= "Potions 🪴 (1)", value= "Potions will give you buffs and boost to harvestors, defenses, etc.", inline= False)
            embed.add_field(name= "Medicines 💊 (2)", value= "Medicines are used to heal the HP of the ORB.", inline = False)
            embed.add_field(name= "Troops 🪖 (3)", value= "These troops who will fight for you.", inline= False)
            await ctx.send(embed = embed)

    @shopp.command(aliases = ["1"])
    async def one(self, ctx):
        embed = discord.Embed(
        title= "Marketplace (1)",
        description= "Here you can find various types of Potions to boost or buff your harvestor, defenses, ORB, etc. type `r!buy (item_name)` to buy the item!",
        color= 0x1ea205
        )

        embed.add_field(name= "HP Booster - 400 Z-Coins", value="Increases the HP by 10% for 20 mins", inline= False)
        embed.add_field(name= "Harvestor Boost - 350 Z-Coins", value="Increases the Z-Energy harvesting rate by 2% for 1h", inline= False)

        await ctx.send(embed = embed)

    @shopp.command(aliases = ["3"])
    async def three(self, ctx):
        embed = discord.Embed(
        title= "Marketplace (3)",
        description= "Here you can find the most of the troops. type `r!recruit (troop_name)` to buy the troop!",
        color= 0x1ea205
        )

        embed.add_field(name= "Indiana Jones - 2500 Z-Coins", value="Who doesn't know about Indiana Jones?", inline= False)
        embed.add_field(name= "Soldier - 800 Z-Coins", value= "IDK", inline=False)
        await ctx.send(embed = embed)

    

    @commands.command()
    async def buy(self, ctx,*,item):

        try:
            item, amount = item.split(" ")
            amount = int(amount)
        except:
            item = item
            amount = 1

        await open_inv(ctx.author)
        await open_account(ctx.author)

        res = await buy_this(ctx.author,item,amount)

        if not res[0]:
            if res[1]==1:
                await ctx.send("The Item doesn't exists")
                return
            if res[1]==2:
                await ctx.send(f"Insufficient Money")
                return

        else:
            await ctx.send(f"You bought {amount}x {res[1]}")




async def setup(client:commands.Bot) -> None:
   await client.add_cog(Shop(client))