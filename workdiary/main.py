# windows10/python3.5
#-*- coding:utf-8 -*-

"""
工作记录小软件的数据库部分
目前实现：
①新增记录②修改记录③查询记录④数据库初始化
TODO：增加计划任务模块
"""


import time
import sqlite3

# 表名称，它就是个表名，没事不要瞎改
TABLE_NAME = "diary"

def mylogging():
    pass
'''
def scrub(table_name):
    """
    处理输入字符串，主要用于自定义表名部分
    from https://stackoverflow.com/questions/3247183/variable-table-name-in-sqlite
    """
    return ''.join( chr for chr in table_name if chr.isalnum() )
'''
class Record(object):
    def __init__(self,database):
        """实例初始化，创建实例时需要传入此函数中的参数"""
        self.database = database
        self.con = sqlite3.connect(self.database)
        self.cur = self.con.cursor()


    '''
    def new_table(self,table_name):
        """以自定义表名新建表"""
        table_name = scrub(table_name)
        self.cur.execute("create table %s(id integer primary key autoincrement, category char(10), date char(19), content char(100), issignificant char(10), detail char(1000))" % table_name)

    def modify_tablename(self,new_name):
        """修改表名"""
        new_name = scrub(new_name)
        self.cur.execute("alter table TABLE_NAME rename to %s" % new_name)
    '''



    def new_record(self,category,date,content,signif,detail):
        """
        新增记录
        为什么值的第一个位置是NULL？忘记了
        """
        self.cur.execute("insert into TABLE_NAME values (NULL,?,?,?,?,?)",(category,date,content,signif,detail))
        self.con.commit()
        

    def query_record(self,category,date,content,signif,detail):
        """查询记录"""
        results = self.cur.execute("select * from TABLE_NAME where category like ? and date like ? and content like ? and issignificant like ? and detail like ?",(category,date,content,signif,detail)).fetchall()
        return results

    '''没用到，目前是查询结果的results直接包括详情，以后查询结果多了应该要改，到时会用到
    def query_detail(self,query_id):
        """查询详情"""
        results = self.cur.execute("select * from TABLE_NAME where id=?",(query_id,)).fetchall()
        return results

    '''
        
    def modify_record(self,id,category,date,content,signif,detail):
        """修改记录"""
        self.cur.execute("update TABLE_NAME set category=?,date=?,content=?,issignificant=?,detail=? where id=?",(category,date,content,signif,detail,id))
        self.con.commit()
        
        
    def del_record(self,id):
        """删除记录"""
        self.cur.execute("delete from TABLE_NAME where id=?",(id,))

    '''待修改
    def clear_table(self,category):
        """清空某个分类"""
        self.cur.execute('delete from TABLE_NAME')
        self.con.commit()

    '''

    def init_sql(self):
        """重建数据库"""
        self.cur.execute("create table TABLE_NAME(id integer primary key autoincrement, category char(10), date char(19), content char(100), issignificant char(10), detail char(1000))")


    def disconnect(self):
        """关闭连接"""
        self.cur.close()
        self.con.close()



def test_new():
   """测试新增记录"""
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
   print(scrub('); drop tables --'))