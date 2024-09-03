import disnake

from disnake.ext import commands



class Errors(commands.Cog):
     def __init__(self, bot: commands.Bot):
          self.bot = bot
          
          
     @commands.Cog.listener()
     async def on_slash_command_error(self, inter: disnake.CmdInter, error: commands.CommandError) -> None:
          if isinstance(error, commands.CommandOnCooldown):
               await inter.send(f'Команду **/{inter.application_command.name}** можно использовать **{error.cooldown.rate} раз** каждые **{int(error.cooldown.per)}с**. Ещё осталось **{error.retry_after:.2f}с**', ephemeral=True)
     
        
        
def setup(bot: commands.Bot):
     bot.add_cog(Errors(bot))
        
        
     