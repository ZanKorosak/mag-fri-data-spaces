from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ADDRESS: str = "lds.cjvt.si"

settings = Settings()