import os
import disnake

from disnake.ext import commands

from bot.utils.getters import Get



class Wallpaper(commands.Cog):
     def __init__(self, bot: commands.Bot) -> None:
          self.bot = bot
          self.get = Get()
          
          
          
     @commands.cooldown(1, 30, commands.BucketType.user)
     @commands.slash_command(description='Обои рабочего стола')
     async def wallpaper(self, inter: disnake.CmdInter) -> None:
          await inter.response.defer(ephemeral=True)
          
          wallpaper_path = await self.get.get_wallpaper(inter.author.id)
          
          await inter.send(file=disnake.File(wallpaper_path))
          os.remove(wallpaper_path)  
          
          
          
def setup(bot: commands.Bot):
     bot.add_cog(Wallpaper(bot))