import disnake

from typing import Any, Annotated, Callable
from datetime import datetime as dt


AnyType = Annotated[Any, None]
TupleType = Annotated[tuple, None]


async def box(
     title: AnyType = None,
     description: AnyType = None,
     url: AnyType = None,
     name_author: AnyType = None,
     icon_author: AnyType = None,
     image_url: AnyType = None,
     thumbnail_url: AnyType = None,
     text_footer: AnyType = None,
     icon_footer: AnyType = None,
     fields: TupleType = None
) -> disnake.Embed:
          
     embed = disnake.Embed(
          timestamp=dt.now(),
          colour=disnake.Colour.blue(),
          description=description,
          url=url,
          title=title
     )
     embed.set_image(url=image_url)
     embed.set_thumbnail(url=thumbnail_url)
     
     
     if name_author:
          embed.set_author(name=name_author, icon_url=icon_author)
      
     if text_footer:
          embed.set_footer(text=text_footer, icon_url=icon_footer) 
          
     if fields:
          for iter in fields:
               embed.add_field(name=iter[0], value=iter[1], inline=iter[2])         
          
     return embed