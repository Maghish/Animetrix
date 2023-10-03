from typing import Any
import datetime
import discord
from discord.ext import commands
from fun_config import *


# here / page
class Page(View):

    def __init__(self, type="Inventory", user=None, asset: list = None, channel=None):
        self.type = type
        self.user = user
        self.asset = asset
        self.channel = channel
        self.page_index = 0


    async def paginate(self, type, user):
        if type != "Inventory":
            embed1 = self.asset[0]
            embed2 = self.asset[1]
            if self.page_index == 0:
                self.add_item(self.next_button)
                await self.channel.send(embed=embed1, view=self)  


    @discord.ui.button(label="▶️", style=discord.ButtonStyle.green)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.page_index += 1








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
                title=f"{ctx.author.global_name}'s Fruits",
                description="This is the collection of fruits that you have obtained. Each fruit will disappear they got used.",
                color= 0xaa5bfc,
                timestamp=datetime.datetime.utcnow()
            )   
            list_of_all_fruits = ""
            try:
                for items in Inventory:
                    name = items["item"]
                    amount = items["amount"]
                    emoji = items["emoji"]
                    active = items["active"]
                    level = items["Level"]
                    star = items["star"]
                    if amount < 1:
                        pass
                    else:
                        if active is False:
                            active = ""
                        else:
                            active = "**[ACTIVE]**"
                        list_of_all_fruits = list_of_all_fruits + f"{emoji} | {name} {await convert_star(star=star)} ・ Lv{level} {active}\n"
                        continue

                embed.add_field(name="\n",value=list_of_all_fruits)
            except:
                pass

            if list_of_all_fruits == "":
                embed.add_field(name="\n",value="*You haven't obtained any fruits yet*")

            embed.add_field(name="\n", value="\n", inline=False)
            embed.set_footer(icon_url=(ctx.author.display_avatar), text= f"For {ctx.author.global_name}")

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
    async def info(self, ctx,*,item = None):
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
        

        embed1 = discord.Embed(
            title= f"{ctx.author.display_name} - Lv{level} {name}",
            description="This provides all the information you needed to know about the fruit. ",
            color = 0xaa5bfc,
            timestamp= datetime.datetime.utcnow()
        )
        embed1.add_field(name="Description", value=attributes[0], inline=False)
        embed1.add_field(name="\n", value=f"🔮 Duplicates - {amount - 1}\n🔼 Level - {level}\n✨ Rarity - {attributes[2]}", inline= False)
        field_value = ""
        for move in ability:
            field_value = field_value + f"{move['emoji']} {move['ability_name']}\n"
            continue

        embed1.add_field(name="Abilities", value=field_value, inline=False)
        embed1.add_field(name="\n", value="\n", inline=False)
        embed1.add_field(name="\n", value="\n", inline=False)
        embed1.set_thumbnail(url=attributes[1])
        embed1.set_footer(icon_url=(ctx.author.display_avatar), text= f"For {ctx.author.global_name}")


        embed2 = discord.Embed(
            title= f"{ctx.author.display_name} - Lv{level} {name}",
            description="This provides all the information you needed to know about the fruit. ",
            color = 0xaa5bfc,
            timestamp= datetime.datetime.utcnow()
        )



        for move in ability:
            if move['level'] <= level:
                title = f"{move['emoji']} {move['ability_name']}"
            else:
                title = f"{move['emoji']} {move['ability_name']} 🔒"

            if not move['repeat']:
                field_value = f"\n🔼 Level - {move['level']}\n💥 Damage - {move['dmg']}\n⚡ Chakra - {move['chakra']}\n🍻 Effects - *None*"
            else:
                field_value = f"\n🔼 Level - {move['level']}\n💥 Damage - {move['dmg']}\n⚡ Chakra - {move['chakra']}\n🍻 Effects - {move['repeat'][0]} {move['repeat'][1]}"
            

            if move['effect_break']:
                field_value = field_value + "\n🛑 This move breaks - "
                for effects in move['effect_break']:
                    field_value = field_value + f"{effects}, "
                    continue
                field_value = field_value[:-1]
                    
            
            if move['effect_ignore']:
                field_value = field_value + "\n🎍 This move gets broke by - "
                for effects in move['effect_ignore']:
                    field_value = field_value + f"{effects}, "
                    continue
                field_value = field_value[:-1]

            field_value = field_value + "\n"

            
            embed2.add_field(name=title, value=field_value, inline=False)

        embed2.add_field(name="\n", value="\n", inline=False)
        embed2.set_thumbnail(url=attributes[1])
        embed2.set_footer(icon_url=(ctx.author.display_avatar), text= f"For {ctx.author.global_name}")
        
        channel = self.client.get_channel(ctx.channel)
        default = Page(type="Info", user=ctx.author, asset=[embed1, embed2], channel=channel)
        await default.paginate("Info", ctx.author)



class Inventory(commands.Cog):
    
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 86400,commands.BucketType.user)
    async def daily(self, ctx):
        amount = random.randint(100, 9999)
        await update_bank(ctx.author, amount, "Chibucks")
        await ctx.send(f"You got {amount} Chibucks <:chibucks:1141752496671445084>!")

    
    @commands.command()
    async def pay(self, ctx,member: discord.Member, amount = None):
        user = ctx.author
        users = await get_inventory_data()
        if str(user.id) not in users:
                return False
        else:
            user = ctx.author
            users = await get_inventory_data()
            balance = (users[str(user.id)]["Chibucks"])
            amount = str(amount)
            result = balance < int(amount)
            print(f'{balance} and {amount} and {result}')
            if amount == None:
                await ctx.send("Enter the amount")
                return 
            if result is True:
                await ctx.send("Insufficient Chibucks")
                return
            if int(amount)<0:
                await ctx.send("Invaild amount")
                return
            await update_bank(ctx.author,-1* int(amount), "Chibucks"),
            await update_bank(member, amount, "Chibucks")
            await ctx.reply (f'{amount} Chibucks <:chibucks:1141752496671445084> has been transferred from {ctx.author.global_name} to {member.global_name}!')


    @commands.command(aliases = ["bal", "inv"])
    async def inventory(self, ctx):
        embed = discord.Embed(
            title=f"{ctx.author.global_name}'s Inventory",
            description="Here you can find a lot of items like food, chibucks, potions and such items. if you want to inspect any of these items (excluding chibucks)",
            color= 0xaa5bfc,
            timestamp=datetime.datetime.utcnow()
        )
        users = await get_inventory_data()
        user = ctx.author
        embed.add_field(name=f"{(users[str(user.id)]['Chibucks']):,} Chibucks <:chibucks:1141752496671445084>", value="\n\n", inline=False)

        inventory_items = ""
        try:
            for items in users[str(user.id)]["Inventory"]:
                if items["amount"] <= 0:
                    pass
                else:
                    inventory_items = inventory_items + f"{items['emoji']} | {items['item']} x{items['amount']}\n"
                    continue
        except:
            pass
        
        if inventory_items == "":
            inventory_items = "*No items in your inventory*"
    
        embed.add_field(name="Inventory", value=inventory_items, inline=False)  

        food_items = ""
        try:
            for items in users[str(user.id)]["Food"]:
                if items["amount"] <= 0:
                    pass
                else:
                    food_items = food_items + f"{items['emoji']} | {items['item']} x{items['amount']}\n"
                    continue
        except:
            pass

        if food_items == "":
            food_items = "*No potions in your inventory*"
        
        embed.add_field(name="Food Chest", value=food_items, inline=False)

        potion_items = ""
        try:
            for items in users[str(user.id)]["Potion"]:
                if items["amount"] <= 0:
                    pass
                else:
                    potion_items = potion_items + f"{items['emoji']} | {items['item']} x{items['amount']}"
                    continue
        except:
            pass

        if potion_items == "":
            potion_items = "*No potions in your inventory*"
        
        embed.add_field(name="Potions", value=potion_items, inline=False)

        embed.add_field(name="\n", value="\n", inline=False)

        embed.set_footer(icon_url=(ctx.author.display_avatar), text= f"For {ctx.author.global_name}")

        await ctx.send(embed=embed)






class Backpack(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client


    @commands.group()
    async def backpack(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                title=f"{ctx.author.global_name}'s Backpack",
                description="Here you can view all items in your backpack. use `a!backpack add <item_name>` to add it to your backpack or if you want to remove it, then use `a!backpack remove <item_name>` to remove it.",
                color= 0xaa5bfc,
                timestamp=datetime.datetime.utcnow() 
            )

            users = await get_inventory_data()
            user = ctx.author

            backpack_items = ""
            try:
                for items in users[str(user.id)]["Backpack"]:
                    if items["amount"] <= 0:
                        pass
                    else:
                        backpack_items = backpack_items + f"{items['emoji']} | {items['item']} x{items['amount']}\n"
                        continue
            except:
                pass

            if backpack_items == "":
                backpack_items = "*No items in your backpack*"

            embed.add_field(name="Backpack", value=backpack_items)

            embed.add_field(name="\n", value="\n", inline=False)
            embed.set_footer(icon_url=(user.display_avatar), text=f"For {ctx.author.global_name}")

            await ctx.send(embed=embed)

    @backpack.command()
    async def add(self, ctx,*, item_name):
        
        res = await sep_int_and_str(item_name)   
        item, amount = res[0].rstrip(), res[1]

        res = await change_backpack(ctx.author, item, amount, "Add")

        if not res[0]:
            if res[1] == 1:
                await ctx.send("The item does not exist!")
            elif res[1] == 2:
                await ctx.send("You don't have that item!")
        else:
            await ctx.send(f"Successfully added {res[2]}x {res[1]} to your backpack 🎒")

    @backpack.command()
    async def remove(self, ctx,*, item_name):
        res = await sep_int_and_str(item_name)   
        item, amount = res[0].rstrip(), res[1]

        res = await change_backpack(ctx.author, item, amount, "Remove")

        if not res[0]:
            if res[1] == 1:
                await ctx.send("The item does not exist!")
            elif res[1] == 2:
                await ctx.send("You don't have that item!")
        else:
            await ctx.send(f"Successfully removed {res[2]}x {res[1]} from your backpack 🎒")


async def setup(client:commands.Bot) -> None:
   await client.add_cog(Scroll(client))
   await client.add_cog(Inventory(client))
   await client.add_cog(Backpack(client))


