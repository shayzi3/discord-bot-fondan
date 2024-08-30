import random
import disnake

from datetime import datetime as dt
from disnake.ext import commands



class Avatar(commands.Cog):
     def __init__(self, bot: commands.Bot) -> None:
          self.bot = bot
          
     
     @commands.cooldown(1, 5, commands.BucketType.user)
     @commands.slash_command(description='Аватар участника сервера.')
     async def avatar(self, inter: disnake.CmdInter, member: disnake.Member | None = None) -> None:
          if not member:
               members = [mem for mem in inter.guild.members if not mem.bot]
               member = random.choice(members)
               
          embed = disnake.Embed(
               colour=disnake.Colour.blue(),
               timestamp=dt.now()
          )
          embed.set_author(name=member.name)
          embed.set_image(url=member.avatar.url)     
          
          await inter.send(embed=embed, ephemeral=True)
          
          
          
def setup(bot: commands.Bot):
     bot.add_cog(Avatar(bot))
          
          