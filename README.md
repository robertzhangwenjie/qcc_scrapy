# 企查查爬虫工具
## 只需要给定企业名称和企查查的账号，就可以自动爬取企业相关信息

## 基本使用
1. 安装依赖
    ```pip install -r requirements.txt```
2. 存放拥有企业信息的excel放到jobbole/qcc/excel目录下
3. 修改配置文件jobbole/settings.py中的QCC_ACCOUNTS信息，可以添加多个账号
4. 修改配置文件中的数据库信息
5. 在指定数据库中执行jobbole/sql/qcc_*.sql    
4. 启动程序开始爬虫,执行命令行或者在idea中运行main程序
    ```scrapy crawler qcc```
   
