import asyncio

import disnake

from typing import Any
from disnake.ext import commands

from bot.utils.box import box
from bot.utils.duel.buttons import DuelButton
from bot.utils.duel.gaming import Gaming




class DuelCommand:
     
     @staticmethod
     async def edited(
          author: disnake.Message, 
          member: disnake.Message,
          embed: disnake.Embed | None = None,
          content: str | None = None,
          view: Any | None = None,
          deleter_after: float | None = None
     ) -> None:
          
          await author.edit(content=content, embed=embed, view=view, delete_after=deleter_after)
          await member.edit(content=content, embed=embed, view=view, delete_after=deleter_after)



     @classmethod
     async def duel_command(
          cls,
          author: disnake.Member,
          member: disnake.Member,
          bot: commands.Bot
          
     ) -> None:
          emb_author = await box(
               title=f'Вызов {member.name} отправлен!'
          )
          msg_author = await author.send(embed=emb_author)
          
          
          view = DuelButton()
          emb_member = await box(
               title=f'{author.name} бросил тебе вызов на дуэль!'
          )
          msg_member = await member.send(embed=emb_member, view=view)
          
          await view.wait()
          
          
          if view.choice:
               sec = 5
               emb_timer = await box(
                    title=f'До дуэли осталось {sec} секунд!'
               )
               await cls.edited(
                    author=msg_author, 
                    member=msg_member,
                    embed=emb_timer
               )  
                           
               while sec != 0:
                    sec -= 1
                         
                    emb_timer.title = f'До дуэли осталось {sec} секунд!'
                         
                    await asyncio.sleep(1)
                         
                    await cls.edited(
                         author=msg_author,
                         member=msg_member,
                         embed=emb_timer
                    )
                         
              
               emb_author.title = 'Дуэль началась!'
               await cls.edited(
                    author=msg_author,
                    member=msg_member,
                    embed=emb_author
               )
                         
               start = Gaming(author.guild.id, author, member, bot)
               await start.send_who_first()
                              
     
          # If member reject duel
          elif view.choice is False:
               await msg_member.delete()
               
               emb_author.title = f'{member.name} отклонил твой вызов!'
               await msg_author.edit(embed=emb_author, delete_after=60)
               
          
          
          # If member ignored on call
          else:
               emb_author.title = 'Запрос на дуэль проигнорирован...'
               await cls.edited(
                    author=msg_author,
                    member=msg_member,
                    embed=emb_author,
                    deleter_after=60 
               )