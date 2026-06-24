from pydantic import BaseModel
from typing import Optional


# Pydantic model = auto-validation
class Book(BaseModel):
    title: str
    author: str
    year: int
    genre: Optional[str] = None


# For PATCH: every field optional, since the client may only send a few of them
class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    genre: Optional[str] = None


# In-memory store
db: dict[int, dict] = {}
next_id: int = 1


def seed_data():
    """Populate db with a small set of fake books for testing."""
    global next_id

    fake_books = [
        Book(title="The Hobbit", author="J.R.R. Tolkien", year=1937, genre="Fantasy"),
        Book(title="Dune", author="Frank Herbert", year=1965, genre="Science Fiction"),
        Book(title="The Hidden Hand", author="Frank Herbert", year=1973, genre="Science Fiction"),
        Book(title="1984", author="George Orwell", year=1949, genre="Dystopian"),
        Book(title="Animal Farm", author="George Orwell", year=1945, genre="Satire"),
        Book(title="The Silent Patient", author="Alex Michaelides", year=2019, genre=None),
    ]

    for book in fake_books:
        db[next_id] = book.dict() | {"id": next_id}
        next_id += 1
