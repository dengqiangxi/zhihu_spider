### 知乎爬虫
#### 简介
项目主要为爬取知乎用户以及知乎关注被关注的关系网，数据库使用MySQL，分为三个表，详情可见 zhihu.sql文件，分别存储用户信息，用户关注和被关注

#### 使用方式
 1. 安装MySQL 教程不在此赘述，新建数据库并将 zhihu.sql建表文件导入数据库 并在 all_secret_set.py中配置好数据库相关项
 2. 安装scrapy以及相关依赖 `pip install -r requirements.txt`
 3. 将zhihu账号cookie拷贝出来用 cookieUtils.py 分割并放入 all_secret_set.py配置项
 4. 运行main.py



