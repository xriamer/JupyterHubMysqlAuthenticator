# coding:utf-8

from jupyterhub.auth import Authenticator
from tornado import gen
from sqlalchemy.orm import sessionmaker
from mysqlauthenticator.DAO.user import User

import os

from mysqlauthenticator.utils.mysql_util import create_mysql_engine


class MysqlAuthenticator(Authenticator):
    """JupyterHub Authenticator Based on Mysql"""

    def __init__(self, **kwargs):
        super(MysqlAuthenticator, self).__init__(**kwargs)

    @gen.coroutine
    def authenticate(self, handler, data):
        engine = create_mysql_engine()
        smaker = sessionmaker(bind=engine)
        session = smaker()
        username = data['username']
        passwd = data['password']

        try:
            user = session.query(User).filter(User.user_code == username).filter(User.pass_word == passwd).one()
            if user is not None:
                print(f'{user.user_code} login in success')
                return user.user_code
            else:
                print('none')
                return None
        except:
            print('something wrong')
            return None
