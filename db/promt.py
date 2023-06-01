from sqlalchemy import Column, BigInteger, Integer, Boolean, ForeignKey, String
from sqlalchemy.orm import relationship
from db.base import Base


class Promt(Base):
    __tablename__ = 'promts'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    text = Column(String, nullable=False)
    user = Column(String, nullable=True)

