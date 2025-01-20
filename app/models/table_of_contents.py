from sqlalchemy import Column, Integer, String, JSON
from app.models.base import Base

class TableOfContents(Base):
    __tablename__ = "table_of_contents"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(String, index=True, nullable=False)
    content = Column(JSON, nullable=False)  # Store the TOC structure as JSON 