import discord
import random
from discord.ui import View, Button
import json



inventory_json_file = 'E:\\Coding\\ActualCodes\\DiscordBots\\Animetrix\\Storage\\Inventory.json'
money_json_file = 'E:\\Coding\\ActualCodes\\DiscordBots\\Animetrix\\Storage\\Money.json'
items_json_file = 'E:\\Coding\\ActualCodes\\DiscordBots\\Animetrix\\Storage\\Items.json'
human_json_file = 'E:\\Coding\\ActualCodes\\DiscordBots\\Animetrix\\Storage\\Human.json'
scroll_data_json_file = 'E:\\Coding\\ActualCodes\\DiscordBots\\Animetrix\\Storage\\Scrolls_data.json'
scroll_json_file = 'E:\\Coding\\ActualCodes\\DiscordBots\\Animetrix\\Storage\\Scroll.json'
quests_json_file = 'E:\\Coding\\ActualCodes\\DiscordBots\\Animetrix\\Storage\\Quests.json'



async def open_account(user):
        
    users =  await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["Wallet"] = 0 


    with open (money_json_file, "w") as f:
        json.dump(users,f, indent= 1)
    return True 

async def get_bank_data():
    with open (money_json_file, "r") as f:
        users = json.load(f)
    return users

async def update_bank(user, change = 0, mode = ("Wallet", "Bank", "Invest", "Invest_value", "Bitcoin", "Locker", "Locker_level")):
    users = await get_bank_data()

    users[str(user.id)][mode] += int(change)
    
    with open (money_json_file, "w") as f:
        json.dump(users,f, indent= 1)
        

    balance = [users[str(user.id)]["Wallet"]]
    return balance



async def get_scroll_data():
    with open(scroll_json_file, "r") as json_file:
        data = json.load(json_file)
    return data

async def create_scroll(user):
    
    users =  await get_scroll_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["Scrolls"] = "None" 


    with open (scroll_json_file, "w") as f:
        json.dump(users,f, indent= 1)
    return True 




async def open_inv(user):
        
    users =  await get_inventory_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["Inventory"] = "None"
        users[str(user.id)]["Food"] = "None"
        users[str(user.id)]["Potion"] = "None"
        users[str(user.id)]["Crystal"] = "None"
        users[str(user.id)]["Backpack"] = []
        users[str(user.id)]["Fragments"] = 0


    with open (inventory_json_file, "w") as f:
        json.dump(users,f,indent=1)
    return True 

async def get_inventory_data():
    with open (inventory_json_file, "r") as f:
        users = json.load(f)
    return users


async def get_human_stats():
    with open (human_json_file, "r") as f:
        data = json.load(f)
    return data

async def create_human(user):
        
    users =  await get_human_stats()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["HP"] = 500
        users[str(user.id)]["MaxHP"] = 500
        users[str(user.id)]["Energy"] = 100
        users[str(user.id)]["MaxEnergy"] = 100
        users[str(user.id)]["PDMG"] = 15
        users[str(user.id)]["exp"] = 0
        users[str(user.id)]["Level"] = 1
        users[str(user.id)]["Quest"] = "None"
        users[str(user.id)]["AttrPoints"] = 0
        


    with open (human_json_file, "w") as f:
        json.dump(users,f, indent= 1)
    return True





async def challenge(user, quest_index):
    # Find the data in the scrolls data file.
    name_ = None
    with open(scroll_data_json_file, "r") as json_file:
        data = json.load(json_file)
        data = (data)
        index = 1
        for things in data:
            mode = things["mode"]
            if mode == "NPC/Quests":
                quest_index = int(quest_index)
                # Find the matching quest_index  
                if quest_index == index:
                    name = things["itemname"]
                    name_ = name
                    img = things["img"]
                    level = things["level"]
                    amount = 8
                    break
                else:
                    index += 1
                    pass
            elif mode == "BOSS/Quests":
                quest_index = int(quest_index)
                # Find the matching quest_index
                if quest_index == index:
                    name = things["itemname"]
                    name_ = name
                    img = things["img"]
                    level = things["level"]
                    amount = 1
                    break
                else:
                    index += 1
                    pass
            else:
                pass
    
    if name_ == None:
        return [False, 0]




    users = await get_human_stats()

    if level > users[str(user.id)]["Level"]:
        return [False, 1]

    try:
        index = 0
        t = None
        for things in users[str(user.id)]["Quests"]:
            if things["quest_name"] == f"Defeat {name}":
                users[str(user.id)]["Quests"][index]["amount"] = int(amount)


                with open(human_json_file, "w") as json_file:
                    json.dump(users, json_file, indent= 1)

                t = 1

            else:
                index += 1
                pass
        if t == None:
            obj = {"quest_name": f"Defeat {name}", "NPC": name, "img": img, "level": level, "amount": int(amount)}
            users[str(user.id)]["Quests"].append(obj)
    except:
        obj = {"quest_name": f"Defeat {name}", "NPC": name, "img": img, "level": level, "amount": int(amount)}
        users[str(user.id)]["Quests"] = [obj]  

              

    with open(human_json_file,"w") as f:
        json.dump(users,f, indent= 1)


    return [True,name]






    





async def heal_human(user, change = 0, mode = ("HP", "MaxHP", "Energy", "MaxEnergy", "AttrPoints")):
    users = await get_human_stats()

    try:
        if (change + int(users[str(user.id)][mode])) > int(users[str(user.id)][f"Max{mode}"]):
            users[str(user.id)][mode] = int(users[str(user.id)][f"Max{mode}"])
        
            with open (human_json_file, "w") as f:
                json.dump(users,f, indent= 1)

            return
        else:
            ...
    except:
        ...
    
    users[str(user.id)][mode] += int(change)
        
    with open (human_json_file, "w") as f:
        json.dump(users,f, indent= 1)
            


async def duel_stats_change(user, change = 0, mode = ("HP", "Energy")):

    users = await get_human_stats()
    stat = users[str(user.id)][mode]
    if (stat - int(change)) < 0:
        users[str(user.id)][mode] = 0
    else:
        users[str(user.id)][mode] -= change

    with open (human_json_file, "w") as f:
        json.dump(users,f, indent=1)
    
    users = await get_human_stats()
    return users[str(user.id)][mode]







async def buy_this(user,item_name,amount):
    await open_inv(user)
    name_ = None
    selected = False
    MODE = None
    with open (items_json_file, "r") as json_file:
        data = json.load(json_file)
        iT = (data)
        for item in iT:
            name = item["itemname"]
            mode = item["mode"]
            name_lower = name.lower()
            item_name_lower = item_name.lower()
            if name_lower == item_name_lower:
                if mode.startswith("Shop"): 
                    if mode.endswith("Food"):
                        format = "Food"
                        selected = False
                    elif mode.endswith("Potion"):
                        format = "Potion"
                        selected = False
                    else:
                        format = "Inventory"   
                        selected = True
                    name_ = name
                    price = item["price"]
                    emoji = item["emoji"]
                    value = item["value"]  
                    break
                else:
                    pass
            else:
                pass
                    

    if name_ == None:
        return [False,1]
    
    cost = price*amount
    users = await get_bank_data()
    bal = users[str(user.id)]["Wallet"]

    if bal<cost:
        return [False,2]

    usersv2 = await get_inventory_data()
    try:
        index = 0
        t = None
        for thing in usersv2[str(user.id)][format]:
            n = thing["item"]
            n_lower = n.lower()
            if n_lower == item_name_lower:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                usersv2[str(user.id)][format][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            if selected is not False:
                obj = {"item": name , "amount" : amount, "mode": mode, "emoji": emoji, "value": value, "selected": False}
            else:
                obj = {"item": name , "amount" : amount, "mode": mode, "emoji": emoji, "value": value}
            usersv2[str(user.id)][format].append(obj)
    except:
        if selected is not False:
            obj = {"item": name , "amount" : amount, "mode": mode, "emoji": emoji, "value": value, "selected": False}
        else:
            obj = {"item": name , "amount" : amount, "mode": mode, "emoji": emoji, "value": value}
        usersv2[str(user.id)][format] = [obj]        

    with open(inventory_json_file,"w") as f:
        json.dump(usersv2,f, indent= 1)

    await update_bank(user,cost*-1,"Wallet")

    return [True,name]
    
        



async def set_scroll_active(user, scroll_name):
    # Check if the item exists
    name_ = None
    with open(scroll_data_json_file, "r") as json_file:
        data = json.load(json_file)
        iT = (data)
        for item in iT:
            name = item["itemname"]
            name_lower = name.lower()
            if name_lower == scroll_name.lower():
                name_ = name
                break
            else:
                pass
    if name_ == None:
        return [False, 1]
    
    users = await get_scroll_data()



    for items in users[str(user.id)]["Scrolls"]:
        name = items["item"]
        if name == name_:
            amount = items["amount"]
            if amount <= 0:
                return [False, 3]
            else:
                pass
        else:
            pass
    # If so, check if the user has it
    t = 0
    index = -1
    for items in users[str(user.id)]["Scrolls"]:
        name = items["item"]
        index += 1
        if name == name_:
            t = 1
            # Then check if it's already active
            active_state = items["active"]
            if active_state is False:
                # If not, then make it active and return

                users[str(user.id)]["Scrolls"][index]["active"] = True
                    
                with open(scroll_json_file, "w") as json_file:
                    json.dump(users, json_file, indent=1)

                continue

            else:
                return [False, 2]
        else:
            active_state = items["active"]
            if active_state is True:

                users[str(user.id)]["Scrolls"][index]["active"] = False
                
                with open(scroll_json_file, "w") as json_file:
                    json.dump(users, json_file, indent=1)

                users[str(user.id)]["Scrolls"][index]["amount"] -= 1

                with open(scroll_json_file, "w") as json_file:
                    json.dump(users, json_file, indent=1)

                continue
            else:
                continue     


    if t == 0:
        return [False, 3]
    else:
        return [True, name_]
            
async def get_all_attributes(*args, **kwargs):
    item_name, file_name = args[0], args[1]
    keys = kwargs["Key"]
    list_of_values = []
    with open(file_name, "r") as f:
        data = json.load(f)
        data = (data)
        for key in data:
            if key["itemname"] == item_name:
                for value in keys:
                    list_of_values.append(key[value])
        return list_of_values
    

async def create_duel(user1, user2):
    users = await get_human_stats()
    user1_dmg = users[str(user1.id)]["PDMG"]
    user1_level = users[str(user1.id)]["Level"]
    user2_dmg = users[str(user1.id)]["PDMG"]
    user2_level = users[str(user1.id)]["Level"]
    users = await get_scroll_data()
    for thing in users[str(user1.id)]["Scrolls"]:
        if thing["active"] == True:
            user1_fruit_name = thing["item"]
            user1_fruit_emoji = thing["emoji"]
            user1_fruit_level = thing["Level"]
            user1_fruit_abilities = []
            for ability in thing["ability"]:
                user1_fruit_abilities.append([ability["ability_name"], ability["emoji"], ability["dmg"], ability["chakra"], ability["level"], ability["repeat"]])
    
    for thing in users[str(user2.id)]["Scrolls"]:
        if thing["active"] == True:
            user2_fruit_name = thing["item"]
            user2_fruit_emoji = thing["emoji"]
            user2_fruit_level = thing["Level"]
            user2_fruit_abilities = []
            for ability in thing["ability"]:
                user2_fruit_abilities.append([ability["ability_name"], ability["emoji"], ability["dmg"], ability["chakra"], ability["level"], ability["repeat"]])

    return [[user1_dmg, user1_level, user1_fruit_name, user1_fruit_emoji, user1_fruit_abilities, user1_fruit_level], [user2_dmg, user2_level, user2_fruit_name, user2_fruit_emoji, user2_fruit_abilities, user2_fruit_level]]

async def create_brawl_npc(user, npc):
    users = await get_human_stats()
    user_dmg = users[str(user.id)]["PDMG"]
    user_level = users[str(user.id)]["Level"]
    users = await get_scroll_data()
    for thing in users[str(user.id)]["Scrolls"]:
        if thing["active"] == True:
            user_fruit_name = thing["item"]
            user_fruit_emoji = thing["emoji"]
            user_fruit_level = thing["Level"]
            user_fruit_abilities = []
            for ability in thing["ability"]:
                user_fruit_abilities.append([ability["ability_name"], ability["emoji"], ability["dmg"], ability["chakra"], ability["level"], ability["repeat"]])

    attributes_for_npc = await get_all_attributes(npc, scroll_data_json_file, Key=["mode", "itemname", "level", "img", "ability", "rewards", "stats"])

    return [[user_dmg, user_level, user_fruit_name, user_fruit_emoji, user_fruit_abilities, user_fruit_level], [attributes_for_npc[0], attributes_for_npc[1], attributes_for_npc[2], attributes_for_npc[3], attributes_for_npc[4], attributes_for_npc[5], attributes_for_npc[6]]]
    
    
async def make_bars(user, mode1, mode2, square1:str, square2:str, healthDashes):
    
    users = await get_human_stats()
    try:
        health = users[str(user.id)][mode1]
        maxHealth = users[str(user.id)][mode2] 
    except:
        health = mode1
        maxHealth = mode2
    dashConvert = int(maxHealth/healthDashes)           
    currentDashes = int(health/dashConvert)            
    remainingHealth = healthDashes - currentDashes      

    healthDisplay = square1 * currentDashes                
    remainingDisplay = square2 * remainingHealth                

        
    return ("|" + healthDisplay + remainingDisplay + "|" + " " + f"{int(health)}/{maxHealth}")

async def eat_this(user, item_name, amount):
    # 1. Check if item exists
    name_ = None
    with open(items_json_file, "r") as json_file:
        data = json.load(json_file)
        data = (data)
        for item in data:
            name = item["itemname"]
            name_lower = name.lower()
            if name_lower == item_name.lower():
                # 2. Check if item is a "Food" and not "Power-Up" or anything else
                mode = item["mode"]
                if mode == "Shop/Food":
                    name_ = name
                    emoji = item["emoji"]
                    value = item["value"] 
                    break
                else:
                    pass
            else:
                pass
    
    if name_ == None:
        return [False, item_name, 1]
    
    users = await get_inventory_data()
    t = None
    # 3. Check if the user has it
    for thing in users[str(user.id)]["Food"]:
        name = thing["item"]
        if name.lower() == item_name.lower():
            if thing["amount"] >= amount:
                t = 1
                break
            else:
                return [False, item_name, 3]
        else:
            pass

    if t == None:
        return [False, item_name, 2]
    
    # 4. If so update the stats of the user
    users = await get_human_stats()
    value = value * amount 
    if (value*amount + int(users[str(user.id)]["HP"])) > users[str(user.id)]["MaxHP"]:
        if value*amount >= (int(users[str(user.id)]["MaxHP"]) - int(users[str(user.id)]["HP"])):
            value = int(users[str(user.id)]["MaxHP"]) - int(users[str(user.id)]["HP"])

        

    await heal_human(user, value, "HP") 
    return [True, item_name, value, amount]


async def add_frag(self, user, crystal_name, amount):
    await open_inv(user)
    # 1. Check if the user already has fragments of the crystal
    users = await get_inventory_data()
    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["Fragments"]:
            if thing[0].lower() == crystal_name.lower():
                old_amt = thing[1]
                new_amt = old_amt + amount
                users[str(user.id)]["Fragments"][index][1] = new_amt

                with open(inventory_json_file, "w") as json_file:
                    json.dump(users, json_file, indent=1)

                t = 1
                break
            index+=1 
        if t == None:
            t = 0
            with open(items_json_file, "r") as json_file:
                data = json.load(json_file)
                data = (data)
                for things in data:
                    if things["itemname"].lower() == crystal_name.lower():
                        crystal_name = things["itemname"]
                        t = 1
                        break
                    else:
                        pass
            if t == 0:
                return [False, 0]
            else:
                users[str(user.id)]["Fragments"].append([crystal_name, amount])

    except:
        # 3. If not, create new list
        t = 0
        with open(items_json_file, "r") as json_file:
            data = json.load(json_file)
            data = (data)
            for things in data:
                if things["itemname"].lower() == crystal_name.lower():
                    crystal_name = things["itemname"]
                    t = 1
                    break
                else:
                    pass
        if t == 0:
            return [False, 0]
        else:
            users[str(user.id)]["Fragments"] =[[crystal_name, amount]]
    
    with open(inventory_json_file, "w") as json_file:
        json.dump(users, json_file, indent=1)

    return [True, 0, crystal_name, amount]
    
    

async def sep_int_and_str(stuff):
    amount = ""
    item_name = ""
    for letter in stuff:
        try:
            letter = int(letter)
            amount = amount + str(letter)
            continue
        except:
            item_name = item_name + str(letter)
            continue
        
    if amount == "":
        amount = 1   
    return [str(item_name), int(amount)] 




async def percentage_change(value, percentage, method="Add"):
    if method == "Add":
        return float(value - (value * (percentage/100)))
    elif method == "Subtract":
        return float(value - (value * (percentage/100)))
    

async def claim_crystal(user, crystal_name, amount):
    name_ = None
    with open(items_json_file, "r") as json_file:
        data = json.load(json_file)
        data = (data)
        for items in data:
            if items["itemname"].lower() == crystal_name.lower():
                mode = items["mode"]
                if mode == "Shop/Crystal":
                    name_ = items["itemname"]
                    price = items["price"]
                    emoji = items["emoji"]
                    value = items["value"]
                    rarity = items["rarity"]
                    break
                else:
                    pass
            else: 
                pass
    
    if name_ == None:
        return [False, 1]
    
    users = await get_inventory_data()
    cost = price*amount
    if int(users[str(user.id)]["Fragments"]) < cost:
        return [False, 2] 
    
    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["Crystal"]:
            n = thing["item"]
            if n == name_:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["Crystal"][index]["amount"] = new_amt
                t = 1
                break
            index += 1

        if t == None:
            obj = {"item": name_, "amount": amount, "emoji":emoji, "value": value, "mode": mode, "rarity": rarity}
            users[str(user.id)]["Crystal"].append(obj)

    except:
        obj = {"item": name_, "amount": amount, "emoji":emoji, "value": value, "mode": mode, "rarity": rarity}
        users[str(user.id)]["Crystal"] = [obj]

    users[str(user.id)]["Fragments"] -= cost

    with open(inventory_json_file, "w") as json_file:
        json.dump(users, json_file, indent=1)

    return [True, name_, amount]


async def open_crystal(user, crystal_name):
    # First check if the crystal exists
    name_ = None
    with open(items_json_file, "r") as json_file:
        data = json.load(json_file)
        data = (data)
        for items in data:
            if items["itemname"].lower() == crystal_name.lower():
                if items["mode"] == "Shop/Crystal":
                    name_ = items["itemname"]
                    mode = items["mode"]
                    rarity = items["rarity"]
                    value = items["value"]
                    break
                else:
                    pass
            else:
                pass
    
    if name_ == None:
        return [False, 1]

    # Then check if the user has it
    users = await get_inventory_data()
    t = 0
    for thing in users[str(user.id)]["Crystal"]:
        if thing["mode"] == "Shop/Crystal":
            if thing["item"] == name_:
                t = 1
                if thing["amount"] <= 0:
                    return [False, 2]
                else:
                    break
            else:
                pass
        else:
            pass
    
    if t == 0:
        return [False, 2]
    
    # Then fetch all the scrolls that have the crystal's rarity
    all_scrolls = []
    with open(scroll_data_json_file, "r") as json_file:
        data = json.load(json_file)
        data = (data)
        for scroll in data:
            if scroll["mode"].endswith("Scrolls"):
                if scroll["rarity"] == rarity:
                    all_scrolls.append(scroll["itemname"])
                    continue
                else:
                    pass
            else:
                pass
            
    # Then randomly pick the scrolls 
    selected_scrolls = []

    for _ in range(0, value):
        selected = random.choice(all_scrolls)
        selected_scrolls.append(selected)
        # and Add them to the user's pocket 
        users = await get_scroll_data()
        await create_scroll(user)
        attributes = await get_all_attributes(selected, scroll_data_json_file, Key=["mode", "emoji", "ability"])
        try:
            index = 0
            t = None
            for thing in users[str(user.id)]["Scrolls"]:
                n = thing["item"]
                if n == selected:
                    users[str(user.id)]["Scrolls"][index]["amount"] += 1
                    t = 1
                    break
                index+=1 
            if t == None:
                obj = {"item": selected , "amount" : 1, "mode": attributes[1], "emoji": attributes[0], "active": False, "ability": attributes[2], "Level": 1, "exp": 0}
                users[str(user.id)]["Scrolls"].append(obj)
        except:
            obj = {"item": selected , "amount" : 1, "mode": attributes[1], "emoji": attributes[0], "active": False, "ability": attributes[2], "Level": 1, "exp": 0}
            users[str(user.id)]["Scrolls"] = [obj]        

        with open(scroll_json_file,"w") as f:
            json.dump(users,f, indent= 1)
    
    users = await get_inventory_data()
    index = 0
    for thing in users[str(user.id)]["Crystal"]:
        if thing["item"] == name_:
            users[str(user.id)]["Crystal"][index]["amount"] -= 1

            with open(inventory_json_file, "w") as json_file:
                json.dump(users,json_file, indent=1)
        else:
            pass

    return [True, name_, selected_scrolls]
        

        
async def change_backpack(user, item, amount, action):
    
    if action == "Add":
        format1 = "Potion"
        format2 = "Backpack"
    else:
        format1 = "Backpack"
        format2 = "Potion"
    # Check if the item exists
    name_ = None
    with open(items_json_file, "r") as json_file:
        data = json.load(json_file)
        data = (data)
        for items in data:
            if items["itemname"].lower() == item.lower() and items["mode"] == "Shop/Potion":
                name_ = items["itemname"] 
                mode = items["mode"]
                emoji = items["emoji"]
                value = items["value"] 
                break
            else:
                pass

    if name_ == None:
        return [False, 1]

            
    # Check if the user has it
    users = await get_inventory_data()
    try:
        t = None
        index = 0
        for things in users[str(user.id)][format1]:
            if things["item"] == name_:
                if things["amount"] >= amount:
                    t = 1
                    users[str(user.id)][format1][index]["amount"] -= amount

                    with open(inventory_json_file, "w") as json_file:
                        json.dump(users, json_file, indent=1)

                    break
                else:
                    return [False, 2]
            else:
                pass

        if t == None:
            return [False, 2]
        
    except:
        return [False, 2]

    try:
        t = None
        index = 0
        for things in users[str(user.id)][format2]:
            if things["item"] == name_:
                t = 1
                users[str(user.id)][format2][index]["amount"] += amount

                with open(inventory_json_file, "w") as json_file:
                    json.dump(users, json_file, indent=1)
            else:
                pass
        if t == None:
            obj = {"item": name_, "amount": amount, "mode": mode, "emoji": emoji, "value": value}
            users[str(user.id)][format2].append(obj)
    except:
        obj = {"item": name_, "amount": amount, "mode": mode, "emoji": emoji, "value": value}
        users[str(user.id)][format2] = [obj]

    with open(inventory_json_file, "w") as json_file:
        json.dump(users, json_file, indent=1)

    return [True, name_, amount]