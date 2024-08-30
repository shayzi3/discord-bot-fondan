import disnake

from datetime import datetime as dt
from disnake.ext import commands

from database.src.db.base import data_funcs
from database.src.db.schemas import BaseMode




class Pay(commands.Cog):
     def __init__(self, bot: commands.Bot) -> None:
          self.bot = bot
        
        
     @staticmethod
     async def send_message_users(inter: disnake.CmdInter, member: disnake.Member, cash: int, comment: str | None = None) -> None:
          emb_author = disnake.Embed(
               description=f'{cash} монет отправлены успешно!',
               colour=disnake.Colour.blue(),
               timestamp=dt.now()
          )
          emb_author.set_author(name=f'Кому: {member.name}', icon_url=member.avatar)
        
        
          emb_member = disnake.Embed(
               description=f'Вы получили {cash} монет.',
               colour=disnake.Colour.blue(),
               timestamp=dt.now()
          )
          emb_member.set_author(name=f'От кого: {inter.author.name}', icon_url=inter.author.avatar)
          emb_member.add_field(name='Комментарий', value=comment) if comment else None
          
          await inter.send(embed=emb_author, ephemeral=True)
          await member.send(embed=emb_member)
          
        
    
    
     @commands.cooldown(1, 75, commands.BucketType.user)
     @commands.slash_command(description='Отправить деньги.')
     async def pay(self, inter: disnake.CmdInter, member: disnake.Member, money: int, comment: str | None = None) -> None:
          if inter.author.id != member.id:
               if money <= 0:
                    return await inter.send(f'{inter.author.mention}, сумму {money} отправить невозможно!', ephemeral=True) 
               
               check = await data_funcs.balance(
                    id_guild=inter.guild.id,
                    id_member=inter.author.id,
                    cash=money,
                    mode=BaseMode.CHECK
               )
               if not check:
                    return await inter.send(f'{inter.author.mention}, у вас на балансе нет {money}!', ephemeral=True)
                    
               await data_funcs.payment(
                    id_guild=inter.guild.id,
                    id_author=inter.author.id,
                    id_member=member.id,
                    moneys=money
               )
               await self.send_message_users(inter, member, money, comment)
                         
          else:
               await inter.send(f'{inter.author.mention}, нельзя отправить деньги самому себе!', ephemeral=True)
            
            
            
def setup(bot) -> None:
     bot.add_cog(Pay(bot))