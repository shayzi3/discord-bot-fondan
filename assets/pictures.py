
import random


class Picture:
     def __init__(self) -> None:
          self.bot_images = [
               r'assets\bot_images\avatar.gif',
               r'assets\bot_images\banner.gif',
               r'assets\bot_images\cupcake.png'
          ]
     
     
     @property
     def get_random_bot_images(self):
          return random.choice(self.bot_images)


     
     
picture = Picture()