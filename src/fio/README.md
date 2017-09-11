
前提条件：
1. 支持librbd引擎的fio工具；
2. 准备待测试的rbd块，rbd块默认在nbs池中，若要修改pool，移步job配置文件。


多卷：

一个task由以下几项组成：
1. IO大小
2. IO类型，例如randread，randwrite等
3. IO队列深度，例如，8,16等

一个task同时跑在多个卷上，一个卷一个进程，所有进程同时执行，最终结果记录到以task命名的csv文件内。
使用`ls | grep .*iodepth_[0-9]*.csv`命令查看每个task的结果。


