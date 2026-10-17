
from pydantic_settings import BaseSettings, SettingsConfigDict


# this class will go and find the env variables
# it'll seartch for database_hostname | DATABASE_HOSTNAME
# u can set defaults so no err when it don't find sth in env vars
# if no defaults and no env var found => ValidationError
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    test_db_name: str
    database_username: str

    mail_username: str
    mail_password: str
    mail_from: str
    mail_server: str
    mail_port: int

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file="app/.env")
    TEST_DB_URL: str

# settings = Settings(_env_file='app/.env')
settings = Settings()
