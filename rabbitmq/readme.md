## 直接发送消息到队列

生产者直接发送消息到队列，消费者直接消费队列中的消息，而不用指定 exchange 并绑定。
这种需求分三种情况。

- 生产者声明队列（指定队列名称），消费者不指定队列，而是直接消费生产者指定的队列。
- 生产者指定队列，但不声明队列，而是直接将消息发送到该队列。消费者声明队列，并从该队列接收消息。
- 生产者声明队列并将消息发送到该队列。消费者也声明该队列，并从该队列消费消息，但是：生产者和消费者声明队列时，指定的参数要一致，否则就会报错。


## exchange 和 queue 的绑定

- 生产者指定了 exchange 和 routing key, 但是不指定 queue, 也不将 queue 绑定到 exchange, 队列声明和绑定工作到 exchange 的工作由消费者方完成。
- 生产者指定了 exchange 和 routing key, 声明队列并将队列绑定到 exchange, 消费者只需从生产者绑定的队列消费即可。

## 名词解释

- `ConnectionFactory`: 与 `RabbitMQ` 服务器连接的管理器。
- `Connection`: 与 `RabbitMQ` 服务器的连接。
- `Channel`: 与 `Exchange` 的连接。
- `Exchange`: 接收生产者的消息，并根据消息的 `RoutingKey` 和 `Exchange` 绑定的 `BindingKey` 分配消息。
- `Queue`: 存储消费者的消息。
- `RoutingKey`: 指定当前消息被谁接收。
- `BindingKey`: 指定当前 `Exchange` 下，什么样的 `RoutingKey` 会被下派到当前绑定的 `Queue` 中。

## `exchange_declare` 方法详解

```
def exchange_declare(self, callback=None, exchange=None, exchange_type='direct', passive=False, durable=False, auto_delete=False, internal=False, nowait=False, arguments=None):
```

- `callback` 如果 `nowait=True` 且 `Exchange.DeclareOk` 时，调用这个回调方法。
- `exchange` 交换器名称。
- `exchange_type` 交换器类型，常见的如 `fanout` `direct` `topic`。
- `passive` 如果为 `true` , 则执行声明或者检查交换器是否存在。
- `durable` 设置是否持久化。`durable` 设置为 `true` 表示持久化，反之非持久化。持久化可以将交换器存盘，在服务器重启的时候不会丢失消息。
- `auto_delete` 设置是否自动删除。`auto_delete` 设置为 `true` 则表示自动删除。自动删除的前提是至少有一个队列或者交换器绑定，之后所有与这个交换器绑定的队列或者交换器都与此解绑。注意不能错误地把这个参数理解为："当与此交换器连接的客户端都断开时，RabbitMQ 会自动删除本交换器"。
- `internal` 设置是否是内置的。如果设置为 `true`，则表示是内置的交换器，客户端程序无法直接发送消息到这个交换器中，只能通过交换器路由到交换器这种方式。
- `nowait` 如果设置为 `false`, 则不期望 `RabbitMQ` 服务器有一个 `Exchange.DeclareOk` 这样响应。
- `arguments` 其他一些结构化参数。比如：`alternate-exchange`。

## `exchange_bind` 方法详解

```
def exchange_bind(self, callback=None, destination=None, source=None, routing_key='', nowait=False, arguments=None):
``` 

- `callback` 如果 `nowait=True` 且 `Exchange.DeclareOk` 时，调用这个回调方法。
- `destinaction` 一种交换器。
- `source` 消息从 `source` 交换器转发到 `destination` 交换器，从某种程度上看 `destination` 交换器可以是一种队列。
- `routing_key` 用来绑定队列和交换器的路由键。
- `nowait` 如果设置为 `false`, 则不期望 `RabbitMQ` 服务器有一个 `Exchange.DeclareOk` 这样响应。
- `arguments` 其他一些结构化参数。

## `queue_declare` 方法详解

```
def queue_declare(self, queue='', passive=False, durable=False, exclusive=False, auto_delete=False, arguments=None):
```

- `queue` 队列名称。
- `passive` 如果为 `true` , 则执行声明或者检查队列是否存在。
- `durable` 设置是否持久化。为 `true` 则设置队列为持久化。持久化的队列会存盘，在服务器重启的时候可以保证不丢失相关的信息。
- `exclusive` 设置是否排他。为 `true` 则设置队列为排他的。如果一个队列被声明为排他队列，该队列对首次声明它的连接可见，并在连接断开时自动删除。这里需要注意三点：
  - 排他队列是基于连接（Connection）可见的，同一个连接的不同信道（Channel）是可以同时访问同一个连接创建的排他队列。
  - "首次" 是指如果一个连接已经声明了一个排他队列，其他连接是不允许建立同名的排他队列，这个与普通队列不同。
  - 即使该队列是持久化的，一旦连接关闭或者客户端退出，该队列都会被自动删除，这种队列适用于一个客户端同时发送和读取消息的应用场景。
- `auto_delete` 设置是否自动删除。为 `true` 则设置队列为自动删除。自动删除的前提是：至少有一个消费者连接到这个队列，之后所有与这个队列连接的消费者都断开时，才会自动删除。不能把这个参数错误的理解为："当连接到此队列的所有客户端断开时，这个队列自动删除"，因为生产者客户端创建这个队列，或者没有消费者客户端与这个队列连接时，都不会自动删除这个队列。
- `arguments` 设置队列的其他一些参数，`如 x-message-ttl、x-expires、x-max-length`。

## `queue_bind` 方法详解

```
def queue_bind(self, queue, exchange, routing_key=None, arguments=None):
```

- `queue` 队列名称。
- `exchange` 交换器的名称。
- `routing_key` 用来绑定队列和交换器的路由键。
- `arguments` 定义绑定的一些参数。


## `basic_publish` 方法详解

```
def basic_publish(self, exchange, routing_key, body, properties=None, mandatory=False, immediate=False):
```

- `exchange` 交换器的名称，指明消息需要发送到哪个交换器。如果设置为空字符串，则消息会被发生到 `RabbitMQ` 默认的交换器中。
- `routing_key` 路由键，交换器根据路由键将消息存储到相应的队列之中。
- `properties` 消息的基本属性集，其包含 14 个属性成员，分别有 `contentType`、`deliveryMode`、`proiotity`等。
- `body` 消息体 `payload`，真正需要发送的消息。
- `mandatory` 当参数设置为 `true` 时，交换器无法根据自身的类型和路由键找到一个符合条件的队列，那么 `RabbitMQ` 会调用 `Basic.Return` 命令消息返回给生产者。当参数设置为 `false` 时，出现上述情况，则消息直接丢失。
- `immediate` 当参数设置为 `true` 时，如果交换器在将消息路由到队列时发现队列上并不存在任何消费者，那么这条消息将不会存入队列中。当与路由键匹配的所有队列都没有消费者时，该消息会通过 `Basic.Return` 返回至生产者。

## `basic_consume` 方法详解

```
def basic_consume(self, consumer_callback, queue='', no_ack=False, exclusive=False, consumer_tag=None, arguments=None):
```

- `consumer_callback` 设置消费者的回调函数。用来处理 `RabbitMQ` 推送过来的消息，比如：DefaultConsumer，使用时需要客户端重写其中的方法。
- `queue` 队列的名称。
- `no_ack` 设置是否自动确认。建议设置成 `false`，即不自动确认。
- `exclusive` 设置是否排他。
- `consumer_tag` 消费者标签，用来区分多个消费者。
- `arguments` 设置消费者的其他参数。

## `exchange_type` 模式

### `fanout` 模式

- 任何发送到 `fanout exchange` 的消息都会被转发到与 `exchange` 绑定的所有的 `queue` 上。
- 不需要指定 `routing_key`, 即使指定了也是无效的。
- 需要提前将 `exchange` 与 `queue` 进行绑定， 一个 `exchange` 可以绑定到多个 `queue`, 一个 `queue` 也可以同多个 `exchange` 进行绑定。
- 接收到消息的 `exchange` 没有与任何 `queue` 绑定， 则消息就会被抛弃。

### `direct` 模式

- 发送到 `direct exchange` 的消息都会被转发到 `routing_key` 中指定的 `queue`。
- 不需要将 `exchange` 进行任何绑定操作。当然也可以进行绑定操作，可以将不同的 `routing key` 与不同的 `queue` 进行绑定，不同的 `queue` 与不同 `exchange` 进行绑定。
- 消息需要传递一个 `routing_key`。
- 如果消息中不存在 `routing_key` 中绑定的队列名，则该消息就会被抛弃。
- 如果一个 `exchange` 声明为 `direct`，并且绑定中指定了 `routing_key`，那么发生消息时。需要同时指明该 `exchange` 和 `routing_key`。

### `topic` 模式

- 这种模式比较复杂，简单来说，就是每个队列都有其关心的主题，所有的消息都带有一个 `routing_key`，`exchange` 会将消息转发到所有关注主题能与 `routing_key` 模糊匹配的队列。
- 需要 `routing_key` 要提前绑定 `exchange` 与 `queue`。
- 在进行绑定的时候，要提供一个该队列关心的主题，如："#.log.#" 表示该队列关心所涉及 log 的消息（一个 routing_key 为 "MQ.log.error" 的消息会被转发到该队列）。
- "#" 表示 0 个或若干个关键字，"*" 表示一个关键字。如 "log.*" 能与 "log.warn.timeout" 匹配，但是 "log.#" 能与上述匹配。
- 如果 `exchange` 没有发现能够与 `routing_key` 匹配的 `Queue`，则会抛弃此消息。
