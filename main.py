from time import time
from enum import Enum

import fastapi
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


class DogCreationModel(BaseModel):
    name: str
    kind: DogType


class DogUpdateModel(BaseModel):
    name: str
    kind: DogType


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/')
async def root():
    ...


@app.get('/post', responses={200: {'model': list[Timestamp]}})
async def get_posts():
    return post_db


@app.post('/post', responses={200: {'model': Timestamp}})
async def create_post():
    post_out = Timestamp(id=len(post_db), timestamp=int(time()))
    post_db.append(post_out)
    return post_out


@app.get('/dog', responses={200: {'model': list[Dog]}})
async def get_dogs(kind: DogType = fastapi.Query(default=None)):
    if kind is None:
        out = (dog for dog in dogs_db.values())
    else:
        out = (dog for dog in dogs_db.values() if dog.kind == kind.value)
    return out


@app.post('/dog', responses={200: {'model': Dog}})
async def create_dog(dog: DogCreationModel = fastapi.Body(...)):
    new_dog = Dog.model_validate({
        **dog.model_dump(),
        'pk': len(dogs_db),
    })
    dogs_db[new_dog.pk] = new_dog
    return new_dog


@app.get('/dog/{pk}', responses={200: {'model': Dog}})
async def get_dog_by_pk(pk: int = fastapi.Path(...)):
    try:
        dog = dogs_db[pk]
    except KeyError:
        return JSONResponse(
            f'No record found for pk {pk}',
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
        )
    return dog


@app.patch('/dog/{pk}', responses={200: {'model': Dog}})
async def update_dog(pk: int = fastapi.Path(...),
                     to_update: DogUpdateModel = fastapi.Body(...)):
    try:
        dog = dogs_db[pk]
    except KeyError:
        return JSONResponse(
            f'No record found for pk {pk}',
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
        )
    dogs_db[pk] = Dog.model_validate({
        **to_update.model_dump(),
        'pk': dog.pk,
    })
    return dogs_db[pk]
