import discord
from discord.ext import commands, tasks
from fun_config import *
from discord.ui import Button, View, Select
import random
from datetime import datetime
import math
import asyncio
import emoji


class Human(commands.Cog):
    
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        
        if message.author.bot:
            return
        
        if message.content.startswith(''):
            try:
                t = 0
                user = message.author
                users = await get_human_stats()
                await heal_human(user, 1, "exp")
                current = users[str(user.id)]["exp"]
                lvl = users[str(user.id)]["Level"]
                if current >= math.ceil(6* (lvl ** 4) / 2.5):
                    temp_level = lvl
                    while True:
                        if current >= math.ceil(6* (temp_level ** 4) / 2.5):
                            temp_level += 1
                        else: 
                            break
                    temp_level = temp_level - lvl
                    await heal_human(message.author, temp_level, "Level")
                    LVL = lvl + temp_level
                    embed = discord.Embed(
                            title=f"Awesome {message.author}!",
                            description=f"You leveled up from {lvl} to {LVL}!",
                            timestamp= datetime.utcnow()
                        )
                    embed.set_footer(icon_url=(message.author.display_avatar), text= f"For {message.author}")
                    await message.channel.send(embed = embed)
                    await message.channel.send(f"You got {2*(int(temp_level))} attribute points!\ncheckout `a!stats`")
                    await heal_human(message.author, 2*(int(temp_level)), "AttrPoints")
                else:
                    return
            except:
                pass

    @commands.group()
    async def stats(self, ctx):
        if ctx.invoked_subcommand is None:
            users = await get_human_stats()
            embed = discord.Embed(
                title=f"{ctx.author.global_name}'s Stats",
                description="You can view all your states here. To use attribute points use `a!stats enhance <stat_name>`, `maxhp` for Max HP, `maxchakra` for Max Chakra and `pdmg` for Phyical Damage.",
                color=0xaa5bfc,
                timestamp= datetime.utcnow()
            )
            embed.add_field(name="\n",value=f'''
HP - {await make_bars(ctx.author, "HP", "MaxHP", "🟥", "⬛", 6)}
Chakra - {await make_bars(ctx.author, "Energy", "MaxEnergy", "🟦", "⬛", 5)}
Level - {users[str(ctx.author.id)]['Level']}
EXP - {(await make_bars(ctx.author, "exp", "exp", "⬜", "⬛", 6)).replace(f"{users[str(ctx.author.id)]['exp']}/{users[str(ctx.author.id)]['exp']}", f"{users[str(ctx.author.id)]['exp']}")}
Attribute Points - {users[str(ctx.author.id)]['AttrPoints']}
''')
            # here / finish the embed
            embed.add_field(name="\n", value="\n", inline=False)
            embed.set_footer(icon_url=(ctx.author.display_avatar), text= f"For {ctx.author.global_name}")
            await ctx.send(embed=embed)

    @stats.command()
    async def enhance(self, ctx, stat_name, amount=1):
        users = await get_human_stats()
        if users[str(ctx.author.id)]["AttrPoints"] >= amount:
            if stat_name.lower() == "maxhp":
                stats = ["MaxHP", 60]
                await ctx.reply(f"Successfully enhanced your Max Health!")
            elif stat_name.lower() == "maxchakra":
                stats = ["MaxEnergy", 45]
                await ctx.reply(f"Successfully enhanced your Max Chakra!")
            elif stat_name.lower() == "pdmg":
                stats = ["PDMG", 5]
                await ctx.reply(f"Successfully enhanced your Physical Damage!")
            else:
                await ctx.reply(f"Invalid name! Please try again!")
                return
            
            await heal_human(ctx.author, stats[1]*amount, stats[0])
            await heal_human(ctx.author, -1*amount, "AttrPoints")
        else:
            await ctx.reply(f"You don't have that much attribute points!")
        
        



    @commands.command()
    async def eat(self, ctx, item, amount=1):
        if item == None:
            return 
        else:

            res = await eat_this(ctx.author, item, amount)

            if not res[0]:
                if res[2] == 1:
                    await ctx.reply(f"The item does not exist or maybe it's not a food!")
                elif res[2] == 2:
                    await ctx.reply(f"You don't have that {res[1]}")
                elif res[2] == 3:
                    await ctx.reply(f"You don't have {amount} {res[1]}!")
            else:
                await ctx.reply(f"You ate {res[3]}x {res[1]} and healed up {res[2]}")







class Duel(commands.Cog):

    def __init__(self, client:commands.Bot):
        self.client = client
        self.effects = []
        self.spawn_channel = []
        self.effect_loop.start()
        self.boss_spawn.start()

    


    async def cog_unload(self):
        self.effect_loop.cancel()
        self.boss_spawn.cancel()


    @tasks.loop(seconds=15)
    async def boss_spawn(self):
        for guild in self.client.guilds:
            for things in self.spawn_channel:
                if things["guild_id"] == guild.id:
                    channel = self.client.get_guild(int(things["guild_id"])).get_channel(int(things["channel_id"]))
                    list_of_boss = []
                    with open(scroll_data_json_file, "r") as json_file:
                        data = json.load(json_file)
                        data = (data)
                        for items in data:
                            if items["mode"] == "BOSS/Quests":
                                list_of_boss.append(items["itemname"])
                                continue
                            else:
                                pass
                    selected_boss = random.choice(list_of_boss)
                    attributes = await get_all_attributes(selected_boss, scroll_data_json_file, Key=["itemname", "img", "level", "stats", "rarity"])
                    embed = discord.Embed(
                        title=f"{attributes[0]} has appeared!",
                        description="This is a boss! A Boss has high HP and High Chakra and once defeated, it drops insane rewards! To battle the boss click the button below!"
                    )
                    embed.set_image(url=attributes[1])
                    embed.add_field(name="Stats:", value=f"⬆️ **Level -** {attributes[2]}\n❤️ **HP -** {attributes[3]['HP']}\n⚡ **Chakra -** {attributes[3]['chakra']}\n✨ **Rarity -** {attributes[4]}")
                    the_view = View()
                    the_button = Button(label="Challenge", style=discord.ButtonStyle.danger, emoji="⚔️")
                    the_view.add_item(the_button)                    
                    
                    async def startcall(interaction):
                        await interaction.response.send_message("The Duel is going to start!", ephemeral=True)
                        await self.boss_fight(channel, interaction.user, attributes[0])
                        the_view.stop()

                    the_button.callback = startcall
                    await channel.send(embed=embed, view=the_view)
                    
                    
                    break
                else:
                    pass







    @tasks.loop(seconds=3)
    async def effect_loop(self):
        for thing in self.effects:
            try:
                if thing["count"] != 0:
                    if thing["type"][2].startswith("Debuff"):
                        if thing["type"][2].endswith("Reduce"):
                            await duel_stats_change(thing["victim"], random.randint(int(thing["amount"]/2), int(thing["amount"])), "HP")
                            thing["count"] -= 1
                            continue
                        elif thing["type"][2].endswith("Stun"):
                            await duel_stats_change(thing["victim"], random.randint(int(thing["amount"]/2), int(thing["amount"])), "Energy")
                            thing["count"] -= 1
                            continue
                    elif thing["type"][2].startswith("Buff"):
                        if thing["type"][2].endswith("HP"):
                            await heal_human(thing["user"], random.randint(1, int(thing["amount"])), "HP")
                            thing["count"] -= 1
                            continue
                        elif thing["type"][2].endswith("Armor"):
                            res = await duel_stats_change(thing["user"], random.randint(int(thing["amount"]/2), int(thing["amount"])), "Energy")
                            if res == 0:
                                thing["count"] = 0
                            else:
                                thing["count"] -= 1
                            continue
                        elif thing["type"][2].endswith("Transform"):
                            users = await get_human_stats()
                            if thing["count"] == 200:
                                await heal_human(thing["user"], int(20 * (int(users[str(thing["user"].id)]["MaxHP"])/100)), "MaxHP")
                            res = await duel_stats_change(thing["user"], random.randint(int(thing["amount"]/2), int(thing["amount"])), "Energy")
                            if res == 0:
                                users = await get_human_stats()

                                value = int(users[str(thing["user"].id)]["MaxHP"]) + int(users[str(thing["user"].id)]["MaxHP"]/100 * -16.666666666666664)
                                users[str(thing["user"].id)]["MaxHP"] = value

                                with open(human_json_file, "w") as json_file:
                                    json.dump(users, json_file, indent=1)
 
                                thing["count"] = 0
                            else:
                                thing["count"] -= 1
                                if thing["count"] == 0:
                                    users = await get_human_stats()

                                    value = int(users[str(thing["user"].id)]["MaxHP"]) + int(users[str(thing["user"].id)]["MaxHP"]/100 * -16.666666666666664)
                                    users[str(thing["user"].id)]["MaxHP"] = value

                                    with open(human_json_file, "w") as json_file:
                                        json.dump(users, json_file, indent=1)
                            continue
                    
                else:
                    self.effects.remove({
                        "user": thing["user"],
                        "victim": thing["victim"],
                        "amount": thing["amount"],
                        "type": thing["type"],
                        "count": thing["count"]
                    })    
                    continue
            except:
                break
    


    class DefaultView(View):

        def __init__(self, ctx):
            super().__init__(timeout=40)
            self.ctx = ctx


        @discord.ui.button(label="Accept", style=discord.ButtonStyle.blurple)
        async def button_callback(self, interaction, button):
            await interaction.response.send_message(f"Get back to {self.ctx.channel.mention}")
            self.stop()




    class Make_Button(Button):

        

        def __init__(self, ctx, outer_instance ,label="Click here!", style=discord.ButtonStyle.blurple, disabled=True, emoji=None, custom_id=None, ability = None, victim = None, view = None):
            super().__init__(label=label, style=style, disabled=disabled, emoji=emoji, custom_id=custom_id)
            self.ability = ability
            self.victim = victim
            self.ctx = ctx
            self.outer_instance = outer_instance
            self.main_view = view
            self.quit = False
            self.pressed = False



        
        async def callback(self, interaction):
            if self.ability == "Quit":
                self.quit = True
                try:
                    await interaction.response.send_message(f"Get back to {self.ctx.channel.mention}")
                except:
                    await interaction.response.send_message(f"Get back to {self.ctx.mention}")
            elif self.ability == "Recharge":
                users = await get_human_stats()
                user = interaction.user       
                max_chakra = int(users[str(user.id)]["MaxEnergy"])  
                chakra = random.randint(0, max_chakra/2)
                if (int(users[str(user.id)]["Energy"]) + chakra) > max_chakra:
                    chakra = max_chakra - int(users[str(user.id)]["Energy"])
                await duel_stats_change(user, -1*chakra, "Energy")
                self.pressed = ["Recharge Chakra", chakra, 0, "*No effects inflicted*"]
                try:
                    await interaction.response.send_message(f"⚡{chakra} recharged!\nGet back to {self.ctx.channel.mention}")
                except:
                    await interaction.response.send_message(f"⚡{chakra} recharged!\nGet back to {self.ctx.mention}")
            elif self.ability == "Backpack":
                users = await get_inventory_data()
                user = interaction.user
                menu_view = View()
                potion = Select(
                    placeholder="Select a potion to consume!",
                    options=[])
                t = 0
                for things in users[str(user.id)]["Backpack"]:
                    if things["mode"] == "Shop/Potion" and things["amount"] > 0:
                        potion.add_option(label=things["item"], value=things["item"], emoji=emoji.emojize(things["emoji"]))
                        t = 1
                        continue
                    else:
                        pass
                if t == 0:
                    users = await get_human_stats()
                    dmg = users[str(interaction.user.id)]["PDMG"]
                    chakra = 0
                    dmg = random.randint(int(dmg/2), int(dmg))
                    await duel_stats_change(self.victim, dmg, "HP")
                    await duel_stats_change(interaction.user, chakra, "Energy")
                    self.pressed = ["Physical Damage", chakra, dmg, "*No effects inflicted*"]
                    await interaction.response.send_message(f"You do not have any items in your backpack! Physical Damage has been choosed instead.\nGet back to {self.ctx.channel.mention}")
                else:
                    menu_view.add_item(potion)
                    await interaction.response.send_message(view=menu_view)        

                    async def startcall(interaction):
                        attributes = await get_all_attributes(potion.values[0], items_json_file, Key=["mode", "value"])
                        for things in self.outer_instance.effects:
                            if things["user"] == interaction.user and things["victim"] == self.victim and things["type"] == [attributes[1][0], attributes[1][1], attributes[1][2]]:
                                self.outer_instance.effects.remove({
                                    "user": things["user"],
                                    "victim": things["victim"],
                                    "amount": things["amount"],
                                    "type": things["type"],
                                    "count": things["count"]
                                })

                            else:
                                pass
                                    

                            break
                    
                        self.outer_instance.effects.append({
                            "user": interaction.user,
                            "victim": self.victim,
                            "amount": attributes[1][3],
                            "type": [attributes[1][0], attributes[1][1], attributes[1][2]],
                            "count": attributes[1][4]
                        })

                        users = await get_inventory_data()
                        index = 0
                        for things in users[str(interaction.user.id)]["Backpack"]:
                            if things["item"] == potion.values[0]:
                                users[str(interaction.user.id)]["Backpack"][index]["amount"] -= 1
                        
                                with open(inventory_json_file, "w") as json_file:
                                    json.dump(users, json_file, indent=1)

                                break
                            else:
                                pass

                        self.pressed = [f"*Consumed {potion.values[0]}*", 0, 0, attributes[1][0]]
                        await interaction.response.send_message(f"Get back to {self.ctx.channel.mention}")
                        self.main_view.stop()

                    potion.callback = startcall
                
                

            elif self.ability == "PDMG":
                users = await get_human_stats()
                dmg = users[str(interaction.user.id)]["PDMG"]
                chakra = 0
                
        
                try:
                    dmg = random.randint(int(dmg/2), int(dmg))
                    await duel_stats_change(self.victim, dmg, "HP")
                    await duel_stats_change(interaction.user, chakra, "Energy")
                    self.pressed = ["Physical Damage", chakra, dmg, "*No effects inflicted*"]
                    await interaction.response.send_message(f"Get back to {self.ctx.channel.mention}")
                except:
                    try:
                        self.victim = int(self.victim)
                        DMG = random.randint(int(dmg/2), int(dmg))
                        if self.victim - DMG < 0:
                            self.victim = 0
                        else:
                            self.victim -= DMG
                        await duel_stats_change(interaction.user, chakra, "Energy")
                        self.pressed = ["Physical Damage", chakra, dmg, "*No effects inflicted*"]
                        try:
                            await interaction.response.send_message(f"Get back to {self.ctx.channel.mention}")
                        except:
                            await interaction.response.send_message(f"Get back to {self.ctx.mention}")
                    except:
                        await interaction.response.send_message("Something went wrong!")
            else:
                attributes = await get_all_attributes(self.ability[0], scroll_data_json_file, Key=["ability"])
                for ability in attributes[0]:
                    if ability["ability_name"] == self.ability[1]:
                        ability_name = ability["ability_name"]
                        dmg = ability["dmg"]
                        chakra = ability["chakra"]
                        repeat = ability["repeat"]
                        effect_ignore = ability["effect_ignore"]
                        effect_break = ability["effect_break"]
                        break
                    else:
                        pass
                try:
                    ignore = False
                    armor = False
                    if effect_ignore:
                        for things in self.outer_instance.effects:
                            if things["user"] == self.victim and things["victim"] == interaction.user:
                                if things["type"][0] in effect_ignore:
                                    self.pressed = [f"~~{ability_name}~~", chakra, 0, f"*Nullified by {things['type'][0]}*"]
                                    ignore = True
                                    break
                                else:
                                    if things["type"][2] == "Buff/Armor":
                                        armor = True
                                        continue
                                    else:
                                        pass
                            else:
                                pass
                        
                    if ignore == False:
                        break_armor = False
                        if effect_break:
                            for things in self.outer_instance.effects:
                                if things["user"] == self.victim and things["victim"] == interaction.user:
                                    if things["type"][0] in effect_break:
                                        self.outer_instance.effects.remove({
                                            "user": things["user"],
                                            "victim": things["victim"],
                                            "amount": things["amount"],
                                            "type": things["type"],
                                            "count": things["count"]
                                        })
                                        self.pressed = [f"{ability_name}", chakra, 0, f"*Broke {things['type'][0]}*"]
                                        break_armor = True
                                        break
                                    else:
                                        if things["type"][2] == "Buff/Armor":
                                            armor = True
                                            continue
                                        else:
                                            pass
                        
                        if break_armor == False:
                            dmg = random.randint(int(dmg/2), int(dmg))
                           

                            if repeat:
                                for things in self.outer_instance.effects:
                                    if things["user"] == interaction.user and things["victim"] == self.victim and things["type"] == [repeat[0], repeat[1], repeat[2]]:
                                        self.outer_instance.effects.remove({
                                            "user": things["user"],
                                            "victim": things["victim"],
                                            "amount": things["amount"],
                                            "type": things["type"],
                                            "count": things["count"]
                                        })
                                        if things["type"][2] == "Buff/Armor":
                                            armor = True
                                    else:
                                        if things["user"] == self.victim and things["victim"] == interaction.user:
                                            if things["type"][2] == "Buff/Armor":
                                                armor = True
                                                continue
                                            else:
                                                pass
                                        else:
                                            pass
                                            
                                        

                                self.outer_instance.effects.append({
                                    "user": interaction.user,
                                    "victim": self.victim,
                                    "amount": repeat[3],
                                    "type": [repeat[0], repeat[1], repeat[2]],
                                    "count": repeat[4]
                                })

                                

                                if armor:
                                    dmg = int(await percentage_change(dmg, int(random.randint(10, 80))))


                                self.pressed = [ability_name, chakra, dmg, repeat[0]]
                            else:
                                self.pressed  = [ability_name, chakra, dmg, "*No effects inflicted*"]

                        
        
                            await duel_stats_change(self.victim, dmg , "HP")
                    

        
                    await duel_stats_change(interaction.user, chakra, "Energy")
                    await interaction.response.send_message(f"Get back to {self.ctx.channel.mention}")
                        
                except:
                    try:
                        self.victim = int(self.victim)
                        DMG = random.randint(int(dmg/2), int(dmg))
                        if self.victim - DMG < 0:
                            self.victim = 0
                        else:
                            self.victim -= DMG
                        await duel_stats_change(interaction.user, chakra, "Energy")
                        self.pressed = [ability_name, chakra, DMG, "*No effects inflicted*"] 
                        try:
                            await interaction.response.send_message(f"Get back to {self.ctx.channel.mention}")
                        except:
                            await interaction.response.send_message(f"Get back to {self.ctx.mention}")
                    except:

                        await interaction.response.send_message("Something went wrong!")

            
            self.main_view.stop()


    
    @commands.group()
    async def config(self, ctx):
        if ctx.invoked_subcommand is None:
            ...
        
    @config.command()
    @commands.has_permissions(manage_channels=True)
    async def spawn(self, ctx, channel_id):
        res = self.client.get_guild(int(ctx.guild.id)).get_channel(int(channel_id))
        if res == None:
            await ctx.reply("Invalid channel!")
        else:
            for guild in self.spawn_channel:
                if guild["guild_id"] == ctx.guild.id:
                    self.spawn_channel.remove({"guild_id": guild["guild_id"], "channel_id": guild["channel_id"]})
                else:
                    pass
        
            self.spawn_channel.append({"guild_id": ctx.guild.id, "channel_id": channel_id})
            await ctx.send("Configuring Boss Spawning channel")




    @commands.command()
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def duel(self, ctx, user: discord.Member):
        if user == ctx.author:
            self.duel.reset_cooldown(ctx)
            return
        loop = True
        view = self.DefaultView(ctx)
        await user.send(f"Yo! {ctx.author.display_name} asked you for a duel, click the button below to enter the duel!", view=view)
        await ctx.send("Request sent!")
        res = await view.wait()
        if res:
            await ctx.send("The user didn't respond")
        else:
            ALL_STUFF = await create_duel(ctx.author, user)
            round = 1
            while loop is True:
                embed = discord.Embed(
                    title=f"{ctx.author.global_name} vs {user.global_name} [Round {round}]",
                    description= "Each player must use their ability simultaneously. Only players will be visible to use the abilities and each abilities cost Chakra, if you run out of chakra you will be unable to use any abilities until it recharges!",
                    color = 0xaa5bfc,
                    timestamp= datetime.utcnow()                
                )

                view2 = View()
                view3 = View()
               




                health_bar = await make_bars(ctx.author, "HP", "MaxHP", "🟥", "⬛", 6)
                energy_bar = await make_bars(ctx.author, "Energy", "MaxEnergy", "🟦", "⬛", 5)

                FIELD_VALUE = f"HP {health_bar}\nChakra {energy_bar}\n\n"

                for abilities in ALL_STUFF[0][4]:
                    FIELD_VALUE = FIELD_VALUE + f"{abilities[1]} {abilities[0]} | {abilities[3]}\n"

                FIELD_VALUE = FIELD_VALUE + f"\n**Buffs/Debuffs**\n"

                for players in self.effects:  
                    if players['type'][2].startswith("Debuff"):
                        if ctx.author == players["victim"] and user == players["user"]:
                            FIELD_VALUE =  FIELD_VALUE + f"{players['type'][1]} {players['type'][0]}\n"
                            continue
                    else:
                        if ctx.author == players["user"] and user == players["victim"]:
                            FIELD_VALUE =  FIELD_VALUE + f"{players['type'][1]} {players['type'][0]}\n"
                            continue

                if FIELD_VALUE.endswith("Debuffs**\n"):
                    FIELD_VALUE = FIELD_VALUE + f"*No Effects*\n"
    

                if round == 1:
                    pass
                
                else:
                    FIELD_VALUE = FIELD_VALUE + f"\n**Last Round**\n"
                    FIELD_VALUE = FIELD_VALUE + f"⭐ **Ability:** {user1_last_move[0]}\n💥 **Damage: ** {user1_last_move[2]} \n⚡ **Chakra:** {user1_last_move[1]}\n🍻 **Effect:** {user1_last_move[3]}\n"


                embed.add_field(name=f"{ctx.author.display_name} **[{ALL_STUFF[0][2]}]**", value=FIELD_VALUE)

                health_bar = await make_bars(user, "HP", "MaxHP", "🟥", "⬛", 6)
                energy_bar = await make_bars(user, "Energy", "MaxEnergy", "🟦", "⬛", 5)

                FIELD_VALUE = f"HP {health_bar}\nChakra {energy_bar}\n\n"

        

                for abilities in ALL_STUFF[1][4]:
                    FIELD_VALUE = FIELD_VALUE + f"{abilities[1]} {abilities[0]} | {abilities[3]}\n"


                FIELD_VALUE = FIELD_VALUE + f"\n**Buffs/Debuffs**\n"

                for players in self.effects:  
                    if players['type'][2].startswith("Debuff"):
                        if user == players["victim"] and ctx.author == players["user"]:
                            FIELD_VALUE =  FIELD_VALUE + f"{players['type'][1]} {players['type'][0]}\n"
                            continue
                    else:
                        if user == players["user"] and ctx.author == players["victim"]:
                            FIELD_VALUE =  FIELD_VALUE + f"{players['type'][1]} {players['type'][0]}\n"
                            continue


                if FIELD_VALUE.endswith("Debuffs**\n"):
                    FIELD_VALUE = FIELD_VALUE + f"*No Effects*\n"

                if round == 1:
                    pass
                else:
                    FIELD_VALUE = FIELD_VALUE + f"\n**Last Round**\n"
                    FIELD_VALUE = FIELD_VALUE + f"⭐ **Ability:** {user2_last_move[0]}\n💥 **Damage: ** {user2_last_move[2]} \n⚡ **Chakra:** {user2_last_move[1]}\n🍻 **Effect:** {user2_last_move[3]}\n"



                embed.add_field(name=f"{user.display_name} **[{ALL_STUFF[1][2]}]**", value=FIELD_VALUE)
                embed.add_field(name="\n", value="\n", inline=False)
                embed.set_footer(icon_url=("https://media.discordapp.net/attachments/1126174753359679498/1148507348835520562/e4ab08280ed1f76ddba1705b5852d8e1.png?width=602&height=602"), text= f"{ctx.author.global_name} vs {user.global_name}")
                await ctx.send(embed=embed)

                await asyncio.sleep(5)
                
                users = await get_human_stats()
                msg = f"⚔️ Attack:\nDamage - {users[str(ctx.author.id)]['PDMG']}\nChakra - 0\n"
                button = self.Make_Button(ctx, outer_instance=self ,label="Attack", style=discord.ButtonStyle.green, emoji="⚔️", custom_id="Attack", ability="PDMG", disabled=False, victim=user, view=view2)
                view2.add_item(button)
                
                for abilities in ALL_STUFF[0][4]:
                    
                    if abilities[4] > ALL_STUFF[0][5]:
                        button = self.Make_Button(ctx, outer_instance=self ,label=abilities[0], style=discord.ButtonStyle.green, emoji=emoji.emojize(abilities[1]), custom_id=abilities[0], disabled=True, ability=[ALL_STUFF[0][2],abilities[0]], victim=user, view=view2)
                        view2.add_item(button)
                        msg = msg + f"{abilities[1]} {abilities[0]} - **Locked**:\nDamage - {abilities[2]}\nChakra - {abilities[3]}\n"
                    else:
                        if users[str(ctx.author.id)]["Energy"] < abilities[3]:
                            button = self.Make_Button(ctx, outer_instance=self ,label=abilities[0], style=discord.ButtonStyle.green, emoji=emoji.emojize(abilities[1]), custom_id=abilities[0], disabled=True, ability=[ALL_STUFF[0][2],abilities[0]], victim=user, view=view2)    
                            view2.add_item(button)
                            msg = msg + f"{abilities[1]} {abilities[0]} - **Low Chakra**:\nDamage - {abilities[2]}\nChakra - {abilities[3]}\n"
                        else:
                            button = self.Make_Button(ctx, outer_instance=self ,label=abilities[0], style=discord.ButtonStyle.green, emoji=emoji.emojize(abilities[1]), custom_id=abilities[0], disabled=False, ability=[ALL_STUFF[0][2],abilities[0]], victim=user, view=view2)    
                            view2.add_item(button)
                            msg = msg + f"{abilities[1]} {abilities[0]}:\nDamage - {abilities[2]}\nChakra - {abilities[3]}\n"

                button = self.Make_Button(ctx, outer_instance=self , label="Recharge", style=discord.ButtonStyle.primary, emoji="⚡", custom_id="Recharge", ability="Recharge", disabled=False, victim=ctx.author, view=view2)
                view2.add_item(button)
                button = self.Make_Button(ctx, outer_instance=self, label="Backpack", style=discord.ButtonStyle.primary, emoji="🎒", custom_id="Backpack", ability="Backpack", disabled=False, victim=user, view=view2)
                view2.add_item(button)
                button = self.Make_Button(ctx, outer_instance=self , label="Declare", style=discord.ButtonStyle.danger, emoji="🏳️", custom_id="Declare", ability="Quit", disabled=False, victim=ctx.author, view=view2)
                view2.add_item(button)
        
                

                msg = msg + "Choose an ability below to perform!"
                await ctx.author.send(msg,view=view2)
                
                

                msg = f"⚔️ Attack:\nDamage - {users[str(ctx.author.id)]['PDMG']}\nChakra - 0\n"
                button = self.Make_Button(ctx, outer_instance=self ,label="Attack", style=discord.ButtonStyle.green, emoji="⚔️", custom_id="Attack", ability="PDMG", disabled=False, victim=ctx.author, view=view3)
                view3.add_item(button)

                for abilities in ALL_STUFF[1][4]:
                    users = await get_human_stats()
                    if abilities[4] > ALL_STUFF[1][5]:
                        button = self.Make_Button(ctx,outer_instance=self , label=abilities[0], style=discord.ButtonStyle.green, emoji=emoji.emojize(abilities[1]), custom_id=abilities[0], disabled=True, ability=[ALL_STUFF[1][2],abilities[0]], victim=ctx.author, view=view3)
                        view3.add_item(button)
                        msg = msg + f"{abilities[1]} {abilities[0]} - **Locked**:\nDamage - {abilities[2]}\nChakra - {abilities[3]}\n"
                    else:
                        if users[str(user.id)]["Energy"] < abilities[3]:
                            button = self.Make_Button(ctx,outer_instance=self , label=abilities[0], style=discord.ButtonStyle.green, emoji=emoji.emojize(abilities[1]), custom_id=abilities[0], disabled=True, ability=[ALL_STUFF[1][2],abilities[0]], victim=ctx.author, view=view3)    
                            view3.add_item(button)
                            msg = msg + f"{abilities[1]} {abilities[0]} - **Low Chakra**:\nDamage - {abilities[2]}\nChakra - {abilities[3]}\n"
                        else:
                            button = self.Make_Button(ctx,outer_instance=self , label=abilities[0], style=discord.ButtonStyle.green, emoji=emoji.emojize(abilities[1]), custom_id=abilities[0], disabled=False, ability=[ALL_STUFF[1][2],abilities[0]], victim=ctx.author, view=view3)    
                            view3.add_item(button)
                            msg = msg + f"{abilities[1]} {abilities[0]}:\nDamage - {abilities[2]}\nChakra - {abilities[3]}\n"

                button = self.Make_Button(ctx,outer_instance=self , label="Recharge", style=discord.ButtonStyle.primary, emoji="⚡", custom_id="Recharge", ability="Recharge", disabled=False, victim=user, view=view3)
                view3.add_item(button)
                button = self.Make_Button(ctx, outer_instance=self, label="Backpack", style=discord.ButtonStyle.primary, emoji="🎒", custom_id="Backpack", ability="Backpack", disabled=False, victim=ctx.author, view=view3)
                view3.add_item(button)
                button = self.Make_Button(ctx,outer_instance=self , label="Declare", style=discord.ButtonStyle.danger, emoji="🏳️", custom_id="Declare", ability="Quit", disabled=False, victim=user, view=view3)
                view3.add_item(button)
                


                msg = msg + "Choose an ability below to perform!"
                await user.send(msg,view=view3)

                res = await view2.wait()
                res2 = await view3.wait()
                if res == False or res == True and res2 == True or res2 == False:
                    if [x for x in view2.children if x.custom_id][int(len([x for x in view2.children if x.custom_id])) - 1].quit == True:
                        loop = [None, ctx.author, user]
                    elif [x for x in view3.children if x.custom_id][int(len([x for x in view3.children if x.custom_id])) - 1].quit == True:
                        loop = [None, user, ctx.author]
                    else:
                        users = await get_human_stats()
                        if users[str(ctx.author.id)]["HP"] == 0:
                            for buttons in [x for x in view3.children if x.custom_id]:
                                if buttons.pressed:
                                    final_move = buttons.pressed
                                    break
                                else:
                                    pass
                            loop = [False, user, ctx.author, final_move]
                        elif users[str(user.id)]["HP"] == 0:
                            for buttons in [x for x in view2.children if x.custom_id]:
                                if buttons.pressed:
                                    final_move = buttons.pressed
                                    break
                                else:
                                    pass
                            loop = [False, ctx.author, user, final_move]
                        else:
                            for buttons in [x for x in view2.children if x.custom_id]:
                                if buttons.pressed:
                                    user1_last_move = buttons.pressed
                                    break
                                else:
                                    pass

                            for buttons in [x for x in view3.children if x.custom_id]:
                                if buttons.pressed:
                                    user2_last_move = buttons.pressed
                                    break
                                else:
                                    pass
                            round += 1



            if loop[0] == False:
                await ctx.send(f"{loop[1].mention} used {loop[3][0]} which lead them to victory against {loop[2].mention}")

                users = await get_human_stats()
                loser_lvl = int(users[str(loop[2].id)]["Level"])
                winner_lvl = int(users[str(loop[1].id)]["Level"])
                diff = (loser_lvl - winner_lvl)/winner_lvl
                exp = ((diff/10)*loser_lvl)*5000 + 250
                
                if str(exp).startswith("-"):
                    exp = -1*int(exp)
                else:
                    exp = exp
                
                await heal_human(loop[1], exp, "exp")

                users = await get_scroll_data()
                index = 0
                lvl = 0
                for thing in users[str(loop[1].id)]["Scrolls"]:
                    active = thing["active"]
                    if active is True:
                        lvl = thing["Level"]
                        old_exp = thing["exp"]
                        users[str(loop[1].id)]["Scrolls"][index]["exp"] += exp*4

                        with open(scroll_json_file, "w") as json_file:
                            json.dump(users, json_file, indent=1)

                        break
                    else:
                        index += 1
                        pass

                

                if (old_exp + exp) >= math.ceil(6* (lvl ** 4) / 2.5):
                    index = 0
                    for thing in users[str(loop[1].id)]["Scrolls"]:
                        active = thing["active"]
                        lvl = thing["Level"]
                        if active == True:
                            
                            temp_level = lvl
                            while True:
                                if int(old_exp + exp) >= math.ceil(6* (temp_level ** 4) / 2.5):
                                    temp_level += 1
                                else:
                                    break
                            users[str(loop[1].id)]["Scrolls"][index]["Level"] = temp_level

                            with open(scroll_json_file, "w") as json_file:
                                json.dump(users, json_file, indent=1)
                            
                            await ctx.reply(f"Your fruit leveled up! from {lvl} to {temp_level}")
                            break
                        else:
                            index += 1
                            pass


            elif loop[0] == None:
                await ctx.send(f"{loop[1].mention} declared the battle! and congrats {loop[2].mention}!")

                users = await get_human_stats()
                loser_lvl = int(users[str(loop[2].id)]["Level"])
                winner_lvl = int(users[str(loop[1].id)]["Level"])
                diff = (loser_lvl - winner_lvl)/winner_lvl
                exp = ((diff/10)*loser_lvl)*500
                
                if loser_lvl > winner_lvl:
                    exp = exp
                else:
                    exp = -1*exp
                
                await heal_human(loop[1], (exp/2), "exp")

                users = await get_scroll_data()
                index = 0
                lvl = 0
                for thing in users[str(loop[1].id)]["Scrolls"]:
                    active = thing["active"]
                    if active == True:
                        lvl = thing["Level"]
                        old_exp = thing["exp"]
                       
                        users[str(loop[1].id)]["Scrolls"][index]["exp"] += exp

                        with open(scroll_json_file, "w") as json_file:
                            json.dump(users, json_file, indent=1)

                        break
                    else:
                        index += 1
                        pass

                

                if (old_exp + exp) >= math.ceil(6* (lvl ** 4) / 2.5):
                    index = 0
                    for thing in users[str(loop[1].id)]["Scrolls"]:
                        active = thing["active"]
                        lvl = thing["Level"]
                        if active == True:
                            
                            temp_level = lvl
                            while True:
                                if int(old_exp + exp) >= math.ceil(6* (temp_level ** 4) / 2.5):
                                    temp_level += 1
                                else:
                                    break
                            users[str(loop[1].id)]["Scrolls"][index]["Level"] = temp_level

                            with open(scroll_json_file, "w") as json_file:
                                json.dump(users, json_file, indent=1)
                            
                            await ctx.reply(f"Your fruit leveled up! from {lvl} to {temp_level}")
                            break

                        else:
                            index += 1
                            pass


    @commands.command()
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def npcfight(self, ctx, npc_name):
        attributes = await get_all_attributes(npc_name, scroll_data_json_file, Key=["itemname"])
        if attributes != []:
           attributes = attributes 
        else:
            await ctx.reply(f"Couldn't find npc called '{npc_name}'")
            self.npcfight.reset_cooldown(ctx)
            return
        loop = True
        npc_current_health = None
        round = 1
        ALL_STUFF = await create_brawl_npc(ctx.author, npc_name)
        while loop is True:
            embed = discord.Embed(
                title=f"{ctx.author.display_name} vs {attributes[0]} [Round {round}]",
                description= "This is a npc battle! The Player can make moves as usual and can't use it if they ran out of chakra. But NPCS can use any moves at anytime without chakra cost. Sadly Players can not inflict effects to NPCS and so do they.",
                color=0xaa5bfc,
                timestamp= datetime.utcnow()
            )

            view2 = View()

            health_bar = await make_bars(ctx.author, "HP", "MaxHP", "🟥", "⬛", 6)
            energy_bar = await make_bars(ctx.author, "Energy", "MaxEnergy", "🟦", "⬛", 5)

            FIELD_VALUE = f"HP {health_bar}\nChakra {energy_bar}\n\n"
            for abilities in ALL_STUFF[0][4]:
                FIELD_VALUE = FIELD_VALUE + f"{abilities[1]} {abilities[0]} | {abilities[3]}\n"

            if round == 1:
                    pass
            else:
                FIELD_VALUE = FIELD_VALUE + f"\n**Last Round**\n"
                FIELD_VALUE = FIELD_VALUE + f"⭐ **Ability:** {user1_last_move[0]}\n💥 **Damage: ** {user1_last_move[2]} \n⚡ **Chakra:** {user1_last_move[1]}\n🍻 **Effect:** {user1_last_move[3]}\n"



            embed.add_field(name=f"{ctx.author.display_name} **[{ALL_STUFF[0][2]}]**", value=FIELD_VALUE)

            # Health Bar
            if npc_current_health is None: 
                npc_current_health = ALL_STUFF[1][6]["HP"]
            else:
                npc_current_health = npc_current_health
    
            health_bar = await make_bars(ctx.author, npc_current_health, ALL_STUFF[1][6]["HP"], "🟥", "⬛", 6)
            # Static bar for energy bar
            energy_bar = await make_bars(ctx.author, ALL_STUFF[1][6]["chakra"], ALL_STUFF[1][6]["chakra"], "🟨", "⬛", 5)
            # Add abilities in the embed
            FIELD_VALUE = f"HP {health_bar}\nChakra {energy_bar}\n\n"
            for abilities in ALL_STUFF[1][4]:
                FIELD_VALUE = FIELD_VALUE + f"{abilities['emoji']} {abilities['ability_name']} | {abilities['chakra']}\n"

            if round == 1:
                    pass
            else:
                FIELD_VALUE = FIELD_VALUE + f"\n**Last Round**\n"
                FIELD_VALUE = FIELD_VALUE + f"⭐ **Ability:** {user2_last_move[0]}\n💥 **Damage: ** {user2_last_move[2]} \n⚡ **Chakra:** {user2_last_move[1]}\n🍻 **Effect:** {user2_last_move[3]}\n"

            
            embed.add_field(name=f"{attributes[0]}", value=FIELD_VALUE)
            # Send the embed
            embed.add_field(name="\n", value="\n", inline=False)
            embed.set_footer(icon_url=(ctx.author.display_avatar), text= f"C'mon {ctx.author.global_name}!")
            await ctx.send(embed=embed)
            # Wait 5 seconds and send ability wheel in the DM
            await asyncio.sleep(5)

            users = await get_human_stats()
            msg = f"⚔️ Attack:\nDamage - {users[str(ctx.author.id)]['PDMG']}\nChakra - 0\n"
            button = self.Make_Button(ctx,outer_instance=self , label="Attack", style=discord.ButtonStyle.green, emoji="⚔️", custom_id="Attack", ability="PDMG", disabled=False, victim=npc_current_health, view=view2)
            view2.add_item(button)
                
            for abilities in ALL_STUFF[0][4]:
                if abilities[4] > ALL_STUFF[0][5]:
                    button = self.Make_Button(ctx,outer_instance=self , label=abilities[0], style=discord.ButtonStyle.green, emoji=emoji.emojize(abilities[1]), custom_id=abilities[0], disabled=True, ability=[ALL_STUFF[0][2],abilities[0]], victim=npc_current_health, view=view2)
                    view2.add_item(button)
                    msg = msg + f"{abilities[1]} {abilities[0]} - **Locked**:\nDamage - {abilities[2]}\nChakra - {abilities[3]}\n"
                else:
                    if users[str(ctx.author.id)]["Energy"] < abilities[3]:
                        button = self.Make_Button(ctx,outer_instance=self , label=abilities[0], style=discord.ButtonStyle.green, emoji=emoji.emojize(abilities[1]), custom_id=abilities[0], disabled=True, ability=[ALL_STUFF[0][2],abilities[0]], victim=npc_current_health, view=view2)    
                        view2.add_item(button)
                        msg = msg + f"{abilities[1]} {abilities[0]} - **Low Chakra**:\nDamage - {abilities[2]}\nChakra - {abilities[3]}\n"
                    else:
                        button = self.Make_Button(ctx,outer_instance=self , label=abilities[0], style=discord.ButtonStyle.green, emoji=emoji.emojize(abilities[1]), custom_id=abilities[0], disabled=False, ability=[ALL_STUFF[0][2],abilities[0]], victim=npc_current_health, view=view2)    
                        view2.add_item(button)
                        msg = msg + f"{abilities[1]} {abilities[0]}:\nDamage - {abilities[2]}\nChakra - {abilities[3]}\n"

            button = self.Make_Button(ctx,outer_instance=self , label="Recharge", style=discord.ButtonStyle.primary, emoji="⚡", custom_id="Recharge", ability="Recharge", disabled=False, victim=npc_current_health, view=view2)
            view2.add_item(button)
            button = self.Make_Button(ctx,outer_instance=self , label="Declare", style=discord.ButtonStyle.danger, emoji="🏳️", custom_id="Declare", ability="Quit", disabled=False, victim=npc_current_health, view=view2)
            view2.add_item(button)
            

            msg = msg + "Choose an ability below to perform!"
            await ctx.author.send(msg,view=view2)

            # Await for the ability wheel response and randomly choose an ability from the NPC's ability wheel
            set_of_abilities = []
            for abilities in ALL_STUFF[1][4]:
                set_of_abilities.append([abilities["ability_name"], abilities["dmg"]])
            ability = random.choice(set_of_abilities)
            ability[1] = random.randint(int(ability[1]/2), int(ability[1]))
            await duel_stats_change(ctx.author, ability[1], "HP")

            # Change stats
            res = await view2.wait()
            if res is True or res is False:
                if [x for x in view2.children if x.custom_id][int(len([x for x in view2.children if x.custom_id])) - 1].quit == True:
                    loop = [None, ctx.author, attributes[0]]
                else:
                    users = await get_human_stats()
                    if users[str(ctx.author.id)]["HP"] == 0:
                        loop = [False, attributes[0], ctx.author]
                    else:
                        for index in range(0, len([x for x in view2.children if x.custom_id])):
                            if [x for x in view2.children if x.custom_id][index].victim <= 0:
                                loop = [False, ctx.author, attributes[0]]
                                break
                            else:
                                if [x for x in view2.children if x.custom_id][index].victim < npc_current_health:
                                    npc_current_health = [x for x in view2.children if x.custom_id][index].victim
                                    continue
                                else:
                                    pass

                                
                                for buttons in [x for x in view2.children if x.custom_id]:
                                    
                                    if buttons.pressed:
                                        user1_last_move = buttons.pressed
                                        break
                                    else:
                                        pass

                                user2_last_move = [ability[0], 0, ability[1], "*No effects inflicted*"]
                                
                                
                        round += 1
        if loop[0] == False:
            if loop[1] != ctx.author:
                await ctx.reply("You died!")
            else:
                exp = int(ALL_STUFF[1][5][0]/2)
                await ctx.reply(f"You defeated {loop[2]} and gained {exp}x EXP")
                await heal_human(ctx.author, exp, "exp")
                await update_bank(ctx.author, ALL_STUFF[1][5][1], "Chibucks")
                
                users = await get_human_stats()
                index = 0
                try:
                    for thing in users[str(loop[1].id)]["Quests"]:
                        if thing["NPC"] == loop[2]:
                            old_amt = thing["amount"]
                            if old_amt - 1 == 0:
                                attributes = await get_all_attributes(loop[2], scroll_data_json_file, Key=["rewards"])
                                await heal_human(ctx.author, int(attributes[0][0] * 8), "exp")
                                await update_bank(ctx.author, int(attributes[0][1] * 8), "Chibucks")

                                await ctx.reply(f"You have completed the **{thing['quest_name']}** Quest and got {int(attributes[0][1] * 8)} Chibucks <:chibucks:1141752496671445084> and {int(attributes[0][0] * 8)} EXP!\nPay a visit to `a!quests` again to challenge more quests")
                            
                                users[str(loop[1].id)]["Quests"][index]["amount"] -= 1

                                with open(human_json_file, "w") as json_file:
                                    json.dump(users, json_file, indent=1)
                                exp = (exp*2)*8
                                break
                            
                            elif (old_amt - 1) < 0:
                                pass
                            else:
                                users[str(loop[1].id)]["Quests"][index]["amount"] -= 1

                                with open(human_json_file, "w") as json_file:
                                    json.dump(users, json_file, indent=1)
                                exp = (exp*2)*8
                                break
                        else:
                            index += 1
                            pass
                except:
                    pass



                users = await get_scroll_data()
                index = 0
                lvl = 0
                for thing in users[str(loop[1].id)]["Scrolls"]:
                    active = thing["active"]
                    if active is True:
                        lvl = thing["Level"]
                        old_exp = thing["exp"]
                        users[str(loop[1].id)]["Scrolls"][index]["exp"] += exp

                        with open(scroll_json_file, "w") as json_file:
                            json.dump(users, json_file, indent=1)

                        break
                    else:
                        index += 1
                        pass
                
                if (old_exp + exp) >= math.ceil(6* (lvl ** 4) / 2.5):
                    
                    index = 0
                    for thing in users[str(loop[1].id)]["Scrolls"]:
                        active = thing["active"]
                        lvl = thing["Level"]
                        if active == True:
                            
                            temp_level = lvl
                            while True:
                                if int(old_exp + exp) >= math.ceil(6* (temp_level ** 4) / 2.5):
                                    temp_level += 1
                                else:
                                    break
                            users[str(loop[1].id)]["Scrolls"][index]["Level"] = temp_level

                            with open(scroll_json_file, "w") as json_file:
                                json.dump(users, json_file, indent=1)

                            await ctx.reply(f"Your fruit leveled up! from {lvl} to {temp_level}")
                            break
                        else:
                            index += 1
                            pass
                
                
                
        elif loop[0] == None:
            await ctx.reply("You left the battle!")


    async def boss_fight(self, channel, user, boss):
        await asyncio.sleep(2)
        loop = True
        npc_current_health = None
        npc_current_energy = None
        round = 1
        ALL_STUFF = await create_brawl_npc(user, boss)
        while loop is True:
            embed = discord.Embed(
                title=f"{user.global_name} vs {boss} [Round {round}]",
                description= "This is a npc battle! The Player can make moves as usual and can't use it if they ran out of chakra. But NPCS can use any moves at anytime without chakra cost. Sadly Players can not inflict effects to NPCS and so do they.",
                color=0xaa5bfc,
                timestamp=datetime.utcnow()
            )

            view2 = View()

            health_bar = await make_bars(user, "HP", "MaxHP", "🟥", "⬛", 6)
            energy_bar = await make_bars(user, "Energy", "MaxEnergy", "🟦", "⬛", 5)

            FIELD_VALUE = f"HP {health_bar}\nChakra {energy_bar}\n\n"
            for abilities in ALL_STUFF[0][4]:
                FIELD_VALUE = FIELD_VALUE + f"{abilities[1]} {abilities[0]} | {abilities[3]}\n"

            if round == 1:
                    pass
            else:
                FIELD_VALUE = FIELD_VALUE + f"\n**Last Round**\n"
                FIELD_VALUE = FIELD_VALUE + f"⭐ **Ability:** {user1_last_move[0]}\n💥 **Damage: ** {user1_last_move[2]} \n⚡ **Chakra:** {user1_last_move[1]}\n🍻 **Effect:** {user1_last_move[3]}\n"



            embed.add_field(name=f"{user} **[{ALL_STUFF[0][2]}]**", value=FIELD_VALUE)

            # Health Bar
            if npc_current_health is None: 
                npc_current_health = ALL_STUFF[1][6]["HP"]
                npc_current_energy = ALL_STUFF[1][6]["chakra"]
            else:
                npc_current_health = npc_current_health
                npc_current_energy = npc_current_energy
    
            health_bar = await make_bars(user, npc_current_health, ALL_STUFF[1][6]["HP"], "🟥", "⬛", 6)
            # Static bar for energy bar
            energy_bar = await make_bars(user, npc_current_energy, ALL_STUFF[1][6]["chakra"], "🟦", "⬛", 5)
            # Add abilities in the embed
            FIELD_VALUE = f"HP {health_bar}\nChakra {energy_bar}\n\n"
            for abilities in ALL_STUFF[1][4]:
                FIELD_VALUE = FIELD_VALUE + f"{abilities['emoji']} {abilities['ability_name']} | {abilities['chakra']}\n"

            if round == 1:
                    pass
            else:
                FIELD_VALUE = FIELD_VALUE + f"\n**Last Round**\n"
                FIELD_VALUE = FIELD_VALUE + f"⭐ **Ability:** {user2_last_move[0]}\n💥 **Damage: ** {user2_last_move[2]} \n⚡ **Chakra:** {user2_last_move[1]}\n🍻 **Effect:** {user2_last_move[3]}\n"

            
            embed.add_field(name=f"{boss}", value=FIELD_VALUE)
            # Send the embed
            embed.add_field(name="\n", value="\n", inline=False)
            embed.set_footer(icon_url=(user.display_avatar), text= f"C'mon {user.global_name}!")
            await channel.send(embed=embed)
            # Wait 5 seconds and send ability wheel in the DM
            await asyncio.sleep(5)

            users = await get_human_stats()
            msg = f"⚔️ Attack:\nDamage - {users[str(user.id)]['PDMG']}\nChakra - 0\n"
            button = self.Make_Button(channel,outer_instance=self , label="Attack", style=discord.ButtonStyle.green, emoji="⚔️", custom_id="Attack", ability="PDMG", disabled=False, victim=npc_current_health, view=view2)
            view2.add_item(button)
                
            for abilities in ALL_STUFF[0][4]:
                if abilities[4] > ALL_STUFF[0][5]:
                    button = self.Make_Button(channel,outer_instance=self , label=abilities[0], style=discord.ButtonStyle.green, emoji=emoji.emojize(abilities[1]), custom_id=abilities[0], disabled=True, ability=[ALL_STUFF[0][2],abilities[0]], victim=npc_current_health, view=view2)
                    view2.add_item(button)
                    msg = msg + f"{abilities[1]} {abilities[0]} - **Locked**:\nDamage - {abilities[2]}\nChakra - {abilities[3]}\n"
                else:
                    if users[str(user.id)]["Energy"] < abilities[3]:
                        button = self.Make_Button(channel,outer_instance=self , label=abilities[0], style=discord.ButtonStyle.green, emoji=emoji.emojize(abilities[1]), custom_id=abilities[0], disabled=True, ability=[ALL_STUFF[0][2],abilities[0]], victim=npc_current_health, view=view2)    
                        view2.add_item(button)
                        msg = msg + f"{abilities[1]} {abilities[0]} - **Low Chakra**:\nDamage - {abilities[2]}\nChakra - {abilities[3]}\n"
                    else:
                        button = self.Make_Button(channel,outer_instance=self , label=abilities[0], style=discord.ButtonStyle.green, emoji=emoji.emojize(abilities[1]), custom_id=abilities[0], disabled=False, ability=[ALL_STUFF[0][2],abilities[0]], victim=npc_current_health, view=view2)    
                        view2.add_item(button)
                        msg = msg + f"{abilities[1]} {abilities[0]}:\nDamage - {abilities[2]}\nChakra - {abilities[3]}\n"

            button = self.Make_Button(channel,outer_instance=self , label="Recharge", style=discord.ButtonStyle.primary, emoji="⚡", custom_id="Recharge", ability="Recharge", disabled=False, victim=npc_current_health, view=view2)
            view2.add_item(button)
            button = self.Make_Button(channel,outer_instance=self , label="Declare", style=discord.ButtonStyle.danger, emoji="🏳️", custom_id="Declare", ability="Quit", disabled=False, victim=npc_current_health, view=view2)
            view2.add_item(button)
            

            msg = msg + "Choose an ability below to perform!"
            await user.send(msg,view=view2)

            # Await for the ability wheel response and randomly choose an ability from the NPC's ability wheel
            if npc_current_energy <= 0:
                amount = random.randint(ALL_STUFF[1][6]["chakra"]/2, ALL_STUFF[1][6]["chakra"])
                ability = ["Recharge Chakra",0,amount]
                npc_current_energy += amount
            else:
                set_of_abilities = []
                if npc_current_energy < ALL_STUFF[1][6]["chakra"]:
                    set_of_abilities.append(["Recharge Chakra",0,ALL_STUFF[1][6]["chakra"]])
                else:
                    pass

                for abilities in ALL_STUFF[1][4]:
                    if abilities["chakra"] <= npc_current_energy:
                        set_of_abilities.append([abilities["ability_name"], abilities["dmg"], abilities["chakra"]])
                        continue
                    else:
                        pass
                ability = random.choice(set_of_abilities)
                if ability[0] == "Recharge Chakra":
                    amount = random.randint(ALL_STUFF[1][6]["chakra"]/2, ALL_STUFF[1][6]["chakra"])
                    if (amount+npc_current_energy) > ALL_STUFF[1][6]["chakra"]: 
                        npc_current_energy = amount
                        amount = ALL_STUFF[1][6]["chakra"]
                    else:
                        npc_current_energy += amount
                    ability = ["Recharge Chakra",0,amount]
                else:
                    ability[1] = random.randint(int(ability[1])/2, int(ability[1]))
                    await duel_stats_change(user, ability[1], "HP")
                    npc_current_energy -= ability[2]


            # Change stats
            res = await view2.wait()
            if res is True or res is False:
                if [x for x in view2.children if x.custom_id][int(len([x for x in view2.children if x.custom_id])) - 1].quit == True:
                    loop = [None, user, boss]
                else:
                    users = await get_human_stats()
                    if users[str(user.id)]["HP"] == 0:
                        loop = [False, boss, user]
                    else:
                        for index in range(0, len([x for x in view2.children if x.custom_id])):
                            if [x for x in view2.children if x.custom_id][index].victim <= 0:
                                loop = [False, user, boss]
                                break
                            else:
                                if [x for x in view2.children if x.custom_id][index].victim < npc_current_health:
                                    npc_current_health = [x for x in view2.children if x.custom_id][index].victim
                                    continue
                                else:
                                    pass

                                
                                for buttons in [x for x in view2.children if x.custom_id]:
                                    
                                    if buttons.pressed:
                                        user1_last_move = buttons.pressed
                                        break
                                    else:
                                        pass

                                user2_last_move = [ability[0], ability[2], ability[1], "*No effects inflicted*"]
                                
                                
                        round += 1

        if loop[0] == False:
            if loop[1] != user:
                await channel.send(f"{user.mention} died in the battle against {boss}!")
            else:
                exp = int(ALL_STUFF[1][5][0]/2)
                await channel.send(f"{user.mention} defeated {loop[2]} and gained {exp}x EXP")
                await heal_human(user, exp, "exp")
                await update_bank(user, ALL_STUFF[1][5][1], "Chibucks")
                
                users = await get_human_stats()
                index = 0
                try:
                    for thing in users[str(loop[1].id)]["Quests"]:
                        if thing["NPC"] == loop[2]:
                            old_amt = thing["amount"]
                            if (old_amt - 1) == 0:
                                attributes = await get_all_attributes(boss, scroll_data_json_file, Key=["rewards"])
                                await heal_human(user, attributes[0][0], "exp")
                                await update_bank(user, attributes[0][1], "Chibucks")

                                await channel.send(f"You have completed the **{thing['quest_name']}** Quest and got {attributes[0][1]} Chibucks <:chibucks:1141752496671445084> and {attributes[0][0]}x EXP!\nPay a visit to `a!quests` again to challenge more quests")
                            
                                users[str(loop[1].id)]["Quests"][index]["amount"] -= 1

                                with open(human_json_file, "w") as json_file:
                                    json.dump(users, json_file, indent=1)
                                exp = (exp*2)*8
                                break
                            
                            elif (old_amt - 1) < 0:
                                pass
                            else:
                                users[str(loop[1].id)]["Quests"][index]["amount"] -= 1

                                with open(human_json_file, "w") as json_file:
                                    json.dump(users, json_file, indent=1)
                                exp = (exp*2)*8
                                break
                        else:
                            index += 1
                            pass
                except:
                    pass



                users = await get_scroll_data()
                index = 0
                lvl = 0
                for thing in users[str(loop[1].id)]["Scrolls"]:
                    active = thing["active"]
                    if active is True:
                        lvl = thing["Level"]
                        old_exp = thing["exp"]
                        users[str(loop[1].id)]["Scrolls"][index]["exp"] += exp

                        with open(scroll_json_file, "w") as json_file:
                            json.dump(users, json_file, indent=1)

                        break
                    else:
                        index += 1
                        pass
                
                if (old_exp + exp) >= math.ceil(6* (lvl ** 4) / 2.5):
                    
                    index = 0
                    for thing in users[str(loop[1].id)]["Scrolls"]:
                        active = thing["active"]
                        lvl = thing["Level"]
                        if active == True:
                            
                            temp_level = lvl
                            while True:
                                if int(old_exp + exp) >= math.ceil(6* (temp_level ** 4) / 2.5):
                                    temp_level += 1
                                else:
                                    break
                            users[str(loop[1].id)]["Scrolls"][index]["Level"] = temp_level

                            with open(scroll_json_file, "w") as json_file:
                                json.dump(users, json_file, indent=1)

                            await channel.send(f"Your fruit leveled up! from {lvl} to {temp_level}")
                            break
                        else:
                            index += 1
                            pass
                
                
                
        elif loop[0] == None:
            await channel.send(f"{user.mention} left the battle against {boss}!")

        

    
class Quests(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client
              

    @commands.group(aliases = ["q"])
    async def quests(self, ctx):
        if ctx.invoked_subcommand is None:
            all_quests = []
            users = await get_human_stats()
            user = ctx.author
            with open(scroll_data_json_file, "r") as json_file:
                data = json.load(json_file)
                data = (data)
                for items in data:
                    if items["mode"].endswith("Quests"):
                        t = None
                        try:
                            for things in users[str(user.id)]["Quests"]:
                                if things["quest_name"] == f"Defeat {items['itemname']}":
                                    if things["amount"] > 0:
                                        amount = things["amount"]
                                        t = 1
                                    else:
                                        break
                                else:
                                    pass
                        except:
                            t = None
                        
                        if t == None:
                            if items["level"] <= users[str(user.id)]["Level"]:
                                if items["mode"].startswith("BOSS"): 
                                    all_quests.append([items["itemname"], True, "BOSS"])
                                elif items["mode"].startswith("NPC"):
                                    all_quests.append([items["itemname"], True, "NPC"])
                                continue
                            else:
                                if items["mode"].startswith("BOSS"):
                                    all_quests.append([items["itemname"], False, "BOSS"])
                                elif items["mode"].startswith("NPC"):
                                    all_quests.append([items["itemname"], False, "NPC"])
                                continue
                        else:
                            if items["mode"].startswith("BOSS"): 
                                all_quests.append([items["itemname"], None, "BOSS"])
                            elif items["mode"].startswith("NPC"):
                                all_quests.append([items["itemname"], None, "NPC"])
                    else:
                        pass
            
            embed = discord.Embed(
                title="NPC Quests",
                description="Quests are basically like tasks which will keep track on your NPC duels and if defeat the respective NPC mentioned in the quest, then you will be heavily rewarded including Chibucks, Universal Shards...! You can simply use `a!quests challenge <Quest_Index>`. Remember, you can challenge quests which have lower level than you or equal level!",
                color=0xaa5bfc,
                timestamp= datetime.utcnow()
            )

            field_value = ""
            index = 0
            for quest in all_quests:
                index += 1
                if quest[1] is None:
                    attributes = await get_all_attributes(quest[0], scroll_data_json_file, Key=["level", "rarity", "rewards"])
                    if quest[2] == "BOSS":
                        field_value = field_value + f"\n**[{index}]** Defeat {quest[0]} x{amount} Left・Lv{attributes[0]} | {attributes[1]} ✨ **|** {attributes[2][1]} Chibucks, {attributes[2][0]} EXP"
                    else:
                        field_value = field_value + f"\n**[{index}]** Defeat {quest[0]} x{amount} Left・Lv{attributes[0]} | {attributes[1]} ✨ **|** {attributes[2][1] * 8} Chibucks, {attributes[2][0]} EXP"
                    continue
                else:
                    pass
            if field_value == "":
                field_value = "*No Quests*"
            embed.add_field(name="Active Quests", value=field_value, inline=False)



            field_value = ""
            index = 0
            for quest in all_quests:
                index += 1
                if quest[1] is True and quest[0] not in all_quests:
                    attributes = await get_all_attributes(quest[0], scroll_data_json_file, Key=["level", "rarity", "rewards"])
                    if quest[2] == "BOSS":
                        field_value = field_value + f"\n**[{index}]** Defeat {quest[0]} x1・Lv{attributes[0]} | {attributes[1]} ✨ **|** {attributes[2][1]} Chibucks, {attributes[2][0]} EXP"
                    else:
                        field_value = field_value + f"\n**[{index}]** Defeat {quest[0]} x8・Lv{attributes[0]} | {attributes[1]} ✨ **|** {attributes[2][1] * 8} Chibucks, {attributes[2][0] * 8} EXP"
                    continue
                else:
                    pass
            if field_value == "":
                field_value = "*No Quests*"
            embed.add_field(name="Available Quests", value=field_value, inline=False)


            field_value = ""
            index = 0
            for quest in all_quests:
                index += 1
                if quest[1] is False and quest[0] not in all_quests:
                    attributes = await get_all_attributes(quest[0], scroll_data_json_file, Key=["level", "rarity"])
                    if quest[2] == "BOSS":
                        field_value = field_value + f"\n**[{index}]** Defeat {quest[0]} x1・Lv{attributes[0]} | {attributes[1]} ✨ **|** {attributes[2][1]} Chibucks, {attributes[2][0]} EXP"
                    else:
                        field_value = field_value + f"\n**[{index}]** Defeat {quest[0]} x8・Lv{attributes[0]} | {attributes[1]} ✨ **|** {attributes[2][1]} Chibucks, {attributes[2][0]} EXP"
                    continue
                else:
                    pass
            if field_value == "":
                field_value = "*No Quests*"
            embed.add_field(name="Unavailable Quests", value=field_value, inline=False)
            await ctx.send(embed=embed)


    @quests.command()
    async def challenge(self, ctx, quest_index):
    
        user = ctx.author
        res = await challenge(user, quest_index)
        if not res[0]:
            if res[1] == 0:
                await ctx.reply("No results found!\nPlease recheck the quests menu and try again!")
            elif res[1] == 1:
                await ctx.reply("Quest conditions not met!\nPlease choose a lower level task than you and try again!")
        else:
            await ctx.reply(f"**Defeat {res[1]}** Quest has been activated!")



async def setup(client:commands.Bot) -> None:
   await client.add_cog(Human(client))
   await client.add_cog(Duel(client))
   await client.add_cog(Quests(client))   