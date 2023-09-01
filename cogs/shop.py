import discord
from discord.ext import commands 
import emoji
from fun_config import *


class Shop(commands.Cog):
    

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.group(aliases = ["shop", "Shop"])
    async def shopp(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                title= "Marketplace",
                description= "Here you can find various items, crystals and buy potions and various materials. Type `a!shop <page>` to open the page!",
                color= 0x1ea205

            )
            embed.add_field(name= "Potions 🪴 (1)", value= "Potions will give you external buffs while during duel or npc battles.", inline= False)
            embed.add_field(name= "Foods 🍉 (2)", value= "These items heals your HP/Chakra outisde the battle.", inline = False)
            embed.add_field(name= "Crystals 📜 (3)", value= "You can buy crystals plus you can collect fragments and claim the crystal.", inline= False)
            await ctx.send(embed = embed)
    

    @shopp.command(aliases = ["1"])
    async def one(self, ctx):
        embed = discord.Embed(
        title= "Marketplace (1)",
        description= "Here you can find various types of Potions to boost or buff yourself in duels or npc battles, remember you can only use this while in a battle. type `a!buy <item_name>` to buy the item!",
        color= 0x1ea205
        )

        embed.add_field(name= "Regeneration Potion - 2000 Chibucks <:chibucks:1141752496671445084>", value="Regenerate the HP for 20 mins", inline= False)

        await ctx.send(embed = embed)

    @shopp.command(aliases = ["3"])
    async def three(self, ctx):
        embed = discord.Embed(
        title= "Marketplace (3)",
        description= "Here you can find all crystals available. You can buy the fragments using `a!buy Universal Fragment`. To claim the crystals, use `a!claim <crystal_name>`.",
        color= 0x1ea205
        )

        
        embed.add_field(name="Fragments", value="🪡 Universal Fragment - 300 Chibucks <:chibucks:1141752496671445084>\n", inline=False)

        crystals = ''''''
        users = await get_inventory_data()
        with open(items_json_file, "r") as json_file:
            data = json.load(json_file)
            data = (data)
            for items in data:
                if items["mode"] == "Shop/Crystal":
                    crystals = crystals + f"{emoji.emojize(items['emoji'])} {items['itemname']} - {users[str(ctx.author.id)]['Fragments']}/{items['price']}\n"
                    continue
                else:
                    pass

        embed.add_field(name="Crystals", value=crystals)

        await ctx.send(embed = embed)

    # here / crystals

    @commands.command()
    async def buy(self, ctx,*,item):
        
        res = await sep_int_and_str(item)   
        item, amount = res[0].rstrip(), res[1]
        await open_inv(ctx.author)
        await open_account(ctx.author)

        if item.lower() == "universal fragment":
            users = await get_bank_data()
            if 300*amount > int(users[str(ctx.author.id)]["Wallet"]):
                await ctx.send("Insufficient Chibucks")
            else:
                users = await get_inventory_data()
                users[str(ctx.author.id)]["Fragments"] += amount

                with open(inventory_json_file, "w") as json_file:
                    json.dump(users, json_file, indent=1)
                
                await update_bank(ctx.author, -1*(300*amount), "Wallet")
                await ctx.send(f"You bought {amount}x Universal Fragments\nUse `a!crystals` to view all the fragments you have.")
        else:        
            res = await buy_this(ctx.author,item,amount)
            
            if not res[0]:
                if res[1]==1:
                    await ctx.send("The Item doesn't exists")
                    return
                if res[1]==2:
                    await ctx.send(f"Insufficient Chibucks")
                    return

            else:
                await ctx.send(f"You bought {amount}x {res[1]}")




async def setup(client:commands.Bot) -> None:
   await client.add_cog(Shop(client))