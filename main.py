from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from bd.database import engine, Base
from routers.movie import routerMovie
from routers.user import routerUser
import uvicorn
import os

app = FastAPI(
    title='Mi primer fast api con python',
    description='Primeros pasos de api',
    version='1.0'    
    )

app.include_router(routerMovie)
app.include_router(routerUser)


Base.metadata.create_all(bind=engine)


@app.get('/',tags=['inicio']) #ruta con verbo
def read_root(): #funcion que se manda llamar
    #return {'hello':'world'} #regresa la respuesta
    return HTMLResponse('<h2>Hola desde fast api</h2>')


if(__name__=='__main__'):
    port = int(os.environ.get('PORT',8000))
    uvicorn.run('main:app',host='0.0.0.0',port=port)