from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Travel Planner"
    DATABASE_URL: str = "sqlite+aiosqlite:///./travel_planner.db"
    ART_INSTITUTE_API_URL: str = "https://api.artic.edu/api/v1"
    ART_INSTITUTE_TIMEOUT: int = 30
    MAX_PLACES_PER_PROJECT: int = 10

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
