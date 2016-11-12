#-* -coding: UTF-8 -* -
__author__ = 'Arvin'

"""
执行前提：
    系统安装python-devel 和 gcc
    Python安装cython

编译整个当前目录：
    python py-setup.py
编译某个文件夹：
    python py-setup.py BigoModel

生成结果：
    目录 build 下

生成完成后：
    启动文件还需要py/pyc担当，须将启动的py/pyc拷贝到编译目录并删除so文件

"""

import sys, os, shutil, time
from distutils.core import setup
from Cython.Build import cythonize

starttime = time.time()
currdir = os.path.abspath('.')
parentpath = sys.argv[1] if len(sys.argv)>1 else ""
setupfile= os.path.join(os.path.abspath('.'), __file__)
build_dir = "build"
build_tmp_dir = build_dir + "/temp"

def getpy(basepath=os.path.abspath('.'), parentpath='', name='', excepts=(), copyOther=False,delC=False):
    """
    获取py文件的路径
    :param basepath: 根路径
    :param parentpath: 父路径
    :param name: 文件/夹
    :param excepts: 排除文件
    :param copy: 是否copy其他文件
    :return: py文件的迭代器
    """
    fullpath = os.path.join(basepath, parentpath, name)
    for fname in os.listdir(fullpath):
        ffile = os.path.join(fullpath, fname)
        #print basepath, parentpath, name,file
        if os.path.isdir(ffile) and fname != build_dir and not fname.startswith('.'):
            for f in getpy(basepath, os.path.join(parentpath, name), fname, excepts, copyOther, delC):
                yield f
        elif os.path.isfile(ffile):
            ext = os.path.splitext(fname)[1]
            if ext == ".c":
                if delC and os.stat(ffile).st_mtime > starttime:
                    os.remove(ffile)
            elif ffile not in excepts and os.path.splitext(fname)[1] not in('.pyc', '.pyx'):
                if os.path.splitext(fname)[1] in('.py', '.pyx') and not fname.startswith('__'):
                    yield os.path.join(parentpath, name, fname)
                elif copyOther:
                        dstdir = os.path.join(basepath, build_dir, parentpath, name)
                        if not os.path.isdir(dstdir): os.makedirs(dstdir)
                        shutil.copyfile(ffile, os.path.join(dstdir, fname))
        else:
            pass

#获取py列表
module_list = list(getpy(basepath=currdir,parentpath=parentpath, excepts=(setupfile)))
try:
    setup(ext_modules = cythonize(module_list),script_args=["build_ext", "-b", build_dir, "-t", build_tmp_dir])
except Exception, ex:
    print "error! ", ex.message
else:
    module_list = list(getpy(basepath=currdir, parentpath=parentpath, excepts=(setupfile), copyOther=True))

module_list = list(getpy(basepath=currdir, parentpath=parentpath, excepts=(setupfile), delC=True))
if os.path.exists(build_tmp_dir): shutil.rmtree(build_tmp_dir)

print "complate! time:", time.time()-starttime, 's'
