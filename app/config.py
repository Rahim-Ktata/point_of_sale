
from pydantic_settings import BaseSettings, SettingsConfigDict


# this class will go and find the env variables
# it'll seartch for database_hostname | DATABASE_HOSTNAME
# u can set defaults so no err when it don't find sth in env vars
# if no defaults and no env var found => ValidationError
class Settings(BaseSettings):
    database_hostname: str= "localhost"
    database_port: str= "5432"
    database_password: str= ""
    database_name: str= "pos_db"
    database_username: str= "postgres"


    mail_username: str= "abdouktata2@gmail.com"
    mail_password: str= "pcwn ujmu viqs xxxx"
    mail_from: str= "abdouktata2@gmail.com"
    mail_server: str= "smtp.gmail.com"
    mail_port: int=587

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
