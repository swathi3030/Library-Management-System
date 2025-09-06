# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

import db  # your file with the DB functions

app = FastAPI()

# Book schema
class Book(BaseModel):
    title: str
    price: float
    copies: int

class UpdateBook(BaseModel):
    title: Optional[str] = None
    price: Optional[float] = None
    copies: Optional[int] = None

@app.on_event("startup")
def startup():
    db.create_table()

@app.post("/books/")
def create_book(book: Book):
    book_id = db.add_book(book.dict())
    if book_id:
        return {"id": book_id}
    raise HTTPException(status_code=500, detail="Failed to add book.")

@app.get("/books/")
def list_books():
    return db.get_books()

@app.put("/books/{book_id}")
def update_book(book_id: int, book: UpdateBook):
    updated = db.update_book(book_id, {k: v for k, v in book.dict().items() if v is not None})
    if updated:
        return {"updated": updated}
    raise HTTPException(status_code=404, detail="Book not found or nothing to update.")

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    deleted = db.delete_book(book_id)
    if deleted:
        return {"deleted": deleted}
    raise HTTPException(status_code=404, detail="Book not found.")
