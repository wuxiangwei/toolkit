


```
g_socket_map: SocketMap
    |-- _map: butil::FlatMap<butil::EndPoint, SingleConnection>
    

Channel::Init() --> SocketMapInsert() --> SocketMap::Insert()
```
