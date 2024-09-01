import disnake

from disnake.ext import commands

from database.src.db.base import data_funcs
from database.src.db.schemas import BaseMode
from bot.utils.box import box



class Gift(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
        
    @commands.cooldown(1, 7200, commands.BucketType.user)
    @commands.slash_command(description='Подарок!')
    async def gift(self, inter: disnake.CmdInter) -> None:
        await inter.response.defer(ephemeral=True)
        
        await data_funcs.balance(
            id_guild=inter.guild.id,
            id_member=inter.author.id,
            cash=25,
            mode=BaseMode.ON
        )
        
        
        await inter.send(
            embed=await box(
                title='Подарок! 🎁',
                description='**Ты получаешь 25 монет!**'
            ),
            ephemeral=True
        )
        
        
        
        
def setup(bot: commands.Bot) -> None:
    bot.add_cog(Gift(bot))