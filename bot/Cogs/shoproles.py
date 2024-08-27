import disnake
from disnake.ext import commands
from disnake import SelectOption, CmdInter, ButtonStyle
import sqlite3 as sql
from typing import List, Dict, Optional
import json
        
# Кнопки подтверждения покупки
class ButtonAccepter(disnake.ui.View):
    def __init__(self) -> None:
        self.choice: Optional[bool] = None
        super().__init__(timeout=60.0)
        
    @disnake.ui.button(label='Купить', style=ButtonStyle.green)
    async def button1(self, button: disnake.ui.Button, inter: CmdInter) -> None:
        await inter.response.defer()
        
        await inter.send('Покупка обрабатывается...', ephemeral=True, delete_after=60.0)
        self.choice = True
        self.stop()
        
    @disnake.ui.button(label='Не покупать', style=ButtonStyle.red)
    async def button2(self, button: disnake.ui.Button, inter: CmdInter) -> None:
        await inter.response.defer()
        
        await inter.send('Покупка отклонена.', ephemeral=True, delete_after=60.0)
        self.choice = False
        self.stop()


# Dropdawn меню магазина
class SelectShop(disnake.ui.Select):
    def __init__(self, guild: int) -> None:
        self.guild = guild
        
        with sql.connect('projectbot.db') as conn:
            cursor = conn.cursor()
            
            
            # Получаю все роли {
            info = cursor.execute("SELECT roles FROM rolles{}".format(self.guild)).fetchone()[0]
            info: Dict[str, List[int]] = json.loads(info)
            # }
            
            
            # Проверяю есть ли роли в словаре {
            if info:
                options: List[SelectOption] = [SelectOption(label=f'Роль: {name_role} • Цена {info[name_role][0]}', emoji='💸', value=name_role) for name_role in info]
                super().__init__(placeholder='Магазин ролей ↓', options=options)
                
            else:
                options: List[SelectOption] = [SelectOption(label='Пусто! ', emoji='🧹', value='False')]
                super().__init__(placeholder='Магазин ролей ↓', options=options)
        cursor.close()
        # }
        
    async def callback(self, inter: CmdInter) -> None:
        await inter.response.defer()
        values = inter.values[0] # str
       
        
        # Ответ после отправки Select окна с лэйблом "Пусто"
        if values == 'False':
            return await inter.send(f'{inter.author.mention}, ролей нет! Попроси модеров чтобы они их добавили.', ephemeral=True, delete_after=30.0)
            
        # Отправляю пользователю подтверждение покупки {
        view = ButtonAccepter()
        await inter.send('Потдвердите покупку.', view=view, ephemeral=True, delete_after=60.0)
        await view.wait()
        # }
            
            
        # Проверю есть ли роль, которую покупают у пользователя {
        if view.choice:
            for val in inter.author.roles:
                if values == val.name:
                    return await inter.send('У тебя уже есть эта роль!', ephemeral=True, delete_after=30.0)
        # }    
                
                
            with sql.connect('projectbot.db') as conn:
                cursor = conn.cursor()
            
                        
                # Забираю баланс пользователя и получаю словарь с ролями {
                balance = cursor.execute("SELECT cash FROM server{} WHERE id = ?".format(self.guild), [inter.author.id]).fetchone()[0]
                info = cursor.execute("SELECT roles FROM rolles{}".format(self.guild)).fetchone()[0]
                info = json.loads(info)
                # }
                        
                        
                # Проверю достаточно ли денег у покупателя {
                if balance < info[values][0]:
                    return await inter.author.send('У тебя недостаточно денег для покупки этой роли!')
                        
                        
                # Если достаточно оформляем покупку, выдаю роль
                cursor.execute("UPDATE server{} SET cash = cash - ? WHERE id = ?".format(self.guild), [info[values][0], inter.author.id])
                conn.commit()
                            
                role = disnake.utils.get(inter.guild.roles, id=info[values][1])
                await inter.author.add_roles(role)
                            
                            
                # Удаляю роль из магазина, заношу эти данные в бд {
                del info[values]
                cursor.execute("UPDATE rolles{} SET roles = ?".format(self.guild), [json.dumps(info)])
                conn.commit()
                # }
                            
                await inter.send('Покупка прошла успешна. Роль выдана.', ephemeral=True, delete_after=60.0)
                # }
                
           
            
            
    
# Отображение меню магазина
class SelectView(disnake.ui.View):
    def __init__(self, guild: int) -> None:
        super().__init__(timeout=180.0)
        self.add_item(SelectShop(guild))

# Создание кога
class ShopCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
    # Отправка меню магазина с ролями
    @commands.slash_command(description='Магазин Ролей')
    async def buyrole(self, inter: CmdInter) -> None:
        view = SelectView(inter.guild.id)
        await inter.send(view=view, ephemeral=True, delete_after=180.0)
        
        
    # Добавление роли в магазин
    @commands.slash_command(description='Добавить роль для покупки.')
    async def shop_add(self, inter: CmdInter, money: int, role: disnake.Role) -> None:
        
        if money <= 0:
            return await inter.send(f'{inter.author.mention}, цена не подходит для продажи!', ephemeral=True, delete_after=30.0) 
        
        with sql.connect('projectbot.db') as conn:
            cursor = conn.cursor()
            
            # Получаю список со всеми невыставляемыми товарами {
            notadd = cursor.execute("SELECT notadd FROM rolles{}".format(inter.guild.id)).fetchone()[0]
            notadd = json.loads(notadd)
            # }
            
            price = cursor.execute("SELECT sale FROM rolles{}".format(inter.guild.id)).fetchone()[0]
            
            
            # Проверяю можно ли выставить эту роль {
            if role.id in notadd:
                return await inter.send(f'{inter.author.mention}, нельзя выставить эту роль на продажу!', ephemeral=True, delete_after=30.0)
            # }
            
            if price > money:
                return await inter.send(f'{inter.author.mention}, минимальная цена для продажи роли - {price}.', ephemeral=True, delete_after=30.0)
            
            # Получаю роль {
            roles_give = cursor.execute("SELECT roles FROM rolles{}".format(inter.guild.id)).fetchone()[0]
            roles_give: Dict[str, List[int]] = json.loads(roles_give)
            # }
            
            # Добавляю роль {
            roles_give[role.name] = [money, role.id] # Добавляю новую роль
            cursor.execute("UPDATE rolles{} SET roles = ?".format(inter.guild.id), [json.dumps(roles_give)]) # Сохраняю в бд
            conn.commit()
            # }
        
            await inter.send(f'{inter.author.mention}, роль добавлена в магазин!', ephemeral=True, delete_after=60.0)
        cursor.close()
        
    # Удаление роли из магазина {
    @commands.slash_command(description='Удалить роль из магазина.')
    async def shop_delete(self, inter: CmdInter, role: disnake.Role) -> None:
        
        try:
            
            with sql.connect('projectbot.db') as conn:
                cursor = conn.cursor()
                    
                # Получаю словарь со всеми ролями {
                roles_give = cursor.execute("SELECT roles FROM rolles{}".format(inter.guild.id)).fetchone()[0]
                roles_give: Dict[str, List[int]] = json.loads(roles_give)
                # }
                    
                # Удаляю роль из магазина {   
                del roles_give[role.name] # Удаляю роль
                cursor.execute("UPDATE rolles{} SET roles = ?".format(inter.guild.id), [json.dumps(roles_give)]) # Сохраняю в бд
                conn.commit()
                # }
                    
                await inter.send(f'{inter.author.mention}, роль удалена из магазина!', ephemeral=True, delete_after=60.0)
            cursor.close()
                   
        except Exception as ex:
            await inter.send(f'{inter.author.mention}, такой роли нет в магазине!', ephemeral=True, delete_after=30.0)
    # }
    
            
    # Добавление в список невыставляемых
    @commands.slash_command(description='Добавить роли, которые нельзя добавлять в магазин.')
    async def cant_sold(self, inter: CmdInter, role: disnake.Role):
        
        with sql.connect('projectbot.db') as conn:
            cursor = conn.cursor()
                    
            # Получаю список с ролями {
            roles_give = cursor.execute("SELECT notadd FROM rolles{}".format(inter.guild.id)).fetchone()[0]
            roles_give: List[int] = json.loads(roles_give)
            # }
            
            
            # Проверка на нахождение роли в списке {
            if role.id not in roles_give:
                
                # Добавляю роль в список {  
                roles_give.append(role.id) # Добавляю роль в список
                cursor.execute("UPDATE rolles{} SET notadd = ?".format(inter.guild.id), [json.dumps(roles_give)]) # Сохраняю в бд
                conn.commit()
                # }
            # }
                await inter.send(f'{inter.author.mention}, роль добавлена в список невыставляемых.', ephemeral=True, delete_after=60.0)
                
            # Ответ если пользователь хочет добавить роль, которая уже есть в списке {
            else:
                await inter.send(f'{inter.author.mention}, такая роль уже есть в списке.', ephemeral=True, delete_after=30.0)
            # }
        cursor.close()
        
        
    # Удаление из списка невыставляемых
    @commands.slash_command(description='Удалить роль, из списка невыставляемых в магазин.')
    async def can_sold(self, inter: CmdInter, role: disnake.Role):
        
        with sql.connect('projectbot.db') as conn:
            cursor = conn.cursor()
            
                    
            # Получаю список со всеми невыставляемыми ролями {
            roles_give = cursor.execute("SELECT notadd FROM rolles{}".format(inter.guild.id)).fetchone()[0]
            roles_give: List[int] = json.loads(roles_give)
            # }
            
            
            # Проверяю находится ли роль уже в нашем списке {
            if role.id in roles_give:
                
                # Удаляю роль из магазина {   
                roles_give.remove(role.id) # Удаляю роль
                cursor.execute("UPDATE rolles{} SET notadd = ?".format(inter.guild.id), [json.dumps(roles_give)]) # Сохраняю в бд
                conn.commit()
                # }
            # }
                await inter.send(f'{inter.author.mention}, роль удалена из списка невыставляемых.', ephemeral=True, delete_after=60.0)
            
            
            # Ответ если роли нет в списке {
            else:
                await inter.send(f'{inter.author.mention}, такой роли в списке нет!', ephemeral=True, delete_after=30.)
            # }
        cursor.close()
        
        
    @commands.slash_command(description='Минимальная цена на роль.')
    async def min_price(self, inter: CmdInter, price: int):
        
        if price <= 0:
            return await inter.send(f'{inter.author.mention} нельзя выставить цену меньше 0!', ephemeral=True, delete_after=60.0)
        
        with sql.connect('projectbot.db') as conn:
            cursor = conn.cursor()
            
            cursor.execute("UPDATE rolles{} SET sale = ?".format(inter.guild.id), [price])
            conn.commit()
            
            await inter.send(f'{inter.author.mention} минимальная цена обновлена!', ephemeral=True, delete_after=60.0)
        cursor.close()
        
        
# Добавление кога в бота {
def setup(bot: commands.Bot) -> None:
    bot.add_cog(ShopCog(bot))
# }