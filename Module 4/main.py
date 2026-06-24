from fastapi import FastAPI, HTTPException
from typing import Optional

from models import Book, BookUpdate, db, seed_data
import models

app = FastAPI(title="Book Library API")

seed_data()


@app.get("/v1/books")
def list_books(
    limit: int = 20,
    page: int = 1,
    author: Optional[str] = None,
    year: Optional[int] = None,
    genre: Optional[str] = None,
):
    results = list(db.values())

    # Filters are combinable - each one narrows the results further (AND logic)
    if author is not None:
        results = [b for b in results if b["author"].lower() == author.lower()]

    if year is not None:
        results = [b for b in results if b["year"] == year]

    if genre is not None:
        results = [b for b in results if (b["genre"] or "").lower() == genre.lower()]

    start = (page - 1) * limit
    end = start + limit
    paginated = results[start:end]

    return {
        "data": paginated,
        "page": page,
        "limit": limit,
        "total": len(results),
    }


@app.post("/v1/books", status_code=201)
def create_book(book: Book):
    new_id = models.next_id
    db[new_id] = book.dict() | {"id": new_id}
    models.next_id += 1
    return db[new_id]


@app.get("/v1/books/{book_id}")
def get_book(book_id: int):
    if book_id not in db:
        raise HTTPException(404, "Book not found")
    return db[book_id]


@app.put("/v1/books/{book_id}")
def replace_book(book_id: int, book: Book):
    """Full replace - client must send every field, missing ones are not preserved."""
    if book_id not in db:
        raise HTTPException(404, "Book not found")
    db[book_id] = book.dict() | {"id": book_id}
    return db[book_id]


@app.patch("/v1/books/{book_id}")
def update_book(book_id: int, book: BookUpdate):
    """Partial update - only fields the client actually sent are changed."""
    if book_id not in db:
        raise HTTPException(404, "Book not found")

    # exclude_unset=True means fields the client didn't include are left alone,
    # rather than overwriting them with their default (None)
    updates = book.dict(exclude_unset=True)
    db[book_id].update(updates)
    return db[book_id]


@app.delete("/v1/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    if book_id not in db:
        raise HTTPException(404, "Book not found")
    del db[book_id]
    return None
