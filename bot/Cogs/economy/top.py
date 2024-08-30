import disnake
import sqlite3 as sql

from datetime import datetime as dt
from typing import List, Dict
from disnake.ext import commands
from disnake import SelectOption, CmdInter
from other import usercad


class SelectBalanceTop(disnake.ui.Select):
    def __init__(self, members) -> None:
        self.members: Dict[str: list[int]] = members   # Баланс участника и id 
        
        # Колонны в Dropdown Menu с Никнеймом и балансом участника
        options: List[SelectOption] = [SelectOption(label = f'{op}: {self.members[op][0]}', value = self.members[op][1]) for op in self.members]
            
        super().__init__(placeholder = 'Топ по балансу 👇', options = options, max_values = 1)
        
    
    async def callback(self, inter: CmdInter) -> None:
        values: List[str] = inter.values[0]   # ID участника
        member = await inter.guild.fetch_member(values)   # Находим участника по id и получаем доступ к классу Member
        
        await usercad(inter.guild.id, member, inter)    # Карточка участника на которого кликнули в Dropdown Menu
        
   
   
# Класс для отображения Dropdown Menu
class SelectViewDropdown(disnake.ui.View):
    def __init__(self, members: dict[str: list[int]]) -> None:
        self.members = members
        
        super().__init__(timeout=120.0)
        self.add_item(SelectBalanceTop(self.members))
        
    
class Reaction(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
        
    # Команда для отображения топа по балнсу
    @commands.slash_command(description='Топ по балансу')
    async def baltop(self, inter: CmdInter, how: int) -> None:  
        with sql.connect('projectbot.db') as conn:
            cursor = conn.cursor()
            
            ''' 1. Получаем баланс всех участников
                2. Сортируем в порядке убывания
                3. Оставляем столько человек в сколько указал участник в переменной how
                4. Список для неповторяющихся элементов
            '''
            
            balance: List[int] = [x[0] for x in cursor.execute("SELECT cash FROM server{}".format(inter.guild.id)).fetchall()] # 1
            balance.sort(reverse=True)    # 2
            balance = balance[:how]    # 3
            new: List[int] = []    # 4
            
            # Создаём список с неповторяющимся балансами
            for member_money in balance:
                if member_money not in new:
                    new.append(member_money)
                    
                    
            dikt_for_class: Dict[str: list[int]] = {}     # Словарь для хранения участника и его баланса и id
            
            # Если участников с неповторяющимся балансом соответсвует указанному how
            if len(new) == how:
                
                # Получаём имя и id по кол-ву денег участника и запоняем словарь полученными данными
                for member_money in new:
                    name_users = cursor.execute("SELECT name FROM server{} WHERE cash = ?".format(inter.guild.id), [member_money]).fetchone()[0]
                    id_users = cursor.execute("SELECT id FROM server{} WHERE cash = ?".format(inter.guild.id), [member_money]).fetchone()[0]
                    
                    dikt_for_class[name_users] = [member_money, id_users]
                
                view = SelectViewDropdown(dikt_for_class)
                await inter.send(view=view, ephemeral=True)
            cursor.close()
            
            
def setup(bot: commands.Bot) -> None:
    bot.add_cog(Reaction(bot))
    