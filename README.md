# py2so
编译py为so文件，更好的隐藏源码

# 准备工作
    系统安装python-devel 和 gcc
    Python安装cython

# 调用方式
    编译某个文件夹：
      python py2so.py mydir_path
    
# 生成的文件
    mydir_path/build文件夹下即为结果目录

# 验证
    在 mydir_path/build/xxx 下使用ipython进入命令行，引用包即可
    
# 注意
    如项目包含如main.py的启动文件，可将源文件copy至 build/下对应位置启动
    
