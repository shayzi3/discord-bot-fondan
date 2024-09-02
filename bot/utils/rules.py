import disnake


from database.src.db.base import data_funcs
from database.src.db.schemas import BaseMode



async def payment_rules(
     inter: disnake.CmdInter,
     member: disnake.Member,
     money: int | None = None,
     mode: BaseMode | None = None
) -> None | tuple:
     if inter.author.id == member.id:
          return None
     
     if not money and money != 0:
          money = await data_funcs.get_balance(
               id_guild=member.guild.id,
               id_member=member.id
          )
          
     if money <= 0:
          return None
               
     if mode == BaseMode.OFF:
          user_money = await data_funcs.balance(
               id_guild=member.guild.id,
               id_member=member.id,
               cash=money,
               mode=BaseMode.CHECK
          )
          if not user_money:
               return None
     
     return True, money
               

     
     
     