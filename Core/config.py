from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME :str
    USER_ID:str
    MOBILE_NO:str
    CLIENT_ID:str
    SECRET_KEY:str
    APP_PIN:str
    TOTP_KEY:str
    
    class Config:
        env_file = ".env"

setting = Settings()