import discord
from discord.ext import commands
from fun_config import *



class Scroll(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    

    @commands.group(aliases=["scroll", "scrolls", "fruit"])
    async def fruits(self, ctx):
        if ctx.invoked_subcommand is None:
            await create_scroll(ctx.author)
            user = ctx.author
            users = await get_scroll_data()

            try:
                Inventory = users[str(user.id)]["Scrolls"]
            except:
                Inventory = []

            embed = discord.Embed(
                title=f"{ctx.author}'s Fruits",
                description="This is the collection of fruits that you have obtained. Each fruit will disappear they got used."
            )   
            list_of_all_fruits = ""
            try:
                for items in Inventory:
                    name = items["item"]
                    amount = items["amount"]
                    emoji = items["emoji"]
                    active = items["active"]
                    level = items["Level"]
                    if amount < 1:
                        pass
                    else:
                        if active is False:
                            active = ""
                        else:
                            active = "**[ACTIVE]**"
                        list_of_all_fruits = list_of_all_fruits + f"{emoji} | {name} x{amount} ・ Lv{level} {active}\n"
                        continue

                embed.add_field(name="\n",value=list_of_all_fruits)
            except:
                embed.add_field(name="\n",value="*You haven't obtained any fruits yet*")

            await ctx.send(embed=embed)


    @fruits.command(aliases=["use"])
    async def select(self, ctx, *, item):
        await create_scroll(ctx.author)
        res = await set_scroll_active(ctx.author, item)

        if not res[0]:
            if res[1] == 1:
                await ctx.reply(f"There is no fruit/scroll called {item} ")
            elif res[1] == 2:
                await ctx.reply(f"The fruit is already active!\nTry `a!fruits`")
            elif res[1] == 3:
                await ctx.reply(f"You don't have the fruit/scroll!")
        else:
            await ctx.reply(f"{res[1]} activated!\nType `a!fruits info` to view the fruit/scroll!")

    
    @fruits.command()
    async def info(self, ctx, item = None):
        user = ctx.author   
        users = await get_scroll_data()
        name = None
        
        
        if item == None:
            
            for items in users[str(user.id)]["Scrolls"]:
                active = items["active"]
                if active is True:
                    name = items["item"]
                    amount = items["amount"]
                    ability = items["ability"]
                    level = items["Level"]
                    attributes = await get_all_attributes(name, scroll_data_json_file, Key=["desc", "img", "rarity"])
                    break
                else:
                    pass

            if name == None:
                await ctx.reply("You haven't selected a fruit yet!")
                return
        else:
            for items in users[str(user.id)]["Scrolls"]:
                name = items["item"]
                name_lower = name.lower()
                if item.lower() == name_lower:
                    name = name
                    amount = items["amount"]
                    if amount < 1:
                        name = None
                        amount = 0
                        continue
                    else:    
                        ability = items["ability"]
                        level = items["Level"]
                        attributes = await get_all_attributes(name, scroll_data_json_file, Key=["desc", "img", "rarity"])
                        break
                else:
                    pass
            if name == None:
                await ctx.reply("You don't have that fruit!")
                return
        

        embed = discord.Embed(
            title= f"{ctx.author.display_name} - Lv{level} {name}",
            description= attributes[0]
        )
        embed.add_field(name="\n", value=f"🥭・Duplicates - {amount - 1}\n🔼・Level - {level}\n✨・Rarity - {attributes[2]}")
        embed.set_thumbnail(url=attributes[1])
        await ctx.send(embed = embed)
        


async def setup(client:commands.Bot) -> None:
   await client.add_cog(Scroll(client))


