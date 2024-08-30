import disnake

from datetime import datetime as dt
from disnake.ext import commands

from bot.scripts.getters import Get



class CitataStatham(commands.Cog):
     def __init__(self, bot: commands.Bot) -> None:
          self.bot = bot
          self.get = Get()
          
          
     @commands.cooldown(1, 5, commands.BucketType.user)
     @commands.slash_command(description='Цитата Джейсона Стетхама')
     async def statham(self, inter: disnake.CmdInter):
          citata = await self.get.get_citata()
          
          embed = disnake.Embed(
               colour=disnake.Colour.blue(),
               timestamp=dt.now()
          )
          embed.set_image(url=citata)
          await inter.send(embed=embed, ephemeral=True)
          
          
def setup(bot: commands.Bot):
     bot.add_cog(CitataStatham(bot))