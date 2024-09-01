import disnake

from database.src.json.base import json_funcs
from bot.utils.box import box
from bot.utils.usercard.dict_models import get_dict_models





async def return_pages(
     user: disnake.Member, 
     balance: int, 
     roles: str
) -> list[disnake.Embed]:
     msg = await json_funcs.get_member_messages(user.id)
     
     model = await get_dict_models(
          user=user,
          balance=balance,
          roles=roles,
          msg=msg
     )
          
     embeds = []
     for m in model.keys():
          embed = await box(**model[m])
          
          embeds.append(embed)
     return embeds