import asyncio

import disnake
import sqlite3 as sql

from typing import Optional, Dict
from random import randint
from disnake.ext import commands
from disnake import CmdInter, ButtonStyle, Colour, File
from other import onBalance, offBalance, moneyCheck


# Кнопки для выбора умножения ставки. Например: Ставка - 10. При выборе 1.5, 10 * 1.5 - выйгрышь
class SelectButtonColour(disnake.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=120.0) 
        self.choice: Optional[str] = None
        
    # Умножение на 1.5
    @disnake.ui.button(label='x1.5', emoji='❤️', style=ButtonStyle.red)
    async def butt1(self, button: disnake.ui.Button, inter: CmdInter) -> None:
        await inter.response.defer()
        await inter.delete_original_response()
                
        self.choice = 'Red'
        self.stop()
        
    # Умножение на 2
    @disnake.ui.button(label='x2', emoji='💚', style=ButtonStyle.green)
    async def butt2(self, button: disnake.ui.Button, inter: CmdInter) -> None:
        await inter.response.defer()
        await inter.delete_original_response()
        
        self.choice = 'Green'
        self.stop()
        
    # Умножение на 3.5
    @disnake.ui.button(label='x3.5', emoji='🩶', style=ButtonStyle.gray)
    async def butt3(self, button: disnake.ui.Button, inter: CmdInter) -> None:
        await inter.response.defer()
        await inter.delete_original_response()
        
        self.choice = 'Gray'
        self.stop()
        
        
# Игра Казино
class Gaming:
    def __init__(self, guild: disnake.Guild, ctx: CmdInter, choice: str, money: int) -> None:
        self.ctx = ctx 
        self.choice = choice
        self.flag: Optional[str] = None
        self.dict_x: Dict[str, int] = {
            'Red': 1.5,
            'Green': 2,
            'Gray': 3.5
        } 
        self.money = money
        self.guild = guild
        
        
    # Функция для опредения выйграл или проиграл игрок
    async def flags(self) -> None:
        
        # Если ставка умножается на 1.5 
        if self.choice == 'Red':
            randomize = randint(1, 100)   # Шанс 30%
            
            if randomize <= 30:
                self.flag = 'Win'
                
            else:
                self.flag = 'Lose'
        
        # Если ставка умножается на 2
        elif self.choice == 'Green':
            randomize = randint(1, 100)   # Шанс 15%
            
            if randomize <= 15:
                self.flag = 'Win'
                
            else:
                self.flag = 'Lose'
        
        # Если ставка умножается на 3.5
        elif self.choice == 'Gray':
            randomize = randint(1, 100)   # Шанс 5%
            
            if randomize <= 5:
                self.flag = 'Win'
                
            else:
                self.flag = 'Lose'
           
        # Если участник не выбрал ничего     
        else:
            return await self.ctx.send('Ты проигнорировал выбор.', ephemeral=True)
        
        await self.ruletka()   # Основная часть игры
        
        
    # Function for output about win or loser player
    async def ruletka(self) -> None:
        emb_text = disnake.Embed(colour=Colour.dark_gray())
        emb_text.add_field(name='Начинаем раскурт колеса. Ждите 5 секунд...', value=' **Желаю вам удачи!** ')
        emb_text.set_thumbnail(file=File(fp=r'Pictures\casinowheel.gif'))
            
        await self.ctx.send(embed=emb_text, ephemeral=True)
            
            
        await asyncio.sleep(5)   # Ждём 5 секунд до начала игры
        
        
        # Если игрок выйграл
        if self.flag == 'Win':
            await onBalance(self.guild.id, self.ctx.author.id, self.money * self.dict_x[self.choice])   
            
                
            emb_text = disnake.Embed(colour=Colour.dark_gray())
            emb_text.add_field(name=f'Выпало поле {self.choice}. Твоя ставка монет {self.money}. Твой выйгрыш {self.money * self.dict_x[self.choice]}', value=' **Поздравляю тебя!** ')
            emb_text.set_thumbnail(file=File(fp=r'Pictures\top.jpg'))
        
            await self.ctx.send(embed=emb_text, ephemeral=True) 
        
        
        # Если игрок проиграл
        elif self.flag == 'Lose':
            await offBalance(self.guild.id, self.ctx.author.id, self.money)
            
            emb_text = disnake.Embed(colour=Colour.dark_gray())
            emb_text.add_field(name=f'Тебе не повезло! Ты проиграл {self.money} монет...', value=' **В следующий раз получится?! :)** ')
            emb_text.set_thumbnail(file=File(fp=r'Pictures\bad.jpg'))
        
            await self.ctx.send(embed=emb_text, ephemeral=True)
            

class BindCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
        
    # Команды для начала игры
    @commands.slash_command(description='Попробуй выйграть ставку!')
    async def casino(self, inter: CmdInter, money: int) -> None:
        await inter.response.defer()
        if money <= 0:
            return await inter.delete_original_response()
        
        if await moneyCheck(inter.guild.id, inter.author.id, money):
            return await inter.send(f'{inter.author.mention}, у тебя на балансе нет {money} монет!', ephemeral=True)
            
        view = SelectButtonColour()
        title = f'{inter.author.mention}, выбери умножения твоей суммы при победе. Чем больше ставка тем меньше шанс выйграть!'
        
        await inter.send(title, view=view, ephemeral=True)
        await view.wait()   # ждём ответа от участника
        
        
        game = Gaming(inter.guild, inter, view.choice, money)
        await game.flags()
        
        

def setup(bot: commands.Bot) -> None:
    bot.add_cog(BindCog(bot))