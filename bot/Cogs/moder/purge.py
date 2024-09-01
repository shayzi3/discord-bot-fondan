import disnake

from disnake.ext import commands

from bot.utils.box import box


class Purge(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
    
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.slash_command(description='Удаление сообщений')
    async def purge(self, inter: disnake.CmdInter, amount: int) -> None:
        await inter.channel.purge(limit=amount)
        
        embed = await box(
            title=f'✅ Удалено {amount} сообщений.',
            name_author=inter.author.name,
            icon_author=inter.author.avatar
        )
        await inter.send(embed=embed, delete_after=300)



def setup(bot: commands.Bot) -> None:
    bot.add_cog(Purge(bot))