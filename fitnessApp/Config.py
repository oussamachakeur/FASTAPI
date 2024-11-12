from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_url : str
    SECRET_KEY: str
    ALGORITHM: str 
    ACCESS_TIME: int

    class Config :
        env_file = "/Users/lenovo/Desktop/oop/fitnessApp/.env"



settings = Settings()