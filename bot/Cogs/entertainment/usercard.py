import disnake

from disnake.ext import commands
from bot.utils.usercard.pages import Card


        
class Usercard(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot 
        self.card = Card()
        
        
    # Команда для показа карточки участника
    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.slash_command(description='Профиль участника в виде карточки.')
    async def usercard(self, inter: disnake.CmdInter, member: disnake.Member | None = None):
        await inter.response.defer(ephemeral=True)
        
        if member:
            await self.card.usercad(ctx=inter, user=member)
            
        else: 
            await self.card.usercad(ctx=inter)
        


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Usercard(bot))