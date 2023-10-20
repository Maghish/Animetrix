import datetime
from discord.ext import commands
from datetime import datetime, timedelta
from fun_config import *


class help(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client
        self.client.remove_command('help')

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

