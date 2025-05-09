import os

class Settings:
    def __init__(self):
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.debug = os.getenv("DEBUG", "true").lower() in ("true", "1", "t")
        self.host = os.getenv("HOST", "0.0.0.0")
        self.port = int(os.getenv("PORT", 8001))
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///./test.db")

settings = Settings()