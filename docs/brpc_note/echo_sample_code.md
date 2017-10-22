
protobuf定义3种接口，接口交由上层应用根据自己的业务来实现：

1. request
2. response
3. service

protobuf除了生成上述3个接口外，还会再生成一个XXX_Stub类。XXX_Stub类相当于远程服务在client的存根或句柄，调用远程服务的某个方法时只要调用XXX_Stub对应的方法即可。brpc例子中，直接make会删除由Protoc生成的源文件，只保留头文件和`.o`文件。XXX_Stub的具体实现定义在源文件中，若要查看具体实现可以手动执行`protoc XXX.proto --cpp_out=tmp `命令。

目标主机可能有多个Service，每个Service又可能有多个method，如何标记调用哪个Service的哪个method？protobuf的MethodDescriptor！


protobuf已有的概念：

1. RpcChannel，实例化stub的入参。调用stub的具体方法，实际上，调用RpcChannel的CallMethod方法。
2. RpcController，1次RPC调用的入参。
    - 准备参数，例如重试次数、重试策、done、method等；
    - 持有返回值；
3. Closure

brpc的ChannelBase派生自RpcChannel，重写CallMethod方法；Controller派生自RpcController接口。

CallMethod流程(参考Channel::CallMethod函数)：

1. 序列化request；
2. 启动定时器，包括backup_request，或者超时处理；
3. 发送请求，Controller::IssueRPC ==> Sender::IssueRPC；
    - 从LB中选1个server；
    - 
4. 检查done。如果为NULL，join；


```
Socket
    |-- _conn: SocketConnection

Stream
    |-- _host_socket: Socket*


Channel
    |-- _server_address // 服务地址，Init时传入
    |-- _server_id // socket在ResourcePool中的索引

Channel::Init() --> SocketMapInsert() --> SocketMap::Insert() --> 
1. SocketCreator::CreateSocket() --> InputMessenger::Create() --> Socket::Create() --> ResourcePool<T>::singleton()::get_resource()  // 使用资源池管理socket实例
2. 
 
Controller
    |-- _request_protocol  // RPC协议
    |-- _lb  // 负载均衡
    |-- _request_buf  // payload序列化后的内容
    |-- _timeout_id   // 超时定时器id
    |-- _current_call
    |    |-- peer_id
    |    |-- sending_sock   // 发送请求的socket，选出socket后设置到该变量
    |-- _pack_request: Protocol::PackRequest

Channel::CallMethod() --> 
1. Channel::_serialize_request()  // 序列化请求到controller._request_buf
2. Controller::IssueRPC() --> 
    2.1 LoadBalancer::SelectServer() // 选择1socket。如果LB，从LB选择；如果single，从channel中获取；
    2.2 // 区分不同connect类型
    2.3 _pack_request()
    2.4 Socket::Write() --> Socket::StartWrite() --> 
        3.1 Socket::ConnectIfNot() // 1. 如果socket没有连接服务，则连接；2. 

Socket::Write() --> Socket::StartWrite() --> Stream::CutMessageIntoFileDescriptor() --> Stream::WriteToHostSocket()
```


**事件分发** Event dispatcher

```
g_edisp // 全局变量，一个EventDispatch的数组
```








