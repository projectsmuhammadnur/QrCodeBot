from sqlalchemy import Column, String, Sequence, Boolean, Integer

from db import db
from db.utils import CreatedModel

db.init()


class User(CreatedModel):
    __tablename__ = 'users'
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    chat_id = Column(String(30))
    fullname = Column(String(255))
    phone_number = Column(String(20))
    qr_code_id = Column(String(10))


class QrCode(CreatedModel):
    __tablename__ = 'qr_codes'
    id = Column(Integer, primary_key=True)
    active = Column(Boolean, default=False)
