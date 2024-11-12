from pydantic_settings import BaseSettings



class settings(BaseSettings):
    DB_URL : str
    SECRET_KEY : str 
    ALGORITHM : str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = "/Users/lenovo/Desktop/oop/app/.env"


settings = settings()







