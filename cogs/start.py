from typing import Optional, Union
import discord
from discord.emoji import Emoji
from discord.enums import ButtonStyle
from discord.ext import commands
from discord.partial_emoji import PartialEmoji
from discord.ui import Button, View
from fun_config import *

class Start(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client


    @commands.command()
    async def start(self, ctx):
        users = await get_scroll_data()
        try:
            if users[str(ctx.author.id)]["Scrolls"] != "None":
                await ctx.reply("You already started!")
                return 
            else:
                pass
        except:
            pass
        embed = discord.Embed(
            title=f"Hello {ctx.author.global_name}!",
            description="Welcome to the world of Animetrix! This is the place where you can fight NPCS and gain rewards to buy crystals to get scrolls to defeat other players! To get started, click the button below to proceed!"
        )
        the_view = View()
        the_button = Button(label="Click here!", style=discord.ButtonStyle.green)
        the_view.add_item(the_button)

        async def startcall(interaction):
            the_view.children.clear()
            await open_inv(interaction.user)
            await create_human(interaction.user)
            await create_scroll(interaction.user)
            embed = discord.Embed(
                title="Quick Guide",
                description="Before you start, here's a quick guide for you!"
            )
            embed.add_field(name="Help", value="Use `a!help` to get the help menu whenever you need.", inline=False)
            embed.add_field(name="Fruits", value="Fruits are things which you can consume to get abilities! Fruits will disappear after use. To view all of your fruits, Type `a!fruits`. To select/consume a fruit, use `a!fruits select <fruit_name>`", inline=False)
            embed.add_field(name="Balance", value="Chibucks is the main currency of this bot, Use `a!bal` to view your Chibucks", inline=False)
            embed.add_field(name="Stats", value="This bot has HP and Chakra (Energy) System, to view your stats, use `a!stats`. You will level up by chatting!", inline=False)
            embed.add_field(name="Shop", value="Shop is where you can buy fragments which you can use to claim crystals which gives fruits! Use `a!shop`", inline=False)
            embed.add_field(name="Quests", value="You can challenge quests which will give you amazing rewards by defeating the NPCs mentioned in the quest! To view all the quests available, Use `a!quests`. To fight npcs, type `a!npcfight <npc_name>` to start a battle! But first you have to select a fruit of yours!", inline=False)
            embed.add_field(name="Server Support", value="If you still have any doubts and questions. then [join our server](https://discord.gg/pFaVxyCJ3K)!", inline=False)
            await interaction.response.send_message(embed=embed)
            the_view.stop()

        the_button.callback = startcall
        await ctx.send(embed=embed, view=the_view)
        res = await the_view.wait()
        if not res:
            embed = discord.Embed(
                title="Enjoy your journey!", 
                description="You have now been gifted **`Novice Scroll`**. This is your first fruit! You may still be unclear about what to do next, so here's another quick step by step process to get started!"
            )
            embed.add_field(name="Step 1:", value="Start by typing `a!fruits` to view your fruit.")
            embed.add_field(name="Step 2:", value="Type `a!fruits select <fruit_name>` to select your fruit")
            embed.add_field(name="Step 3:", value="Now it's time to battle! Type")
            embed.add_field(name="Step 4:", value="Start by typing `a!fruits` to view your fruit.")
            embed.add_field(name="Step 5:", value="Start by typing `a!fruits` to view your fruit.")
            embed.add_field(name="Step 6:", value="Start by typing `a!fruits` to view your fruit.")
            embed.add_field(name="Step 7:", value="Start by typing `a!fruits` to view your fruit.")
            embed.add_field(name="Step 8:", value="Start by typing `a!fruits` to view your fruit.")
            # here / steps guide
            the_view = View()
            the_button = Button(label="Join Our Server!", url="https://discord.gg/pFaVxyCJ3K")
            the_view.add_item(the_button)
            users = await get_scroll_data()
            with open(scroll_data_json_file, "r") as json_file:
                data = json.load(json_file)
                data = (data)
                for items in data:
                    if items["mode"] == "Shop/Scrolls" and items["itemname"] == "Novice Scroll":
                        users[str(ctx.author.id)]["Scrolls"] = {"item": items["itemname"], "amount": 1, "mode": items["mode"], "emoji": items["emoji"], "active": True, "ability": items["ability"], "Level": 1, "exp": 0}

                        with open(scroll_json_file, "w") as json_file:
                            json.dump(users, json_file, indent= 1)

                        break
                    else:
                        pass        
            await ctx.send(embed=embed, view=the_view)
            



async def setup(client:commands.Bot) -> None:
   await client.add_cog(Start(client))