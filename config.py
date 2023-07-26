from pydantic import BaseSettings


class Settings (BaseSettings):
    DB_HOSTNAME : str
    DB_PASSWORD : str
    DB_USERNAME : str
    DB_URL : str
    DB_PORT : str
    DB_NAME : str
    SECRET : str
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRY_MINUTES : int = 30

    class Config :
        env_file = "pythonCode/.env"

Setting = Settings()
