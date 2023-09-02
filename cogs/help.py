import datetime
from discord.ext import commands, tasks
from fun_config import *


class help(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, message, error):
        if isinstance(error, commands.MissingPermissions):
            await message.send("Seems, I lack permissions! Please ask the server moderators or administrators.")
        elif isinstance(error, commands.CommandNotFound):
            await message.send("No such command!")
        elif isinstance(error, commands.CommandOnCooldown):
            seconds = round(error.retry_after)
            time_delta = datetime.timedelta(seconds=seconds)
            time_str = str(time_delta)
            if time_str.startswith("0:"):
                time_str = time_str[2:]
            await message.send(f"Command on cooldown! Please try after {time_str}")
        else:
            raise error


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

