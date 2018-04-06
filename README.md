# python-work-diary
A desktop application for logging details of work.

---

**数据库文件在0.4.2中移到了代码文件夹中，已有的数据库手动移动后再使用**

---

工作记录小软件，功能如下（截止2018-04-06）：
1. 本地数据库实现添加记录、查询记录、修改近两日记录、清空某个分类记录、重置数据库等功能；
2. 添加记录时有工作、学习、生活等预设分类
3. 可通过日期、分类、关键字等精确查询和模糊查询
4. 添加日志功能，记录正常日志和错误日志
5. 查询记录的结果可导出为excel

说明：日期选择插件来源：https://github.com/moshekaplan/tkinter_components


### 软件截图

![mark](http://omvy9d3lc.bkt.clouddn.com/blog/180326/b82h50iJmf.png?imageslim)

![mark](http://omvy9d3lc.bkt.clouddn.com/blog/180326/4DhhmfBAjJ.png?imageslim)


### 需求

 日期选择：TtkCalendar，链接在上面
 导出excel：xlwt
 UI：tkinter
 数据库逻辑：sqlite3

### 使用Tips

 - 初次使用请点击【初始化数据库】
 - 将鼠标放在滚动条上，滚轮用起来会很爽
 - 默认重要性'否'，点【全部清空】会清除掉
 - 想修改近两日的记录，可以点击【近两日记录】
 - 想搜什么，哪怕只能想起一个字，也能【查询记录】
 - 导出的excel在代码文件夹里，文件名是当前时间；想立即打开点'是'即可

 
### 下一步

 - 界面美化
 - 增加待办事项
 - 增加保密措施

 
### 版权说明

代码使用MIT许可证