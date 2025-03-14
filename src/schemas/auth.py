from pydantic import BaseModel


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    authjwt_algorithm: str = "HS256"
    authjwt_token_location: set = {"cookies"}
    authjwt_access_token_expires: int = 3600


class UserLogin(BaseModel):
    username: str
    password: str
