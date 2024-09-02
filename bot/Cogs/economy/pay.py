import disnake

from datetime import datetime as dt
from disnake.ext import commands

from database.src.db.base import data_funcs
from database.src.db.schemas import BaseMode
from bot.utils.box import box
from bot.utils.rules import payment_rules




class Pay(commands.Cog):
     def __init__(self, bot: commands.Bot) -> None:
          self.bot = bot
        
        
     @staticmethod
     async def send_message_users(inter: disnake.CmdInter, member: disnake.Member, cash: int, comment: str | None = None) -> None:
          emb_author = await box(
               description=f'{cash} монет отправлены успешно!',
               name_author=f'Кому: {member.name}',
               icon_author=member.avatar
          )
          emb_member = await box(
               description=f'Вы получили {cash} монет.',
               name_author=f'От кого: {inter.author.name}',
               icon_author=inter.author.avatar,
               fields=(
                    ('Комментарий', comment, True)
               ) if comment else None
          )
          
          await inter.send(embed=emb_author, ephemeral=True)
          await member.send(embed=emb_member)
          
        
    
    
     @commands.cooldown(1, 5, commands.BucketType.user)
     @commands.slash_command(description='Отправить деньги.')
     async def pay(self, inter: disnake.CmdInter, member: disnake.Member, money: int, comment: str | None = None) -> None:
          await inter.response.defer()
          
          rule = await payment_rules(inter=inter, member=member, money=money)
          if not rule:
               return await inter.send('Отправьте команду ещё раз и на этот раз без ошибок!', delete_after=60)
               
          check = await data_funcs.balance(
               id_guild=inter.guild.id,
               id_member=inter.author.id,
               cash=money,
               mode=BaseMode.CHECK
          )
          if not check:
               return await inter.send(f'{inter.author.mention}, у вас на балансе нет {money}!', delete_after=60)
                    
          await data_funcs.payment(
               id_guild=inter.guild.id,
               id_author=inter.author.id,
               id_member=member.id,
               moneys=money
          )
          await self.send_message_users(inter, member, money, comment)
            
            
            
def setup(bot) -> None:
     bot.add_cog(Pay(bot))