import random
import disnake

from datetime import datetime as dt
from disnake.ext import commands

from bot.scripts.bored_member.get_phrase import GetPhrase


class BoredMember(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.get_phrase = GetPhrase()
        
    
    @commands.cooldown(1, 5,  commands.BucketType.user)
    @commands.slash_command(description='Чем заняться когда скучно?')
    async def bored(self, inter: disnake.CmdInter): 
        embed = disnake.Embed(
            description=await self.get_phrase.bored_phrase(),
            colour=disnake.Colour.blue(),
            timestamp=dt.now()
        )
        await inter.send(embed=embed, ephemeral=True)
        
        
        
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.slash_command(description='Рандомный участник.')
    async def random_member(self, inter: disnake.CmdInter, text: str  = None):
        member = random.choice([mem for mem in inter.guild.members]).mention
        
        embed = disnake.Embed(
            description=f'{text} - {member}' if text else member,
            colour=disnake.Colour.blue(),
            timestamp=dt.now()
        )
        await inter.send(embed=embed, delete_after=300)
        
                
        
        
        
def setup(bot: commands.Bot):
    bot.add_cog(BoredMember(bot))