import disnake

from disnake.ext import commands

from bot.scripts.getters import Get
from bot.utils.box import box



class Statham(commands.Cog):
     def __init__(self, bot: commands.Bot) -> None:
          self.bot = bot
          self.get = Get()
          
          
     @commands.cooldown(1, 5, commands.BucketType.user)
     @commands.slash_command(description='Цитата Джейсона Стетхама')
     async def statham(self, inter: disnake.CmdInter):
          citata = await self.get.get_citata()
          
          await inter.send(
               embed=await box(image_url=citata), 
               ephemeral=True
          )
          
          
def setup(bot: commands.Bot):
     bot.add_cog(Statham(bot))