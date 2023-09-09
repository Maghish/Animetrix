import datetime
import termcolor
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from fun_config import *
from db_config import *


class help(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client
        self.client.remove_command('help')
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
        await cursor.update(mode="scrolls_data")
        print(f"{termcolor.colored((str(datetime.now()))[:-7], 'red', attrs=['dark', 'bold'])} " + info_text + f"{termcolor.colored('Push & Updated', 'magenta')}" + " scrolls_data (firebase)")
        await cursor.update(mode="items_data")
        print(f"{termcolor.colored((str(datetime.now()))[:-7], 'red', attrs=['dark', 'bold'])} " + info_text + f"{termcolor.colored('Push & Updated', 'magenta')}" + " items_data (firebase)")
       


    @commands.Cog.listener()
    async def on_command_error(self, message, error):
        if isinstance(error, commands.MissingPermissions):
            await message.send("Seems, I lack permissions! Please ask the server moderators or administrators.")
        elif isinstance(error, commands.CommandNotFound):
            await message.send("No such command!")
        elif isinstance(error, commands.CommandOnCooldown):
            seconds = round(error.retry_after)
            time_delta = timedelta(seconds=seconds)
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
        if self.update_firebase.count == None:
            cursor = DB()
            await cursor.create()
            info_text = termcolor.colored("FETCH", "blue", attrs=["bold", "blink"]) + "     "
            await cursor.update_json(mode="inventory")
            print(f"{termcolor.colored((str(datetime.now()))[:-7], 'green', attrs=['dark', 'bold'])} " + info_text + f"{termcolor.colored('Fetch & Updated', 'magenta')}" + " inventory (firebase)")
            await cursor.update_json(mode="human") 
            print(f"{termcolor.colored((str(datetime.now()))[:-7], 'green', attrs=['dark', 'bold'])} " + info_text + f"{termcolor.colored('Fetch & Updated', 'magenta')}" + " human (firebase)")
            await cursor.update_json(mode="scroll")
            print(f"{termcolor.colored((str(datetime.now()))[:-7], 'green', attrs=['dark', 'bold'])} " + info_text + f"{termcolor.colored('Fetch & Updated', 'magenta')}" + " scroll (firebase)")
            await cursor.update_json(mode="scrolls_data")
            print(f"{termcolor.colored((str(datetime.now()))[:-7], 'green', attrs=['dark', 'bold'])} " + info_text + f"{termcolor.colored('Fetch & Updated', 'magenta')}" + " scrolls_data (firebase)")
            await cursor.update_json(mode="items_data")
            print(f"{termcolor.colored((str(datetime.now()))[:-7], 'green', attrs=['dark', 'bold'])} " + info_text + f"{termcolor.colored('Fetch & Updated', 'magenta')}" + " items_data (firebase)")
            return 

        try:
            users = await get_human_stats()
            if users == {}: raise ValueError
            users = await get_inventory_data()
            if users == {}: raise ValueError
            users = await get_scroll_data()
            if users == {}: raise ValueError
            
            await get_scroll_data()
        except:
            return 
        
        cursor = DB()
        await cursor.create()
        info_text = termcolor.colored("PUSH", "blue", attrs=["bold", "blink"]) + "     "
        await cursor.update(mode="inventory")
        print(f"{termcolor.colored((str(datetime.now()))[:-7], 'green', attrs=['dark', 'bold'])} " + info_text + f"{termcolor.colored('Push & Updated', 'magenta')}" + " inventory (firebase)")
        await cursor.update(mode="human") 
        print(f"{termcolor.colored((str(datetime.now()))[:-7], 'green', attrs=['dark', 'bold'])} " + info_text + f"{termcolor.colored('Push & Updated', 'magenta')}" + " human (firebase)")
        await cursor.update(mode="scroll")
        print(f"{termcolor.colored((str(datetime.now()))[:-7], 'green', attrs=['dark', 'bold'])} " + info_text + f"{termcolor.colored('Push & Updated', 'magenta')}" + " scroll (firebase)")
        await cursor.update(mode="scrolls_data")
        print(f"{termcolor.colored((str(datetime.now()))[:-7], 'green', attrs=['dark', 'bold'])} " + info_text + f"{termcolor.colored('Push & Updated', 'magenta')}" + " scrolls_data (firebase)")
        await cursor.update(mode="items_data")
        print(f"{termcolor.colored((str(datetime.now()))[:-7], 'green', attrs=['dark', 'bold'])} " + info_text + f"{termcolor.colored('Push & Updated', 'magenta')}" + " items_data (firebase)")


    @commands.command()
    @commands.is_owner()
    async def update_temp(self, ctx, mode="all"):
        if mode == "all":
            index = 0
            while True:
                if index == 0: mode = "inventory"
                elif index == 1: mode = "human"
                elif index == 2: mode = "scroll"
                elif index == 3: mode = "scrolls_data"
                elif index == 4: mode = "items_data"
                elif index == 5: break
                cursor = DB()
                await cursor.update_json(mode=mode)
                info_text = termcolor.colored("FETCH", "blue", attrs=["bold", "blink"]) + "     "
                print(f"{termcolor.colored((str(datetime.now()))[:-7], 'green', attrs=['dark', 'bold'])} " + info_text + f"{termcolor.colored('Fetch & Updated', 'magenta')}" + f" {mode} (firebase)")
                index += 1

        cursor = DB()
        await cursor.update_json(mode=mode)
        info_text = termcolor.colored("FETCH", "blue", attrs=["bold", "blink"]) + "     "
        print(f"{termcolor.colored((str(datetime.now()))[:-7], 'green', attrs=['dark', 'bold'])} " + info_text + f"{termcolor.colored('Fetch & Updated', 'magenta')}" + f" {mode} (firebase)")
        
        await ctx.send("Successfully updated!")  
             

    @commands.command()
    async def help(self, ctx, command=None):
        if command is None:
            embed = discord.Embed(
                title="Animetrix's List of commands!",
                description="You can find all commands here, use `a!help <command_name>` to inspect the command itself!",
                color=0xaa5bfc,
                timestamp= datetime.utcnow()
            )
            embed.add_field(name="Basics ⚡", value="`help`, `ping`, `start`, `animehub`", inline=False)
            embed.add_field(name="Config ⚙️", value="`config spawn`, `config default`", inline=False)
            embed.add_field(name="Fruits/Scrolls 🍊", value="`scrolls`, `scrolls select`, `scrolls info`", inline=False)
            embed.add_field(name="Inventory 👜", value="`inv`, `inspect`", inline=False)
            embed.add_field(name="Chibucks <:chibucks:1141752496671445084>", value="`bal`, `pay`, `daily`", inline=False)
            embed.add_field(name="Backpack 🎒", value="`backpack`, `backpack add`, `backpack remove`", inline=False)
            embed.add_field(name="Stats/Profile 😎", value="`profile`, `stats`, `stats enhance`, `eat`", inline=False)
            embed.add_field(name="NPCS 🍣", value="`npcfight`, `npcinfo`", inline=False)
            embed.add_field(name="Dueling ⚔️", value="`duel`", inline=False)
            embed.add_field(name="Crystals 🔮", value="`claim`, `crystals`, `crystals open`", inline=False)
            embed.add_field(name="Quests 🍰", value="`quests`, `quests challenge`, `quests info`", inline=False)
            embed.add_field(name="Shop 🛒", value="`shop`, `shop <page>`, `buy`", inline=False)
            embed.add_field(name="\n", value="\n", inline=False)
            embed.set_footer(icon_url=(ctx.author.display_avatar), text= f"For {ctx.author.global_name}")
            await ctx.send(embed=embed) 
        else:
            ...







    @commands.command()
    async def ping(self, ctx):
        await ctx.reply(f"Pong 🏓  ! {round(self.client.latency, 3)}ms")


    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        if ctx.author.id == 978672079291449424:
            await ctx.reply("Shutting Down......")
            await self.client.close()
            
        else:
            return
        


async def setup(client:commands.Bot) -> None:
   await client.add_cog(help(client))

