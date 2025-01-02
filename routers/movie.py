
from fastapi import HTTPException, Path, Query, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
from typing import Optional
from user_jwt import validateToken
from bd.database import Session
from models.movie import Movie as ModelMovie
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter

routerMovie = APIRouter()


class BearerJWT(HTTPBearer):
    async def __call__(self, request:Request):
        auth = await super().__call__(request)
        data = validateToken(auth.credentials)
        if data['email']!='victor':
            raise HTTPException(status_code=403, detail='Credenciales incorrectas')        


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default='Titulo de la pelicula',min_length=5, max_length=60)
    overview: str =  Field(default='Descripcion de la pelicula',min_length=15, max_length=60)
    year: int = Field(default=2023)
    raiting: float = Field(ge=1,le=10)
    category: str = Field(default="Categoria",min_length=3,max_length=15)
    
    #def to_dict(self):
        #return {
            #'id': self.id,
            #'title': self.title,
            #'overview': self.overview,
            #'year': self.year,
            #'raiting': self.raiting,
            #'category': self.category,
        #}



@routerMovie.get('/movies',tags=['Movies'], dependencies=[Depends(BearerJWT())]) #ruta con verbo
def get_movies():
    db=Session()
    data=db.query(ModelMovie).all()
    return JSONResponse(content=jsonable_encoder(data))

@routerMovie.get('/movies/{id}',tags=['Movies'], status_code=200) #ruta con verbo // controller net core
def get_movie_by_id(id:int=Path(ge=1,le=100)):
    db=Session()
    data=db.query(ModelMovie).filter(ModelMovie.id ==id).first()
    print(data)
    if not data:
        return JSONResponse(status_code=404, content={'mesage0':'Pelicula no encontrada'})
    return JSONResponse(status_code=200, content=jsonable_encoder(data))
    #for item in movies:
        #if item["id"]==id:
            #return item 
        #return []
    
@routerMovie.get('/movies/',tags=['Movies']) #ruta con verbo // controller net core
def get_movie_by_category(category:str=Query(min_length=3,max_length=15)):
    db=Session()
    data=db.query(ModelMovie).filter(ModelMovie.category ==category).all()
    if not data:
        return JSONResponse(status_code=404, content={'message':'No se encontro la pelicula'})
    return JSONResponse(status_code=200, content=jsonable_encoder(data))
    #return category

@routerMovie.post('/movies/',tags=['Movies'], status_code=201) #ruta con verbo // controller net core 
def create_movie(movie: Movie): #old way in the body
    #movies.append(movie)
    db=Session()
    newMovie=ModelMovie(**movie.dict())
    db.add(newMovie)
    db.commit()
    return JSONResponse(status_code=201,content={'message':'se ha cargado neva pelicula','movie':[movie.dict() for m in movies]})

@routerMovie.put('/movies/{id}',tags=['Movies']) #ruta con verbo // controller net core
def update_movie(id:int, movie: Movie):
    db=Session()
    data=db.query(ModelMovie).filter(ModelMovie.id ==id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message':'No se encontro la pelicula'})        
    data.title=movie.title
    data.overview=movie.overview
    data.year=movie.year
    data.raiting=movie.raiting
    data.category=movie.category
    db.commit()
    return JSONResponse(content={'message':'Se ha actualizado la pelicula'})
            
    #for item in movies:
        #if item["id"]==id:
            #item["title"]=movie.title,
            #item["overview"]=movie.overview,
            #item["year"]=movie.year,
            #item["raiting"]=movie.raiting,
            #item["category"]=movie.category,
            #return JSONResponse(content={'message':'Se ha actualizado la pelicula'})
        
@routerMovie.delete('/movies/{id}',tags=['Movies'], status_code=200) #ruta con verbo // controller net core
def delete_movie(id:int):
    db=Session()
    data=db.query(ModelMovie).filter(ModelMovie.id ==id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message':'No se encontro la pelicula'})    
    db.delete(data)
    db.commit()
    return JSONResponse(content={'message':'Se ha eliminado la pelicula','data':jsonable_encoder(data)})
    #print(movies)
    #for item in movies:
        #if item["id"]==id:            
            #movies.remove(item)
            #print(movies)
            #return JSONResponse(content={'message':'Se ha eliminado la pelicula'})
        #elif item["id"]!=id:            
            #print(movies)
            #return movies