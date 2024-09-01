import disnake

from disnake.ext import commands

from database.src.db.base import data_funcs
from bot.utils.top.select_menu import SelectView
        
        
        
    
class Top(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
        
    @commands.slash_command(description='Топ по балансу')
    async def top(self, inter: disnake.CmdInter) -> None:  
        data = await data_funcs.get_top_balance(id_guild=inter.guild.id)
        await inter.send(view=SelectView(data), ephemeral=True)
            
            
def setup(bot: commands.Bot) -> None:
    bot.add_cog(Top(bot))
    