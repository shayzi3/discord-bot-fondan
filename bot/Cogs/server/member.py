import random
import disnake

from datetime import datetime as dt
from disnake.ext import commands

from database.src.db.base import data_funcs
from database.src.json.base import json_funcs
from assets.pictures import bot_images
from bot.utils.box import box




class Member(commands.Cog):
     def __init__(self, bot: commands.Bot) -> None:
          self.bot = bot
     
     
     @commands.Cog.listener()
     async def on_member_join(self, member: disnake.Member) -> None:
          await data_funcs.insert_new_user(member)
           
          await member.send(
               embed=await box(
                    title=f'Привет, {member.name}',
                    description=f'Добро пожаловать на сервер {member.guild.name}!',
                    thumbnail_file=disnake.File(fp=random.choice(bot_images))
               )
          )
          
          
          
     @commands.Cog.listener()
     async def on_member_remove(self, member: disnake.Member) -> None:
          if not member.bot:
               await data_funcs.delete_user(
                    id_guild=member.guild.id,
                    id_member=member.id
               )
               await json_funcs.delete_member(member.id)
          
          
          
def setup(bot: commands.Bot) -> None:
     bot.add_cog(Member(bot))