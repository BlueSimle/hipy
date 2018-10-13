# 查询构造器

## 介绍

这个数据库查询构造器，提供便利的接口可以创建和执行查询操作，可以在大多数数据库中使用。

## 查询`select`操作

### 查询表中所有的数据。

```python
users = db.table('users').get()

for user in users:
    print(user['name'])
```

### 分片查询表中的数据

```python
for users in db.table('users').chunk(100):
    for user in users:
        # ...
```

### 查询表中的某一条数据

```python
user = db.table('users').where('name', 'John').first()
print(user['name'])
```

### 查询某一行的某一列数据

```python
user = db.table('users').where('name', 'John').pluck('name')
```

### 查询某一列的数据

```python
roles = db.table('roles').lists('title')
```

这个方法返回一个list，如果在加一个参数将返回一个字典。

```python
roles = db.table('roles').lists('title', 'name')
```

### 指定一个`selcet`语句

```python
users = db.table('users').select('name', 'email').get()

users = db.table('users').distinct().get()

users = db.table('users').select('name as user_name').get()
```

### 添加一个`select`语句在额外查询语句里。

```python
query = db.table('users').select('name')

users = query.add_select('age').get()
```

### 使用`where`操作

```python
users = db.table('users').where('age', '>', 25).get()
```

### 使用`or`操作

```python
users = db.table('users').where('age', '>', 25).or_where('name', 'John').get()
```

### 使用`where between`操作

```python
users = db.table('users').where_between('age', [25, 35]).get()
```

### 使用`where not between`操作

```python
users = db.table('users').where_not_between('age', [25, 35]).get()
```

### 使用`where in`操作

```python
users = db.table('users').where_in('id', [1, 2, 3]).get()

users = db.table('users').where_not_in('id', [1, 2, 3]).get()
```

### 使用`where null`查询`Null`记录

```python
users = db.table('users').where_null('updated_at').get()
```

### 使用`order by, group by and having`操作

```python
query = db.table('users').order_by('name', 'desc')
query = query.group_by('count')
query = query.having('count', '>', 100)

users = query.get()
```

### 使用`offset and limit`操作

```python
users = db.table('users').skip(10).take(5).get()

users = db.table('users').offset(10).limit(5).get()
```

## 使用`Join`操作

在查询构造器中也可以使用`join`连表查询。

### 基本`join`操作

```python
db.table('users') \
    .join('contacts', 'users.id', '=', 'contacts.user_id') \
    .join('orders', 'users.id', '=', 'orders.user_id') \
    .select('users.id', 'contacts.phone', 'orders.price') \
    .get()
```

### 左连接操作`left join`

```python
db.table('users').left_join('posts', 'users.id', '=', 'posts.user_id').get()
```

可以使用更高级的连表用法

```python
clause = JoinClause('contacts').on('users.id', '=', 'contacts.user_id').or_on(...)

db.table('users').join(clause).get()
```

还可以加入`where`等条件

```python
clause = JoinClause('contacts').on('users.id', '=', 'contacts.user_id').where('contacts.user_id', '>', 5)

db.table('users').join(clause).get()
```

## `where`高级用法

有时候我们需要一些`where`更高级的用法，这些我们在orator中得以实现。

### 参数分组

```python
db.table('users') \
    .where('name', '=', 'John') \
    .or_where(
        db.query().where('votes', '>', 100).where('title', '!=', 'admin')
    ).get()
```

这个查询的sql将是这样。

```sql
SELECT * FROM users WHERE name = 'John' OR (votes > 100 AND title != 'Admin')
```

### 存在查询

```python
db.table('users').where_exists(
    db.table('orders').select(db.raw(1)).where_raw('order.user_id = users.id')
)
```

这个查询的sql将是这样。

```sql
SELECT * FROM users
WHERE EXISTS (
    SELECT 1 FROM orders WHERE orders.user_id = users.id
)
```

## 聚合查询

这个查询构造器提供了聚合查询。例如：`count, max, min, avg, sum`。

```python
users = db.table('users').count()

price = db.table('orders').max('price')

price = db.table('orders').min('price')

price = db.table('orders').avg('price')

total = db.table('users').sum('votes')
```

## 原生表达式

有时候我们会用到原生表达式，但是要小心sql注入。我们可以使用raw方法，创建一个原生表达式。

```python
db.table('users') \
    .select(db.raw('count(*) as user_count, status')) \
    .where('status', '!=', 1) \
    .group_by('status') \
    .get()
```

## 插入数据`insert`

往表中插入数据。

```python
db.table('users').insert(email='foo@bar.com', votes=0)

db.table('users').insert({
    'email': 'foo@bar.com',
    'votes': 0
})
```

插入一条记录，并获取自增id。

```python
db.table('users').insert([
    {'email': 'foo@bar.com', 'votes': 0},
    {'email': 'bar@baz.com', 'votes': 0}
])
```

## 更新数据`update`

更新表中数据。

```python
db.table('users').where('id', 1).update(votes=1)

db.table('users').where('id', 1).update({'votes': 1})
```

增加或减少某一列的值。

```python
db.table('users').increment('votes')  # Increment the value by 1

db.table('users').increment('votes', 5)  # Increment the value by 5

db.table('users').decrement('votes')  # Decrement the value by 1

db.table('users').decrement('votes', 5)  # Decrement the value by 5
```

指定增加某一行记录的值。

```python
db.table('users').increment('votes', 1, name='John')
```

## 删除数据`delete`

删除数据。

```python
db.table('users').where('age', '<', 25).delete()
```

删除所有的数据。

```python
db.table('users').delete()
```

清空表数据

```python
db.table('users').truncate()
```

## 合并`unions`

这个查询构造器提供了合并两个查询的方法。

```python
first = db.table('users').where_null('first_name')

users = db.table('users').where_null('last_name').union(first).get()
```

注：使用union_all也可以。

## 悲观锁

这个查询构造器有一些方法，来帮助在查询中我们实现悲观共享锁。

```python
db.table('users').where('votes', '>', 100).shared_lock().get()
```

```python
db.table('users').where('votes', '>', 100).lock_for_update().get()
```
