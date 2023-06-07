from db.base import Base
from sqlalchemy import Column, BigInteger, String, DateTime

class Consultant(Base):
    __tablename__ = 'consultants'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    owner = Column(String, nullable=True)
    channel = Column(String, nullable=True)
    promt = Column(String, nullable=True)
    untilDate = Column(DateTime, nullable=True)
