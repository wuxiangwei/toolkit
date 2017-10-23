brpc分析

## 基本功能

1. RPC协议
    - 应用层(request、response、service **对象**，用于完成业务逻辑)，client的一个request对象，发送到server后反序列化为一个request对象，然后交由service处理；
    - RPC 层(baidu_rpc, http 协议，确定消息边界，从二进制中分离出完整的request、response)，默认的baidu_rpc协议包括如下几个部分：4字节协议标识PRBC、4字节meta+payload大小、4字节meta大小、meta数据、payload数据、attatchment数据。attatchment不是request或者response实例的部分，是用户传递的额外数据；
    - TCP 层(传送数据)
2. 连接管理
3. 异步、同步、超时机制；
4. 名字服务、负载均衡、组合访问；
5. 内置服务 & 调试工具
6. 性能
7. 认证
8. 流式数据

**高级功能**

1. backup request
2. RPC cancellation
3. 数据压缩、加密
4. RPC dump & replay


**基本概念**


## client 流程

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

## server 流程

1. 请求、回复、服务的接口均定义在proto文件中；
2. 

## 连接方式

1. 短连接，每次调用都有建立连接的开销，延迟高（1.5RTT + 1RTT + 处理时间）。
2. 连接池，一个client对一台server可能有多条连接，每次RPC前取用空闲连接，结束后归还；
    - 关闭超过10s闲置的连接；
    - CPU使用率比单连接高，单连接可以合并写。
3. 单连接，进程内所有client与一台server最多只有一个连接，一个连接上可能同时有多个请求，回复返回顺序和请求顺序不需要一直，baidu_std协议的默认选项。


多个channel可能会引用同个连接，当所有channel析构时关闭连接。    
连接缓存区配置。    


## 压缩方式

支持以下几种压缩方法，压缩方法主要考虑两个因素：压缩率、速度。

1. snappy，速度快，压缩率低
2. gzip， 速度慢，压缩率高
3. zlib，速度比gzip快比snappy慢，压缩率比gzip高

具体比较，参考https://github.com/brpc/brpc/blob/master/docs/cn/client.md


**Channel**



## 内置服务

目标：提高开发调试效率，通过多种形式展现服务内部状态。

主要服务：
1. status
2. vars
3. connections 查看所有连接的状态；
4. flags 查看配置，brpc的配置使用gflag来管理；
5. rpcz
6. cpu profiler 分析cpu热点
7. heap profiler 分析内存热点
8. cotention profiler 分析锁竞争


内置服务的实现：
1. proto文件 src/brpc/builtin_service.proto
2. service实现 src/brpc/builtin 目录


## IO操作方式

1. blocking io 阻塞当前线程；
2. asynchronous io 不阻塞当前线程，使用回调处理结果；
3. non-blocking io 批量同步，用户阻塞等待多个asynchronous io完成。


## 事件分发

epoll

线程模型

## Stream

解决的问题：client发送的数据非常大，大到不能放在attachment中。如果用多个RPC分次传输，会存在如下问题：
1. 如果RPC是并行的，拼接数据的逻辑非常复杂；
2. 如果RPC是串行的，每次传递都要等待一个RTT+处理数据的延迟；


**client** 

1. 创建stream
    - StreamCreate创建streamid并和controller关联；
    - 发送请求给server，建立stream连接；
2. 向stream写数据
3. 关闭stream

```
StreamCreate() --> Stream::Create() // 实例化Stream对象，设置Controller._request_stream为stream对象的id；
```

**server**

1. 接收到建立stream的请求，brpc::StreamAccept；
2. 使用StreamInputHandler来处理stream数据；


