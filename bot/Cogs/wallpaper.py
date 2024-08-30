import os
import disnake

from datetime import datetime as dt
from disnake.ext import commands

from bot.scripts.getters import Get



class Wallpaper(commands.Cog):
     def __init__(self, bot: commands.Bot) -> None:
          self.bot = bot
          self.get = Get()
          
          
          
     @commands.cooldown(1, 90, commands.BucketType.user)
     @commands.slash_command(description='Обои рабочего стола')
     async def wallpaper(self, inter: disnake.CmdInter) -> None:
          wallpaper = await self.get.get_wallpaper()
          embed = disnake.Embed(
               colour=disnake.Colour.blue(),
               timestamp=dt.now()
          )
          embed.set_image(url=wallpaper)
          await inter.send(embed=embed, ephemeral=True)          
          
          
          
def setup(bot: commands.Bot):
     bot.add_cog(Wallpaper(bot))