# windows10/python3.5
#-*- coding:utf-8 -*-

'''
工作记录小软件UI，距离起初吹下的牛B还有很长一段距离
计划功能如下（TODO）：
1.记录时有多种预设分类，并可自定义分类，如工作、学习、娱乐等
2.本地数据库记录，可通过日期、分类、关键字查询
3.可导出为excel
4.待办事项，默认为全部列出，可设提醒时间
5.默认记录时间为当前时间，可手动填入
6.录入时可选择是否标记为重要工作
7.软件运行日志记录
8.可以进行用户设置，包括开机自启、字体等

TODO：
1.修改记录后查询记录弹窗实时更新

日期选择插件来源：https://github.com/moshekaplan/tkinter_components
'''


import os                                   # for delete db file
import datetime
import hashlib
from tkinter import *
from tkinter import ttk

# 日期选择
from TtkCalendar import ttkcalendar
from TtkCalendar import tkSimpleDialog
from TtkCalendar import CalendarDialog

import main


class DiaryRoot(Tk):
    def __init__(self):
        super().__init__()
        self.title('Python Workdiary')
        self.database = 'd:/workdiary.db'
        self.record = main.Record(self.database)
        self.detail = ''                         # 详细内容
        self.init_frame()
        self.clear_frame()
        self.new_frame()
        
        
    def init_frame(self):
        # 初始化选择
        init_frame = Frame(self)
        init_frame.grid(row=0,column=0,columnspan=2)

        # 分类选择
        Label(init_frame,text='分类').grid(row=0,column=0,padx=5,pady=5)
        self.category = StringVar()
        ttk.Combobox(init_frame,textvariable=self.category,values=['工作','生活','学习'],width=4,state='readonly').grid(row=1,column=0,padx=5,pady=5)

        # 日期录入
        Label(init_frame,text='日期（当天添加记录可不选）').grid(row=0,column=1,padx=5,pady=5,columnspan=2)  
        self.date = StringVar()
        #self.date.set()
        Label(init_frame, textvariable=self.date,width=11,bd=3,relief=SUNKEN).grid(row=1,column=1)
        Button(init_frame, text="点击选择日期", command=self.getdate).grid(row=1,column=2)

        # 重要性选择
        Label(init_frame,text='是否重要').grid(row=0,column=3,padx=5,pady=5,columnspan=2)
        self.signif = StringVar()
        self.signif.set('否')
        Radiobutton(init_frame,text="是",variable=self.signif,value="是").grid(row=1,column=3,padx=5,pady=5)
        Radiobutton(init_frame,text="否",variable=self.signif,value="否").grid(row=1,column=4,padx=5,pady=5)

        # 记录主题录入
        Label(init_frame,text="录入主题").grid(row=0,column=5)
        self.content = StringVar()
        Entry(init_frame,textvariable=self.content,width=30,bd=3).grid(row=1,column=5,rowspan=2)

        # 录入详细内容
        Button(init_frame,text='详细内容',command=self.input_detail,height=2,width=6,wraplength=30).grid(row=1,rowspan=2,column=6)

        # 保存记录
        Button(init_frame,text='添加记录',wraplength=2,command=self.save_record,width=3).grid(row=0,column=7,padx=6,pady=5,rowspan=2)

        # 查询记录
        Button(init_frame,text='查询记录',wraplength=2,command=self.query_record,width=3).grid(row=0,column=8,padx=5,pady=5,rowspan=2)

        # 清空内容按钮
        Button(init_frame,text='全部清空',wraplength=2,command=self.clear_all,width=3).grid(row=0,column=9,padx=5,pady=5,rowspan=2)

    
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
    
    
    def save_record(self):
        '''保存记录'''
        category,date,content,issignif,detail = self.get_data()
        
        if date == '':
            date = str(self.get_localtime())[:10]
            
        self.record.new_record(category,date,content,issignif,detail)
        
        
    def query_record(self):
        '''查询记录'''
        category,date,content,issignif,detail = self.get_data()
        
        date = '%' + date + '%'
        content = '%' + content + '%'
        issignif = '%' + issignif + '%'
        detail = '%' + detail + '%'

        results_temp = self.record.query_record(category,date,content,issignif,detail)
        self.results = [('ID','分类','日期','内容','是否重要','点击查看详情'),]
        for result in results_temp:
            self.results.append(result)
            
        frame_text = '查询记录'
        
        query_window = QueryRoot(self.results,frame_text,state=DISABLED)
                    
                    
    def clear_all(self):
        '''清空软件各输入框所有内容'''
        self.category.set('')
        self.date.set('')
        self.signif.set('')
        self.content.set('')
        self.detail = ''       
        
        
    def clear_frame(self):
        # 初始化区框架
        clear_frame = LabelFrame(self,text='下列操作将清空表或数据库，谨慎操作')
        clear_frame.grid(row=1,column=0)

        # 清空表数据按钮
        self.clr_table = StringVar()
        ttk.Combobox(clear_frame,textvariable=self.clr_table,values=['工作','生活','学习'],width=4,state='readonly').grid(row=0,column=0,padx=5,pady=5)

        Button(clear_frame,text='清空所选表',command=lambda:self.clear_table(self.clr_table.get())).grid(row=0,column=1,padx=5,pady=5)

        # 初始化数据库按钮
        Button(clear_frame,text='初始化数据库',command=self.init_sql).grid(row=0,column=2,padx=5,pady=5)
        
        # 退出按钮
        Button(clear_frame,text='退出程序',command=self.quit).grid(row=0,column=3,padx=5,pady=5)

        
    def clear_table(self,table):
        '''清空所选表'''
        self.record.clear_table(table)
        
        
    def init_sql(self):
        '''重建并初始化数据库'''
        self.record.disconnect()
        os.unlink(self.database)
        self.record = main.Record(self.database)
        self.record.init_sql()

        
    def quit(self):
        '''关闭程序'''
        self.destroy()
        
        
    def new_frame(self):
        new_frame = Frame(self)
        new_frame.grid(row=1,column=1)
    
        # 显示近两日记录按钮
        Button(new_frame,text='显示近两日记录',command=self.show_new_records,width=30).grid(padx=5,pady=5)

        
    def get_localtime(self):
        '''获得当地时间'''
        return datetime.datetime.now()
        
        
    def get_lastday(self):
        '''计算今日和昨日日期并返回列表'''
        localtime = self.get_localtime()
        lastday = localtime - datetime.timedelta(days=1)
        date_list = []
        today = str(localtime)[:10]
        yesterday = str(lastday)[:10]
        date_list.append(today)
        date_list.append(yesterday)
        return date_list
        
    def show_new_records(self):
        '''显示最近两天所有的记录'''
        date_list = self.get_lastday()
        category_list = ["工作","生活","学习"]
        content = '%%'
        issignif = '%%'
        detail = '%%'
        
        results = [('ID','分类','日期','内容','是否重要','点击查看详情'),]
        for category in category_list:
            for date in date_list:
                results_temp = self.record.query_record(category,date,content,issignif,detail)
                for result in results_temp:
                    results.append(result)
                    
        frame_text = '近两日记录'
        query_window = QueryRoot(results,frame_text)
      


class DetailRoot(Toplevel):
    def __init__(self,detail,state=NORMAL):
        super().__init__()
        self.detail = detail        # 把主窗口的detail赋值给此页面
        self.title('详细内容')
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
        
        
        
class QueryRoot(Toplevel):
    def __init__(self,results,frame_text,state=NORMAL):
        super().__init__()
        self.title(frame_text)
        self.results = results
        self.state = state
        self.query_record()

        
    def query_record(self):
        '''查询记录'''
        
        width_list = [0,10,10,30,10]
        bar = Scrollbar(self,takefocus=False)
        bar.pack(side=RIGHT,fill=Y)
        # bg选白烟色，最接近默认组件的颜色
        self.text = Text(self,bg='WhiteSmoke',height=12,width=85,yscrollcommand=bar.set)
        self.text.pack(side=RIGHT,fill=X)
        bar['command'] = self.text.yview
        
        for i in range(len(self.results)):
            for j in range(1,len(self.results[i])-1):
                entry = StringVar()
                entry.set(self.results[i][j])
                label = Label(self.text, textvariable=entry,width=width_list[j],bd=3,relief=SUNKEN,justify=CENTER)
                self.text.window_create(INSERT,window=label)
            if i == 0:
                self.text.insert(END,'\n')
            else:
                show_detail = Button(self.text,text='查看详情')
                show_detail.bind("<ButtonRelease-1>",self.get_detail)
                self.text.window_create(INSERT,window=show_detail)
                modify_button = Button(self.text,text='修改记录',state=self.state)
                self.text.window_create(INSERT,window=modify_button)
                if self.state == NORMAL:
                    modify_button.bind('<ButtonRelease-1>',self.modify_record)
        self.text['state'] = DISABLED                

    
    def get_detail(self,event):
        '''建立一个已排版的detail'''
        row = int(self.text.index(event.widget)[0]) - 1
        
        self.detail = '分类：' + self.results[row][1] + \
                        '\n日期：'+self.results[row][2] + \
                        '\n重要否：'+self.results[row][4] + \
                        '\n主题：'+self.results[row][3] + \
                        '\n详情：\n'+self.results[row][5]
        detail_root = DetailRoot(self.detail,state=DISABLED)


    def modify_record(self,event):
        row = int(self.text.index(event.widget)[0]) - 1
        modify_root = ModifyRoot(self.results[row])
        

class ModifyRoot(Toplevel):
    '''
    考虑修改分类的清空
    '''
    def __init__(self,results):
        super().__init__()
        self.title('修改记录页')
        self.database = 'd:/workdiary.db'
        self.record = main.Record(self.database)
        self.results = results
        self.detail = results[5]
        self.id = int(results[0])
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
        category,date,content,issignif,detail = self.get_data()
        modify_category = 0
        if category != self.results[1]:
            modify_category = 1
        
        self.record.modify_record(self.id,category,date,content,issignif,detail,modify_category)
        self.quit()

        
    def quit(self):
        self.destroy()


if __name__ == '__main__':
    APP = DiaryRoot()
    APP.mainloop()

