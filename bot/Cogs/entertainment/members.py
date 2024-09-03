import random
import disnake

from disnake.ext import commands

from bot.scripts.getters import Get
from bot.utils.box import box 



# Random Message Member
class Members(commands.Cog):
     def __init__(self, bot: commands.Bot) -> None:
          self.bot = bot
          self.get = Get()
          
        
        
     @commands.cooldown(1, 10, commands.BucketType.user)
     @commands.slash_command(description='Отправить сообщение рандомному участнику')
     async def message_member(
          self, 
          inter: disnake.CmdInter, 
          message: str,
          member: disnake.Member | None = None,
          anonim: bool =  commands.Param(choices=[
               disnake.OptionChoice(name='True', value=True),
               disnake.OptionChoice(name='False', value=False)
     ])) -> None:
          embed = await box(description=message)
          
          if not anonim:
               embed.set_author(name=f'От кого: {inter.author.name}', icon_url=inter.author.avatar)

          if not member:
               members = [mem for mem in inter.guild.members if not mem.bot]
               member: disnake.Member = random.choice(members)

          await member.send(embed=embed)
          await inter.send(f'Сообщение было отправлено {member.mention}', ephemeral=True)
          
          
          
     @commands.cooldown(1, 5, commands.BucketType.user)
     @commands.slash_command(description='Рандомный участник')
     async def random_member(self, inter: disnake.CmdInter, text: str  = None):
          member = random.choice([mem for mem in inter.guild.members]).mention
        
          embed = await box(
               description=f'{text} - {member}' if text else member
          )
          await inter.send(embed=embed, delete_after=300)
          



def setup(bot: commands.Bot):
     bot.add_cog(Members(bot))