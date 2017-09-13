
# 全平台配置

配置步骤：

1. 新建`~/.vim`目录；
2. 拷贝`.vimrc`到HOME目录；
3. `git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim`
4. 打开vim，执行`:VundleInstall`命令，安装完成。
5. `apt-get install ctags`


# Win平台

下载ctags，将ctags.exe文件放到一个目录，例如`~/bin`，将该目录加入PATH。    
对git bash的场景，通过`echo $PATH`查看是否包含指定目录，如果不包含将其加入。    
对gvim场景，直接`Win+R` + cmd，执行`ctags.exe --version`测试是否能够范围。    


