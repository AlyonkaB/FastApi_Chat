from pydantic import BaseModel


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"  # Ваш секретний ключ
    authjwt_algorithm: str = "HS256"  # Алгоритм підпису
    authjwt_access_token_expires: int = 3600


class UserLogin(BaseModel):
    username: str
    password: str
