import configparser
from pydantic_settings import BaseSettings
import urllib.parse

config = configparser.ConfigParser()
config.read("dev.conf")

RAPIDAPI_KEY = config.get("Rapid Api", "RAPIDAPI_KEY")
RAPIDAPI_HOST = config.get("Rapid Api", "RAPIDAPI_HOST")

SECRET_KEY = config.get("Jwt", "SECRET_KEY")
ALGORITHM = config.get("Jwt", "ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = config.get("Jwt", "ACCESS_TOKEN_EXPIRE_MINUTES")
REFRESH_TOKEN_EXPIRE_DAYS =  config.get("Jwt", "REFRESH_TOKEN_EXPIRE_DAYS")