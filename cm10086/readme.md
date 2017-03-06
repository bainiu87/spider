spider b2b.10086.cn 
招标采购公告结果公示
===================
----------
说明
-------------



> **Client.py:**

> - 入口文件，内含计时器，默认为1秒取出一个页数发送一次请求. 
> - 数据在入口文件中存入数据库. 
> - 入口文件可以设置页数范围
> - 该入口文件没有使用消息队列

>**send_activeMQ.py:**

> - 使用activeMQ消息队列，向消息队列添加消息
> - 需要设置页数范围
> 
>**get_activeMQ.py:**

> - 使用activeMQ消息队列，消费队列消息
> - 数据在这里存入数据库
> 
>**cm10086_spider.py:**

> - 主体文件，对一页的数据进行请求，处理，排重

>**Mysql_DB.py:**

> - 数据库操作

>**Redis_DB.py:**

> - redis操作，主要使用redis做排重

>**record_log.py:**

> - 日志记录

>**其他:**

> - test文件，前期测试使用，与其他文件没有关联
> - 使用队列时，需先启动多个get_activeMQ.py然后再启动send_activeMQ文件，主要由于activeMQ 默认persistent queues (default value: 1000)，而python 使用stomp连接activeMQ ,不知道哪里可以设置jms.prefetchPolicy.all或者ms.prefetchPolicy.queuePrefetch参数





