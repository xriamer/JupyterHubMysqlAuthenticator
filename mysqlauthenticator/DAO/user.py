# coding:utf-8
from sqlalchemy import Column, String
from mysqlauthenticator.DAO.base import Base


class User(Base):

    __tablename__ = 'sy_user'

    user_id = Column(String(20), primary_key=True)
    user_code = Column(String(32), nullable=False, unique=True)
    pass_word = Column(String(1024), nullable=False)
