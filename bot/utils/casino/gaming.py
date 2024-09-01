import asyncio
import random
import disnake

from bot.utils.casino.schemas import Choice
from database.src.db.base import data_funcs
from database.src.db.schemas import BaseMode



class Gaming:
     def __init__(
          self, 
          inter: disnake.CmdInter, 
          choice: Choice, 
          money: int
     ) -> None:
          
          self.inter = inter
          self.choice = choice
          self.money = money        
        
        
     async def flags(self) -> None:
          randomize = random.randint(1, 100)
          flag = None
               
          if self.choice == Choice.RED:
               if randomize <= 30:
                    flag = 'Win'
                    
          elif self.choice == Choice.GREEN:
               if randomize <= 15:
                    flag = 'Win'
                    
          elif self.choice == Choice.GRAY:
               if randomize <= 5:
                    flag = 'Win'
                    
          if not flag: 
               flag = 'Lose'
          
          await self.ruletka(flag)
        
        
     async def ruletka(self, flag: str) -> None:
          emb_text = disnake.Embed(colour=disnake.Colour.blue())
          emb_text.add_field(name='Начинаем раскурт колеса. Ждите 5 секунд...', value=' **Желаю вам удачи!** ')
          emb_text.set_thumbnail(file=disnake.File(fp=r'assets/chat_images/Pictures/casinowheel.gif'))
          await self.inter.send(embed=emb_text, ephemeral=True)
                         
          await asyncio.sleep(5)
          
          if flag == 'Win':
               await data_funcs.balance(
                    id_guild=self.inter.guild.id,
                    id_member=self.inter.author.id,
                    cash=self.money * self.choice.value,
                    mode=BaseMode.ON
               )  
               
               emb_text = disnake.Embed(colour=disnake.Colour.blue())
               emb_text.add_field(name=f'Твоя ставка {self.money} монет. Твой выйгрыш {self.money * self.choice.value}', value=' **Поздравляю тебя!** ')
               emb_text.set_thumbnail(file=disnake.File(fp=r'assets/chat_images/Pictures/top.jpg'))
          
               await self.inter.send(embed=emb_text, ephemeral=True) 
          
          
          elif flag == 'Lose':
               await data_funcs.balance(
                    id_guild=self.inter.guild.id,
                    id_member=self.inter.author.id,
                    cash=self.money,
                    mode=BaseMode.OFF
               )  
               
               emb_text = disnake.Embed(colour=disnake.Colour.blue())
               emb_text.add_field(name=f'Тебе не повезло! Ты проиграл {self.money} монет...', value=' **В следующий раз получится?! :)** ')
               emb_text.set_thumbnail(file=disnake.File(fp=r'assets/chat_images/Pictures/bad.jpg'))
          
               await self.inter.send(embed=emb_text, ephemeral=True)