import disnake

from disnake.ext import commands

from database.src.db.base import data_funcs
from bot.utils.box import box



class Money(commands.Cog):
     def __init__(self, bot: commands.Bot) -> None:
          self.bot = bot
            
            
     @commands.cooldown(1, 12, commands.BucketType.user)
     @commands.slash_command(description='Ваш баланс')
     async def money(self, inter: disnake.CmdInter, member: disnake.Member | None = None) -> None:
          moneys = await data_funcs.get_balance(
               id_guild=inter.guild.id,
               id_member=inter.author.id if not member else member.id
          )  
          
          text = f'**Твой баланс {moneys}**'
          if member:
               text = f'**На балансе {member.mention} {moneys} монет**'   


          await inter.send(
               embed=await box(
                    description=text
               ), 
               ephemeral=True
          )
            
            

def setup(bot) -> None:
    bot.add_cog(Money(bot))