from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from utils import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME

Base = declarative_base()


class Qrcode(Base):
    __tablename__ = 'qrcodes'

    id = Column(Integer, primary_key=True)
    active = Column(Boolean)

    def __init__(self, id, active):
        self.id = id
        self.active = active


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50))
    name = Column(String(50))
    phone = Column(String(50))
    qrcode_id = Column(Integer, ForeignKey('qrcodes.id'))
    created_at = Column(DateTime, default=func.current_timestamp())

    qrcode = relationship("Qrcode")


engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}')
Session = sessionmaker(bind=engine)
session = Session()


class QrcodeDAO:
    def select(self, id):
        return session.query(Qrcode).filter(Qrcode.id == id).first()

    def insert_into(self, id, active):
        instance = Qrcode(id=id, active=active)
        session.add(instance)
        session.commit()

    def update(self, qrcode_id, **kwargs):
        instance = session.query(Qrcode).get(qrcode_id)
        if instance:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            session.commit()
        else:
            raise Exception("Qrcode not found")


class UserDAO:
    def select(self):
        return session.query(User).all()

    def insert_into(self, user_id, name, phone, qrcode_id):
        instance = User(user_id=user_id, name=name, phone=phone, qrcode_id=qrcode_id)
        session.add(instance)
        session.commit()

    def update(self, user_id, **kwargs):
        instance = session.query(User).filter_by(user_id=user_id).first()
        if instance:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            session.commit()
        else:
            raise Exception("User not found")
