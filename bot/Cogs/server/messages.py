from string import ascii_letters

from disnake.ext import commands
from disnake import MessageCommandInteraction
from disnake import DMChannel

from database.src.db.schemas import BaseMode
from database.src.db.base import data_funcs
from database.src.json.base import json_funcs
from bot.utils.box import box



class Messages(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
        self.letters = 'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ' + ascii_letters.upper()
        
    
    @commands.Cog.listener()
    async def on_message(self, message: MessageCommandInteraction) -> None:
        await self.bot.process_commands(message)
        
        if message.author.id != self.bot.user.id:
            msg = message.content.replace(' ', '')
            
            if len(msg) >= 5:
                if len(msg.strip(self.letters)) <= 1:
                    await message.delete()
                        
                    title = f'{message.author.mention}, использование CAPS запрещено❗'
                    return await message.channel.send(title, delete_after=120.0) 
            
            if not isinstance(message.channel, DMChannel):
                await json_funcs.update_member(member=message.author)
                
            count_messages = await json_funcs.get_member_messages(member_id=message.author.id)
            if count_messages % 100 == 0:
                await data_funcs.balance(
                    id_guild=message.guild.id,
                    id_member=message.author.id,
                    cash=35,
                    mode=BaseMode.ON
                )
                await message.author.send(
                    embed=await box(
                        title=f'📱 Ты накопил {count_messages} сообщений! Получай 35 монет.'
                    )
                )
                
        
        
def setup(bot: commands.Bot) -> None:
    bot.add_cog(Messages(bot))
