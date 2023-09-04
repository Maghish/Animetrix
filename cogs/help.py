import datetime
import termcolor
from discord.ext import commands, tasks
from datetime import datetime
from fun_config import *
from db_config import *


class help(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client
        self.update_firebase.start()

    async def cog_unload(self):
        self.update_firebase.cancel()
        cursor = DB()
        await cursor.create()
        await cursor.update(mode="inventory")
        info_text = termcolor.colored("SHUTDOWN", "blue", attrs=["bold", "blink"]) + "  "
        print(f"{termcolor.colored((str(datetime.now()))[:-7], 'red', attrs=['dark', 'bold'])} " + info_text + f"{termcolor.colored('Push & Updated', 'magenta')}" + " inventory (firebase)")
        await cursor.update(mode="human")
        print(f"{termcolor.colored((str(datetime.now()))[:-7], 'red', attrs=['dark', 'bold'])} " + info_text + f"{termcolor.colored('Push & Updated', 'magenta')}" + " human (firebase)")
        await cursor.update(mode="scroll")
        print(f"{termcolor.colored((str(datetime.now()))[:-7], 'red', attrs=['dark', 'bold'])} " + info_text + f"{termcolor.colored('Push & Updated', 'magenta')}" + " scroll (firebase)")
       


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
        elif isinstance(error, commands.NotOwner):
            pass
        else:
            raise error
        

    @tasks.loop(minutes=10)
    async def update_firebase(self):
        cursor = DB()
        await cursor.create()
        info_text = termcolor.colored("PUSH", "blue", attrs=["bold", "blink"]) + "     "
        await cursor.update(mode="inventory")
        print(f"{termcolor.colored((str(datetime.now()))[:-7], 'green', attrs=['dark', 'bold'])} " + info_text + f"{termcolor.colored('Push & Updated', 'magenta')}" + " inventory (firebase)")
        await cursor.update(mode="human") 
        print(f"{termcolor.colored((str(datetime.now()))[:-7], 'green', attrs=['dark', 'bold'])} " + info_text + f"{termcolor.colored('Push & Updated', 'magenta')}" + " human (firebase)")
        await cursor.update(mode="scroll")
        print(f"{termcolor.colored((str(datetime.now()))[:-7], 'green', attrs=['dark', 'bold'])} " + info_text + f"{termcolor.colored('Push & Updated', 'magenta')}" + " scroll (firebase)")


    @commands.command()
    @commands.is_owner()
    async def update_temp(self, ctx, mode):
        cursor = DB()
        await cursor.update_json(mode=mode)
        info_text = termcolor.colored("FETCH", "blue", attrs=["bold", "blink"]) + "     "
        print(f"{termcolor.colored((str(datetime.now()))[:-7], 'green', attrs=['dark', 'bold'])} " + info_text + f"{termcolor.colored('Fetch & Updated', 'magenta')}" + f" {mode} (firebase)")
        await ctx.send("Successfully updated!")  

    @commands.command()
    async def ping(self, ctx):
        await ctx.reply(f"Pong 🏓 ! {round(self.client.latency)}ms")


    @commands.command()
    async def shutdown(self, ctx):
        if ctx.author.id == 978672079291449424:
            await ctx.reply("Shutting Down......")
            await self.client.close()
            
        else:
            return
        


async def setup(client:commands.Bot) -> None:
   await client.add_cog(help(client))

