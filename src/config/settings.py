from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    azure_openai_endpoint: str
    azure_openai_api_key: str
    azure_deployment_name: str
    sqlite_db_path: str = "database.sqlite"
    
    class Config:
        env_file = ".env"

settings = Settings()