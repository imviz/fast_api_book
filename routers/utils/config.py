import os

from dotenv import find_dotenv, load_dotenv

#
load_dotenv(find_dotenv())

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
