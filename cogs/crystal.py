import discord
from discord.ext import commands
from emoji import emojize
import asyncio
from fun_config import *

class Crystal(commands.Cog):
    
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    async def claim(self, ctx,*, crystal_name):

        res = await sep_int_and_str(crystal_name)   
        item, amount = res[0].rstrip(), res[1]

        res = await claim_crystal(ctx.author, item, amount)

        if not res[0]:
            if res[1] == 1:
                await ctx.send("The item does not exist")
            if res[1] == 2:
                await ctx.send("You don't have that much Fragments to claim this crystal!")
        else:
            await ctx.send(f"You have claimed {res[2]}x {res[1]}\nUse `a!crystals` to view all the claimed crystals.")
    



    @commands.group()
    async def crystals(self, ctx):
        if ctx.invoked_subcommand == None:
            await open_inv(ctx.author)
            user = ctx.author
            users = await get_inventory_data()

            try:
                Crystals = users[str(user.id)]["Crystal"]
            except:
                Crystals = []

            embed = discord.Embed(
                title=f"{ctx.author}'s Crystals", 
                description="This is the list of all the crystals you have ready to open. Use `a!crystals open <crystal_name>` to open the crystal! To inspect the crystal, type `a!crystals info <crystal_name>`"
            )
            list_of_all_crystals = ""
            try:
                for crystal in Crystals:
                    name = crystal["item"]
                    amount = crystal["amount"]
                    emoji = crystal["emoji"]
                    if amount < 1:
                        pass
                    else:
                        list_of_all_crystals = list_of_all_crystals + f"{emojize(emoji)} ・ {name} x{amount}\n"
                embed.add_field(name="\n", value=list_of_all_crystals)
            except:
                embed.add_field(name="\n", value="*You haven't obtained any crystals yet!*")
    
            await ctx.send(embed=embed)

        
    @crystals.command()
    async def open(self, ctx,*, crystal_name):


        res = await open_crystal(ctx.author, crystal_name)

        if not res[0]:
            if res[1] == 1:
                await ctx.send("The item does not exist")
            if res[1] == 2:
                await ctx.send("You don't have that item!")
        else:
            print("tf")
            message = await ctx.reply(f"Opening {res[1]}... **|**")
            symbol = ["/", "-", "\ ", "|", "/", "-", "\ ", "|"]
            for count in range(0, 8):
                await asyncio.sleep(0.5)
                await message.edit(content=f"Opening {res[1]}... **{symbol[count]}**")

            await message.delete()
            msg = f"You opened {res[1]} and got.."
            message = await ctx.send(msg)
            for things in res[2]:
                await asyncio.sleep(0.5)
                msg = str(msg + f"\n1x {things}")
                await message.edit(content=msg)


        

    @crystals.command()
    async def info(self, ctx, crystal_id):
        # here / info command
        ...

    



      

async def setup(client: commands.Bot) -> None:
      await client.add_cog(Crystal(client))