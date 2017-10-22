

参考：https://github.com/brpc/brpc/blob/master/docs/cn/new_protocol.md

目标：server在同端口同时支持多种协议，client不同于sever，明确知道自己采用的协议类型。

问题：server如何识别多种不同的协议；

解决：

1. 将协议大致分为3类，然后逐个尝试。第一类协议有标记或特殊字符在最前面，例如baidu_std，解析消息先检查前面几个字节是否跟协议标记匹配；第二类协议没有特殊标记，但有一定的语法，需要解析一段输入后才能匹配，例如http协议；第三类，协议标记在中间；
2. 对同个连接优先尝试最近一次的协议，降低识别效率。


实现协议的接口：

1. serialize_request 序列化请求
2. pack_request
3. process_request


具体例子，参考baidu_rpc_meta.proto




