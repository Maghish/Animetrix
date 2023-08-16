import discord
from discord.ext import commands
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
            # TODO:
            # 1. List all the crystals that the user have
            # 2. Display the fragments
            ...

    @crystals.command()
    async def open(self, ctx,*, crystal_name):


        res = await open_crystal(ctx.author, crystal_name)

        if not res[0]:
            if res[1] == 1:
                await ctx.send("The item does not exist")
            if res[1] == 2:
                await ctx.send("You don't have that item!")
        else:
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
        ...

    



      

async def setup(client: commands.Bot) -> None:
      await client.add_cog(Crystal(client))