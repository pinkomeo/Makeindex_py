#-*- coding: utf-8 -*-
#author:pinko
#version:1.0
#date:2016/09/27

import os, sys, getopt, time
import webbrowser


def printbanner():
    print (
        """
=======================================================================

             __ __   __  |__,  ___  o  __   __|  ___  \_' 
            |  )  ) (__( |  \ (__/_ | |  ) (__| (__/_ / \     
                                                               by pinko
=======================================================================
        """
    )

def printversion():
    print 'makeindex.py 1.0 powered by pinko'

def usage():
    print (
        """
        用法：  makeindex.py [-a]
                makeindex.py [-k] searchkeyword
                makeindex.py [-h]
                makeindex.py [-v]
        选项：
                --keyword=searchkeyword     根据输入的关键词进行搜索
                --all                       生成所有文件的索引目录
                --help                      打印用法
                --version                   打印版本

        """.decode('utf-8').encode('gbk')
    )

skipexts = ['.rar','.zip','.pyd','.txt','.py','.gif', '.exe', '.pyc', '.o', '.a','.dll','.lib','.pdb','.mdb']        # ignore binary files

def generator(dirpath,searchKey):
    start = time.clock()

    global fcount, vcount
    global skey
    skey = ""
    fcount = vcount = 0
    show_all = False

    skey = searchKey
    if not skey:
        show_all = True
    f_index = open("index.html","w+")

    f_index.writelines("<html>")
    f_index.writelines("<meta charset='UTF-8'><body align='center'>")
    
    f_index.writelines("<h1 style='width:100%'><mark> === MAKEINDEX === </mark></h1>")

    f_index.writelines("<h4>在当前目录 "+str(dirpath)+" 下共发现 <a name='vcount'></a> 个文件</h4>")
    if not show_all:
        f_index.writelines("<h4>其中 <a name='fcount'></a> 个文件含有关键词</h4>")
        f_index.writelines("<h5>下面是关键词 <mark>"+str(skey)+"</mark> 的搜索结果</h5>")
    f_index.writelines("<div text-align='left'>")
    for root,dirs,files in os.walk(dirpath):  
        for dir in dirs:  
            print os.path.join(root,dir).decode('gbk').encode('utf-8')
        for file in files: 
            if not show_all: 
                if os.path.splitext(file)[1] not in skipexts and os.path.splitext(file)[0] != 'index':
                    #print os.path.join(root,file).decode('gbk').encode('utf-8')
                    if open(file).read().find(skey) != -1:
                        name_pre = os.path.join(root,file).decode('gbk').encode('utf-8').split('\\')[-1]
                        #print name_pre
                        #print skey
                        if skey in name_pre:
                            name_pre = name_pre.replace(skey,'<mark>'+skey+'</mark>')
                        # else:
                        #     name_pre = '<mark>'+name_pre+'</mark>'
                        #print name_pre
                        f_index.writelines("<a target=_blank href='file:\\"+os.path.join(root,file).decode('gbk').encode('utf-8')+"''>"+name_pre+"</a></br></br>")
                        fcount += 1
                    else:
                        pass
                        #f_index.writelines("<a arget=_blank href='file:\\"+os.path.join(root,file).decode('gbk').encode('utf-8')+"''>"+os.path.join(root,file).decode('gbk').encode('utf-8').split('\\')[-1]+"</a></br></br>")
                    vcount += 1
            else:
                if os.path.splitext(file)[1] not in skipexts and os.path.splitext(file)[0] != 'index':
                    f_index.writelines("<a target=_blank href='file:\\"+os.path.join(root,file).decode('gbk').encode('utf-8')+"''>"+os.path.join(root,file).decode('gbk').encode('utf-8').split('\\')[-1]+"</a></br></br>")
                    vcount += 1

    f_index.writelines("</div>")
    f_index.writelines("<footer>")
    end = time.clock()
    f_index.writelines("<h5>目录生成器MakeIndex v1.0 by pinko</h5>")
    f_index.writelines("<h5>生成本页面用时"+" %f s" % (end - start)+"</h5>")
    f_index.writelines("</footer>")
    f_index.writelines("</body>")

    f_index.writelines("<script>var a = document.getElementsByName('fcount');a[0].innerHTML='"+str(fcount)+"';</script>")
    f_index.writelines("<script>var a = document.getElementsByName('vcount');a[0].innerHTML='"+str(vcount)+"';</script>")
    f_index.writelines("</html>")
    f_index.close()
      
if __name__ == '__main__':
    global show_all
    root = os.path.abspath(os.curdir)
    #key=raw_input("type key:")
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'k:hav', ['keyword=','help','version',"all"])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)
    if len(opts) <= 0:
        usage()
        sys.exit(1)
    else:
        for o, a in opts:
            if o in ('-h', '--help'):
                usage()
                sys.exit(1)
            elif o in ('-v', '--version'):
                printversion()
                sys.exit(0)
            elif o in ('-a', '--all'):
                show_all = True
                keyword = ""
                print "程序已启动...".decode('utf-8').encode('gbk')
                time.sleep(2)
                print "正在为您生成当前目录下所有文件的索引结果...".decode('utf-8').encode('gbk')
                time.sleep(3)
                generator(root,keyword)
            elif o in ('-k', '--keyword'):
                print a
                if a:
                    printbanner()
                    print "程序已启动...".decode('utf-8').encode('gbk')
                    time.sleep(2)
                    print "正在为您生成关键字为 ".decode('utf-8').encode('gbk')+str(a)+" 的搜索结果...".decode('utf-8').encode('gbk')
                    time.sleep(3)
                    keyword = a.decode('gbk').encode('utf-8')
                    generator(root,keyword)
                else:
                    print "No keyword!"
                    usage()
                    sys.exit(0)
            else:
                print 'Unhandled option!'
                sys.exit(3)

    #key = "android"
    # for root,dirs,files in os.walk("D:\\work\\drops2\\drops2\\makeindex"):  
    #     for dir in dirs:  
    #         print os.path.join(root,dir).decode('gbk').encode('utf-8');  
    #     for file in files:  
    #         print os.path.join(root,file).decode('gbk').encode('utf-8');  
    #searcher(root,key)
    
    #print 'Found in %d files, visited %d' % (fcount, vcount)
    #generator(root,key)
    url=root+"/index.html"
    print "生成成功".decode('utf-8').encode('gbk')
    #print "是否在浏览器中打开网页？".decode('utf-8').encode('gbk')
    ask_open = "是否在浏览器中打开网页？Y/N  ".decode('utf-8').encode('gbk')
    while True:
        open_browser = raw_input(ask_open)
        if open_browser in ('N', 'n'):
            print "结果可以在本目录下的index.html中查看，再见！".decode('utf-8').encode('gbk')
            sys.exit(3)
        if open_browser in ('Y', 'y'):
            print "即将跳转到浏览器...".decode('utf-8').encode('gbk')
            time.sleep(5)
            webbrowser.open(url,new=1)
            break
