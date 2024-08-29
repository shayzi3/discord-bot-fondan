import random
import disnake

from datetime import datetime as dt

from disnake.ext import commands



class RandomMessageMember(commands.Cog):
     def __init__(self, bot: commands.Bot) -> None:
          self.bot = bot
          
        
     @commands.cooldown(1, 10, commands.BucketType.user)
     @commands.slash_command(description='Отправить сообщение рандомному участнику.')
     async def message_member(
          self, 
          inter: disnake.CmdInter, 
          message: str,
          member: disnake.Member | None = None,
          anonim: bool =  commands.Param(choices=[
               disnake.OptionChoice(name='True', value=True),
               disnake.OptionChoice(name='False', value=False)
     ])) -> None:
          embed = disnake.Embed(
               description=message,
               color=disnake.Colour.blue(),
               timestamp=dt.now()
          )
          if not anonim:
               embed.set_author(name=f'От кого: {inter.author.name}', icon_url=inter.author.avatar)

          if member:
               await member.send(embed=embed)
               
          else:
               members = [mem for mem in inter.guild.members if not mem.bot]
               member: disnake.Member = random.choice(members)

               await member.send(embed=embed)
          await inter.send(f'Сообщение было отправлено {member.mention}', ephemeral=True)
          
          
          

def setup(bot: commands.Bot):
     bot.add_cog(RandomMessageMember(bot))