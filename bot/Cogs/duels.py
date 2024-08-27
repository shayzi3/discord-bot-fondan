# Import modules
import asyncio

import disnake
import sqlite3 as sql

from typing import Optional, List
from random import choice
from disnake.ext import commands
from disnake import ButtonStyle, CmdInter, File
from datetime import datetime as dt
from loguru import logger
from other import onBalance


# Button for accept or reject invite on duel
class DuelButton(disnake.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=120.0)   # Wait before stopping the button
        self.choi: Optional[bool] = None  # For determining choice member
        
        
    # Button 'Accept'
    @disnake.ui.button(label='Принять', style=ButtonStyle.green)
    async def acccept(self, button: disnake.ui.Button, inter: CmdInter):
        await inter.response.defer()
        
        title = 'Ты принял вызов!'
        await inter.send(title, delete_after=20.0)  # Send 'U accept duel!'
        
        self.choi = True
        self.stop()   # Stopping the button
        
        
    # Button 'Reject'
    @disnake.ui.button(label='Отклонить', style=ButtonStyle.red)
    async def reject(self,  button: disnake.ui.Button, inter: CmdInter):
        await inter.response.defer()
        
        title = 'Ты отклонил вызов!'
        await inter.send(title, delete_after=20.0)  # Send 'U reject duel!'
        
        self.choi = False
        self.stop()  # Stopping the button
        

# Class for create games
class Gaming:
    def __init__(self, guild: disnake.Guild, author: disnake.Member, member: disnake.Member, bot: commands.Bot) -> None:
        
        # Author (the one who start duel), member and which he choose
        self.author = author
        self.member = member
        
        # For database
        self.guild = guild
        
        # Wait message from player
        self.bot = bot 
        
        
    # Determining who start game (it author)
    async def send_who_first(self) -> None:
        
        # Send embed author. 'U starting this game. For shoot u need enter command in chat !.shoot.
        emb_author = disnake.Embed(
            title=' ```Ты начинаешь игру.``` ', 
            description='!.shoot - чтобы стрельнуть', 
            timestamp=dt.now()
        )
        emb_author.set_image(file=File(fp=r'Pictures\rul.gif'))
            
            
         # Send embed member. 'Game starting {self.author.name}. For shoot u need enter command in chat !.shoot.
        emb_member = disnake.Embed(
            title=f' ```Игру начинает {self.author.name}.``` ',
            description='!.shoot - чтобы стрельнуть',
            timestamp=dt.now()
        )
            
        await self.author.send(embed=emb_author, delete_after=300.0)   # Send self.author
        await self.member.send(embed=emb_member, delete_after=300.0)   # Send self.member
        
        
        # Start game first player
        await self.author_russian()
            
    # First player Russian roulette
    async def author_russian(self):
        
        # Function for check message only from author
        def check(m: disnake.Member) -> bool:
            return m.author == self.author
        
        # Ammo shop for shoots
        global patrons
        global patron_shot
        
        patrons = [1, 2, 3, 4, 5, 6]
        patron_shot = choice(patrons)
        
        '''
        
        Wait that what enter first player
        Check messages, if message player is !.shoot spin the dram
        Watch how spined the dram if bullet shoting that self.author loser
        if not that self.member next
        
        '''
        
        try:
            # Wait 300 seconds messages from player
            message = await self.bot.wait_for('message', check=check,  timeout=300.0)
           
            # If this message !.shoot, that shooting
            if message.content == '!.shoot':
                random = choice(patrons)  # spin the dram
                 
                # If fell out loaded bullet, that author loser
                if random == patron_shot:
                    emb_winner = disnake.Embed(title=f'🔥 Поздравляю, ты выйграл! Ты получаешь 15 монет.', colour=disnake.Colour.dark_magenta())
                    emb_loser = disnake.Embed(title=f'😢 К сожалению, ты проиграл!', colour=disnake.Colour.dark_magenta())
                    
                    
                    await onBalance(self.guild.id, self.member.id, 15)   # Adding member on balance 15 coins
                    
                    await self.member.send(embed=emb_winner, delete_after=120.0)   # Send self.member
                    await self.author.send(embed=emb_loser, delete_after=120.0)    # Send self.author
                    
                    
                # If bullet not loaded, that author not die
                else:
                    # Delete not loaded bullet from self.patrons
                    patrons.remove(random)
                    
                    title_author = f'Тебе повезло, револьвер не выстрелил! Очередь {self.member.name}.'
                    title_member = f'На этот раз {self.author.name} повезло! Твоя очередь!'
                    
                    await self.author.send(title_author, delete_after=300.0)  # Send author 'U lucky, gun not shoot! Shooting self.member'
                    await self.member.send(title_member, delete_after=300.0)  # Send member 'self.author lucky! U shooting.'
                    
                    # Second member
                    await self.member_russian()
                    
            # If player entered not !.shoot
            else:
                await self.author.send('Нужно писать команду !.shoot', delete_after=300.0)  # Send 'Need write command !.shoot'
                
                # Again wait enter command !.shoot from player
                await self.author_russian()
                        
        # Answer if player not wrote command !.shoot
        except Exception as ex:
            logger.error(f'{ex}')
            
            # Send self.author and self.member 'Game over! Because one player not enter command !.shoot'
            title_end = 'Игра прекращена! Потому - что один из игроков так и не написал !.shot.'
            await self.author.send(title_end, delete_after=120.0)  
            await self.member.send(title_end, delete_after=120.0)
            
            
    # Similarly self.author_russian()
    async def member_russian(self) -> None:
        def check(m: disnake.Member) -> bool:
            return m.author == self.member
        
        try:
            message = await self.bot.wait_for('message', check=check,  timeout=300.0)
                
            if message.content == '!.shoot':
                random = choice(patrons)
                
                if random == patron_shot:
                    emb_winner = disnake.Embed(title=f'🔥 Поздравляю, ты выйграл! Ты получаешь +15 монет!', colour=disnake.Colour.dark_magenta())
                    emb_loser = disnake.Embed(title=f'😢 К сожалению, ты проиграл!', colour=disnake.Colour.dark_magenta())
                    
                    await onBalance(self.guild.id, self.author.id, 15)
                    
                    await self.member.send(embed=emb_loser, delete_after=120.0)
                    await self.author.send(embed=emb_winner, delete_after=120.0)
                   
                else:
                    patrons.remove(random)
                    
                    title_member = f'Тебе повезло, револьвер не выстрелил! Очередь {self.author.name}.'
                    title_author = f'На этот раз {self.member.name} повезло! Твоя очередь.'
                    
                    await self.member.send(title_member, delete_after=300.0)
                    await self.author.send(title_author, delete_after=300.0)
                    
                    await self.author_russian()
        
            else:
                await self.member.send('Нужно писать команду !.shoot', delete_after=300.0)
                await self.member_russian()
                        
        except Exception as ex:
            logger.error(f'{ex}')
            
            title_end = 'Игра прекращена! Потому - что один из игроков так и не написал !.shot'
            await self.author.send(title_end, delete_after=120.0)
            await self.member.send(title_end, delete_after=120.0)
        


# Class for command: /duel
class DuelCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
        
    # Command for call duel
    @commands.slash_command(description='Брось вызов на дуэль своему другу.')
    async def duel(self, inter: CmdInter, member: disnake.Member) -> None:
        await inter.response.defer()
        
        if inter.author.id == member.id:
            return await inter.send(f'{inter.author.mention}, нельзя отправить дуэль самому себе!', ephemeral=True, delete_after=60.0)
        
        await inter.delete_original_response()
        
        # Send inter.author
        emb_author = disnake.Embed(title=f'Вызов {member.name} отправлен!', colour=disnake.Colour.dark_magenta())
        msg_author = await inter.author.send(embed=emb_author)
        
        # send member
        emb_member = disnake.Embed(title=f'{inter.author.name} бросил тебе вызов на дуэль!', colour=disnake.Colour.dark_magenta())
        view = DuelButton()
        msg_member = await member.send(embed=emb_member, view=view)
        
        await view.wait()   # Check, what did answer member
        
        # if member accept duel
        if view.choi:
            emb_author = disnake.Embed(title=f'{member.name} принял твой вызов!', colour=disnake.Colour.dark_magenta())
            await msg_author.edit(embed=emb_author)
            
            
            # Start countdown from 10 second
            sec = 5
            emb_timer = disnake.Embed(title=f'До дуэли осталось {sec} секунд!', colour=disnake.Colour.dark_magenta())
                    
            await msg_author.edit(embed=emb_timer)  # Send inter.author
            await msg_member.edit(embed=emb_timer, view=None)  # Send member
                    
            while sec != 0:
                sec -= 1
                        
                # Edit Embed with timer
                emb_timer = disnake.Embed(title=f'До дуэли осталось {sec} секунд!', colour=disnake.Colour.dark_magenta())
                        
                await asyncio.sleep(1)   # Every second edit embed with timer
                        
                await msg_author.edit(embed=emb_timer)  # Edit embed inter.author
                await msg_member.edit(embed=emb_timer)  # Edit embed member
                        
                        
            # Edit embed last time, 'Start duel!'
            emb_end = disnake.Embed(title='Да начнётся же поединок!', colour=disnake.Colour.dark_magenta())    
            await msg_author.edit(embed=emb_end)  # Edit embed inter.author
            await msg_member.edit(embed=emb_end)  # Edit embed member
                    
    
            ex = Gaming(inter.guild, inter.author, member, self.bot)
            await ex.send_who_first()
                         
   
        # If member reject duel
        elif view.choi is False:
            emb_end = disnake.Embed(title=f'{member.name} отклонил твой вызов!', colour=disnake.Colour.dark_magenta())    
            await msg_member.delete()
            await msg_author.edit(embed=emb_end, delete_after=20.0)  # Edit message author '{member.name} reject your call!'
            
        
        # If member ignored on call
        else:
            emb_end = disnake.Embed(title=f'{member.name} тебя проигнорировал!', colour=disnake.Colour.dark_magenta())    
            await msg_author.edit(embed=emb_end, delete_after=20.0)   # Edit message author '{member.name} ignored u!'
            
            emb_end = disnake.Embed(title='Ты игнорщик!', colour=disnake.Colour.dark_magenta())    
            await msg_member.edit(embed=emb_end, view=None, delete_after=20.0)  # Send member 'U ignorman!'
            
# Adding cog in bot
def setup(bot: commands.Bot) -> None:
    bot.add_cog(DuelCog(bot))
    