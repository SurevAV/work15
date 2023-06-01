from sqlalchemy import Column, BigInteger, Integer, Boolean, ForeignKey, String
from sqlalchemy.orm import relationship
from data import Config
from db.base import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    balance = Column(Integer, default=Config.TOKENS_FOR_NEW_USER)
    is_admin = Column(Boolean, default=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    idTelegram = Column(String, nullable=True)

    #referral_id = Column(ForeignKey('users.id'), nullable=True)
    #referral = relationship("User", backref='referrals', remote_side="User.id")
