# -*- coding: UTF-8 -*-

import os
from Tkinter import *
from PIL import Image, ImageTk
from tkMessageBox import showwarning
import tkFileDialog
import re

img =None
i=0;
s = None
dirs = None

class Application(Frame):
        def __init__(self, master=None):
            Frame.__init__(self, master)
            self.pack()
            self.createWidgets()

        def createWidgets(self):
            self.path = StringVar()
            self.path.set("e:/duorou1")
            self.L_path = Label(self,text = "多肉位置：",font =(16))
            self.L_path.pack(padx=5,pady=10,side=LEFT)
            self.E_path = Entry(self,textvariable = self.path,font =(16))
            self.E_path.pack(padx=5,pady=20,side=LEFT)
            self.B_path = Button(self,text = "路径选择",font =(16),command = self.selectPath)
            self.B_path.pack(padx=5,pady=20,side=LEFT)
            self.L_name = Label(self,text = "修改为：",font = (16))
            self.L_name.pack(padx=5,pady=50,side=BOTTOM)
            self.nameInput = Entry(self, font =("楷体",16))
            self.nameInput.pack(padx=5,pady=500,side=LEFT)
            self.quitButton = Button(self, text="确定", font=(16), command=self.rename)
            self.quitButton.pack(padx=5,pady=50,side=LEFT)
        def showImg(self):
            global img
            load = Image.open(s)
            render= ImageTk.PhotoImage(load)
            img = Label(self,image=render)
            img.image = render
            img.pack()
            return img
        def rename(self):
            global i
            global s
            global img
            n=self.nameInput.get()
            if i<len(dirs)-3:
                print i,len(dirs)
                os.rename(rootdir+os.sep+dirs[i],rootdir+os.sep+n+".jpg")
                os.rename(rootdir+os.sep+dirs[i+1],rootdir+os.sep+n+"(1)"+".jpg")
                os.rename(rootdir+os.sep+dirs[i+2],rootdir+os.sep+n+"(2)"+".jpg")
                i=i+3
                s=rootdir+os.sep+dirs[i]
                load = Image.open(s)
                render= ImageTk.PhotoImage(load)
                img.configure(image = render)
                img.image = render
            else:
                showwarning("open","修改已全部完成！")
        def  selectPath(self):
            path_ = tkFileDialog.askdirectory()
            global dirs
            global s
            pattern = re.compile(".*\.(jpg|JPG)")
            is_show = 1
            self.path.set(path_)
            dirs = os.listdir(path_)
            s=path_+os.sep+dirs[i]
            for file in dirs:
                if not pattern.match(file):
                    print file
                    showwarning("open","请选择全为图片的文件夹！")
                    is_show = 0
                    break
            if is_show == 1 and len(dirs)//3 !=0:
                showwarning("open","警告：您所选择的图片个数不为3的倍数\n重命名后文件名可能发生错乱\n请修改文件夹后重试")
                is_show = 0
            if is_show == 1:    
                self.showImg()
            
app =Application()
app.master.title("REname")
app.master.geometry("900x900")
app.mainloop()

      
      
