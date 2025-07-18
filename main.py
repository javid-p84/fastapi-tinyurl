from fastapi import Depends, HTTPException
from fastapi import FastAPI, status, Request
from pydantic import BaseModel
from pydantic import BaseModel
from typing import Annotated
from database import engine, SessionLocal
from sqlalchemy.orm import Session
# from .models import User as MyUser
import models
import hashlib
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class ItemBase(BaseModel):
    url: str
    user_id: int


class UserBase(BaseModel):
    username: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
templates = Jinja2Templates(directory="templates")


@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemBase, db: db_dependency):
    db_item = models.Item(**item.model_dump())
    db_item.code = hashlib.sha256(item.url.encode('utf-8')).hexdigest()[:5]
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return "http://localhost:8000/i/{}".format(db_item.code)


@app.get("/i/{code}", response_class=HTMLResponse)
async def get_item(request: Request,code: str, db: db_dependency):
    print("Code received:", code)
    item = db.query(models.Item).filter(models.Item.code == code).first()
    if not item:
        return templates.TemplateResponse(
            request=request,
            name="notfound.html",
            context={"some_data": "This is passed to the template"}
        )
    return '<meta http-equiv="refresh" content="0;url={}">'.format(item.url)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"some_data": "This is passed to the template"}
        )

# items = []

# class Item(BaseModel):
#     text : str
#     is_done: bool = False


# @app.get("/")
# def root():
#     return {"Hello": "World"}

# @app.post("/items/")
# def create_item(item: Item):
#     items.append(item)
#     return items

# @app.get("/items/", response_model=list[Item])
# def read_items(limit:int = 10, offset: int = 0):
#     return items[offset:offset + limit]

# @app.get("/items/{item_id}", response_model=Item)
# def read_item(item_id: int) -> Item:
#     if item_id < 0 or item_id >= len(items):
#         raise HTTPException(status_code=404, detail="Item not found")
#     return  items[item_id]
