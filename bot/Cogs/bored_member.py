import random
import disnake

from datetime import datetime as dt
from disnake.ext import commands

from bot.scripts.bored_yesno.response import Responses


class AioCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.responses = Responses()
        
        
    @commands.slash_command(description='Чем заняться когда скучно?')
    async def bored(self, inter: disnake.CmdInter):
        await inter.response.defer()
        
        data = await self.responses.api_bored()
        if not data:
            return await inter.send('Не получилось выполнить запрос. Попробуйте позже.', ephemeral=True)
        
        embed = disnake.Embed(
            description=data,
            colour=disnake.Colour.blue(),
            timestamp=dt.now()
        )
        await inter.send(embed=embed, ephemeral=True)
        
        
        
    @commands.slash_command(description='Рандомный участник')
    async def random_member(self, inter: disnake.CmdInter, text: str  = None):
        member = random.choice([mem for mem in inter.guild.members]).mention
        
        embed = disnake.Embed(
            description=f'{text} - {member}' if text else member,
            colour=disnake.Colour.blue(),
            timestamp=dt.now()
        )
        await inter.send(embed=embed, delete_after=300)
        
        
def setup(bot: commands.Bot):
    bot.add_cog(AioCog(bot))