import disnake

from disnake.ext import commands
from loguru import logger

from config import secret



bot = commands.Bot(
    command_prefix = '-', 
    help_command = None, 
    intents = disnake.Intents.all(),
    activity = disnake.Activity(name='Нарды'),
    test_guilds=[1198187444684734505 ],
    reload=True
)



@bot.event
async def on_ready():
    logger.info(f'Bot {bot.user.name} ready!')    
    bot.load_extensions('bot/Cogs/')
        
            
    

if __name__ == '__main__':
    bot.run(secret.token)
   

