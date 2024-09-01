import disnake




async def get_dict_models(
     user: disnake.Member,
     balance: int,
     roles: str,
     msg: int
) -> tuple[dict]:
     pages = 5
     
     model = {
          '1': {
               'text_footer': f'1/{pages}',
               'title': f'Карточка {user.name}',
               'thumbnail_url': user.avatar.url,
               'fields': (
                    ('Nickname', user.name, False),
                    ('ID', user.id, False)
               )
          },
          '2': {
               'text_footer': f'2/{pages}',
               'title': f'Карточка {user.name}',
               'thumbnail_url': user.avatar.url,
               'fields': (
                    ('Created Account', user.created_at.strftime("%d-%m-%Y %H:%M:%S"), False),
                    ('Joined', user.joined_at.strftime("%d-%m-%Y %H:%M:%S"), False)
               )
          },
          '3': {
               'text_footer': f'3/{pages}',
               'title': f'Карточка {user.name}',
               'thumbnail_url': user.avatar.url,
               'fields': (
                    ('Balance', balance, False),
                    ('Roles', roles, False)
               )
          },
          '4': {
               'text_footer': f'4/{pages}',
               'title': f'Карточка {user.name}',
               'thumbnail_url': user.avatar.url,
               'fields': (
                    ('Bot', user.bot, False),
                    ('Messages', msg, False)
               )
          }
     }
     return model