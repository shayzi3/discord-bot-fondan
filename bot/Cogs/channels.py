import asyncio

import disnake

from disnake.ext import commands
from loguru import logger

# Создание таймера для удаления канала по истечению 5 часов
async def timer(channel, name: str):
    await asyncio.sleep(5 * 3600)
            
    await channel.delete()
    logger.info(f'Channel {name} deleted.')


class CreateChannelCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @commands.cooldown(1, 3600, commands.BucketType.user)   # Использовать команду можно 2 раза. Перезарядка 2 часа
    @commands.slash_command(description='Создание приватного текстового или голосового канала(text, voice)')
    async def creator(self, inter: disnake.CmdInter, *, name: str, mode: str, member: disnake.Member):
        # Подключение прав для канала
        overwrites = {
            inter.guild.default_role: disnake.PermissionOverwrite(read_messages=False),
            member: disnake.PermissionOverwrite(read_messages=True)
        }
        
        if mode == 'text':
            channel = await inter.guild.create_text_channel(name=name, overwrites=overwrites)  # Создание текстового канала
            logger.info(f'Created text channel for {inter.author.name} and {member.name}')
            
            return await inter.send(f'Текстовый канал {name} создан успешно для вас и {member.name}!', ephemeral=True, delete_after=600.0)
        
        channel = await inter.guild.create_voice_channel(name=name, overwrites=overwrites)   # Создание голосовго канала
        await inter.send(f'Голосовой канал {name} создан успешно для вас и {member.name}!', ephemeral=True, delete_after=600.0)
        
        logger.info(f'Created voice channel for {inter.author.name} and {member.name}')
            
        await timer(channel, name)
        
    # Обработка ошибки
    @creator.error
    async def creator_error(self, inter: disnake.CmdInter, error):
        if isinstance(error, commands.CommandOnCooldown):
            await inter.send('Команду можно использовать только 1 раз. Перезарядка 1 час.', ephemeral=True, delete_after=5 * 60)
            

def setup(bot: commands.Bot):
    bot.add_cog(CreateChannelCog(bot))