from fastapi import APIRouter


router = APIRouter()


@router.get("/users/")
async def read_user():
    return {"Hello world"}
