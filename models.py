from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base, engine
from pydantic import BaseModel, constr
import uuid
from sqlalchemy.sql.expression import text

class post(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True,
         server_default=text("uuid_generate_v4()"))
     # to run uuid_generate_v4 first write this code in pgadmin posts table
     #CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    title = Column(String(60), index=True, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False,
        server_default= func.now())
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id",
        ondelete="CASCADE"),nullable=False)
     # can write server_default= text('now()') instead of func.now()
     #and to import:  from sqlalchemy.sql.expression import text
    owner = relationship("ap")


class ap(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key= True,
        server_default=text("uuid_generate_v4()"))
    name = Column(String(32), nullable= False)
    password = Column(String, nullable= False)
    time = Column(DateTime(timezone=True), server_default= func.now())
    items = Column(ARRAY(String))


Base.metadata.create_all(bind=engine)
