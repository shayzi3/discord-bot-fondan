import disnake

from disnake.ext import commands

from bot.scripts.getters import Get
from bot.utils.box import box



class Bored(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.get = Get()        
    
    
    @commands.cooldown(1, 5,  commands.BucketType.user)
    @commands.slash_command(description='Чем заняться когда скучно?')
    async def bored(self, inter: disnake.CmdInter): 
        phrase = await self.get.get_bored_phrase()
        
        await inter.send(
            embed=await box(description=phrase), 
            ephemeral=True
        )
        
                
        
def setup(bot: commands.Bot):
    bot.add_cog(Bored(bot))