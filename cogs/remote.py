import termcolor
from datetime import datetime
from discord.ext import commands, tasks
from db_control import *


class Remote(commands.Cog):
    
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
        await cursor.update(mode="scrolls_data")
        print(f"{termcolor.colored((str(datetime.now()))[:-7], 'red', attrs=['dark', 'bold'])} " + info_text + f"{termcolor.colored('Push & Updated', 'magenta')}" + " scrolls_data (firebase)")
        await cursor.update(mode="items_data")
        print(f"{termcolor.colored((str(datetime.now()))[:-7], 'red', attrs=['dark', 'bold'])} " + info_text + f"{termcolor.colored('Push & Updated', 'magenta')}" + " items_data (firebase)")

    @tasks.loop(minutes=10)
    async def update_firebase(self):
        if self.update_firebase.current_loop == 0:
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

async def setup(client:commands.Bot) -> None:
   await client.add_cog(Remote(client))
