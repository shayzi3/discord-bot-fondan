import disnake

from disnake import ButtonStyle

from bot.utils.casino.schemas import Choice




class SetColur(disnake.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=120.0) 
        self.choice: Choice | None = None
        
        
    @disnake.ui.button(label='x2', emoji='❤️', style=ButtonStyle.red)
    async def button1(self, button: disnake.ui.Button, inter: disnake.CmdInter) -> None:
        await inter.response.defer()
        await inter.delete_original_response()
                
        self.choice = Choice.RED
        self.stop()
        
        
    @disnake.ui.button(label='x3', emoji='💚', style=ButtonStyle.green)
    async def button2(self, button: disnake.ui.Button, inter: disnake.CmdInter) -> None:
        await inter.response.defer()
        await inter.delete_original_response()
        
        self.choice = Choice.GREEN
        self.stop()
        
        
    @disnake.ui.button(label='x4', emoji='🩶', style=ButtonStyle.gray)
    async def button3(self, button: disnake.ui.Button, inter: disnake.CmdInter) -> None:
        await inter.response.defer()
        await inter.delete_original_response()
        
        self.choice = Choice.GRAY
        self.stop()