import disnake


from bot.utils.box import box
from bot.utils.duel.buttons import DuelButton



async def sending(
     user: disnake.Member,
     member: disnake.Member
) -> tuple:
     emb_user = await box(
          title=f'Вызов {member.name} отправлен!'
     )
     msg_user = await user.send(embed=emb_user)
        
     view = DuelButton()   
     emb_member = await box(
          title=f'{user.name} бросил тебе вызов на дуэль!'
     )
     msg_member = await member.send(embed=emb_member, view=view)
        
     return msg_member, msg_user, view