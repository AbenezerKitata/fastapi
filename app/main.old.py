import psycopg
from fastapi import Depends, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase as Base
from . import models
from .dbConnect import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


DB_URL = "postgresql://myuser:mypassword@localhost:5432/mydatabase"
try:
    conn = psycopg.connect(DB_URL)
    cur = conn.cursor()  # Define the cursor object at the module level
    print("DB connection was successful!")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    exit()


class Media(BaseModel):
    title: str
    content: str
    cool: bool
    rating: int


some_media = [
    {"title": "someFirstTitle", "content": "someFirstContent", "id": 1},
    {"title": "someFirstTitle", "content": "someFirstContent", "id": 2},
]


def findById(id):
    for el in some_media:
        if el["id"] == id:
            return el


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/media")
async def root(db: Session = Depends(get_db)):
    allMedia = db.query(models.Media).all()
    # cur.execute(""" SELECT * FROM media """)
    # allMedia = cur.fetchall()

    return {"message": allMedia}


# This is left to be the last of the
@app.get("/media/{id}")
async def getId(id: int, response: Response, db: Session = Depends(get_db)):
    found = db.query(models.Media).filter(models.Media.id == id).first()
    # cur.execute("""SELECT * FROM media WHERE id= %s """, (id,))
    # found = cur.fetchone()
    if found == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Media with an id of {id} not found",
        )

    # found = findById(id)
    # if not found:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Media with an id of {id} not found",
    #     )
    #     # response.status_code = status.HTTP_404_NOT_FOUND
    #     # return {"message": f"Media with an id of {id} not found"}
    return {"message": found}


@app.post("/media")
async def createComedy(
    payload: Media, response: Response, db: Session = Depends(get_db)
):
    # cur.execute(
    #     """INSERT INTO media (title,content, cool, rating ) VALUES (%s,%s,%s,%s) RETURNING * """,
    #     (payload.title, payload.content, payload.cool, payload.rating),
    # )
    # inserted = cur.fetchone()
    # conn.commit()
    # inserted = models.Media(
    #     title=payload.title,
    #     content=payload.content,
    #     rating=payload.rating,
    #     cool=payload.cool,
    # )
    inserted = models.Media(**payload.model_dump())
    db.add(inserted)
    db.commit()
    db.refresh(inserted)
    response.status_code = status.HTTP_201_CREATED
    # return {"new drama": f"title {payload['title']} content: {payload['content']}"}
    return {"data": inserted}


@app.delete("/media/{id}")
async def deleteMedia(id: int, db: Session = Depends(get_db)):
    found = db.query(models.Media).filter(models.Media.id == id)
    if found.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failed to delete, no item with the id of {id} exists",
        )
    found.delete(synchronize_session=False)
    db.commit()
    raise HTTPException(
        status_code=status.HTTP_204_NO_CONTENT,
        # detail=f"removed item with the id of {id} from Media object", ## Errors will be ignored!
    )

    # cur.execute("""DELETE FROM media WHERE id= %s RETURNING * """, (id,))
    # deleted = cur.fetchone()
    # if deleted != None:
    #     conn.commit()
    #     raise HTTPException(
    #         status_code=status.HTTP_204_NO_CONTENT,
    #         # detail=f"removed item with the id of {id} from Media object", ## Errors will be ignored!
    #     )

    # raise HTTPException(
    #     status_code=status.HTTP_404_NOT_FOUND,
    #     detail=f"Failed to delete, no item with the id of {id} exists",
    # )

    # for item in some_media:
    #     if item["id"] == id:
    #         some_media.remove(item)
    #         raise HTTPException(
    #             status_code=status.HTTP_204_NO_CONTENT,
    #             # detail=f"removed item with the id of {id} from Media object", ## Errors will be ignored!
    #         )
    # raise HTTPException(
    #     status_code=status.HTTP_404_NOT_FOUND,
    #     detail=f"no item with the id of {id} exists",
    # )


@app.put("/media/{id}")
async def update_media(id: int, updated_data: Media, db: Session = Depends(get_db)):
    update_query = db.query(models.Media).filter(models.Media.id == id)
    updated_itm = update_query.first()

    if updated_itm != None:
        update_query.update(updated_data.model_dump(), synchronize_session=False)
        db.commit()
        return {"Updated Media": "SUCCESS!"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No item with the id of {id} exists",
    )
    # cur.execute(
    #     """UPDATE media SET title=%s, content=%s, cool=%s, rating=%s WHERE id=%s RETURNING *""",
    #     (
    #         updated_data.title,
    #         updated_data.content,
    #         updated_data.cool,
    #         updated_data.rating,
    #         id,
    #     ),
    # )
    # updatedItm = cur.fetchone()
    # if updatedItm != None:
    #     conn.commit()

    #     return {"Updated Media": updatedItm}

    # raise HTTPException(
    #     status_code=status.HTTP_404_NOT_FOUND,
    #     detail=f"No item with the id of {id} exists",
    # )
    # for item in some_media:
    #     if item["id"] == id:
    #         item.update(updated_data)
    #         return {"updatedMedia": some_media}
    # raise HTTPException(
    #     status_code=status.HTTP_404_NOT_FOUND,
    #     detail=f"No item with the id of {id} exists",
    # )
