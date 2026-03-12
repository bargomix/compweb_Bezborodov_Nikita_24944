from fastapi import FastAPI

from app.database import engine, SessionLocal, Base
from app.table_model import Quote
from app.parser import pagination_parse


app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/parse")
def run_parser(url: str):
    quotes = pagination_parse(url)

    db = SessionLocal()
    try:
        db.query(Quote).delete()
        db.commit()

        for item in quotes:
            quote = Quote(
                text=item["text"],
                author=item["author"],
                author_link=item["author_link"],
                tags=item["tags"],
            )
            db.add(quote)

        db.commit()

        return {
            "status": "ok",
            "saved": len(quotes)
        }
    finally:
        db.close()


@app.get("/quotes")
def get_quotes():
    db = SessionLocal()
    try:
        quotes = db.query(Quote).all()

        result = []
        for q in quotes:
            result.append(
                {
                    "id": q.id,
                    "text": q.text,
                    "author": q.author,
                    "author_link": q.author_link,
                    "tags": q.tags,
                }
            )

        return result
    finally:
        db.close()