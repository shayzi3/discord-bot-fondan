import disnake

from disnake import ButtonStyle




class DuelButton(disnake.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=60)
        self.choice: bool | None = None        
        

    @disnake.ui.button(label='Принять', style=ButtonStyle.green)
    async def acccept(self, button: disnake.ui.Button, inter: disnake.CmdInter):
        await inter.send('Ты принял вызов!', delete_after=20.0)
        
        self.choice = True
        self.stop()
        
        
    @disnake.ui.button(label='Отклонить', style=ButtonStyle.red)
    async def reject(self,  button: disnake.ui.Button, inter: disnake.CmdInter):
        await inter.send('Ты отклонил вызов!', delete_after=20.0)
        
        self.choice = False
        self.stop()