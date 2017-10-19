
brpc分析


**基本功能**

1. RPC协议
2. 连接管理
3. 异步、同步、超时机制；
4. 名字服务、负载均衡、组合访问；
5. 内置服务 & 调试工具
6. 性能

**高级功能**

1. backup request
2. RPC cancellation
3. 数据压缩、加密
4. RPC dump & replay


**基本概念**


**client**

1. 参数配置，例如线程数、连接类型等，通过brpc::ChannelOptions设置，或者通过glags全局配置；
2. 连接到单台服务器和连接到服务集群。连接到服务集群，给定名字服务地址和负载均衡算法，Channel定期从名字服务中拉取服务列表，并使用负载均衡算法选取一个服务。连接到单台服务，给定server ip和port。
3. 名字服务和负载均衡，见下图。名字服务可增加黑名单。负载均衡算法包括round robin、random、locality-aware、一致性hash等。locality-aware优先选择延迟较低的服务。另外，负载均衡考虑连接中断服务的处理，选择算法排除这些连接中断的服务，并定期检查这些服务是否恢复。

![lb](https://github.com/brpc/brpc/blob/master/docs/images/lb.png)

4. 同步和异步访问。同步，等待；异步，回调。
5. 半同步，使用join等待多个异步访问完成。


Channel    
ChannelOptions 设置超时时间、重试次数、重试策略（自定义重试策略brpc::RetryPolicy）、连接类型等。     
Controller 用于在某次RPC中覆盖ChannelOptions中的选项，可根据上下文每次均不同。线程不安全，同时只能被一个RPC使用。    
线程池，client没有独立线程池。如果程序中同时使用了server，那么client和server共用线程池。    

![client_side](https://github.com/brpc/brpc/blob/master/docs/images/client_side.png)

1. 指定目标server。名字服务，负载均衡；
2. 指定socket。连接类型：短连接、连接池、单连接；
3. 序列化request；
4. 发送request；
5. 接收response；
6. 反序列化response；
7. 处理response，包括重试等。

**server**


**连接方式**

1. 短连接，每次调用都有建立连接的开销，延迟高（1.5RTT + 1RTT + 处理时间）。
2. 连接池，一个client对一台server可能有多条连接，每次RPC前取用空闲连接，结束后归还；
    - 关闭超过10s闲置的连接；
    - CPU使用率比单连接高，单连接可以合并写。
3. 单连接，进程内所有client与一台server最多只有一个连接，一个连接上可能同时有多个请求，回复返回顺序和请求顺序不需要一直，baidu_std协议的默认选项。


多个channel可能会引用同个连接，当所有channel析构时关闭连接。    
连接缓存区配置。    


**压缩方式**

支持以下几种压缩方法，压缩方法主要考虑两个因素：压缩率、速度。

1. snappy，速度快，压缩率低
2. gzip， 速度慢，压缩率高
3. zlib，速度比gzip快比snappy慢，压缩率比gzip高

具体比较，参考https://github.com/brpc/brpc/blob/master/docs/cn/client.md

