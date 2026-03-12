from sqlalchemy import Column, Integer, Text
from database import Base


class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    author = Column(Text, nullable=False)
    author_link = Column(Text, nullable=False)
    tags = Column(Text, nullable=True)