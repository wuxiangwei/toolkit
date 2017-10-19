
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
3. 

![](lb.png)



**server**



