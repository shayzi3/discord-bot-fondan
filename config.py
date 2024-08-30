import os

from dotenv import load_dotenv


class Secrets:
    load_dotenv()
    
    token: str = os.environ.get('token')    
    
secret = Secrets()

