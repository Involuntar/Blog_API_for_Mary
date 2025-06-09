from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME:str='default' 
    model_config=SettingsConfigDict(env_file='.env')

settings = Settings()