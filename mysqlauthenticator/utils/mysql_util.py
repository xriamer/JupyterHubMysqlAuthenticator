from sqlalchemy import create_engine


def create_mysql_engine():
    engine = create_engine(
        "mysql+pymysql://{}:{}@{}/{}?charset=utf8".format('DBName', 'DBPassword', '<DBHost:DBport>', '<DBName>'))
    con = engine.connect()
    return con