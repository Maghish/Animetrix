from typing import Optional
import discord 
from fun_config import *
import datetime
import math

class Backpack():

    def __init__(self, ctx, content):
        self.ctx = ctx
        self.content = content
        self.current_page = 1
        self.num_per_page = 10
        self.total_pages = math.ceil(len(content) / self.num_per_page)
        if self.total_pages <= 0:
            self.total_pages = 1
        self.message = None

    class PageView(discord.ui.View):
        
        def __init__(self, outer_instance):
            super().__init__(timeout=None)
            self.outer_instance = outer_instance
            start_btn = [x for x in self.children if x.custom_id == 'start_btn'][0]
            back_btn = [x for x in self.children if x.custom_id == 'back_btn'][0]
            next_btn = [x for x in self.children if x.custom_id == 'next_btn'][0]
            finish_btn = [x for x in self.children if x.custom_id == 'finish_btn'][0]

            if self.outer_instance.current_page == 1 and self.outer_instance.total_pages == 1:
                start_btn.disabled = True
                back_btn.disabled = True
                next_btn.disabled = True
                finish_btn.disabled = True

            elif self.outer_instance.current_page == self.outer_instance.total_pages: 
                start_btn.disabled = False
                back_btn.disabled = False
                next_btn.disabled = True
                finish_btn.disabled = True

            elif self.outer_instance.current_page == 1: 
                start_btn.disabled = True
                back_btn.disabled = True
                next_btn.disabled = False
                finish_btn.disabled = False
            
            else:
                start_btn.disabled = False
                back_btn.disabled = False
                next_btn.disabled = False
                finish_btn.disabled = False

                
                
    
        @discord.ui.button(label="⏮️", style=discord.ButtonStyle.green, custom_id="start_btn")
        async def start_button_callback(self, interaction, button):
            await interaction.response.defer()
            self.outer_instance.current_page = 1
            await self.outer_instance.resend()
        
        @discord.ui.button(label="◀️", style=discord.ButtonStyle.green, custom_id="back_btn")
        async def back_button_callback(self, interaction, button):
            await interaction.response.defer()
            self.outer_instance.current_page -= 1
            await self.outer_instance.resend()
            
        @discord.ui.button(label="▶️", style=discord.ButtonStyle.green, custom_id="next_btn")
        async def next_button_callback(self, interaction, button):
            await interaction.response.defer()
            self.outer_instance.current_page += 1
            await self.outer_instance.resend()

        @discord.ui.button(label="⏭️", style=discord.ButtonStyle.green, custom_id="finish_btn")
        async def finish_button_callback(self, interaction, button):
            await interaction.response.defer()
            self.outer_instance.current_page = self.outer_instance.total_pages
            await self.outer_instance.resend()

    class BuildEmbed():

        def __init__(self, user, content, outer_instance):
            self.user = user
            self.content = content
            self.outer_instance = outer_instance

        async def build(self):

            embed = discord.Embed(
                title=f"{self.user.global_name}'s Backpack",
                description="Here you can view all items in your backpack. use `a!backpack add <item_name>` to add it to your backpack or if you want to remove it, then use `a!backpack remove <item_name>` to remove it.",
                color= 0xaa5bfc,
                timestamp=datetime.datetime.utcnow() 
            )

            

            backpack_items = []
            try:
                for items in self.content:
                    if items["amount"] <= 0:
                        pass
                    else:
                        backpack_items.append(f"{items['emoji']} | {items['item']} x{items['amount']}\n")
                        continue
            except:
                pass

            if not backpack_items:
                backpack_items = "*No items in your backpack*"

            backpack_items = await self.outer_instance.get_content(backpack_items)
            backpack_items_string = ""
            for items in backpack_items:
                backpack_items_string = backpack_items_string + items
                continue

            embed.add_field(name="Backpack", value=backpack_items_string)

            embed.add_field(name="\n", value="\n", inline=False)
            embed.set_footer(icon_url=(self.user.display_avatar), text=f"For {self.user.global_name}")

            return embed
        
    
    async def get_content(self, content):
        start_index = (self.current_page - 1) * self.num_per_page
        end_index = start_index + self.num_per_page
        new_content = content[start_index:end_index]
        return new_content
    
    async def send(self):
        content = self.content
        embed = await self.BuildEmbed(self.ctx.author, content ,self).build()
        my_view = self.PageView(self)
        self.message = await self.ctx.send(embed=embed, view=my_view)

    async def resend(self):
        content = self.content
        embed = await self.BuildEmbed(self.ctx.author, content, self).build()
        my_view = self.PageView(self)
        await self.message.edit(embed=embed, view=my_view)
        