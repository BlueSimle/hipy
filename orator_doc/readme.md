# Orator

Orator提供一个简单和方便的数据库数据处理库。
它的灵感来源于PHP的Laravel框架，借助其思想实现了python版的查询构造器和ORM。
这是完整的文档：http://orator-orm.com/docs


## 安装

你可以有两种不同的安装方式。

- 使用pip安装。

```
pip install orator
```

- 使用官方的源码安装(https://github.com/sdispater/orator)

## 基本使用

### 配置

你需要开始配置数据库连接，及创建一个`DatabaseManager`实例。

```
from orator import DatabaseManager, Model

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
Model.set_connection_resolver(db)
```

### 定义一个模型

```
class User(Model):
    pass
```

在模型中定义`__table__`属性来确定表名。

```
class User(Model):

    __table__ = 'my_users'
```

其次还可以定义`__primary_key`来确定主键，`__connection__`来确定连接。
如果你不希望默认创建`updated_at`和`created_at`字段，则将`__timestamps__`属性置为`False`。

### 查询模型所有数据

```
users = User.all()
```

### 通过主键查询数据

```
user = User.find(1)

print(user.name)
```

### 使用模型查询

```
users = User.where('votes', '>', 100).take(10).get()

for user in users:
    print(user.name)
```

### 聚合查询

你可以使用查询构造器。

```
count = User.where('votes', '>', 100).count()
```

```
users = User.where_raw('age > ? and votes = 100', [25]).get()
```

### 分片查询

如果你希望一次查询一部分数据，则可以使用`chunk`方法。

```
for users in User.chunk(100):
    for user in users:
        # ...
```

### 指定数据库连接

在模型中，可以使用`on`方法指定数据库连接。

```
user = User.on('connection-name').find(1)
```

你还可以使用`read/write`指定只读或只写连接。

```
user = User.on_write_connection().find(1)
```

## 字段管理

当创建一个新的模型，通过构造函数给模型设置属性。
例如：在模型中设置`__filltble`或者`__guarded__`属性。

### 在模型中定义填充字段

这个`__filltable__`属性。

```
class User(Model):

    __fillable__ = ['first_name', 'last_name', 'email']
```

### 在模型中定义禁止字段

这个`__guarded__`属性。

```
class User(Model):

    __guarded__ = ['id', 'password']
```

禁止所有字段

```
__guarded__ = ['*']
```

## 插入、更新和删除

### 保存一个新的模型

在数据库中创建一个新的记录，使用`save`方法。

```
user = User()

user.name = 'John'

user.save()
```

在创建完成之后，可以这样获取到自增id。

```
inserted_id = user.id
```

### 使用`create`方法

```
# Create a new user in the database
user = User.create(name='John')

# Retrieve the user by attributes, or create it if it does not exist
user = User.first_or_create(name='John')

# Retrieve the user by attributes, or instantiate it if it does not exist
user = User.first_or_new(name='John')
```

### 更新数据

```
user = User.find(1)

user.name = 'Foo'

user.save()
```

你也可以这样更新数据。

```
affected_rows = User.where('votes', '>', 100).update(status=2)
```

### 删除数据

```
user = User.find(1)

user.delete()
```

### 通过主键删除数据

```
User.destroy(1)

User.destroy(1, 2, 3)
```

你还可以这样删除数据。

```
affected_rows = User.where('votes', '>' 100).delete()
```

### 仅仅更新时间

如果你想更新模型的时间，可以使用`touch`方法。

```
user.touch()
```

## 时间`Timestamps`

在这个模型中`created_at`和`updated_at`是在数据库中默认生成的。如果，你不希望创建这两个字段，你可以设置属性`__timestamps__`为`false`。

```
class User(Model):

    __timestamps__ = False
```

### 提供自定义时间格式

如果，你希望自己定义时间格式，你可以这样操作。

```
class User(Model):

    def get_date_format():
        return 'DD-MM-YY'
```
