from typing import Callable
import disnake

from disnake.ext import commands

from database.src.db.base import data_funcs
from bot.utils.box import box
from bot.utils.rules import payment_rules
from database.src.db.schemas import BaseMode





class OnOffBalance(commands.Cog):
     def __init__(self, bot: commands.Bot) -> None:
          self.bot = bot
          
          
     @commands.cooldown(1, 300, commands.BucketType.user)
     @commands.slash_command(description='Пополнить баланс')
     async def on_balance(self, inter: disnake.CmdInter, member: disnake.Member, money: int):
          await inter.response.defer()
          
          rule = await payment_rules(inter=inter, member=member, money=money)
          if not rule:
               return await inter.send('Отправьте команду ещё раз и на этот раз без ошибок!', ephemeral=True)
          
          await data_funcs.balance(
               id_guild=member.guild.id,
               id_member=member.id,
               cash=money,
               mode=BaseMode.ON
          )
          await inter.send(
               embed=await box(
                    name_author=f'Кому: {member.name}',
                    icon_author=member.avatar,
                    description=f'Баланс пополнен успешно! Сумма: {money} монет.',
                    text_footer=f'Пополнил: {inter.author.name}',
                    icon_footer=inter.author.avatar
               )
          )
          
          
     @commands.cooldown(1, 300, commands.BucketType.user)
     @commands.slash_command(description='Отнять от баланса')
     async def off_balance(self, inter: disnake.CmdInter, member: disnake.Member, money: int | None = None):
          await inter.response.defer()
          
          rule = await payment_rules(inter=inter, member=member, money=money, mode=BaseMode.OFF)
          if not rule:
               return await inter.send('Проверьте баланс участника или заново отправьте команду.', ephemeral=True)
          
          await data_funcs.balance(
               id_guild=member.guild.id,
               id_member=member.id,
               cash=rule[1],
               mode=BaseMode.OFF
          )
          await inter.send(
               embed=await box(
                    name_author=f'У кого: {member.name}',
                    icon_author=member.avatar,
                    description=f'Баланс отнят успешно! Сумма: {rule[1]} монет.',
                    text_footer=f'Отнял: {inter.author.name}',
                    icon_footer=inter.author.avatar
               )
          )
          
          

def setup(bot: commands.Bot):
     bot.add_cog(OnOffBalance(bot))