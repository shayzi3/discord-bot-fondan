import disnake

from disnake.ext import commands

from bot.utils.duel.duel_command import DuelCommand

        
        


class Duel(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.duels = DuelCommand()
        
            
        
    @commands.slash_command(description='Брось вызов на дуэль своему другу')
    async def duel(self, inter: disnake.CmdInter, member: disnake.Member) -> None:
        await inter.response.defer(ephemeral=True)
        
        if inter.author.id == member.id:
            return await inter.send(f'{inter.author.mention}, нельзя отправить вызов на дуэль самому себе!', ephemeral=True)
        
        await inter.delete_original_response()
        await self.duels.duel_command(
            author=inter.author,
            member=member,
            bot=self.bot
        )
        
        
            
            
def setup(bot: commands.Bot) -> None:
    bot.add_cog(Duel(bot))
    