
小工具介绍


# 小工具

## debcompare

用于比较新编译的deb包的依赖和已安装的deb包的依赖是否一致。

【缘起】    

正常地，在相同debian版本中编译的包的依赖是相同的。     
不过，对一些依赖包的版本有特定要求的情况，会将这些依赖包保存在自己的源中。    
如果编译环境没有添加该源，那么下载的依赖包就是debian默认的版本。      

如果依赖包的版本不对，那么在升级的情况下，程序就会包无法加载到共享库，可以使用`ldd`命令查看。

【使用】    

将编译出的deb包放到已经安装了旧版本的服务器，修改`debcompare.py`中的路径，执行脚本，会在当前目录生成两个文件`i.o`和`u.o`，将这两个文件sz到PC，然后使用Beyond Compare工具比较差异。







