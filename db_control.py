import json
import firebase_admin
from firebase_admin import db, credentials
from fun_config import *
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
credentials_path = os.path.join(script_dir, 'credentials.json')

cred = credentials.Certificate(credentials_path)
firebase_admin.initialize_app(cred, {"databaseURL": "https://animetrix-7e080-default-rtdb.asia-southeast1.firebasedatabase.app/"})



class DB():

    def __init__(self):
        self.db = db

    async def create(self):
        if self.db.reference("/").get() == None:
            self.db.reference("/").update({"inventory": "None"})
            self.db.reference("/").update({"human": "None"})
            self.db.reference("/").update({"scroll": "None"})
            self.db.reference("/").update({"scrolls_data": "None"})
            self.db.reference("/").update({"items_data": "None"})
            return True
        else:
            return False
        
    async def update(self, mode=("inventory", "human", "scroll", "scrolls_data", "items_data")):
        if mode == "inventory":
            users = await get_inventory_data()
        elif mode == "human":
            users = await get_human_stats()
        elif mode == "scroll":
            users = await get_scroll_data()
        elif mode == "scrolls_data":
            with open(scroll_data_json_file, "r") as json_file:
                users = json.load(json_file)
                users = (users)
        elif mode == "items_data":
            with open(items_json_file, "r") as json_file:
                users = json.load(json_file)
                users = (users)
 
        try:
            self.db.reference(f"/{mode}").update(users)
        except:
            self.db.reference(f"/{mode}").set(users)

    async def retrieve(self, mode=("inventory", "human", "scroll", "scrolls_data", "items_data")):
        return self.db.reference(f"/{mode}").get()
    
    async def update_json(self, mode=("inventory", "human", "scroll", "scrolls_data", "items_data")):
        if mode == "inventory":
            users = self.db.reference("/inventory").get()
            with open(inventory_json_file, "w") as json_file:
                json.dump(users, json_file, indent=1)
        elif mode == "human":
            users = self.db.reference("/human").get()
            with open(human_json_file, "w") as json_file:
                json.dump(users, json_file, indent=1)
        elif mode == "scroll":
            users = self.db.reference("/scroll").get()
            with open(scroll_json_file, "w") as json_file:
                json.dump(users, json_file, indent=1)
        elif mode == "scrolls_data":
            users = self.db.reference("/scrolls_data").get()
            with open(scroll_data_json_file, "w") as json_file:
                json.dump(users, json_file, indent=2)
        elif mode == "items_data":
            users = self.db.reference("/items_data").get()
            with open(items_json_file, "w") as json_file:
                json.dump(users, json_file, indent=2)
        
        return users
    