import disnake

from random import choice
from disnake.ext import commands

from database.src.db.base import data_funcs
from bot.utils.box import box
from database.src.db.schemas import BaseMode



class Gaming:
     def __init__(
          self, 
          guild_id: int, 
          author: disnake.Member, 
          member: disnake.Member, 
          bot: commands.Bot
     ) -> None:
          
          self.__author = author
          self.__member = member
          self.__guild_id = guild_id
          self.__bot = bot         
        
        
     async def send_who_first(self) -> None:
          embed_a = await box(
               title=' ```Ты начинаешь игру.``` ', 
               description='!.shoot - чтобы стрельнуть'
          )
          embed_m = await box(
               title=f'```Игру начинает {self.__author.name}.```', 
               description='!.shoot - чтобы стрельнуть'
          )
          
          await self.__author.send(embed=embed_a, delete_after=60)
          await self.__member.send(embed=embed_m, delete_after=60)          
          await self.author_start()
          
          
            
            
     async def author_start(
          self, 
          patrons: list[int] | None = None, 
          patron_shot: int | None = None
     ) -> None:
          def check(m: disnake.Member) -> bool:
               return m.author == self.__author
          
          
          if not patrons and not patron_shot:
               patrons = [1, 2, 3, 4, 5, 6]
               patron_shot = choice(patrons)
          
         
          
          try:
               message = await self.__bot.wait_for('message', check=check,  timeout=60)
               
               if message.content == '!.shoot':
                    rnd = choice(patrons)
                    
                    if rnd == patron_shot:
                         await data_funcs.balance(
                              id_guild=self.__guild_id,
                              id_member=self.__member.id,
                              cash=15,
                              mode=BaseMode.ON
                         )
                         
                         embed = await box(
                              title=f'🔥 Поздравляю, ты выйграл! Ты получаешь 15 монет.'
                         )
                         await self.__member.send(embed=embed, delete_after=60)
                         
                         
                         embed.title = '😢 К сожалению, ты проиграл!'
                         await self.__author.send(embed=embed, delete_after=60)
                         
                         
                    else:
                         patrons.remove(rnd)
                         
                         title_author = f'Тебе повезло, револьвер не выстрелил! Очередь {self.__member.name}.'
                         title_member = f'На этот раз {self.__author.name} повезло! Твоя очередь!'
                         
                         await self.__author.send(title_author, delete_after=60)
                         await self.__member.send(title_member, delete_after=60)
                         
                         await self.member_start(patrons, patron_shot)
                         
               else:
                    await self.__author.send('Нужно писать команду !.shoot', delete_after=60)
                    await self.author_start(patrons, patron_shot)
                         
          except Exception as ex:
               print(ex)
               
               title_end = 'Игра прекращена! Потому - что один из игроков так и не написал !.shot.'
               
               await self.__author.send(title_end, delete_after=60)  
               await self.__member.send(title_end, delete_after=60)
               
               
               
               
     async def member_start(self, patrons: list[int], patron_shot: int) -> None:
          def check(m: disnake.Member) -> bool:
               return m.author == self.__member
          
          try:
               message = await self.__bot.wait_for('message', check=check,  timeout=60)
                    
               if message.content == '!.shoot':
                    random = choice(patrons)
                    
                    if random == patron_shot:
                         await data_funcs.balance(
                              id_guild=self.__guild_id,
                              id_member=self.__author.id,
                              cash=15,
                              mode=BaseMode.ON
                         )
                         embed = await box(
                              title=f'🔥 Поздравляю, ты выйграл! Ты получаешь 15 монет.'
                         )
                         await self.__author.send(embed=embed, delete_after=60)
                        
                         embed.title = '😢 К сожалению, ты проиграл!'
                         await self.__member.send(embed=embed, delete_after=60)
                    
                    
                    else:
                         patrons.remove(random)
                         
                         title_member = f'Тебе повезло, револьвер не выстрелил! Очередь {self.__author.name}.'
                         title_author = f'На этот раз {self.__member.name} повезло! Твоя очередь.'
                         
                         await self.__member.send(title_member, delete_after=60)
                         await self.__author.send(title_author, delete_after=60)
                         
                         await self.author_start(patrons, patron_shot)
          
               else:
                    await self.__member.send('Нужно писать команду !.shoot', delete_after=60)
                    await self.member_start(patrons, patron_shot)
                         
                         
          except Exception as ex:
               title_end = 'Игра прекращена! Потому - что один из игроков так и не написал !.shot'
               
               await self.__author.send(title_end, delete_after=120.0)
               await self.__member.send(title_end, delete_after=120.0)