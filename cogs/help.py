import discord
from discord.ext import commands
from fun_config import *


class help(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client


    @commands.command()
    async def ping(self, ctx):
        await ctx.reply(f"Pong 🏓 ! {round(self.client.latency)}ms")
        await self.bleed.start()


    @commands.command()
    async def shutdown(self, ctx):
        if ctx.author.id == 978672079291449424:
            await ctx.reply("Shutting Down......")
            await self.client.close()
            
        else:
            return
                
    


async def setup(client:commands.Bot) -> None:
   await client.add_cog(help(client))

