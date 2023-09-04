import json
import firebase_admin
from firebase_admin import db, credentials
from fun_config import *

cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://animetrix-7e080-default-rtdb.asia-southeast1.firebasedatabase.app/"})




class DB():

    def __init__(self):
        self.db = db

    async def create(self):
        if self.db.reference("/").get() == None:
            self.db.reference("/").update({"inventory": "None"})
            self.db.reference("/").update({"human": "None"})
            self.db.reference("/").update({"scroll": "None"})
            return True
        else:
            return False
        
    async def update(self, mode=("inventory", "human", "scroll")):
        if mode == "inventory":
            users = await get_inventory_data()
        elif mode == "human":
            users = await get_human_stats()
        elif mode == "scroll":
            users = await get_scroll_data()

        self.db.reference(f"/{mode}").update(users)

    async def retrieve(self, mode=("inventory", "human", "scroll")):
        return self.db.reference(f"/{mode}").get()
    
    async def update_json(self, mode=("inventory", "human", "scroll")):
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
        
        return users
    