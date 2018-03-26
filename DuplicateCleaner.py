# -*- coding: utf-8 -*- 

"""
Created on Wed Mar 14 08: 08: 52 2018

@author: SCL
"""

import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体,字号等,解决中文乱码显示方框的问题
mpl.rcParams['axes.unicode_minus'] = False
mpl.rcParams['font.size'] = 10
import sys
sys.path.append('E:\\PROGRAM\\UI2') #设置路径，如果与Mythreads同一目录下无法导入Mythreads，启用此行代码，加入实际存放路径
from PyQt5.QtWidgets import QFileDialog,QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import  QtCore, QtGui, QtWidgets
import os,time,collections
from send2trash import send2trash #此模块需要安装，实现移动文件至回收站

#定义全局变量
includedlist = []
ruleoutlist = []
setlist = []
results = []
listshowindex = [i for i in range(20)]
tablelist = []
#UI代码，采用PYQT5 Designer生成，添加了部分设置代码
class Ui_Form(QtWidgets.QWidget):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1022, 643)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(9)
        Form.setFont(font)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pathdef = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pathdef.sizePolicy().hasHeightForWidth())
        self.pathdef.setSizePolicy(sizePolicy)
        self.pathdef.setMinimumSize(QtCore.QSize(0, 30))
        self.pathdef.setObjectName("pathdef")
        self.horizontalLayout.addWidget(self.pathdef, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.searchpath = QtWidgets.QLineEdit(Form)
        self.searchpath.setMinimumSize(QtCore.QSize(0, 25))
        self.searchpath.setObjectName("searchpath")
        self.horizontalLayout.addWidget(self.searchpath, 0, QtCore.Qt.AlignVCenter)
        self.searchstart = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchstart.sizePolicy().hasHeightForWidth())
        self.searchstart.setSizePolicy(sizePolicy)
        self.searchstart.setMinimumSize(QtCore.QSize(0, 30))
        self.searchstart.setObjectName("searchstart")
        self.horizontalLayout.addWidget(self.searchstart, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.ignorempty = QtWidgets.QCheckBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ignorempty.sizePolicy().hasHeightForWidth())
        self.ignorempty.setSizePolicy(sizePolicy)
        self.ignorempty.setObjectName("ignorempty")
        self.gridLayout.addWidget(self.ignorempty, 0, 0, 1, 1, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.ruleout = QtWidgets.QCheckBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ruleout.sizePolicy().hasHeightForWidth())
        self.ruleout.setSizePolicy(sizePolicy)
        self.ruleout.setObjectName("ruleout")
        self.gridLayout.addWidget(self.ruleout, 0, 1, 1, 1, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.ruleoutext = QtWidgets.QLineEdit(self.groupBox)
        self.ruleoutext.setObjectName("ruleoutext")
        self.gridLayout.addWidget(self.ruleoutext, 0, 2, 1, 1)
        self.included = QtWidgets.QCheckBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.included.sizePolicy().hasHeightForWidth())
        self.included.setSizePolicy(sizePolicy)
        self.included.setObjectName("included")
        self.gridLayout.addWidget(self.included, 0, 3, 1, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.includedext = QtWidgets.QLineEdit(self.groupBox)
        self.includedext.setObjectName("includedext")
        self.gridLayout.addWidget(self.includedext, 0, 4, 1, 1, QtCore.Qt.AlignVCenter)
        self.searchall = QtWidgets.QCheckBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchall.sizePolicy().hasHeightForWidth())
        self.searchall.setSizePolicy(sizePolicy)
        self.searchall.setObjectName("searchall")
        self.gridLayout.addWidget(self.searchall, 1, 0, 1, 1, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_12 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 1, 2, 1, 1, QtCore.Qt.AlignVCenter)
        self.label_13 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 1, 4, 1, 1, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.officeext = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.officeext.sizePolicy().hasHeightForWidth())
        self.officeext.setSizePolicy(sizePolicy)
        self.officeext.setMinimumSize(QtCore.QSize(0, 30))
        self.officeext.setObjectName("officeext")
        self.horizontalLayout_2.addWidget(self.officeext, 0, QtCore.Qt.AlignVCenter)
        self.picturext = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.picturext.sizePolicy().hasHeightForWidth())
        self.picturext.setSizePolicy(sizePolicy)
        self.picturext.setMinimumSize(QtCore.QSize(0, 30))
        self.picturext.setObjectName("picturext")
        self.horizontalLayout_2.addWidget(self.picturext, 0, QtCore.Qt.AlignVCenter)
        self.videoext = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.videoext.sizePolicy().hasHeightForWidth())
        self.videoext.setSizePolicy(sizePolicy)
        self.videoext.setMinimumSize(QtCore.QSize(0, 30))
        self.videoext.setObjectName("videoext")
        self.horizontalLayout_2.addWidget(self.videoext, 0, QtCore.Qt.AlignVCenter)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.excelext = QtWidgets.QCheckBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.excelext.sizePolicy().hasHeightForWidth())
        self.excelext.setSizePolicy(sizePolicy)
        self.excelext.setObjectName("excelext")
        self.horizontalLayout_3.addWidget(self.excelext, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.wordext = QtWidgets.QCheckBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wordext.sizePolicy().hasHeightForWidth())
        self.wordext.setSizePolicy(sizePolicy)
        self.wordext.setObjectName("wordext")
        self.horizontalLayout_3.addWidget(self.wordext, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.pptext = QtWidgets.QCheckBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pptext.sizePolicy().hasHeightForWidth())
        self.pptext.setSizePolicy(sizePolicy)
        self.pptext.setObjectName("pptext")
        self.horizontalLayout_3.addWidget(self.pptext, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.jpgext = QtWidgets.QCheckBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jpgext.sizePolicy().hasHeightForWidth())
        self.jpgext.setSizePolicy(sizePolicy)
        self.jpgext.setObjectName("jpgext")
        self.horizontalLayout_3.addWidget(self.jpgext, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.pngext = QtWidgets.QCheckBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pngext.sizePolicy().hasHeightForWidth())
        self.pngext.setSizePolicy(sizePolicy)
        self.pngext.setObjectName("pngext")
        self.horizontalLayout_3.addWidget(self.pngext, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.bmpext = QtWidgets.QCheckBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bmpext.sizePolicy().hasHeightForWidth())
        self.bmpext.setSizePolicy(sizePolicy)
        self.bmpext.setObjectName("bmpext")
        self.horizontalLayout_3.addWidget(self.bmpext, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.aviext = QtWidgets.QCheckBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.aviext.sizePolicy().hasHeightForWidth())
        self.aviext.setSizePolicy(sizePolicy)
        self.aviext.setObjectName("aviext")
        self.horizontalLayout_3.addWidget(self.aviext, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.mkvext = QtWidgets.QCheckBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mkvext.sizePolicy().hasHeightForWidth())
        self.mkvext.setSizePolicy(sizePolicy)
        self.mkvext.setObjectName("mkvext")
        self.horizontalLayout_3.addWidget(self.mkvext, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.mp4ext = QtWidgets.QCheckBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mp4ext.sizePolicy().hasHeightForWidth())
        self.mp4ext.setSizePolicy(sizePolicy)
        self.mp4ext.setObjectName("mp4ext")
        self.horizontalLayout_3.addWidget(self.mp4ext, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.figpielayout = QtWidgets.QGridLayout()
        self.figpielayout.setHorizontalSpacing(7)
        self.figpielayout.setObjectName("figpielayout")

        self.horizontalLayout_8.addLayout(self.figpielayout)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.allnumlabel = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(14)
        self.allnumlabel.setFont(font)
        self.allnumlabel.setObjectName("allnumlabel")
        self.gridLayout_3.addWidget(self.allnumlabel, 1, 0, 1, 1, QtCore.Qt.AlignRight)
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 2, 0, 1, 1)
        self.disposalnum = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(14)
        self.disposalnum.setFont(font)
        self.disposalnum.setObjectName("disposalnum")
        self.gridLayout_3.addWidget(self.disposalnum, 3, 0, 1, 1, QtCore.Qt.AlignRight)
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 4, 0, 1, 1)
        self.duplicatednum = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(14)
        self.duplicatednum.setFont(font)
        self.duplicatednum.setObjectName("duplicatednum")
        self.gridLayout_3.addWidget(self.duplicatednum, 5, 0, 1, 1, QtCore.Qt.AlignRight)
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 6, 0, 1, 1)
        self.preleasespace = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(14)
        self.preleasespace.setFont(font)
        self.preleasespace.setObjectName("preleasespace")
        self.gridLayout_3.addWidget(self.preleasespace, 7, 0, 1, 1, QtCore.Qt.AlignRight)
        self.horizontalLayout_8.addLayout(self.gridLayout_3)
        self.frame_2 = QtWidgets.QFrame(self.groupBox_2)
        self.frame_2.setMinimumSize(QtCore.QSize(50, 0))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_8.addWidget(self.frame_2)
        self.gridLayout_4.addLayout(self.horizontalLayout_8, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.progressBar = QtWidgets.QProgressBar(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setValue(0)
        self.horizontalLayout_4.addWidget(self.progressBar, 0, QtCore.Qt.AlignVCenter)
        self.searchstop = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchstop.sizePolicy().hasHeightForWidth())
        self.searchstop.setSizePolicy(sizePolicy)
        self.searchstop.setMinimumSize(QtCore.QSize(0, 30))
        self.searchstop.setObjectName("searchstop")
        self.horizontalLayout_4.addWidget(self.searchstop, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.savesearchlist = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.savesearchlist.sizePolicy().hasHeightForWidth())
        self.savesearchlist.setSizePolicy(sizePolicy)
        self.savesearchlist.setMinimumSize(QtCore.QSize(0, 30))
        self.savesearchlist.setObjectName("savesearchlist")
        self.horizontalLayout_4.addWidget(self.savesearchlist, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_9.addLayout(self.verticalLayout_2)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_9.addWidget(self.line)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_11 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(11)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_4.addWidget(self.label_11)
        self.dellists = QtWidgets.QTableWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dellists.sizePolicy().hasHeightForWidth())
        self.dellists.setSizePolicy(sizePolicy)
        self.dellists.setMinimumSize(QtCore.QSize(350, 450))
        self.dellists.setBaseSize(QtCore.QSize(0, 0))
        self.dellists.setShowGrid(True)
        self.dellists.setRowCount(20)
        self.dellists.setColumnCount(4)
        self.dellists.setObjectName("dellists")
        item = QtWidgets.QTableWidgetItem()
        self.dellists.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.dellists.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.dellists.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        
        self.dellists.setHorizontalHeaderItem(3, item)
        self.dellists.horizontalHeader().setDefaultSectionSize(80)
        self.dellists.horizontalHeader().setMinimumSectionSize(50)
        self.dellists.verticalHeader().setDefaultSectionSize(23)
        self.dellists.verticalHeader().setMinimumSectionSize(22)
        self.dellists.setColumnWidth(0,150)
        self.dellists.setColumnWidth(1,100)
        self.dellists.setColumnWidth(3,200)
        self.dellists.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.dellists.setSelectionMode(QtWidgets.QTableWidget.ExtendedSelection)
        self.dellists.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        
        self.verticalLayout_4.addWidget(self.dellists)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.prepage = QtWidgets.QPushButton(Form)
        self.prepage.setMinimumSize(QtCore.QSize(0, 30))
        self.prepage.setObjectName("prepage")
        self.horizontalLayout_5.addWidget(self.prepage)
        self.nextpage = QtWidgets.QPushButton(Form)
        self.nextpage.setMinimumSize(QtCore.QSize(0, 30))
        self.nextpage.setObjectName("nextpage")
        self.horizontalLayout_5.addWidget(self.nextpage)
        self.confirmonebyone = QtWidgets.QPushButton(Form)
        self.confirmonebyone.setMinimumSize(QtCore.QSize(0, 30))
        self.confirmonebyone.setObjectName("confirmonebyone")
        self.horizontalLayout_5.addWidget(self.confirmonebyone)
        self.hlatestfile = QtWidgets.QPushButton(Form)
        self.hlatestfile.setMinimumSize(QtCore.QSize(0, 30))
        self.hlatestfile.setObjectName("hlatestfile")
        self.horizontalLayout_5.addWidget(self.hlatestfile)
        self.disposalcancel = QtWidgets.QPushButton(Form)
        self.disposalcancel.setMinimumSize(QtCore.QSize(0, 30))
        self.disposalcancel.setObjectName("disposalcancel")
        self.horizontalLayout_5.addWidget(self.disposalcancel)
        self.executelist = QtWidgets.QPushButton(Form)
        self.executelist.setMinimumSize(QtCore.QSize(0, 30))
        self.executelist.setObjectName("executelist")
        self.horizontalLayout_5.addWidget(self.executelist)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_14 = QtWidgets.QLabel(Form)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_6.addWidget(self.label_14)
        self.delnum = QtWidgets.QLabel(Form)
        self.delnum.setObjectName("delnum")
        self.horizontalLayout_6.addWidget(self.delnum)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.label_15 = QtWidgets.QLabel(Form)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_6.addWidget(self.label_15)
        self.releasespace = QtWidgets.QLabel(Form)
        self.releasespace.setObjectName("releasespace")
        self.horizontalLayout_6.addWidget(self.releasespace)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem1)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.disposalstatus = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.disposalstatus.sizePolicy().hasHeightForWidth())
        self.disposalstatus.setSizePolicy(sizePolicy)
        self.disposalstatus.setMinimumSize(QtCore.QSize(300, 30))
        self.disposalstatus.setMaximumSize(QtCore.QSize(400, 50))
        
        font = QtGui.QFont()
        font.setPointSize(10)
        self.disposalstatus.setFont(font)
        self.disposalstatus.setObjectName("disposalstatus")
        self.verticalLayout_4.addWidget(self.disposalstatus)
        self.horizontalLayout_9.addLayout(self.verticalLayout_4)
        self.horizontalLayout_10.addLayout(self.horizontalLayout_9)
        self.groupBox_2.raise_()
        self.groupBox.raise_()
        self.executelist.raise_()
        self.disposalcancel.raise_()
        self.progressBar.raise_()
        self.searchpath.raise_()
        self.pathdef.raise_()
        self.searchstart.raise_()
        self.searchstop.raise_()
        self.savesearchlist.raise_()
        self.hlatestfile.raise_()
        self.confirmonebyone.raise_()
        self.line.raise_()
        self.dellists.raise_()
        self.label_11.raise_()
        self.nextpage.raise_()
        self.prepage.raise_()
        self.label_14.raise_()
        self.label_15.raise_()
        self.delnum.raise_()
        self.releasespace.raise_()
        self.disposalstatus.raise_()

        self.ignorempty.toggle()    #忽略空文件复选框默认选择
        self.searchall.toggle()     #检索全部格式文件复选框默认选择
        self.executelist.setEnabled(False)  #与结果相关按钮及表格部分按钮界面初始化时默认不可用
        self.nextpage.setEnabled(False)
        self.prepage.setEnabled(False)
        self.disposalcancel.setEnabled(False)
        self.hlatestfile.setEnabled(False)
        self.confirmonebyone.setEnabled(False)
        self.searchstop.setEnabled(False)
        self.savesearchlist.setEnabled(False)

        self.retranslateUi(Form)

        self.pathdef.clicked.connect(self.dirselect)    #点击“检索路径”按钮，通过dirselect槽函数启动系统对话框
        self.searchstart.clicked.connect(self.getlist)  #点击“开始”按钮，通过getlist槽函数启动检索处理程序
        self.officeext.clicked.connect(self.wordext.click)  #点击“office文件”、“图片文件”、“视频文件”按钮，设置office文件常见后缀复选框状态
        self.officeext.clicked.connect(self.excelext.click)
        self.officeext.clicked.connect(self.pptext.click)
        self.picturext.clicked.connect(self.jpgext.click)
        self.picturext.clicked.connect(self.pngext.click)
        self.picturext.clicked.connect(self.bmpext.click)
        self.videoext.clicked.connect(self.aviext.click)
        self.videoext.clicked.connect(self.mp4ext.click)
        self.videoext.clicked.connect(self.mkvext.click)
        self.nextpage.clicked.connect(self.nextpageshow)     #点击“上一页”、“下一页”按钮，通过相应槽函数显示删除文件列表
        self.prepage.clicked.connect(self.prepageshow)  

        self.searchstop.clicked.connect(self.threadstop)    #点击“停止”按钮，通过相应槽函数停止检索处理线程

        self.wordext.stateChanged['int'].connect(self.checkboxsel)  #监控相应按钮、文本框、复选框状态，通过checkboxsel槽函数更新和获取设置信息
        self.excelext.stateChanged['int'].connect(self.checkboxsel)
        self.pptext.stateChanged['int'].connect(self.checkboxsel)
        self.jpgext.stateChanged['int'].connect(self.checkboxsel)
        self.pngext.stateChanged['int'].connect(self.checkboxsel)
        self.bmpext.stateChanged['int'].connect(self.checkboxsel)
        self.aviext.stateChanged['int'].connect(self.checkboxsel)
        self.mp4ext.stateChanged['int'].connect(self.checkboxsel)
        self.mkvext.stateChanged['int'].connect(self.checkboxsel)
        self.searchall.stateChanged['int'].connect(self.checkboxsel)
        self.ruleout.stateChanged['int'].connect(self.checkboxsel)
        self.included.stateChanged['int'].connect(self.checkboxsel)
        self.ruleoutext.textChanged.connect(self.checkboxsel)
        self.includedext.textChanged.connect(self.checkboxsel)

        self.savesearchlist.clicked.connect(self.saveresults)   #点击“保存检索结果”按钮，通过saveresults槽函数保存结果至检索目录，文件格式为txt
        self.confirmonebyone.clicked.connect(self.onebyoneconf) #点击“逐一确认”按钮，通过onebyoneconf在表格中显示所有重复文件信息，供用户选择需要保留的文件
        self.disposalcancel.clicked.connect(self.removeselect)  #点击“排除”按钮，通过removeselect从删除文件列表中移除选中文件记录
        self.executelist.clicked.connect(self.delconfirm)   #点击“执行”按钮，通过delconfirm提示用户，删除列表中文件至回收站
        self.hlatestfile.clicked.connect(self.hlatestinitial)   #点击“保留最新”按钮，通过hlatestinitial自动从删除列表中移除最新修改文件
        self.dellists.itemDoubleClicked.connect(self.openfile)  #双击列表相应文件，通过openfile调用系统功能，打开文件

        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "文件搜索去重工具-by Tech v1.0"))
        self.pathdef.setText(_translate("Form", "检索路径"))
        self.searchstart.setText(_translate("Form", "开始"))
        self.groupBox.setTitle(_translate("Form", "搜索选项"))
        self.ignorempty.setText(_translate("Form", "忽略空文件"))
        self.ruleout.setText(_translate("Form", "排除"))
        self.included.setText(_translate("Form", "包括"))
        self.searchall.setText(_translate("Form", "所有格式文件"))
        self.label_12.setText(_translate("Form", "<html><head/><body><p>*多个后缀名以&quot;,&quot;隔开</p></body></html>"))
        self.label_13.setText(_translate("Form", "<html><head/><body><p>*多个后缀名以&quot;,&quot;隔开</p></body></html>"))
        self.officeext.setText(_translate("Form", "Office文件"))
        self.picturext.setText(_translate("Form", "图片搜索"))
        self.videoext.setText(_translate("Form", "视频搜索"))
        self.excelext.setText(_translate("Form", "Excel"))
        self.wordext.setText(_translate("Form", "Word"))
        self.pptext.setText(_translate("Form", "PPT"))
        self.jpgext.setText(_translate("Form", "jpg/jpeg"))
        self.pngext.setText(_translate("Form", "PNG"))
        self.bmpext.setText(_translate("Form", "BMP"))
        self.aviext.setText(_translate("Form", "AVI"))
        self.mkvext.setText(_translate("Form", "MKV"))
        self.mp4ext.setText(_translate("Form", "MP4"))
        self.groupBox_2.setTitle(_translate("Form", "检索结果概览"))
        self.label.setText(_translate("Form", "文件总数："))
        self.allnumlabel.setText(_translate("Form", "0"))
        self.label_2.setText(_translate("Form", "检索用时："))
        self.disposalnum.setText(_translate("Form", "0"))
        self.label_3.setText(_translate("Form", "重复文件总数："))
        self.duplicatednum.setText(_translate("Form", "0"))
        self.label_4.setText(_translate("Form", "预计可清理空间："))
        self.preleasespace.setText(_translate("Form", "0"))
        self.searchstop.setText(_translate("Form", "停止"))
        self.savesearchlist.setText(_translate("Form", "保存搜索结果"))
        self.label_11.setText(_translate("Form", "拟删除文件列表："))
        self.dellists.setSortingEnabled(True)
        item = self.dellists.horizontalHeaderItem(0)
        item.setText(_translate("Form", "文件名"))
        item = self.dellists.horizontalHeaderItem(1)
        item.setText(_translate("Form", "修改日期"))
        item = self.dellists.horizontalHeaderItem(2)
        item.setText(_translate("Form", "文件大小"))
        item = self.dellists.horizontalHeaderItem(3)
        item.setText(_translate("Form", "存储位置"))
        self.prepage.setText(_translate("Form", "上一页"))
        self.nextpage.setText(_translate("Form", "下一页"))
        self.confirmonebyone.setText(_translate("Form", "逐一确认"))
        self.hlatestfile.setText(_translate("Form", "保留最新"))
        self.disposalcancel.setText(_translate("Form", "排除"))
        self.executelist.setText(_translate("Form", "执行"))
        self.label_14.setText(_translate("Form", "拟删除文件数："))
        self.delnum.setText(_translate("Form", "0"))
        self.label_15.setText(_translate("Form", "可清理空间："))
        self.releasespace.setText(_translate("Form", "0"))
        self.disposalstatus.setText(_translate("Form", ""))

        self._fig = Figure(figsize = (4, 5), dpi = 100) #定义绘图特性
        self._canvas = FigureCanvas(self._fig)  #定义画布
        self.figpielayout.addWidget(self._canvas) #向指定布局添加画布
        self.axes = self._fig.add_subplot(111)  
        self.axes.get_yaxis().set_visible(False)    #设置坐标轴不可见
        self.axes.get_xaxis().set_visible(False)
        self.axes.spines['right'].set_color('none') #设置图框不可见
        self.axes.spines['top'].set_color('none')
        self.axes.spines['bottom'].set_color('none')
        self.axes.spines['left'].set_color('none')

    def dirselect(self,Form):   #调用系统对话框，选择检索路径，默认为c:/
        try:
            directory1 = QFileDialog.getExistingDirectory(self,"选取文件夹","C:/")
            self.searchpath.setText(directory1)
        except:
            print(sys.exc_info())

    def getlist(self):  #初始化界面和程序，获取界面设置信息，启动检索线程
        #初始化变量
        global includedlist,ruleoutlist,setlist,results,listshowindex,tablelist
        includedlist = []
        ruleoutlist = []
        setlist = []
        results = []
        listshowindex = [i for i in range(20)]
        tablelist = []
        #初始化界面
        self.checkboxsel()
        self.progressBar.setValue(0)
        self.dellists.clearContents()
        self.tableinit([])
        self.disposalnum.setText('0')
        self.duplicatednum.setText('0')
        self.preleasespace.setText('0')
        self.allnumlabel.setText('0')
        self.releasespace.setText('0')
        self.delnum.setText('0')
        self.axes.clear()   #
        self._canvas.draw()
        self.searchstop.setEnabled(False)
        self.savesearchlist.setEnabled(False)
        self.searchstart.setEnabled(False)
        #获取界面状态，添加设置信息到变量
        if self.ignorempty.isChecked():
            setlist.append(int(1))
        else:
            setlist.append(int(0))
        setlist.append(ruleoutlist)
        setlist.append(includedlist)
        #导入检索线程
        from Mythreads import SearchThread
        print(setlist)

        if self.searchpath.text():
            mypath = self.searchpath.text() #获取检索路径

            if os.path.exists(mypath):  #路径存在，设置检索变量，定义信号与槽的连接，开始线程
                setlist.append(mypath)
                print(setlist,'\n','已完成搜索设置，发出检索请求！\n')
                self.disposalstatus.setText('已获取搜索设置，并发出检索请求！')
                self.searchthread = SearchThread(setlist)
                self.searchthread.ListGetSignal.connect(self.ShowSum)   #检索完成与结果处理连接
                self.searchthread.sumsignal.connect(self.drawfig)   #概览信息与绘图连接
                self.searchthread.allnumsignal.connect(self.setallnum)  #文件总数与显示连接
                self.searchthread.nownumsignal.connect(self.setprogressbar) #完成数与进度条设置连接
                self.searchthread.nowfilesignal.connect(self.setdispstatus) #当前文件与信息显示连接
                self.searchthread.hlatestsignal.connect(self.tableinit) #保留最新文件列表与表格初始化连接

                self.searchthread.start()
                self.disposalstatus.setText('检索开始！')    #更新界面信息

            else:    #如果路径不存在，显示提示框
                QMessageBox.information(self,"提示","请输入正确的路径！")  
                self.searchstart.setEnabled(True)

        else:   ##如果检索路径文本框为空，显示提示框
            QMessageBox.information(self,"提示","请通过检索路径按钮选择或直接输入路径！")
            self.searchstart.setEnabled(True)

    def onebyoneconf(self): #调用检索线程onebyone函数获取所有重复文件的列表信息，并更新表格显示
        global tablelist,results
        tablelist = self.searchthread.onebyone(results)
        self.tableinit(tablelist)

    def hlatestinitial(self):   #调用检索线程Hlatest函数获取保留最新列表信息，并更新表格显示
        global results,tablelist
        initialtablelist = self.searchthread.Hlatest(results)
        tablelist = initialtablelist
        self.tableinit(initialtablelist)

    def delconfirm(self):   #点击执行按钮后，询问用户是否确认删除列表所示文件
        global tablelist
        tablelistcopy = tablelist
        button = QMessageBox.warning(self,"警告",
                                   self.tr("是否确认删除列表中所有文件?"),
                                   QMessageBox.Ok|QMessageBox.Cancel,
                                   QMessageBox.Cancel)
        if button == QMessageBox.Ok:    #用户确认后删除文件
            for file in tablelistcopy:
                if os.path.exists(file[0]):
                    try:
                        send2trash(file[0])
                        self.disposalstatus.setText(file[0])

                    except:
                        print('无法删除指定文件：%s'%file[0])
                else:
                    print('指定文件不存在：%s'%file[0])
            tablelist = []  #删除后情况列表变量，更新表格和界面，显示提示信息
            self.tableinit(tablelist)
            self.disposalstatus.setText('删除完成！')
            QMessageBox.warning(self,"提示",
                                self.tr("文件删除完成，所有文件均移至回收站，如果需要可从回收站恢复文件！"),
                                QMessageBox.Ok,
                                QMessageBox.Ok)

        if button == QMessageBox.Discard:
            pass

    def removeselect(self): #点击排除按钮，从列表中移除选中文件
        global listshowindex,tablelist
        self.selectedRow = []   #用于保存需要移除信息的行号
        item = self.dellists.selectedItems()    #获取表格中选中项目
        for i in item:
            if self.dellists.indexFromItem(i).row() not in self.selectedRow:    #如果不在变量中则添加所选行号
                self.selectedRow.append(self.dellists.indexFromItem(i).row())   
        for j in self.selectedRow:
            tablelist[listshowindex[j]] = [] #更新移除列表删除项为空列表
#        print(tablelist)
        filtertablelist = filter(lambda x: x !=  [], tablelist)  #过滤移除列表中空列表
        tablelist = list(filtertablelist)   #将filter转换为List
#        print(tablelist)

        self.showtable()    #更新表格和界面
        filenum = len(tablelist)
        self.delnum.setText(str(filenum))
        releasespace = 0
        for file in tablelist:
            releasespace  += file[3]
        self.releasespace.setText(self.searchthread.sizeconvert(releasespace))

    def setdispstatus(self,filename):   #在界面显示目前操作文件的路径信息
        self.filename = filename
        self.disposalstatus.setText(self.filename)

    def saveresults(self):  #以txt格式保存检索结果至检索目录
        global setlist,results
        saveformat = collections.OrderedDict()  #设置输出内容为有序字典
        saveformat['时间:\t'] = time.strftime('%Y - %m - %d %H:%M:%S',time.localtime(time.time()))
        saveformat['检索路径:\t'] = setlist[3]
        saveformat['是否忽略空文件:\t'] = setlist[0]
        saveformat['排除文件格式:\t'] = setlist[1]
        saveformat['包括文件格式:\t'] = setlist[2]
        saveformat['文件总数:\t'] = results[0]
        saveformat['检索耗时:\t'] = results[1]
        saveformat['重复文件数量:\t'] = results[2]
        saveformat['预计可清理空间:\t'] = results[3]
        saveformat['序号:\t\t\t'] = 'MD5' + '\t\t\t' + '大小' + '\t\t' + '格式' + '\t' + '路径'
        print(saveformat)
        print('准备写入文件！')
        self.disposalstatus.setText('准备写入文件！')
        try:
            with open('%s\\Dupclresults.txt'%setlist[3], 'wt') as f:    #以文本写入方式打开文件
                for k,v in saveformat.items():
                    print('%s%s'%(k,v), file = f)   #打印输出字符串
                i = 0
                for rk,rv in results[4].items():
                    print('%s\t%s\t%s\t\t%s\t%s\n'%(i,rk,rv[0],rv[1],rv[2:]) ,file = f)
                    i  += 1
            print('结果写入完成！')
            self.disposalstatus.setText('结果写入完成！')
        except:
            print(sys.exc_info())
            print('无法写入文件！')

    def tableinit(self,listtoremove):   #初始化表格
        global listshowindex,tablelist
        listshowindex = [i for i in range(20)]  #初始化显示序号
        tablelist = listtoremove

        self.prepage.setEnabled(False)  
        self.dellists.clearContents()   #清空表格内容
        self.delnum.setText('0')    
        self.releasespace.setText('0')
        self.hlatestfile.setEnabled(False)
        self.executelist.setEnabled(False)
        self.disposalcancel.setEnabled(False)
        self.confirmonebyone.setEnabled(False)

        filenum = len(tablelist)
        if filenum == 0:    #控制界面按钮状态，初始化表格界面
            self.executelist.setEnabled(False)
            self.disposalcancel.setEnabled(False)
            self.confirmonebyone.setEnabled(False)
            self.hlatestfile.setEnabled(False)
            self.nextpage.setEnabled(False)
        elif filenum>0:
            self.executelist.setEnabled(True)
            self.disposalcancel.setEnabled(True)
            self.confirmonebyone.setEnabled(True)
            self.hlatestfile.setEnabled(True)
            self.nextpage.setEnabled(True)
            self.showtable()
            self.delnum.setText(str(filenum))
            releasespace = 0
            for file in tablelist:
                releasespace  += file[3]
            self.releasespace.setText(self.searchthread.sizeconvert(releasespace))
        else:
            pass

    def openfile(self): #双击表格文件信息，调用系统功能显示文件
        global tablelist
        item = self.dellists.selectedItems()
        try:    #采用系统默认程序打开文件
            os.startfile(tablelist[listshowindex[self.dellists.indexFromItem(item[0]).row()]][0])
        except:
            print(sys.exc_info())
            print('无法打开指定文件!')
            QMessageBox.warning(self,"提示",
                                self.tr("无法打开指定文件!"),
                                QMessageBox.Ok,
                                QMessageBox.Ok)

    def nextpageshow(self): #点击下一页更新表格和界面按钮状态
        global listshowindex,tablelist
        listshowindex = [i + 20 for i in listshowindex] #更新显示序号
        filenum = len(tablelist)
        self.showtable()
        self.prepage.setEnabled(True)
        if listshowindex[19] + 1 >= filenum:    #如果剩余内容不够一页，下一页按钮将不可用
            self.nextpage.setEnabled(False)

    def prepageshow(self):  #点击上一页更新表格和界面按钮状态
        global listshowindex
        listshowindex = [i - 20 for i in listshowindex] #更新显示序号
        self.showtable()
        self.nextpage.setEnabled(True)
        if listshowindex[0] == 0:   #如果显示序号为0，上一页按钮不可用
            self.prepage.setEnabled(False)

    def showtable(self):    #显示拟删除文件列表
        global listshowindex,tablelist,setlist
        self.listtoremove = tablelist
#        print(self.listtoremove)
        filenum = len(self.listtoremove)
        self.dellists.clearContents()
#        print(listshowindex)
        if listshowindex[19] + 1 <= filenum:    #如果显示序号在信息总数以内，执行以下代码
            j = 0
            for i in listshowindex: #逐一设置表格显示内容
#                print(self.listtoremove[i][1])
                self.dellists.setItem(j, 0, QtWidgets.QTableWidgetItem(self.listtoremove[i][1]))
                self.dellists.setItem(j, 1, QtWidgets.QTableWidgetItem(self.listtoremove[i][2]))
                self.dellists.setItem(j, 2, QtWidgets.QTableWidgetItem(self.searchthread.sizeconvert(self.listtoremove[i][3])))
                self.dellists.setItem(j, 3, QtWidgets.QTableWidgetItem(self.listtoremove[i][0].replace(setlist[3], '..', 1)))   #将绝对路径通过字符串替换转换为相对路径，缩短显示长度
                j  += 1
            if listshowindex[19] + 1 == filenum:    #如果显示序号与内容总数相等，则下一页不可用
                self.nextpage.setEnabled(False)
        elif listshowindex[19] + 1>filenum: #如果显示序号大于内容总数，则执行以下代码
            indexnum = divmod(filenum,20)[1]    #总数取余获取最后一页显示序号的序号
#            print(indexnum)
            j = 0
            for i in listshowindex[:indexnum]:
#                print(self.listtoremove[i][1])
                self.dellists.setItem(j, 0, QtWidgets.QTableWidgetItem(self.listtoremove[i][1]))
                self.dellists.setItem(j, 1, QtWidgets.QTableWidgetItem(self.listtoremove[i][2]))
                self.dellists.setItem(j, 2, QtWidgets.QTableWidgetItem(self.searchthread.sizeconvert(self.listtoremove[i][3])))
                self.dellists.setItem(j, 3, QtWidgets.QTableWidgetItem(self.listtoremove[i][0].replace(setlist[3], '..', 1)))
                j  += 1
            self.nextpage.setEnabled(False)
        else:
            pass

    def threadstop(self):   #停止检索进程
        self.searchthread.stop()
        self.disposalstatus.setText('检索停止！')

    def setallnum(self,num):    #设置文件总数
        self.num = str(num)
        self.allnumlabel.setText(self.num)
        self.searchstop.setEnabled(True)

    def ShowSum(self,sumlistshow):  #显示概览
        self.disposalstatus.setText('搜索结束，显示概览！')
        global results
        results = sumlistshow
        self.dispnum = sumlistshow[1]
        self.duplnum = str(sumlistshow[2])
        self.total_vol = sumlistshow[3]
        self.disposalnum.setText(self.dispnum)
        self.duplicatednum.setText(self.duplnum)
        self.preleasespace.setText(self.total_vol)
        self.savesearchlist.setEnabled(True)    #改变按钮状态
        self.searchstart.setEnabled(True)

    def setprogressbar(self,allnum,nownum): #设置进度条状态
        self.allnum = allnum
        self.nownum = nownum
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(self.allnum)
        self.progressBar.setValue(self.nownum)

    def drawfig(self,sumlist):  #画饼图
        self.labels = sumlist[0]    #提取所需要的变量
        self.size = sumlist[3]
        self.num = sumlist[4]
        self.sizestr = sumlist[1]
        self.numstr = sumlist[2]
        #设置绘制颜色、外框线等参数
        colors  = ["red","orangered","orange","yellowgreen","turquoise","lightskyblue"]
        wedgeporp = {'linewidth':0.8,
                   'edgecolor':'w'
                       }
        samplepie = [1]

        self.axes.clear()   #清空绘图，绘制3个饼图，最内层为纯白饼图，形成环形图
        self.axes.pie(self.size, labels = self.sizestr, colors = colors,labeldistance = 0.75,pctdistance = - 0.8, radius = 1 , wedgeprops = wedgeporp)
        self.axes.pie(self.num, labels = self.numstr, colors = colors,  labeldistance = 0.6, pctdistance = - 0.6, radius = 0.7, wedgeprops = wedgeporp)
        self.axes.pie(samplepie, radius = 0.4,colors = 'w')
        self.axes.set(aspect = "equal", title = '重复文件概览')
        self.axes.legend(self.labels, loc = 'lower center',fontsize = 9, bbox_to_anchor = (0.5, - 0.15),borderaxespad = 0., ncol = 3)

        self._canvas.draw()

    def checkboxsel(self):  #收集界面信息，写入检索设置变量
        global includedlist,ruleoutlist
        includedlist.clear()
        ruleoutlist.clear()
        try:
            if self.searchall.isChecked(): #全部检索与排除可共用，与包括不可共用，排除与包括也不共用，排除与包括共用常用文件格式选择内容
                self.included.setChecked(False)
                if self.ruleout.isChecked():
                    if self.ruleoutext.text():
                        extstr = self.ruleoutext.text()
                        extstrlist = extstr.split(',')
                        for strl in extstrlist:
                            ruleoutlist.append('.' + strl)
                    if self.excelext.isChecked():
                        ruleoutlist.extend(['.xls','.xlsx'])
                    if self.wordext.isChecked():
                        ruleoutlist.extend(['.doc','.docx'])
                    if self.pptext.isChecked():
                        ruleoutlist.extend(['.ppt','.pptx'])
                    if self.jpgext.isChecked():
                        ruleoutlist.extend(['.jpg','.jpeg'])
                    if self.pngext.isChecked():
                        ruleoutlist.extend(['.png'])
                    if self.bmpext.isChecked():
                        ruleoutlist.extend(['.bmp'])
                    if self.aviext.isChecked():
                        ruleoutlist.extend(['.avi'])
                    if self.mp4ext.isChecked():
                        ruleoutlist.extend(['.mp4'])
                    if self.mkvext.isChecked():
                        ruleoutlist.extend(['.mkv'])
            elif self.included.isChecked():
                self.ruleout.setChecked(False)
                if self.includedext.text():
                    extstr = self.includedext.text()
                    extstrlist = extstr.split(',')
                    for strl in extstrlist:
                        includedlist.append('.' + strl)
                if self.excelext.isChecked():
                    includedlist.extend(['.xls','.xlsx'])
                if self.wordext.isChecked():
                    includedlist.extend(['.doc','.docx'])
                if self.pptext.isChecked():
                    includedlist.extend(['.ppt','.pptx'])
                if self.jpgext.isChecked():
                    includedlist.extend(['.jpg','.jpeg'])
                if self.pngext.isChecked():
                    includedlist.extend(['.png'])
                if self.bmpext.isChecked():
                    includedlist.extend(['.bmp'])
                if self.aviext.isChecked():
                    includedlist.extend(['.avi'])
                if self.mp4ext.isChecked():
                    includedlist.extend(['.mp4'])
                if self.mkvext.isChecked():
                    includedlist.extend(['.mkv'])
            else:
                pass
            print(set(includedlist))
            print(set(ruleoutlist))
        except:
            print(sys.exc_info())

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())