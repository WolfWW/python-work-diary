# windows10/python3.5
#-*- coding:utf-8 -*-

'''
工作记录小软件的数据库部分
目前实现：
①新增记录②修改记录③查询记录④数据库初始化
TODO：增加计划任务模块
'''


import time
import sqlite3

def mylogging():
    pass

class Record(object):
    def __init__(self,database):
        '''实例初始化，创建实例时需要传入此函数中的参数'''
        self.database = database
        self.con = sqlite3.connect(self.database)
        self.cur = self.con.cursor()
        
    
    def new_record(self,category,date,content,signif,detail):
        '''新增记录'''
        if category == '工作':
            self.cur.execute("insert into work values (NULL,?,?,?,?,?)",(category,date,content,signif,detail))
        elif category == '生活':
            self.cur.execute("insert into life values (NULL,?,?,?,?,?)",(category,date,content,signif,detail))
        elif category == '学习':
            self.cur.execute("insert into learn values (NULL,?,?,?,?,?)",(category,date,content,signif,detail))
        self.con.commit()
        

    def query_record(self,category,date,content,signif,detail):
        '''查询记录'''
        if category == '工作':
            results = self.cur.execute("select * from work where date like ? and content like ? and issignificant like ? and detail like ?",(date,content,signif,detail)).fetchall()
        elif category == '生活':
            results = self.cur.execute("select * from life where date like ? and content like ? and issignificant like ? and detail like ?",(date,content,signif,detail)).fetchall()
        elif category == '学习':
            results = self.cur.execute("select * from learn where date like ? and content like ? and issignificant like ? and detail like ?",(date,content,signif,detail)).fetchall()

        return results        

        
    def query_detail(self,category,query_id):
        '''查询详情'''
        if category == '工作':
            results = self.cur.execute("select * from work where id=?",(query_id,)).fetchall()
        elif category == '生活':
            results = self.cur.execute("select * from life where id=?",(query_id,)).fetchall()
        elif category == '学习':
            results = self.cur.execute("select * from learn where id=?",(query_id,)).fetchall()
        return results
        
        
    def modify_record(self,id,old_category,new_category,date,content,signif,detail,modify_category):
        '''修改记录'''
        if modify_category == 1:
            self.del_record(id,old_category)
            self.new_record(new_category,date,content,signif,detail)
        else:
            if old_category == '工作':
                self.cur.execute("update work set date=?,content=?,issignificant=?,detail=? where id=?",(date,content,signif,detail,id))
            elif old_category == '生活':
                self.cur.execute("update life set date=?,content=?,issignificant=?,detail=? where id=?",(date,content,signif,detail,id))
            elif old_category == '学习':
                self.cur.execute("update learn set date=?,content=?,issignificant=?,detail=? where id=?",(date,content,signif,detail,id))
        self.con.commit()
        
        
    def del_record(self,id,category):
        '''删除记录'''
        if category == '工作':
            self.cur.execute("delete from work where id=?",(id,))
        elif category == '生活':
            self.cur.execute("delete from life where id=?",(id,))
        elif category == '学习':
            self.cur.execute("delete from learn where id=?",(id,))

    
    def clear_table(self,table):
        '''清空数据表'''
        if table == '工作':
            self.cur.execute('delete from work')
        elif table == '生活':
            self.cur.execute('delete from life')
        elif table == '学习':
            self.cur.execute('delete from learn')
        self.con.commit()
            
            
    def init_sql(self):
        '''重建数据库'''
        self.cur.execute("create table work(id integer primary key autoincrement, category char(10), date char(19), content char(100), issignificant char(10), detail char(1000))")
        self.cur.execute("create table life(id integer primary key autoincrement, category char(10), date char(19), content char(100), issignificant char(10), detail char(1000))")
        self.cur.execute("create table learn(id integer primary key autoincrement, category char(10), date char(19), content char(100), issignificant char(10), detail char(1000))")


    def disconnect(self):
        '''关闭连接'''
        self.cur.close()
        self.con.close()
    
    

def test_new():
    '''测试新增记录'''
    database = 'd:/workdiary.db'
    while True:
        user_choice = input("1为添加记录，2为待办事项，3为工作检索：")
        if user_choice == '1':
        
            category = input("选择分类（工作,生活 or 学习）:") 
            date = time.strftime("%Y-%m-%d",time.localtime())
            content = input("记录主题：")
            signif = input("是否重要（0为不重要，1为重要）:")
            detail = input("输入详细内容：")
            record = Record(database)
            record.new_record(category,date,content,signif,detail)
            break
        elif user_choice == '2':
            pass
        elif user_choice == '3':
            pass
        else:
            print("请输入正确选择！")
            continue

    
if __name__ == '__main__':
    test_new()