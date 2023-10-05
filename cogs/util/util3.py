import discord 
from fun_config import *
from emoji import emojize
import datetime
import math

class Crystals():

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
                title=f"{self.user.global_name}'s Crystals", 
                description="This is the list of all the crystals you have ready to open. Use `a!crystals open <crystal_name>` to open the crystal! To inspect the crystal, type `a!crystals info <crystal_name>`",
                color = 0xaa5bfc,
                timestamp = datetime.datetime.utcnow()
            )
            
            list_of_all_crystals = []
            try:
                for crystal in self.content:
                    name = crystal["item"]
                    amount = crystal["amount"]
                    emoji = crystal["emoji"]
                    if amount < 1:
                        pass
                    else:
                        list_of_all_crystals.append(f"{emojize(emoji)} ・ {name} x{amount}\n")

                list_of_all_crystals = await self.outer_instance.get_content(list_of_all_crystals)
                list_of_all_crystals_string = ""
                for crystal in list_of_all_crystals:
                    list_of_all_crystals_string = list_of_all_crystals_string + crystal
                    continue

                embed.add_field(name="\n", value=list_of_all_crystals_string)
            except:
                pass

            if not list_of_all_crystals:
                embed.add_field(name="\n", value="*You haven't obtained any crystals yet!*")
    
            embed.add_field(name="\n", value="\n", inline=False)
            embed.set_footer(icon_url=(self.user.display_avatar), text= f"For {self.user.global_name}")
        
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
