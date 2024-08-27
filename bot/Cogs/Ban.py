import disnake

from typing import Optional
from datetime import datetime as dt
from disnake.ext import commands
from disnake import CmdInter
from loguru import logger


class BanCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
    # Команда для бана участника
    @commands.slash_command(description='Забанить участника сервера.')
    async def banned(self, inter: CmdInter, member: disnake.Member, *, reason: str) -> None:
        emb = disnake.Embed(
            title = f'{inter.author.name}, забанил {member.name}.',
            timestamp = dt.now(),
            colour = disnake.Colour.dark_blue()
        )
        
        if inter.author.id != member.id:
            await inter.guild.ban(member, reason = reason)   # Баним участника
            logger.info(f'{member.name} was ban on server {inter.guild.name}')
                
            await inter.send(embed = emb)
        
            
    # Команда для разбана участника
    @commands.slash_command(description='Разбанить участника')
    async def unbanned(self, inter: CmdInter, member: disnake.User) -> None:
        if inter.author.id != member.id:  
            await inter.guild.unban(member)   # Разбаниваем участника
            logger.info(f'{member.name} unban on server {inter.guild.name}')
                
            emb = disnake.Embed(
                title = f'{inter.author.name}, разбанил {member.name}.', 
                timestamp = dt.now(),
                colour = disnake.Colour.dark_blue()
            )
            await inter.send(embed = emb)
            
            
    # Команда для кика участника
    @commands.slash_command(description='Кмкнуть участника')
    async def kicked(self, inter: CmdInter, member: disnake.Member) -> None:
        if inter.author.id != member.id:
            await inter.guild.kick(member)   # Кикаем участника сервера
            logger.info(f'{member.name} kick from server {inter.guild.name}')
            
            emb = disnake.Embed(
                title = f'{inter.author.name}, кикнул {member.name}.', 
                colour = disnake.Colour.dark_blue(), 
                timestamp = dt.now())
                
            await inter.send(embed = emb) 
            
            
def setup(bot: commands.Bot) -> None:
    bot.add_cog(BanCog(bot))
    
    