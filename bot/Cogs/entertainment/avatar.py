import random
import disnake

from datetime import datetime as dt
from disnake.ext import commands

from bot.utils.box import box



class Avatar(commands.Cog):
     def __init__(self, bot: commands.Bot) -> None:
          self.bot = bot
          
     
     @commands.cooldown(1, 5, commands.BucketType.user)
     @commands.slash_command(description='Аватар участника сервера')
     async def avatar(self, inter: disnake.CmdInter, member: disnake.Member | None = None) -> None:
          if not member:
               members = [mem for mem in inter.guild.members if not mem.bot]
               member = random.choice(members)
               
               
          await inter.send(
               embed=await box(
                    name_author=member.name, 
                    image_url=member.avatar.url
               ), 
               ephemeral=True
          )
          
          
          
def setup(bot: commands.Bot):
     bot.add_cog(Avatar(bot))
          
          