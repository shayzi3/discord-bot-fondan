import asyncio

import disnake

from datetime import datetime as dt
from typing import List, Dict, Any, Optional
from disnake.ext import commands
from disnake import TextInputStyle, CmdInter, ButtonStyle
from loguru import logger

class CreateModalEmbed(disnake.ui.Modal):
    def __init__(self) -> None:
        components: List[disnake.ui.TextInput] = [
            
            disnake.ui.TextInput(
                label='Название Embed.',
                placeholder='Заголовок',
                custom_id='title',
                style=TextInputStyle.short,
                max_length=20,
                required=False
            ),
            disnake.ui.TextInput(
                label='Описание Embed.',
                placeholder='Добавьте описание',
                custom_id='description',
                style=TextInputStyle.paragraph,
                max_length=1024,
                required=False
            ),
            disnake.ui.TextInput(
                label='Доп. описание Embed.',
                placeholder='Название; описание',
                custom_id='add_field',
                style=TextInputStyle.paragraph,
                max_length=1024,
                required=False
            ),
            disnake.ui.TextInput(
                label='Добавить картинку в Embed',
                placeholder='Размер; ссылка',
                custom_id='image',
                style=TextInputStyle.paragraph,
                max_length=500,
                required=False
            )
        ] 
        
        super().__init__(title='Создание ембеда.', components=components)
        
        
    # Функция для отправки модального окна
    async def callback(self, inter: CmdInter):
        values: Dict[str: Any] = inter.text_values

        # Embed который запоняет пользователь
        emb = disnake.Embed(
            title=f'{values["title"]}',
            colour=disnake.Colour.random(),
            description=values['description'],
            timestamp=dt.now()
        )
        emb.set_footer(text=inter.author.name, icon_url=inter.author.avatar)
                
        try:
                
            # Если поле add_field не пустое, добавляем его
            if values['add_field']:
                field = list(values['add_field'].split(';'))
                emb.add_field(name=f'{field[0]}', value=field[1])
                
            # Если в поле image не пустое то определяем указанный размер и вставляем в Embed картинку
            if values['image']:
                image = list(values['image'].split(';'))
                if image[0] == 'big':
                    emb.set_image(url=image[1])
                        
                elif image[0] == 'small':
                    emb.set_thumbnail(url=image[1])
                            
            await inter.send(embed=emb)
                
        except Exception as ex:
            logger.error(f'{inter.guild.name} - {ex}')
                
            await inter.send('Ты не правильно заполнил таблицу! /helping → /create_embed', ephemeral=True)  
            
            
       
class CreateEmbedCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
    # Команда для отправления модального окна для заполнения Embed
    @commands.slash_command(description='Создание собственного Embed. Отправка сообщения на время.')
    async def embed(self, inter: CmdInter) -> None:
        await inter.response.send_modal(modal=CreateModalEmbed())
        

def setup(bot: commands.Bot) -> None:
    bot.add_cog(CreateEmbedCog(bot))
    
        