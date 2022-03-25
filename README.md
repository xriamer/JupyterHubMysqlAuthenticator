# Jupyterhub 自定义验证类

## 功能描述

新建一个 mysqlauthenticator 的 Package，使得 Jupyterhub 能够通过 MysqlAuthenticator 这个类做用户校验的工作。

MysqlAuthenticator 校验用户登录也非常的简单，只要在 MySQL 数据库查询相应的账户和密码，如果能查询到，就验证通过。

```python
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
```

## 安装到 Docker 中
* 首先启动 jupyterhub Docker 服务

* 进入容器先安装一些依赖的模块

```shell
docker exec -it 3dd37753b827 bin/bash
```

* 安装wheel、sqlalchemy、py

```shell
 python3 -m pip install wheel
 python3 -m pip install sqlalchemy
 python3 -m pip install pymysql
```

* 退出容器，把 mysqlauthenticator 包拷贝到 pip3 的下载目录

 ```shell
docker cp /root/jupter_auth_mysql/mysqlauthenticator 3dd37753b827:/usr/local/lib/python3.8/dist-packages/
 ```

## 修改config.yaml

*  需要将 Jupyterhub 默认的校验类设置为我们定义的 MysqlAuthenticator

```python
c.JupyterHub.authenticator_class = 'mysqlauthenticator.MysqlAuthenticator'
```
* 特别需要留意的是，若当前登录的用户并不是 JupyterHub Docker 容器内部的用户时，Jupyterhub 将无法为这位用户分发 Jupter Notebook / JupyterLab 实例，那么我们就需要在生成器启动之前执行一些引导工作：在 Docker 容器中创建当前登录的用户。

```python
import pwd
import subprocess

def pre_spawn_hook(spawner):
    username = spawner.user.name
    try:
        pwd.getpwnam(username)
    except KeyError:
        subprocess.check_call(['useradd', '-ms', '/bin/bash', username])

c.Spawner.pre_spawn_hook = pre_spawn_hook

c.LocalAuthenticator.create_system_users = True
```

然后重启一下 Jupyterhub 服务就行了。输入的账号密码没有通过数据库验证的话提示 Invalid username or password 就算成功了。