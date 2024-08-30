import random
import disnake

from datetime import datetime as dt
from disnake.ext import commands

from bot.scripts.getters import Get


class Bored(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.get = Get()
        
    
    @commands.cooldown(1, 5,  commands.BucketType.user)
    @commands.slash_command(description='Чем заняться когда скучно?')
    async def bored(self, inter: disnake.CmdInter): 
        embed = disnake.Embed(
            description=await self.get.get_bored_phrase(),
            colour=disnake.Colour.blue(),
            timestamp=dt.now()
        )
        await inter.send(embed=embed, ephemeral=True)
        
                
        
def setup(bot: commands.Bot):
    bot.add_cog(Bored(bot))