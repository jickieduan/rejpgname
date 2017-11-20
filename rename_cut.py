# -*- coding: utf-8 -*-

import os
from Tkinter import *
from PIL import Image, ImageTk
from tkMessageBox import showwarning
import tkFileDialog
import re
import shutil
import datetime
import sys
import zipfile

reload(sys)
sys.setdefaultencoding( "utf-8" )
img =None #图片显示
i=0; #记录当前在目录中的位置
img_path = None# 要显示的图片的路径
dirs = None#文件夹目录
li_name=["_ddd","_jjj"]#用于存放使用过的所有文件名
is_rename=0 #是否进行重命名

class Application(Frame):
        def __init__(self, master=None):
            Frame.__init__(self, master)
            self.pack()
            self.createWidgets()

        def createWidgets(self):
            self.path = StringVar()
            self.nname = StringVar()
            self.path.set("")
            self.L_path = Label(self,text = "多肉位置：",font =(16))
            self.L_path.grid(row=1,column=1)
            self.E_path = Entry(self,textvariable = self.path,font =(16))
            self.E_path.grid(row=1,column=2)
            self.B_path = Button(self,text = "路径选择",font =(16),command = self.selectPath)
            self.B_path.grid(row=1,column=3)
            self.L_name = Label(self,text = "修改为：",font = (16))
            self.L_name.grid(row=2,column=1)
            self.nameInput = Entry(self, textvariable = self.nname,font =(16))
            self.nameInput.grid(row=2,column=2)
            self.quitButton = Button(self, text="确定", font=(16), command=self.rename)
            self.quitButton.grid(row=2,column=3)
            self.B_cut = Button(self,text = "裁剪",font=(16), command=self.cut)
            self.B_cut.grid(row=1,column=4)
            self.B_zip = Button(self,text = "压缩",font=(16), command=self.zip) 
            self.B_zip.grid(row=2,column=4)
        #显示图片函数
        def showImg(self):
            global img
            load = Image.open(s)
            render= ImageTk.PhotoImage(load)
            img = Label(self,image=render)
            img.image = render
            img.grid(row=4,columnspan=10)
            return img
        #重命名函数
        def rename(self):
            global i
            global s
            global img
            global li_name
            global is_rename
            if dirs == None:
                    showwarning("提示","请先选择文件夹！")
                    is_rename = 1
            n=self.nameInput.get()
            _n=n+".jpg"
            for  named in li_name:
                    if named == _n:
                            showwarning("警告","这个名字已经存在啦！")
                            is_rename = 1
                            break
                
            if is_rename == 0 :
                os.rename(self.E_path.get()+os.sep+dirs[i],self.E_path.get()+os.sep+n+".jpg")
                os.rename(self.E_path.get()+os.sep+dirs[i+1],self.E_path.get()+os.sep+n+"(1)"+".jpg")
                os.rename(self.E_path.get()+os.sep+dirs[i+2],self.E_path.get()+os.sep+n+"(2)"+".jpg")
                li_name.append(n+".jpg")
                li_name.append(n+"(1)"+".jpg")
                li_name.append(n+"(2)"+".jpg")
                i=i+3
                if (i>=len(dirs)):
                        is_rename = 1
                        showwarning("提示","修改已全部完成！")
                else:
                        img_path=self.E_path.get()+os.sep+dirs[i]
                        load = Image.open(img_path)
                        render= ImageTk.PhotoImage(load)
                        img.configure(image = render)
                        img.image = render
                        self.nname.set("")
            elif is_rename == 1:
                showwarning("提示","修改已全部完成！")
        #文件夹选择函数
        def  selectPath(self):
            path_ = tkFileDialog.askdirectory()
            global dirs
            global s
            global li_name
            pattern = re.compile(".*\.(jpg|JPG)")
            is_show = 1
            self.path.set(path_)
            dirs = os.listdir(path_)
            if(len(dirs)==0):
                    showwarning("警告","您选择了一个空文件夹。。。")
                    is_show = 0
            if is_show ==1:
                    s=path_+os.sep+dirs[i]
            for file in dirs:
                if not pattern.match(file):
                    showwarning("提示","请选择全为图片的文件夹！")
                    is_show = 0
                    break
            if is_show == 1 and len(dirs)%3 !=0:
                showwarning("警告","警告：您所选择的图片个数不为3的倍数\n重命名后文件名可能发生错乱\n请修改文件夹后重试")
                is_show = 0
            if is_show == 1:
                li_name=["_ddd","_jjj"]
                is_rename=1
                for file in dirs:
                        li_name.append(str(file))
                self.showImg()
        #图片剪裁函数
        def cut(self):
            global dirs
            path = self.E_path.get()
            datename = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H.%M.%S")+"_cut"
            os.makedirs(m_path)
            for file in dirs:
                im = Image.open(self.E_path.get()+os.sep+file)
                h = max(im.size)
                w = min(im.size)
                x = 0
                y=(h-w)/2
                region = im.crop((x,y,x+w,y+w))
                out = region.resize((750, 750),Image.ANTIALIAS)  
                out.save(m_path+os.sep+file)
            self.path.set(m_path)
            dirs = os.listdir(m_path)
            img_path = self.E_path.get()+os.sep+dirs[i]
            load = Image.open(img_path)
            render= ImageTk.PhotoImage(load)
            img.configure(image = render)
            img.image = render
            showwarning("提示","剪裁完成！\n剪裁后的文件保存当前目录下,文件名为当前时间加cut\n注意：\n当前目录已自动切换至剪切后的文件夹，已可以直接改名")
        def zip(self):
            os.chdir(self.E_path.get())
            os.chdir(os.pardir)
            path = os.getcwd()+datename
            path = m_path.replace("\\","/")
            datename = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d")
            zipName = path + os.sep + datename + ".zip"
            f = zipfile.ZipFile( zipName, 'w', zipfile.ZIP_DEFLATED )  
            for dirpath, dirnames, filenames in os.walk( path ):  
                for filename in filenames:    
                    f.write(os.path.join(dirpath,filename))  
            f.close() 
            showwarning("提示","打包成功，打包的文件放在剪切后的文件夹内")


app =Application()
app.master.title("REname")
app.master.geometry("900x900")
app.mainloop()