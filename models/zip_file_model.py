from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from models.database import Base


class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    content = relationship(
        "Content", back_populates="file", cascade="all, delete-orphan"
    )

    def as_dict(self) -> dict:
        return {'id': self.id, 'file': self.name}

    def __repr__(self):
        return f"File(id={self.id!r}, name={self.name!r})"


class Content(Base):
    __tablename__ = "files_content"
    id = Column(Integer, primary_key=True)
    path = Column(String)
    size = Column(String)
    file_id = Column(Integer, ForeignKey("files.id"), nullable=False)

    file = relationship("File", back_populates="content")

    def as_dict(self) -> dict:
        return {'path': self.path, 'size': self.size}

    def __repr__(self):
        return f"Content(id={self.id!r}, path={self.path!r}, size={self.size}, file_id={self.file_id})"
