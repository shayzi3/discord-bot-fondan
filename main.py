import disnake

from disnake.ext import commands
from loguru import logger

from config import secret



bot = commands.Bot(
    command_prefix = '-', 
    help_command = None, 
    intents = disnake.Intents.all(),
    activity = disnake.Activity(name='Нарды', state='Жду твоего сообщения...'),
    test_guilds=[1198187444684734505]
)


@bot.event
async def on_ready():
    logger.info(f'Bot {bot.user.name} ready!')    
    
    bot.load_extensions('bot/Cogs/economy/')
    bot.load_extensions('bot/Cogs/entertainment/')
    bot.load_extensions('bot/Cogs/server/')    
    bot.load_extensions('bot/Cogs/moder/')        


if __name__ == '__main__':
    bot.run(secret.token)
   

