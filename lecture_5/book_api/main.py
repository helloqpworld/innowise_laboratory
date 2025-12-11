"""
    Learn to use SQLAlchemy, FastAPI
    Source vidio on YouTube: https://www.youtube.com/watch?v=oMmDTmLDQCg
"""

from typing import Annotated, Optional

from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy import select, delete, or_
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


app = FastAPI()

engine = create_async_engine("sqlite+aiosqlite:///books.db")

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    """Something"""
    async with new_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

class Base(DeclarativeBase):
    """Something"""

class BookModel(Base):
    """Something"""
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]
    year: Mapped[Optional[int]]

class BookAddSchema(BaseModel):
    """Something"""
    title: str
    author: str
    year: int | None

@app.post(path="/setup_database",
          tags=['Endpoints'],
          summary='Overwrite the table or create a new one.')
async def setup_database():
    """Something"""
    async with engine.begin() as conn: # OR async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"ok": True}

@app.post(path="/books",
          tags=['Endpoints'],
          summary='Add a new book.')
async def add_book(data: BookAddSchema, session: SessionDep):
    """Something"""
    new_book = BookModel(
        title=data.title,
        author=data.author,
        year=data.year
    )
    session.add(new_book)
    await session.commit()
    return {"ok": True}

@app.put(path="/book/{book_id}",
         tags=['Endpoints'],
         summary='Update book details by ID.')
async def update_book(book_id: int, data: BookAddSchema, session: SessionDep):
    """Something"""
    # Получить текущий объект
    stmt = select(BookModel).where(BookModel.id == book_id)
    result = await session.execute(stmt)
    book_obj = result.scalar_one_or_none()
    if not book_obj:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    if data.title is not None:
        book_obj.title = data.title
    if data.author is not None:
        book_obj.author = data.author
    if data.year is not None:
        book_obj.year = data.year

    await session.commit()
    return {"UPDATED": True}

@app.get(path="/books",
         tags=['Endpoints'],
         summary='Get all books.')
async def get_books(session: SessionDep):
    """Something"""
    query = select(BookModel)
    result = await session.execute(query)
    return result.scalars().all()

@app.delete(path="/book/{book_id}",
            tags=['Endpoints'],
            summary='Delete a book by ID.')
async def delete_book(book_id: int, session: SessionDep):
    """Something"""
    stmt = delete(BookModel).where(BookModel.id == book_id)
    result = await session.execute(stmt)
    await session.commit()
    if result.rowcount > 0:
        return {"ok": True, "message": f"Book with ID {book_id} deleted."}
    else:
        return {"ok": False, "message": f"Book with ID {book_id} not found."}


@app.get(path="/book/{book_id}",
         tags=['Endpoints'],
         summary='Search books by title, author or year.')
async def search_book(info: str, session: SessionDep):
    """Something"""
    if info.isdigit():
        stmt = select(BookModel).where(BookModel.year == int(info))

    if info is None or info == "null":
        # Поиск записей, где хотя бы одно поле равно NULL
        stmt = select(BookModel).where(or_(
            BookModel.title.is_(None),
            BookModel.author.is_(None),
            BookModel.year.is_(None)
        ))
    else:
        # Стандартный поиск по значению info
        stmt = select(BookModel).where(or_(
            BookModel.title == str(info),
            BookModel.author == str(info),
            BookModel.year == info
        ))

    result = await session.execute(stmt)
    book = result.scalars().all()
    if book != []:
        return book
    return {"ok": False, "message": f"There is NO book with such discription '{info}'."}
