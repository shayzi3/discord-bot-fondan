import disnake

from datetime import datetime as dt
from disnake.ext import commands

from database.src.base import data_funcs
from assets.pictures import Picture




class MembersAction(commands.Cog):
     def __init__(self, bot: commands.Bot) -> None:
          self.bot = bot
          self.picrure = Picture()
     
     
     @commands.Cog.listener()
     async def on_member_join(self, member: disnake.Member) -> None:
          await data_funcs.insert_new_user(member)
          
          embed = disnake.Embed(
               title=f'Привет, {member.name}',
               colour=disnake.Colour.blue(),
               timestamp=dt.now()
          )
          embed.set_thumbnail(file=disnake.File(fp=self.picrure.get_random_bot_images))
                    
          await member.send(embed=embed)
          
          
          
     @commands.Cog.listener()
     async def on_member_remove(self, member: disnake.Member) -> None:
          await data_funcs.delete_user(
               id_guild=member.guild.id,
               id_member=member.id
          )
          
          
          
def setup(bot: commands.Bot) -> None:
     bot.add_cog(MembersAction(bot))