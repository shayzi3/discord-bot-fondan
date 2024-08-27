# Import modules
import asyncio

import disnake
import sqlite3 as sql

from disnake.ext import commands
from disnake import MessageCommandInteraction
from loguru import logger
from numba import prange


logger.add('logging.log', format='{time} {level} {message}', level='ERROR')    # Write logs


# Cog with command event on_message
class MessageCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
        
    # Creating event on_message for interections with chat
    @logger.catch
    @commands.Cog.listener()
    async def on_message(self, message: MessageCommandInteraction) -> None:
        await self.bot.process_commands(message)
        
        if message.author.id != self.bot.user.id:
              
            messages: list[str] = message.content.split()
            summa = 0
                
            for msg in prange(len(messages)):
                for letter in prange(len(messages[msg]) - 1):
                        
                    if messages[msg][letter].isupper():
                        summa += 1
                            
            if summa >= len(''.join(messages)) / 1.5:
                await message.delete()
                    
                title = f'{message.author.mention}, использование CAPS запрещено❗'
                messages = await message.channel.send(title, delete_after=10.0)   # Send 'Use to CAPS forbidden!'
            
        
        
# Adding cog in bot
def setup(bot: commands.Bot) -> None:
    bot.add_cog(MessageCog(bot))
