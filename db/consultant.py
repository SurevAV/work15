from sqlalchemy import Column, BigInteger, String
from db.base import Base


class Consultant(Base):
    __tablename__ = 'consultants'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    owner = Column(String, nullable=True)
    channel = Column(String, nullable=True)
    promt = Column(String, nullable=True)
