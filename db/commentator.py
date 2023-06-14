from sqlalchemy import Column, BigInteger, Boolean, ForeignKey, String, Integer, DateTime
from db.base import Base


class Commentator(Base):
    __tablename__ = 'commentators'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    usage = Column(Boolean, default=False)
    promt = Column(String, nullable=True)
    channels = Column(String, nullable=True)
    owner = Column(String, nullable=True)
    apiId = Column(Integer, nullable=True)
    apiHash = Column(String, nullable=True)
    stringConnection = Column(String, nullable=True)
    proxyHttp = Column(String, nullable=True)
    proxyIp = Column(String, nullable=True)
    proxyPort = Column(Integer, nullable=True)
    proxyPass = Column(String, nullable=True)
    proxyUser = Column(String, nullable=True)
    is_humanity = Column(Boolean, nullable=True)
    untilDate = Column(DateTime, nullable=True)


