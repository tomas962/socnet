from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    age = Column(Integer)
    username = Column(String(45), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)