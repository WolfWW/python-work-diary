# python-work-diary
A desktop application for logging details of work.

---

请注意：

如果提示密文库和明文库都存在，请想清楚连接哪个

---

**工作记录小软件，功能如下（截止2018-05-26）：**
1. 本地数据库实现添加记录、查询记录、修改近两日记录、清空某个分类记录、重置数据库等功能；
2. 添加记录时有工作、学习、生活等预设分类
3. 可通过日期、分类、关键字等精确查询和模糊查询
4. 运行日志功能，记录正常日志和错误日志
5. 查询记录的结果可导出为excel
6. 数据库加密。使用AES-256对库加密，基于口令生成密钥
7. 删除单条记录
8. 可以增加分类，或修改分类名称


### 软件截图

![mark](https://wolfww.oss-cn-hongkong.aliyuncs.com/workdiary%E6%A0%B7%E5%9B%BE.PNG)


### 需求

 日期选择：TtkCalendar
 
 导出excel：xlwt
 
 UI：tkinter
 
 数据库逻辑：sqlite3
 
 数据库加密：pyaes

**第三方库说明：**

1. 日期选择插件来源：https://github.com/moshekaplan/tkinter_components
2. 加密库：https://github.com/ricmoo/pyaes
3. excel处理：https://github.com/python-excel/xlwt
4. 第三方库安装：`pip install -r requirements.txt`
 
### 使用方法

1. 有Python3环境
 - 安装第三方库
 - 直接运行diaryUI.py即可
2. 无Python3环境
 - 安装第三方库
 - 使用pyinstaller将代码打包，打包方法可参考[我的打包记录](http://blog.csdn.net/elang6962/article/details/69259026)
 
### 使用Tips

 - 初次使用请点击【初始化数据库】
 - 将鼠标放在滚动条上，滚轮用起来会很爽
 - 默认重要性'否'，点【全部清空】会清除掉，虽然此时看起来是两个都选上了
 - 想修改近两日的记录，可以点击【近两日记录】
 - 想搜什么，哪怕只能想起一个字，也能【查询记录】
 - 导出的excel在代码文件夹里，文件名是当前时间；想立即打开点'是'即可
 - 加密后明文库暂时会移动到D盘，妥善保管，万一出错还能救救
 - 设置为不加密后又变卦了？把`check.pass`删除试试

 
### 下一步

 - 增加待办事项
 - 修改口令以及口令合法性检测
 - 按年查询记录

 
### 版权说明

代码使用MPL2.0许可证

说明：非商用请随意折腾，商用时本部分代码必须开源