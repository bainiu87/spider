####文件说明
*入口文件（无队列），内含定时器则使用Client
*爬虫含有队列入口，消息队列使用apache的activeMQ,使用stomp进行连接
*使用队列则：添加队列信息：send_activeMQ ,消费队列信息：get_activeMQ
*使用队列启动方式建议先启动多个get_activeMQ,然后再向队列里添加消息，原因为python stomp连接persistent queues (default value: 1000)，不知道在哪里修改activeMQ的jms.prefetchPolicy.all或者ms.prefetchPolicy.queuePrefetch参数

*爬虫使用redis 进行排重
*爬虫数据保存在mysql中
*爬虫在cm10086_request文件中对数据进行了一次简单的清洗
*test开头文件为测试文件，和其他文件没有关系
