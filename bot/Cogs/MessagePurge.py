import disnake

from disnake.ext import commands
from disnake import CmdInter


class PurgeMessage(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
    # Команда для удаления сообщений
    @commands.slash_command(description='Удаление сообщений')
    async def purge(self, inter: CmdInter, amount: int) -> None:
        await inter.channel.purge(limit=amount)     # Удаление сообщений
        
        emb = disnake.Embed(title=f'✅ Удалено {amount} сообщений.', colour=disnake.Colour.green())
        emb.set_footer(text=inter.author.name, icon_url=inter.author.avatar)
        await inter.send(embed=emb, delete_after=20.0)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(PurgeMessage(bot))