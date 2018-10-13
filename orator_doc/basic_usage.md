# 配置

设置数据库配置参数，创建一个DatabaseManager实例。

```python
from orator import DatabaseManager

config = {
    'mysql': {
        'driver': 'mysql',
        'host': 'localhost',
        'database': 'database',
        'user': 'root',
        'password': '',
        'prefix': ''
    }
}

db = DatabaseManager(config)
```

如果多个不同的数据库，你可以指定默认的一个。

```python
config = {
    'default': 'mysql',
    'mysql': {
        'driver': 'mysql',
        'host': 'localhost',
        'database': 'database',
        'user': 'root',
        'password': '',
        'prefix': ''
    }
}
```

# 配置读写分离数据库

有的情况下我们需要配置读写分离数据库，一个数据库用来查询，另一个数据库用来插入、更新和删除。Orator可以很容易的实现。

```python
config = {
    'mysql': {
        'read': {
            'host': '192.168.1.1'
        },
        'write': {
            'host': '192.168.1.2'
        },
        'driver': 'mysql',
        'database': 'database',
        'username': 'root',
        'password': '',
        'prefix': ''
    }
}
```

需要注意：这里配置了read和write字典，这两个字典都有单独的host。数据库的database、user等配置都是共用的，如果需要单独配置，则配置到自己的字典里面和host一样。

# 执行查询

## 执行一个查询操作

```python
results = db.select('select * from users where id = ?', [1])
```

这个查询语句的结果返回的一个list。

## 执行一个插入操作

```python
db.insert('insert into users (id, name) values (?, ?)', [1, 'John'])
```

## 执行一个更新操作

```python
db.update('update users set votes = 100 where name = ?', ['John'])
```

这一个操作返回更新的记录行数。

## 执行一个删除操作

```python
db.delete('delete from users')
```

这一个操作返回删除的记录行数。

## 执行所有的操作

```python
db.statement('drop table users')
```

# 数据库事务

执行一个数据库的事务，我们可以用以下的这种方式。

```python
with db.transaction():
    db.table('users').update({votes: 1})
    db.table('posts').delete()
```

如果执行事务过程中有任何异常抛出，都将回滚。

还可以这样开启事务

```python
db.begin_transaction()
```

回滚操作

```python
db.rollback()
```

提交事务

```python
db.commit()
```

# 使用数据库连接

当我们使用多个数据库连接的时候，可以指定其中一个连接。

```python
users = db.connection('foo').table('users').get()
```

获取一个数据库连接实例

```python
db.connection().get_connection()
```

重新连接建立一个连接

```python
db.reconnect('foo')
```

关闭一个连接

```python
db.disconnect('foo')
```

# 查询日志

Orator可以配置查询和执行的日志记录。通过设置`log_queries`为`true`开启。

```python
config = {
    'mysql': {
        'driver': 'mysql',
        'host': 'localhost',
        'database': 'database',
        'username': 'root',
        'password': '',
        'prefix': '',
        'log_queries': True
    }
}
```

也可以这样设置

```python
db.connection().enable_query_log()
```

现在，这个日志将在`debug`级别输出。

```python
Executed SELECT COUNT(*) AS aggregate FROM "users" in 1.18ms

Executed INSERT INTO "users" ("email", "name", "updated_at") VALUES ('foo@bar.com', 'foo', '2015-04-01T22:59:25.810216'::timestamp) RETURNING "id" in 3.6ms
```

## 自定义日志

```python
import logging

logger = logging.getLogger('orator.connection.queries')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    'It took %(elapsed_time)sms to execute the query %(query)s'
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger.addHandler(handler)
```
