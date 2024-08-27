import disnake

from datetime import datetime as dt

from database.src.models import Member



async def return_pages(
     user: disnake.Member, 
     balance: int, 
     roles: str
) -> list[disnake.Embed]:
     
     page1 = disnake.Embed(
          title=f'Карточка {user.name}', 
          timestamp=dt.now(), 
          colour=disnake.Colour.dark_magenta()
     )
     
     page1.set_footer(text='Page 1/3')
     page1.add_field(name='Nickname', value=user.name, inline=False)
     page1.add_field(name='ID', value=user.id, inline=False)
     page1.set_thumbnail(url=user.avatar)
                    
     
     page2 = disnake.Embed(
          title=f'Карточка {user.name}', 
          timestamp=dt.now(), 
          colour=disnake.Colour.dark_magenta()
     )
     
     page2.set_footer(text='Page 2/3')
     page2.add_field(name='Created Account', value=user.created_at.strftime("%d-%m-%Y %H:%M:%S"), inline=False)
     page2.add_field(name='Joined', value=user.joined_at.strftime("%d-%m-%Y %H:%M:%S"), inline=False)
     page2.set_thumbnail(url=user.avatar)
                    
                    
     page3 = disnake.Embed(
          title=f'Карточка {user.name}', 
          timestamp=dt.now(), 
          colour=disnake.Colour.dark_magenta()
     )
     
     page3.set_footer(text='Page 3/3')
     page3.add_field(name='Balance', value=balance, inline=False)
     page3.add_field(name='Roles', value=roles, inline=False)
     page3.set_thumbnail(url=user.avatar)
               
               
     return [page1, page2, page3]