from string import ascii_letters
from disnake.ext import commands
from disnake import MessageCommandInteraction

from database.src.json.base import json_funcs



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
                    return await message.channel.send(title, delete_after=120) 
            
            await json_funcs.update_member(member=message.author)
                
        
        
def setup(bot: commands.Bot) -> None:
    bot.add_cog(Messages(bot))
