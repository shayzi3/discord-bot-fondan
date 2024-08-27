import os

from dotenv import load_dotenv


class Secrets:
    load_dotenv()
    
    token: str = os.environ.get('token')
    api: str = os.environ.get('api')
    
    
secret = Secrets()

