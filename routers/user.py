from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, JSONResponse
from user_jwt import createToken

routerUser = APIRouter()

class User(BaseModel):
    email:str
    password:str


@routerUser.post('/login', tags=['authentication'])
def login(user: User):
    if user.email=='victor' and user.password == '123':
        token:str = createToken(user.dict())
        print(token)
        return JSONResponse(content=token)


