# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 08: 08: 52 2018

@author: SCL
"""

from PyQt5 import QtCore
from time import clock as now
import os, hashlib, operator
import time

class SearchThread(QtCore.QThread): 
    ListGetSignal = QtCore.pyqtSignal(list) #信号声明
    sumsignal = QtCore.pyqtSignal(list)
    allnumsignal = QtCore.pyqtSignal(int)
    nownumsignal = QtCore.pyqtSignal(int, int)
    nowfilesignal = QtCore.pyqtSignal(str)
    hlatestsignal = QtCore.pyqtSignal(list)
    
    def __init__(self, pathsets, parent = None): 
        super(SearchThread, self).__init__(parent)
        self.pathsets = pathsets  #获取检索设置
        self.flag = 1   #停止标记初始化
    
    def run(self):  #线程run函数
        filelistsumdef = self.searchfile()  #调用searchfile函数获取检索结果
#        print(filelistsumdef)
        self.ListGetSignal.emit(filelistsumdef) #发射检索概览信号
        self.sumlist = self.listsum(filelistsumdef) #调用listsum获取概览饼图所需信息
        self.sumsignal.emit(self.sumlist)   #发射概览饼图信息信号
        tablehllist = self.Hlatest(filelistsumdef)  #调用Hlatest获取表格显示信息，初始默认为保留最新模式
        self.hlatestsignal.emit(tablehllist)    #发射表格显示信息
        
    def stop(self):     #点击停止按钮调用此函数，将停止标记设为0
        self.flag = 0
        print('检索停止!\n')

    def getmd5(self, filename):     #获取文件MD5值
        m = hashlib.md5()
        self.filename = filename
        file_txt = open(self.filename, 'rb').read()
        m.update(file_txt)
        return m.hexdigest()
    
    def sizeconvert(self, size):    #转换文件大小为格式化字符串
        for (carnum, label) in [(1024**3, 'GB'), (1024**2, 'MB'), (1024, 'KB')]: 
            if size >= carnum: 
                return "%.1f %s"%(size*1.0/carnum, label)
        if size == 1: 
            return "1 byte"
        else: 
            return str(size)+'bytes'
    
    def searchfile(self):   #检索文件
        filelistsum = []    #结果变量清空
        ignoremptyset = self.pathsets[0]    #初始化设置参数
        ruleoutlistset = self.pathsets[1]
        includedlistset = self.pathsets[2]
        pathset = self.pathsets[3]
        print(pathset)  
        all_size = {}
        removelist = {}
        total_file = 0
        all_file = 0
        total_delete = 0
        total_vol = 0
        start = now()
        real_paths = []
        nownum = 0
        start = now()
        
        
        for roots, dirs, files in os.walk(pathset):     #遍历检索指定文件夹及子文件夹下所有文件
            if self.flag == 1:  #停止标记为1时运行以下代码，为0时跳出循环
                for file in files: 
                    all_file += 1   #文件总数计数
                    path = os.path.join(roots, file)    #获取文件绝对路径
#                    print(path)
                    extstr = str.lower(os.path.splitext(path)[1])   #获取文件后缀
                    if ignoremptyset == 1:  #如果忽略空文件，执行以下代码，跳过文件大小为0的文件
                        if os.stat(path).st_size == 0:  #跳过文件大小为0的文件
                            pass
                        else: 
                            if ruleoutlistset:  #如果排除列表不为空
                                if extstr in ruleoutlistset:    #在排除列表中的文件格式不处理
                                    pass
                                else: 
                                    total_file  += 1    #需处理文件计数
                                    real_paths.append(os.path.join(roots, file))    #需处理的文件路径加入real_paths
                            elif includedlistset:   #如果包括列表不为空
                                if extstr in includedlistset:   #在包括列表中的文件格式处理
                                    total_file  += 1
                                    real_paths.append(os.path.join(roots, file))
                            else:   #如果排除与包括列表均为空，所有非空文件都处理
                                total_file  += 1
                                real_paths.append(os.path.join(roots, file))
                    elif ruleoutlistset:    #处理空文件条件下，如果排除列表不为空，执行以下代码
                        if extstr in ruleoutlistset: 
                            pass
                        else: 
                            total_file  += 1
                            real_paths.append(os.path.join(roots, file))
                    elif includedlistset:   #处理空文件条件下，如果包括列表不为空，执行以下代码
                        if extstr in includedlistset: 
                            total_file  += 1
                            real_paths.append(os.path.join(roots, file))
                    else:   #处理空文件条件下，排除与包括列表均为空，执行以下代码，即所有文件均处理
                        total_file  += 1
                        real_paths.append(os.path.join(roots, file))
#                print(real_paths)
                self.allnumsignal.emit(all_file)    #发射所有文件数量信号
            else: 
                break
         
        for real_path in real_paths:    #对在处理列表中的文件执行以下代码，查找重复文件
            
            if self.flag == 1:  #停止标记为1时运行
            
                if os.path.isfile(real_path) == True:   #判断是否为文件
                    self.nowfilesignal.emit(real_path)  #发射当前文件信息
                    size = os.stat(real_path).st_size   #获取文件大小
                    name_and_md5 = [real_path, '']      #临时变量，存放文件与MD5列表
                        
                    if size in all_size.keys():     #对于大小重复的文件，计算MD5值
                        new_md5 = self.getmd5(real_path)    #获取文件MD5
                            
                        if all_size[size][1] == '':     #如果记录中MD5为空，补充到记录中
                            all_size[size][1] = self.getmd5(all_size[size][0])
                            
                        if new_md5 in all_size[size]:   #如果当前文件MD5与记录中重复，则加入结果数据中
                            total_delete  += 1  #重复文件计数
                            total_vol  += size  #重复文件大小增加
                                
                                
                            if new_md5 in removelist.keys():    #将重复文件信息加入结果数据中
                                removelist[new_md5].append(real_path)   #字典键为MD5，值为[大小，扩展名，路径...]的列表
                            else: 
                                removelist[new_md5] = [size, str.lower(os.path.splitext(real_path)[1]), all_size[size][0], real_path]
        
                        else: 
                            all_size[size].append(new_md5)  #如果MD5不在记录中则加入记录
                        
                    else: 
                        all_size[size] = name_and_md5   #如果大小不在记录中，则加入记录
                nownum += 1 #当前已处理文件计数
                self.nownumsignal.emit(total_file, nownum)  #发射所有待处理文件和当前已处理文件计数，设置进度条

            else: 
                break

#        print(removelist)
        end=now()    
        time_last = end - start     #检索持续时间
        filelistsum.append(total_file)  #将需要处理的总文件数加入结果变量
        filelistsum.append('%.2f'%time_last+'s')    #格式化持续时间并加入结果变量
        filelistsum.append(total_delete)    #将重复文件数加入结果变量
        filelistsum.append(self.sizeconvert(total_vol)) #将文件大小数据格式化输出
        filelistsum.append(removelist)  #将重复文件信息加入结果变量
        print(filelistsum[0], filelistsum[2], filelistsum[3])

        self.ListGetSignal.emit(filelistsum)    #发射结果数据
        return filelistsum
    
    def listsum(self, removelist):  #通过结果数据计算概览数据
        sumlist = []    #初始化内部变量
        sumdic = {}
        extstr = []
        sizeint = []
        numint = []

        for k in removelist[4]:     #遍历结果数据
            sumdickey = removelist[4][k][1] #提取扩展名作为概览字典的键
            filenum = len(removelist[4][k])-3   #提取重复文件数（-2），-3为可清理的文件数
            persize = removelist[4][k][0]   #提取每个文件的大小
            sumsize = persize*filenum       #计算可清理空间
            if sumdickey in sumdic:     #以扩展名为键，可清理文件数和总大小为值的概览数据
                sumdic[sumdickey][0] += filenum
                sumdic[sumdickey][1] += sumsize
            else: 
                sumdic[sumdickey] = [filenum, sumsize]

        sumdicsorted = sorted(sumdic.items(), key = lambda item: item[1][1], reverse = True)    #对概览结果进行排序，倒序
        print(sumdic)
        print(sumdicsorted)
        
        if len(sumdicsorted)>6:     #如果扩展名数量大于6，执行以下代码
            flag = 0    
            
            for i in range(len(sumdicsorted)): 
                if flag<5:  #前五项均原样加入最终概览结果
                    extstr.append(sumdicsorted[i][0])
                    sizeint.append(sumdicsorted[i][1][1])
                    numint.append(sumdicsorted[i][1][0])
                    flag += 1
                elif flag == 5:     #第六项及以后合计入其它中
                    extstr.append('其它')
                    sizeint.append(sumdicsorted[i][1][1])
                    numint.append(sumdicsorted[i][1][0])
                    flag += 1
                else: 
                    sizeint[5] += sumdicsorted[i][1][1]
                    numint[5] += sumdicsorted[i][1][0]
        else:   #扩展名小于等于6个，均原样加入概览结果中
            for k in range(len(sumdicsorted)): 
                extstr.append(sumdicsorted[k][0])
                sizeint.append(sumdicsorted[k][1][1])
                numint.append(sumdicsorted[k][1][0])
        sizestr = [self.sizeconvert(i) for i in sizeint]    #文件大小格式化
        print(sizestr)
        numstr = [str(i) for i in numint]   #文件数量转化为字符串
        print(numstr)
        sumlist = [extstr, sizestr, numstr, sizeint, numint]    #汇总形成概览数据[扩展名，大小，数量，大小int，数量int]
        print('com', sumlist)
 
        return sumlist

    def Hlatest(self, filelist):    #保留最新表格数据处理
        self.filelist = filelist
        
        listpost = []
        print(self.filelist[4])
        for k in self.filelist[4]:  #遍历结果数据
            listsort = []
            for v in self.filelist[4][k][2: ]:  #遍历结果数据中文件路径信息
                filename = os.path.split(v)[-1]     #获取文件名
                filetime = time.strftime("%Y-%m-%d %H: %M: %S", time.localtime(os.stat(v).st_mtime))    #获取文件修改时间
                filesize = self.filelist[4][k][0]   #获取文件大小
                print(v, filename, filetime, filesize)
                listsort.append([v, filename, filetime, filesize])  #将表格数据加入临时变量
            listsort.sort(key = operator.itemgetter(2), reverse = True)     #对列表进行排序，倒序
            del listsort[0] #将最新修改文件剔除
            for perlist in listsort:    
                listpost.append(perlist)    
        print(listpost)
        return listpost
    
    def onebyone(self, fileonebyone):   #逐一确认表格数据处理，不剔除最新修改文件
        self.fileonebyone = fileonebyone
        listpost = []
#        print(self.fileonebyone[4])
        for k in self.fileonebyone[4]: 
            listsort = []
            for v in self.fileonebyone[4][k][2: ]: 
                filename = os.path.split(v)[-1] 
                filetime = time.strftime("%Y-%m-%d %H: %M: %S", time.localtime(os.stat(v).st_mtime))
                filesize = self.fileonebyone[4][k][0]
#                print(v, filename, filetime, filesize)
                listsort.append([v, filename, filetime, filesize])
            listsort.sort(key = operator.itemgetter(2), reverse = True) 
            for perlist in listsort: 
                listpost.append(perlist)
        print(listpost)
        return listpost