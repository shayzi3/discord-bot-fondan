import disnake

from disnake import SelectOption

from bot.utils.usercard.pages import Card


class SelectTop(disnake.ui.Select):
     def __init__(self, members: list[tuple]) -> None:
          self.members = members
          self.card = Card()
          
          options: list[SelectOption] = [SelectOption(label = f'{i[2]}: {i[1]} монет', value = str(i[0]), emoji='🪙') for i in self.members]
          super().__init__(placeholder = 'Топ по балансу 👇', options = options)
        
    
     async def callback(self, inter: disnake.CmdInter) -> None:
          values: str = inter.values[0]
          member = await inter.guild.fetch_member(int(values))
          
          await self.card.usercad(ctx=inter, user=member)
        
   
   
class SelectView(disnake.ui.View):
     def __init__(self, members: list[tuple]) -> None:
          self.members = members
          
          super().__init__(timeout=120.0)
          self.add_item(SelectTop(self.members))