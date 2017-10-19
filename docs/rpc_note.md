
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

![](https://github.com/brpc/brpc/blob/master/docs/images/lb.png)

4. 同步和异步访问。同步，等待；异步，回调。
5. 半同步，使用join等待多个异步访问完成。


Channel
ChannelOptions 设置超时时间、重试次数、连接类型等。
Controller 用于在某次RPC中覆盖ChannelOptions中的选项，可根据上下文每次均不同。线程不安全，同时只能被一个RPC使用。
线程池，client没有独立线程池。如果程序中同时使用了server，那么client和server共用线程池。


**server**



