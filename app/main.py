import httpx

from typing import Dict, List, Optional

from fastapi import FastAPI, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, RedirectResponse

from pydantic import BaseModel

# Structures for requests & responses
class Book(BaseModel):
    authors: List[str]
    description: str
    isbn: str
    title: str

class Books(BaseModel):
    result: Dict[str, Book]

app = FastAPI()

# Constrain query results & return only this data
fields = "&fields=".join(['', 'authors', 'description', 'isbn', 'title'])
cache = {}

@app.on_event("startup")
async def hydrate_cache():
    async with httpx.AsyncClient() as client:
        query_string = f"https://learning.oreilly.com/api/v2/search/?query=python&formats=book{fields}"
        response = await client.get(query_string)
        cache.update({ book["isbn"]: book for book in response.json()["results"] })

@app.get("/books", response_model=Books)
async def get_books():
    if cache is not None:
        print('Returning cached result')
        return JSONResponse(content=cache)
    else:    
        async with httpx.AsyncClient() as client:
            print('Fetching data from remote')
            await hydrate_cache()
            return JSONResponse(content=cache.values())

@app.get("/books/{isbn}", response_model=Book)
async def get_book(isbn: str):
    if cache is not None:
        print('Returning cached result')
        try:
            return JSONResponse(content=cache[isbn])
        except KeyError:
            return Response(status_code=404)
    async with httpx.AsyncClient() as client:
        print('Fetching data from remote')
        query_string = f"https://learning.oreilly.com/api/v2/search/?query={isbn}&field=isbn{fields}"
        try:
            res = await client.get(query_string)
            book = { isbn: res.json()["results"][0] }
            cache.update(book)
            return JSONResponse(content=book)
        except KeyError as err:
            raise HTTPException(status_code=404, detail="Item not found")

@app.post("/books", response_model=Book, status_code=201)
async def add_book(book: Book):
    print('Adding item to cache')
    cache.update({ book.isbn: { 
        "isbn": book.isbn,
        "authors": book.authors,
        "title": book.title,
        "description": book.description
    }})
    
    return book

# Liveness probe
@app.get("/live", status_code=200)
def liveness_probe():
    pass

@app.get("/ready")
async def readiness_probe(response: Response):
    if cache is not None:
        response.status_code = status.HTTP_200_OK
    else:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    
    return