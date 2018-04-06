# windows10/python3.5
#-*- coding:utf-8 -*-

from xlwt import *
import datetime

class ToExcel(Workbook):
    def __init__(self,results,sheetname):
        super().__init__()
        self.results = results
        self.sheetname = sheetname
        self.write_to_wkbook()
        self.save_to_file()
        
        
    def write_to_wkbook(self):
        '''
        写工作表
        results中的id不写，因此column从1开始
        '''
        sheet = self.add_sheet(self.sheetname)
        
        for row in range(len(self.results)):
            for column in range(1,len(self.results[row])):
                sheet.write(row,column-1,self.results[row][column])
        
        
    def save_to_file(self):
        '''
        保存在当前路径下
        空格替换成下划线，是因为用os.system()打开excel时路径不能有空格
        '''
        self.filename = str(datetime.datetime.now())[:19].replace(':','：') + '.' + 'xls'
        self.filename = self.filename.replace(' ','_')
        self.filepath = './%s' % self.filename
        self.save(self.filepath)
        
if __name__ == "__main__":
    results = 'TEST'
    ToExcel(results)
