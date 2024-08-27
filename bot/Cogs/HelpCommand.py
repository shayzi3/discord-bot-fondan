# Подключение модулей
import disnake


from datetime import datetime as dt
from typing import Dict, List
from disnake.ext import commands
from disnake import SelectOption, CmdInter



# Class for SelectMenu with commands for member
class HelpSelectMembers(disnake.ui.Select):
    
    # Create new table in SelectMenu
    def __init__(self, commands) -> None:
        self.command_members: Dict[str: str] = commands
        options: List[SelectOption] = [SelectOption(label=cm, emoji='🔎', value=cm) for cm in self.command_members]
        
        super().__init__(placeholder='↓ Команды сервера', options=options)
        
        
    # Answer on SelectMenu
    async def callback(self, inter: CmdInter) -> None:
        values: List[str] = inter.values[0]
        
        # Create Embed with docs for ccommand
        emb = disnake.Embed(colour=disnake.Colour.dark_magenta())
        emb.set_footer(text=inter.author.name, icon_url=inter.author.avatar)
        
        emb.add_field(name=f'Команда {values}', value=self.command_members[values])
        emb.set_thumbnail(file=disnake.File(fp=r'Pictures\help.gif'))
        
        await inter.send(embed=emb, ephemeral=True, delete_after=120.0)
        
        
            
# Class for SelectMenu with commands for members
class SendSelectMembers(disnake.ui.View):
    
    # Create dict with command for members
    def __init__(self) -> None:
        self.commands_members: Dict[str: str] = {
            '/balik': '/Покажет ваш баланс на сервере. \n member - покажет баланс того кого вы отметили.',
            '/baltop': 'Покажет топеров сервера по деньгам.',
            '/pay': 'Переведёт деньги тому кого вы отметили. \n member - кому вы хотите отправить деньги, сумма - сколько денег вы хотите отправить денег \n Отправлять деньги можно только > 0❗',
            '/usercard': 'Показывает вашу карточку. \n member - покажет карточку того кого вы пинганули.',
            '/embed': '''Самое главное написать хотя бы в одном поле❗ \n 1-ое поле - название Embed \n 2-ое поле - описание Embed
            \n 3-е роле - дополнение к описанию. Правильная запись → Название; Комментарий к названию \n
            4-ое поле - добавление картинки. Размер → big, small. Правильная запись → Размер; ссылка на изображение. \n
            Добавление знака  ;  в 3-ем и 4-ом поле после Названия, размера обязательное❗\n Если следовать правилам правилам на 
            выходе получится красивый Embed.''',
            '/duels': '''/duels - отправить дуэль игроку. Тот кому вы кинули дуэль должен её принять,
            затем вы должны выбрать ОДИНАКОВЫЙ режим дуэли, начнётся отсчёт до дуэли. 
            Как отсчёт пройдёт вы будуте стрелять по очереди. Команда для выстрела - !.shoot''',
            '/checkroles': 'Просмотр всех ролей у участника сервера.',
            '/casinowheel': 'Колесо фортуны',
            '/buyrole': 'Покупка роли',
            '/getgift': 'Получение подарка каждый час'
        }
        super().__init__(timeout=180.0)
        self.add_item(HelpSelectMembers(self.commands_members))
        
        
# Класс для SelectMenu
class SelectMenuAdmins(disnake.ui.Select):
    
    # Передаём словарь с командами, создаём столбцы дл SelecctMenu
    def __init__(self, commands) -> None:
        self.commands_admins: Dict[str: str] = commands
        options: List[SelectOption] = [SelectOption(label=cm, emoji='🧑‍💻', value=cm) for cm in self.commands_admins]
        
        super().__init__(placeholder='↓ Команды сервера для админов', options=options)
        
    # Ответ на SelectMenu
    async def callback(self, inter) -> None:
        values: List[str] = inter.values[0]
        channel = inter.guild.get_channel(1195672441394036759)
            
        # Создание Embed в котором будет руководство к команде
        emb = disnake.Embed(title=f'{values}', timestamp=dt.now())
        emb.set_footer(text=inter.author.name, icon_url=inter.author.avatar)
        emb.add_field(name='Что же делает команда или как её использовать❔', value=self.commands_admins[values])
        emb.set_thumbnail(url='https://i.gifer.com/embedded/download/Lp4S.gif')
        await channel.send(embed=emb)
        
class SendSelectAdmins(disnake.ui.View):
    def __init__(self) -> None:
        
        # Admins
        self.command_admins = {
            '/purge': 'Удаление сообщений с сервера. amount - число сообщений, которые нужно удалить.',
            '/giverole': 'Выдать роль участнику сервера.',
            '/takerole': 'Забрать роль у участника сервера',
            '/createrole': 'Создать роль на сервере',
            '/delrole': 'Удалить роль с сервера',
            '/delallroles': 'Удалить все роли у участника сервера. \n Доступна только Главным❗',
            '/muted': 'Замутить участника, также можно замутить на время',
            'unmuted': 'Размутить участника, также можно размутить на время',
            '/banned': 'Забанить участника сервера',
            '/unbanned': 'Разбанить участника сервера',
            '/shop_add': 'Добавить роль в магазин',
            '/shop_del': 'Удалить роль из магазина',
            '/cant_sold': 'Роль которую недьзя выставить на продажу',
            '/can_sold': 'Удалить роль из списка ролей которые нельзя выствить',
            '/kick': 'Кикнуть участника сервера',
            '/createbase': 'Обязательная команда! Создание таблицы под ваш сервер.',
            '/min_price': 'Минимальная цена на роль'
        }
        
        super().__init__(timeout=300.0)
        self.add_item(SelectMenuAdmins(self.command_admins))
        
        
# Ког для отправки SelectMenu
class HelpCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    # Команда help для участников
    @commands.slash_command(description='Аудит по командам сервера')
    async def helping(self, inter: CmdInter) -> None:
        view = SendSelectMembers()
        
        text = f'Всегда рад помочь! {inter.author.mention}'
        await inter.send(text, view=view, ephemeral=True, delete_after=180.0)
        
        
    # Команда /help для Главных и Продолжающих
    @commands.slash_command(description='Help для модераторов')
    async def helpadmin(self, inter: CmdInter) -> None:
        view = SendSelectAdmins()
        
        text='Рад помочь!'
        await inter.send(text, view=view, ephemeral=True, delete_after=180.0)
        
        
        
# Добавления кога в бота
def setup(bot: commands.Bot) -> None:
    bot.add_cog(HelpCog(bot))