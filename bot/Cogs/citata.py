import random
import disnake

from datetime import datetime as dt
from disnake.ext import commands

from bot.scripts.statham.parse import statham


class CitataStatham(commands.Cog):
     def __init__(self, bot: commands.Bot) -> None:
          self.bot = bot
          
          
     @commands.cooldown(1, 8, commands.BucketType.user)
     @commands.slash_command(description='Цитата Джеймона Стетхама')
     async def statham(self, inter: disnake.CmdInter):
          citata = await statham.get_citata()
          
          embed = disnake.Embed(
               colour=disnake.Colour.blue(),
               timestamp=dt.now()
          )
          embed.set_image(url=random.choice(citata))
          await inter.send(embed=embed, ephemeral=True)
          
          
def setup(bot: commands.Bot):
     bot.add_cog(CitataStatham(bot))