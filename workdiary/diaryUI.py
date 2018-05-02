# windows10/python3.5
#-*- coding:utf-8 -*-

'''
工作记录小软件UI，距离起初吹下的牛B还有很长一段距离
计划功能如下（TODO）：
1.[x]记录时有多种预设分类，并可自定义分类，如工作、学习、娱乐等
2.本地数据库记录，可通过日期、分类、关键字查询
3.可导出为excel
4.[x]待办事项，默认为全部列出，可设提醒时间
5.默认记录时间为当前时间，可手动填入
6.录入时可选择是否标记为重要工作
7.软件运行日志记录
8.[x]可以进行用户设置，包括开机自启、字体等

目前功能请参考README
'''

'''
日期选择插件来源：https://github.com/moshekaplan/tkinter_components
'''


import os                                   # for delete db file & open excel
import datetime
import hashlib
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import logging
import logging.handlers

# 日期选择
from TtkCalendar import ttkcalendar
from TtkCalendar import tkSimpleDialog
from TtkCalendar import CalendarDialog

import main                                 # datebase logic
import export                               # for export to excel
import myaes                                # for encrypt & decrypt dbfile


LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
ERROR_FORMAT = "%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
INFO_FILE = "./info.log"
ERROR_FILE = "./error.log"
INFO_LEVEL = logging.DEBUG
ERROR_LEVEL = logging.ERROR 

logger = logging.getLogger(__name__)
logger.setLevel(INFO_LEVEL)

info_handler = logging.handlers.TimedRotatingFileHandler(INFO_FILE,when='D',interval=3,backupCount=3)
info_formatter = logging.Formatter(fmt=LOG_FORMAT,datefmt=DATE_FORMAT)
info_handler.setFormatter(info_formatter)

error_handler = logging.FileHandler(ERROR_FILE)
error_formatter = logging.Formatter(fmt=ERROR_FORMAT,datefmt=DATE_FORMAT)
error_handler.setFormatter(error_formatter)
error_handler.setLevel(ERROR_LEVEL)

logger.addHandler(info_handler)
logger.addHandler(error_handler)

def log_info(msg):
    logger.info(msg)

def log_error(msg):
    logger.error(msg,stack_info=True,exc_info=True)



class DiaryRoot(Tk):
    def __init__(self):
        super().__init__()
        self.passwd_file = './check.pass'
        self.plain_DB = './workdiary.db'
        self.encrypted_DB = './diary.enc'
        self.temp_plain = './plain.temp'                    # 明文的hash||明文
        self.user_chose_enc = 1                             # 用户对加密的选择，1表示要加密，0表示不加密
        self.check_enc_state()

    
    def check_enc_state(self):
        '''
        检查是否已设置口令
        直接搜索有没有口令文件存在就好了
        '''
        if os.path.exists(self.passwd_file):
            '''查看是0还是hash'''
            if open(self.passwd_file,'r').read() == '0':
                self.user_chose_enc = 0
                self.root_window()
                log_info('没有设置过加密，直接打开明文库')
            else:
                self.input_passwd()
        else:
            '''进入设置口令流程'''
            self.set_passwd()

            
    def input_passwd(self):
        '''
        数据库已加密，进入输入口令流程
        '''
        self.crypto_DB('input')
            
            
    def set_passwd(self):
        '''
        数据库未加密，进入设置口令流程
        '''
        if messagebox.askyesno('ASK','是否设置口令？'):
            try:
                self.crypto_DB('set')
                log_info('选择加密，成功设置口令')
            except Exception:
                log_error('选择加密，设置口令出错')
        else:
            self.user_chose_enc = 0
            with open(self.passwd_file,'w') as f:
                f.write('0')
                f.close()
            self.root_window()
            log_info('选择不加密，打开程序')


    def crypto_DB(self,operation):
        '''
        打开口令窗口
        '''
        crypto_window = CryptoRoot()
        if operation == 'input':
            crypto_window.input_passwd()
        elif operation == 'set':
            crypto_window.set_passwd()
        self.wait_window(crypto_window)
        self.password = crypto_window.password
        if crypto_window.check_password == 1:
            self.root_window()
        else:
            self.destroy()

        
    def root_window(self):
        '''
        这里才是真正的init
        '''
        self.title('Python Workdiary')
        self.protocol("WM_DELETE_WINDOW",self.quit)   # 如果在函数后面加上()，就会在初始化时直接执行
        
        self.record = main.Record(self.plain_DB)
        self.detail = ''                              # 详细内容
        self.resizable(False,True)
        
        self.left_frame = Frame(self,width=30)
        self.left_frame.pack(side=LEFT,fill=Y)
        
        self.right_frame = Frame(self)
        self.right_frame.pack(side=LEFT,fill=Y)
        
        self.init_frame()
        self.new_frame()
        self.clear_frame()
        self.author_frame()
        
        # 以下设置窗口最小也要保持原始尺寸
        self.update()
        init_height = self.winfo_reqheight()
        self.minsize(0,init_height)

        
    def init_frame(self):
        '''
        内容区
        '''
        init_frame = LabelFrame(self.left_frame,text='内容区')
        init_frame.pack()

        # 分类选择
        Label(init_frame,text='分类',relief=RIDGE,width=8).grid(row=0,column=0,padx=5,pady=5)
        self.category = StringVar()
        ttk.Combobox(init_frame,textvariable=self.category,values=['工作','生活','学习'],width=4,state='readonly').grid(row=0,column=1,padx=5,pady=5,sticky=W+E)

        # 日期录入
        Label(init_frame,text='日期',relief=RIDGE,width=8).grid(row=1,column=0,padx=5,pady=5)  
        self.date = StringVar()
        self.date.set('不选默认当天')
        Label(init_frame, textvariable=self.date,width=11,bd=3,relief=SUNKEN,foreground='GRAY').grid(row=1,column=1)
        Button(init_frame, text="选择日期", command=self.getdate).grid(row=1,column=2)

        # 重要性选择
        Label(init_frame,text='是否重要',relief=RIDGE,width=8).grid(row=2,column=0,padx=5,pady=5)
        self.signif = StringVar()
        Radiobutton(init_frame,text="是",variable=self.signif,value='是').grid(row=2,column=1,padx=5,pady=5)
        Radiobutton(init_frame,text="否",variable=self.signif,value='否').grid(row=2,column=2,padx=5,pady=5)

        # 记录主题录入
        Label(init_frame,text="录入主题",relief=RIDGE,width=8).grid(row=3,column=0)
        #self.content = StringVar()
        self.content = Text(init_frame,width=20,bd=3,height=2)
        self.content.grid(row=3,column=1,columnspan=2)

        # 录入详细内容
        Button(init_frame,text='点击录入详细内容',command=self.input_detail,width=20).grid(row=4,columnspan=2,column=1,pady=5)
        
        
    def new_frame(self):
        '''
        功能区
        '''
        new_frame = LabelFrame(self.left_frame,text='功能区')
        new_frame.pack()

        # 保存记录
        Button(new_frame,text='添加记录',command=self.save_record,width=13).grid(row=0,column=0,padx=5,pady=5)
        # 清空内容按钮
        Button(new_frame,text='清空内容区',command=self.clear_all,width=13).grid(row=0,column=1,padx=5,pady=5)
        # 显示近两日记录按钮
        Button(new_frame,text='近两日记录',command=self.show_new_records,width=13).grid(row=1,column=0,padx=5,pady=5)
        # 查询记录
        Button(new_frame,text='查询记录',command=self.query_record,width=13).grid(row=1,column=1,padx=5,pady=5)
        
    
    def getdate(self):
        '''
        获取在组件中选择的日期
        如果不选择日期就关闭，会出现AttributeError，所以捕获了
        '''
        cd = CalendarDialog.CalendarDialog(self)
        result = cd.result
        try:
            self.date.set(result.strftime("%Y-%m-%d"))
        except:
            result = ''
    
    
    def input_detail(self):
        '''
        获取弹窗中的详情内容
        '''
        detail_window = DetailRoot(self.detail)
        self.wait_window(detail_window)
        self.detail = detail_window.detail
    
    
    def get_data(self):
        '''
        获取用户输入数据
        '''
        category = self.category.get()
        date = self.date.get()
        if date == '不选默认当天':
            date = ''
        content = self.content.get(1.0,END)[:-1]
        signif = self.signif.get()
        detail = self.detail
        return category,date,content,signif,detail
    
    
    def save_record(self):
        '''
        保存记录
        '''
        try:
            category,date,content,issignif,detail = self.get_data()
            
            if date == '':
                date = str(self.get_localtime())[:10]
            
            self.record.new_record(category,date,content,issignif,detail)
            log_info("成功在【%s】添加一条记录，主题'%s'\n" % (category,content))
        except Exception:
            log_error("【添加记录】过程出现错误：\n\
                分类：%s\n\
                日期：%s\n\
                主题：%s\n\
                重要否：%s\n\
                详情：%s\n" % \
                (category,date,content,issignif,detail))
            messagebox.showerror("ERROR","发生错误")
        
        
    def query_record(self):
        '''查询记录'''
        try:
            category,date,content,issignif,detail = self.get_data()
            
            date = '%' + date + '%'
            content = '%' + content + '%'
            issignif = '%' + issignif + '%'
            detail = '%' + detail + '%'
            date_list = [date,]

            if category == '':
                category_list = ['工作','生活','学习']
            else:
                category_list = [category,]
             
            frame_text = '查询记录'

            self.query_results(frame_text,category_list,date_list,content,issignif,detail,state=DISABLED)
            log_info("【执行查询】记录命令：\n\
                分类：%s\n\
                日期：%s\n\
                主题：%s\n\
                重要否：%s\n\
                详情：%s\n" % \
                (category_list,date_list,content,issignif,detail))
        except Exception:
            log_error("【查询记录】过程出现错误！")
            messagebox.showerror("ERROR","发生错误")
                    
                    
    def clear_all(self):
        '''
        清空软件各输入框所有内容
        '''
        try:
            self.category.set('')
            self.date.set('不选默认当天')
            self.signif.set('')
            self.content.delete(1.0,END)
            self.detail = ''       
        except Exception:
            log_error("【清空内容区】出现错误！")
            messagebox.showerror("ERROR","发生错误")
        
        
    def get_localtime(self):
        '''
        获得当地时间
        '''
        return datetime.datetime.now()
        
        
    def get_lastday(self):
        '''
        计算今日和昨日日期并返回列表
        '''
        localtime = self.get_localtime()
        lastday = localtime - datetime.timedelta(days=1)
        date_list = []
        today = str(localtime)[:10]
        yesterday = str(lastday)[:10]
        date_list.append(today)
        date_list.append(yesterday)
        return date_list
        
    def show_new_records(self):
        '''
        显示最近两天所有的记录
        '''
        try:
            date_list = self.get_lastday()
            category_list = ["工作","生活","学习"]
            content = '%%'
            issignif = '%%'
            detail = '%%'
            frame_text = '近两日记录'

            self.query_results(frame_text,category_list,date_list,content,issignif,detail)
            log_info("执行【查询近两日】命令！")
        except Exception:
            log_error("【查询近两日】出错！")
            messagebox.showerror("ERROR","发生错误")
        
        
    def clear_frame(self):
        '''
        初始化区
        '''
        # 初始化区框架
        clear_frame = LabelFrame(self.left_frame,text='初始化区，谨慎操作')
        clear_frame.pack()

        # 清空表数据按钮
        self.clr_table = StringVar()
        ttk.Combobox(clear_frame,textvariable=self.clr_table,values=['工作','生活','学习'],width=8,state='readonly').grid(row=0,column=1,padx=5,pady=5,sticky=W)

        Button(clear_frame,text='清空所选表',command=lambda:self.clear_table(self.clr_table.get()),width=13).grid(row=0,column=0,padx=5,pady=5)

        # 初始化数据库按钮
        Button(clear_frame,text='初始化数据库',command=self.init_sql,width=13).grid(row=1,column=0,padx=5,pady=5)
        
        # 退出按钮
        Button(clear_frame,text='退出程序',command=self.quit,width=13).grid(row=1,column=1,padx=5,pady=5)

        
    def clear_table(self,table):
        '''
        清空所选表
        '''
        if table == "":
            messagebox.showwarning("WARNING","请选择要清空的表")
        else:
            if messagebox.askokcancel("清空表","确定要清空%s表吗？"%table):
                try:
                    self.record.clear_table(table)
                    log_info("【清空-%s】表！" % table)
                except Exception:
                    log_error("【清空-%s】出现错误！" % table)
                    messagebox.showerror("ERROR","发生错误")
        
        
    def init_sql(self):
        '''
        重建并初始化数据库
        '''
        if messagebox.askokcancel("初始化","初始化会删除所有记录!\n确定要初始化数据库吗？"):
            try:
                self.record.disconnect()
                os.unlink(self.plain_DB)
                self.record = main.Record(self.plain_DB)
                self.record.init_sql()
                log_info("执行【数据库初始化】命令！")
            except Exception:
                log_error("【初始化错误】")
                messagebox.showerror("ERROR","发生错误")

        
    def quit(self):
        '''
        关闭程序
        '''
        if self.user_chose_enc == 0:
            self.destroy()
        else:
            self.encrypt_DB()
            self.destroy()
        
        
    def encrypt_DB(self):
        '''
        加密明文库
        新的密文库会直接覆盖原来的
        删除明文库
        最后关闭程序窗口
        '''
        self.record.disconnect()

        try:
            plain_data = open(self.plain_DB,'rb').read()                                        # 这里只能rb读
            whole_data = hashlib.sha256(plain_data).hexdigest().encode('utf-8') + plain_data    # 明文全用bytes
            with open(self.temp_plain,'wb') as f:
                f.write(whole_data)
                f.close()
            myaes.aesMode(self.temp_plain,self.encrypted_DB,'加密',self.password)
            temp_plain_path = os.path.abspath(self.temp_plain)
            cmd_command = 'move /Y ./workdiary.db d:/'
            os.system(cmd_command)
            cmd_command = 'del %s' % temp_plain_path
            os.system(cmd_command)
            log_info("【程序关闭】正常，数据库已加密")
        except Exception:
            log_error("【加密数据库】发生错误！")
            messagebox.showerror("ERROR","加密数据库发生错误")
        
        
    def query_results(self,frame_text,category_list,date_list,content,issignif,detail,state=NORMAL):
        '''
        执行查询记录的方法
        '''
        results = [('ID','分类','日期','内容','是否重要','详情'),]
        for category in category_list:
            for date in date_list:
                results_temp = self.record.query_record(category,date,content,issignif,detail)
                for result in results_temp:
                    results.append(result)
                    
        self.result_frame(results,frame_text,modify_button_state=state)
        
        
    def result_frame(self,results,frame_text,modify_button_state):
        '''
        查询结果显示区域
        '''
        result_frame = LabelFrame(self.right_frame,text=frame_text)
        result_frame.grid(row=0,column=0,sticky=N+S)
        self.right_frame.rowconfigure(0,weight=1)
        self.right_frame.columnconfigure(0,weight=1)
        
        self.results = results
        width_list = [0,11,13,44,11]
        bar = Scrollbar(result_frame,takefocus=False)
        bar.pack(side=RIGHT,fill=Y)
        # bg选白烟色，最接近默认组件的颜色
        # width别问我101怎么来的
        self.text = Text(result_frame,bg='WhiteSmoke',width=101,yscrollcommand=bar.set)
        self.text.pack(side=RIGHT,fill=BOTH)
        bar['command'] = self.text.yview
        
        for i in range(len(self.results)):
            for j in range(1,len(self.results[i])-1):
                entry = StringVar()
                entry.set(self.results[i][j])
                label = Label(self.text, textvariable=entry,width=width_list[j],bd=3,relief=SUNKEN,justify=CENTER)
                self.text.window_create(INSERT,window=label)
            if i == 0:
                export_button = Button(self.text,text='导出excel',width=15)
                export_button.bind("<ButtonRelease-1>",self.export_to_excel)
                self.text.window_create(INSERT,window=export_button)
            else:
                show_detail = Button(self.text,text='查看详情')
                show_detail.bind("<ButtonRelease-1>",self.get_detail)
                self.text.window_create(INSERT,window=show_detail)
                modify_button = Button(self.text,text='修改记录',state=modify_button_state)
                self.text.window_create(INSERT,window=modify_button)
                if modify_button_state == NORMAL:
                    modify_button.bind('<ButtonRelease-1>',self.modify_record)
            self.text.insert(END,'\n')                                      # 这一行不能删！否则无法获得显示详情时的row
        self.text['state'] = DISABLED                

    
    def get_detail(self,event):
        '''
        建立一个已排版的detail
        '''
        row = int(self.text.index(event.widget)[0]) - 1
        
        self.detail = '分类：' + self.results[row][1] + \
                        '\n日期：'+self.results[row][2] + \
                        '\n重要否：'+self.results[row][4] + \
                        '\n主题：'+self.results[row][3] + \
                        '\n详情：\n'+self.results[row][5]
        detail_root = DetailRoot(self.detail,state=DISABLED)


    def modify_record(self,event):
        '''
        在新弹窗中修改记录
        '''
        row = int(self.text.index(event.widget)[0]) - 1
        modify_root = ModifyRoot(self.results[row])
        self.wait_window(modify_root)
        if modify_root.modified == 1:
            self.show_new_records()
            
            
    def export_to_excel(self):
        '''
        导出excel到当前文件夹
        '''
        try:
            excel = export.ToExcel(self.results,self.export_title)
            log_info('导出excel。\n导出内容为：%s\n文件路径：%s\n' % (self.export_title,excel.filepath))
            if messagebox.askyesno("导出成功","文件名如下：\n%s\n是否打开?" % excel.filename):
                filepath = os.path.abspath(excel.filepath)
                os.system(filepath)
        except Exception:
            log_error('【导出excel】出现错误')
            messagebox.showerror("ERROR","导出过程发生错误")
    
    
    def author_frame(self):
        '''
        联系我区域
        '''
        author_frame = Frame(self.left_frame)
        author_frame.pack(expand=True,fill=BOTH)
        Label(author_frame,text='联系我：45908757').pack(fill=BOTH)
      


class DetailRoot(Toplevel):
    '''
    详情窗口
    '''
    def __init__(self,detail,state=NORMAL):
        super().__init__()
        self.detail = detail        # 把主窗口的detail赋值给此页面
        self.title('详细内容')
        self.resizable(False,False)
        self.state = state
        self.input_detail()

        
    def input_detail(self):
        '''输入详细内容'''
        detailbar = Scrollbar(self,takefocus=False)
        detailbar.grid(row=0,column=1,sticky=N+S)
        self.text = Text(self,height=10,width=80,yscrollcommand=detailbar.set,relief=SUNKEN,wrap=WORD)
        self.text.grid(row=0,column=0)
        self.text.insert(END,self.detail)
        self.text['state'] = self.state
        detailbar['command'] = self.text.yview
        Button(self,text="确定",width=8,command=self.get_detail).grid(row=1,columnspan=2,padx=10,pady=5,sticky=E+W)
        Button(self,text="清空",width=8,state=self.state,command=self.clear_detail).grid(row=2,columnspan=2,padx=10,pady=5,sticky=E+W)


    def get_detail(self):
        '''
        将text中的内容赋值给detail，然后销毁窗口
        -1的作用是去掉最后的换行符
        '''
        self.detail = self.text.get(1.0,END)[:-1]
        self.destroy()

            
    def clear_detail(self):
        '''
        若detail直接赋值给text.delete，detail会是None
        选择：删除text后，赋值空字符串给detail
        '''
        self.text.delete(1.0,END)
        self.detail = ''
        
        
        
class ModifyRoot(Toplevel):
    '''
    考虑修改分类的清空
    '''
    def __init__(self,results):
        super().__init__()
        self.title('修改记录页')
        self.resizable(False,False)
        self.database = './workdiary.db'
        self.record = main.Record(self.database)
        self.results = results
        self.detail = results[5]
        self.modified = 0
        self.frame()

        
    def frame(self):
        init_frame = Frame(self)
        init_frame.grid(row=0,column=0)

        # 分类选择
        self.category = StringVar()
        self.category.set(self.results[1])
        ttk.Combobox(init_frame,textvariable=self.category,values=['工作','生活','学习'],width=4,state='readonly').grid(row=0,column=0,padx=5,pady=5)

        # 日期录入  
        self.date = StringVar()
        self.date.set(self.results[2])
        Label(init_frame, textvariable=self.date,width=11,bd=3,relief=SUNKEN).grid(row=0,column=1)
        Button(init_frame, text="点击选择日期", command=self.getdate).grid(row=0,column=2)

        # 重要性选择
        self.signif = StringVar()
        self.signif.set(self.results[4])
        Radiobutton(init_frame,text="重要",variable=self.signif,value="是").grid(row=0,column=3,padx=5,pady=5)
        Radiobutton(init_frame,text="不重要",variable=self.signif,value="否").grid(row=0,column=4,padx=5,pady=5)

        # 记录主题录入
        self.content = StringVar()
        self.content.set(self.results[3])
        Entry(init_frame,textvariable=self.content,width=30,bd=3).grid(row=0,column=5)

        # 详细内容
        Button(init_frame,text='详细内容',command=self.input_detail,height=2,width=6,wraplength=30).grid(row=0,rowspan=2,column=6)
        
        # 保存和退出按钮的frame
        ok_frame = Frame(self)
        ok_frame.grid(row=1,column=0)
        
        # 保存修改后的记录
        Button(ok_frame,text='确定修改',command=self.modify_record,width=20).grid(row=0,column=0,padx=10)
        
        # 退出修改弹窗
        Button(ok_frame,text='取消',command=self.quit,width=20).grid(row=0,column=1,padx=10)


    def getdate(self):
        '''选取日期'''
        cd = CalendarDialog.CalendarDialog(self)
        result = cd.result
        try:
            self.date.set(result.strftime("%Y-%m-%d"))
        except:
            result = ''


    def input_detail(self):
        '''获取弹窗中的详情内容'''
        detail_window = DetailRoot(self.detail)
        self.wait_window(detail_window)
        self.detail = detail_window.detail
        

    def get_data(self):
        '''获取用户输入数据'''
        category = self.category.get()
        date = self.date.get()
        content = self.content.get()
        signif = self.signif.get()
        detail = self.detail
        return category,date,content,signif,detail
    
    
    def modify_record(self):
        '''保存记录'''
        try:
            category,date,content,issignif,detail = self.get_data()
            modify_category = 0
            old_category = self.results[1]
            new_category = category
            if old_category != new_category:
                modify_category = 1

            self.record.modify_record(self.results[0],old_category,new_category,date,content,issignif,detail,modify_category)
            log_info("【修改记录】成功！\n\
            原纪录：%s\n\
            新记录：%s" % \
            (self.results[1:-1],(new_category,date,content,issignif)))
        except Exception:
            log_error("【修改记录】出现错误！")
            messagebox.showerror("ERROR","发生错误")
        self.modified = 1
        self.quit()

        
    def quit(self):
        self.destroy()
        
        
        
class CryptoRoot(Toplevel):
    '''
    加密窗口
    程序运行时出现的第一个窗口
    '''
    def __init__(self):
        super().__init__()
        self.title('口令页')
        self.resizable(False,False)
        self.attributes('-topmost',True)                      # 本窗口置于主窗口之上
        # pass文件的路径获取
        # 用python IDLE打开肯定正常
        # notepad++需要在'运行'命令中进入当前文件目录，否则获取的是编辑器的路径
        self.passfilename = './check.pass'
        self.passwd_file = os.path.abspath('.') + self.passfilename[1:]
        self.plain_DB = './workdiary.db'
        self.encrypted_DB = './diary.enc'
        self.temp_plain = './plain.temp'
        self.user_password = ''                               # 用户输入的口令，会经过处理成为密钥
        self.password = ''                                    # 最终密钥，调用myaes时参数key都是它
        self.check_password = 0                               # 口令输入正确或设置口令后置1，否则为0，程序关闭
        
            
    def input_passwd(self):
        '''输入口令的frame，用于解密'''
        Label(self,text='输入口令',width=12).grid(row=0,column=0,padx=5,pady=5)
        self.pass1 = StringVar()
        Entry(self,textvariable=self.pass1,width=15,show='*').grid(row=0,column=1,padx=5,pady=5)
        
        Button(self,text="确定",width=10,command=self.check_passwd).grid(row=1,columnspan=2,padx=10,pady=5,sticky=E+W)
        Button(self,text="取消",width=10,command=self.destroy).grid(row=2,columnspan=2,padx=10,pady=5,sticky=E+W)

        
    def set_passwd(self):
        '''
        设置口令
        口令的hash值会保存到一个文本中
        以后输入口令会和这个hash比较，不同就不会进入下一步
        '''
        Label(self,text='输入口令',width=12).grid(row=0,column=0,padx=5,pady=5)
        self.pass2 = StringVar()
        Entry(self,textvariable=self.pass2,width=15,show='*').grid(row=0,column=1,padx=5,pady=5)
        
        Label(self,text='再次输入口令',width=12).grid(row=1,column=0,padx=5,pady=5)
        self.pass3 = StringVar()
        Entry(self,textvariable=self.pass3,width=15,show='*').grid(row=1,column=1,padx=5,pady=5)
        
        Button(self,text="确定",width=10,command=self.gene_pass_file).grid(row=2,columnspan=2,padx=10,pady=5,sticky=E+W)
        Button(self,text="取消",width=10,command=self.destroy).grid(row=3,columnspan=2,padx=10,pady=5,sticky=E+W)
        
        
    def check_passwd(self):
        '''
        检查口令是否正确
        计算输入口令的hash，和口令文件中保存的hash比较
        '''
        final_password = hashlib.sha256(self.pass1.get().encode('utf-8')).hexdigest()[:32]
        user_hash = hashlib.sha256(final_password.encode('utf-8')).hexdigest()
        saved_hash = open(self.passwd_file,'r').read()
        if user_hash == saved_hash:
            self.check_password = 1
            self.password = final_password
            self.check_dbfile()
            self.destroy()
        else:
            messagebox.showwarning('WARNING','口令错误，请重新输入')
            log_error("【口令错误】错误口令：%s" % self.pass1.get())
            self.pass1.set('')
        
        
    def check_dbfile(self):
        '''
        判断当前文件夹中密文库和明文库的存在
        密文有明文无，正常解密连接
        密文无明文无，提示后关闭
        密文有明文有，用户选择
        密文无明文有，用户选择连明文或关闭
        '''
        if os.path.exists(self.encrypted_DB) and not os.path.exists(self.plain_DB):
            try:
                self.decryption()
                log_info("【数据库解密成功】")
            except Exception:
                log_error("【数据库解密】发生错误！")
        elif not os.path.exists(self.encrypted_DB) and not os.path.exists(self.plain_DB):
            messagebox.showerror("ERROR",'数据库不存在，请检查后重启程序')
            self.destroy()
        elif os.path.exists(self.encrypted_DB) and os.path.exists(self.plain_DB):
            if messagebox.askyesno('INFO','密文库和明文库都存在，请仔细检查\n\
                            "是"连接明文库，关闭程序时会覆盖现有密文库\n\
                            "否"解密密文库，会立刻覆盖现有明文库'):
                log_info("两种库都有，用户选择连接明文库")
                return
            else:
                log_info("两种库都有，用户选择连接密文库")
                try:
                    self.decryption()
                    log_info("【数据库解密成功】")
                except Exception:
                    log_error("两种库都有，用户选择连接密文库；解密中出现错误")
                    messagebox.showerror("ERROR","发生错误")
        else:
            if messagebox.askokcancel("Warn",'当前文件夹不存在密文库\n"确定"将连接明文库'):
                return
            else:
                self.destroy()
                
                
    def decryption(self):
        '''
        解密数据库
        '''
        myaes.aesMode(self.encrypted_DB,self.temp_plain,'解密',self.password)
        data = open(self.temp_plain,'rb').read()
        if hashlib.sha256(data[64:]).hexdigest() != data[:64].decode('utf-8'):
            messagebox.showwarning("WARNING",'注意！检测到密文可能被修改')
            log_error('【完整性检测】发现密文可能被修改')
        with open(self.plain_DB,'wb') as f:
            f.write(data[64:])
            f.close()
        cmd_command = 'del %s' % os.path.abspath(self.temp_plain)
        os.system(cmd_command)
        #enc_db_path = os.path.abspath(self.encrypted_DB)
        #cmd_command = 'del %s' % enc_db_path               # 删除密文库
        #os.system(cmd_command)
        # 上面的代码开启后，程序连接明文库期间，当前文件夹中没有密文库
        
        
    def gene_pass_file(self):
        '''
        设置口令后生成口令文件
        先检查两次口令是否相同且不是空的
        然后计算hash值写到文件里
        '''
        try:
            if self.verify_passwd():
                self.check_password = 1
                file = open(self.passfilename,'wb')
                self.password = hashlib.sha256(self.user_password.encode('utf-8')).hexdigest()[:32]
                hash = hashlib.sha256(self.password.encode('utf-8')).hexdigest()
                file.write(hash.encode('utf-8'))
                file.close()
                log_info("【生成口令文件】成功！")
                self.destroy()
        except Exception:
            log_error("【生成口令文件】出现错误！")
            messagebox.showerror("ERROR","生成口令文件时发生错误")
            
            
    def verify_passwd(self):
        '''
        设置口令时的验证
        '''
        if self.pass2.get().strip() != '':
            if self.pass2.get() == self.pass3.get():
                self.user_password = self.pass2.get()
                return 1
            else:
                messagebox.showinfo('INFO','两次口令输入不一致')
                self.pass2.set('')
                self.pass3.set('')
        else:
            messagebox.showwarning('WARNING','无效的口令')
            self.pass2.set('')
            self.pass3.set('')
            
            

if __name__ == '__main__':
    APP = DiaryRoot()
    APP.mainloop()

