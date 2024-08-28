import disnake


from bot.utils.usercard import buttons, get_pages
from database.src.db.base import data_funcs





class Card:
     
     
     @staticmethod
     async def usercad(ctx: disnake.CmdInter, user: disnake.Member = None) -> None:
          if not user:
               user = ctx.author
          
          roles_member = ''.join(roles.mention for roles in user.roles)  # Получаю все роли
          user_balance = await data_funcs.get_balance(
               id_guild=user.guild.id,
               id_member=user.id
          )
          
          pagination = await get_pages.return_pages(
               user=user,
               roles=roles_member,
               balance=user_balance
          )
               
          view = buttons.PaginationButton()
          await ctx.send(embed=pagination[0], view=view)
          await view.wait()
               
          page = 0
          while True:
               if view.pagination == 'Right':
                    if page == len(pagination) - 1:
                         page = 0
                              
                    else:
                         page += 1
                              
                    view = buttons.PaginationButton()
                    await ctx.edit_original_response(embed=pagination[page], view=view)
                    await view.wait()
                         
               if view.pagination == 'Left':
                    if page == 0: 
                         page = len(pagination) - 1
                              
                    else:
                         page -= 1
                              
                    view = buttons.PaginationButton()
                    await ctx.edit_original_response(embed=pagination[page], view=view)
                    await view.wait()
                         
               if view.pagination == 'Stop':
                    return await ctx.delete_original_response()