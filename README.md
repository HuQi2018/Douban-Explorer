# Douban-Explorer

## 作品简介：
  豆瓣探索者这个作品是依托豆瓣这个平台制作的一个数据分析系统。本作品使用Python的BeautifulSoup库爬取了电影、图书、音乐这三个方向的数据存入MongoDB的NoSQL数据库，使用Pyecharts库得到了诸如单部电影评分分布的一维数据图、评分与评论数关系的二维数据图甚至于多维数据图，并结合Django框架、前后端分离技术进行展示。
  本系统还有搜索功能，可以具体查询某一部电影、音乐或图书的数据分析，同时当搜索到一个数据库中不存在的数据时，后台将自动进行在线爬取存入数据库，即我们将数据搜集的过程也加入到了网站上，从而实现了数据收集、预处理、存储、处理与分析、可视化的集成系统。

## 使用说明（安装Redis、MongoDB的说明，及具体说明请移步 [安装说明书.pdf](安装说明书.pdf)）
	1.修改mongodb的连接配置：\web\web\settings.py
	2.修改redis的连接配置：\web\utils\redis_pool.py
	3.安装所需的Python库：在\web目录下执行 pip install --index https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
	4.启动Django服务：python .\manage.py runserver
	5.打开 html 文件夹（前端网页文件），点击 index.html 打开主页面


## 开源代码与组件使用情况说明：
	http://sc.chinaz.com/moban/200303241840.htm
	该作品除前端使用了上述链接的模板框架外（其余全为团队所写）。
	后端主要使用的Python库（除Python自带库外）：
	Django、pyecharts、requests、redis、mongoengine、pandas、numpy、matplotlib、beautifulsoup4、wordcloud、jieba、snownlp等。
	
	前端使用了：jquery、vue、bootstrap、echarts等。
	
	开发使用了：
	Windows下的：PyCharm、Jupyter、SVN、Robo 3T等。
	
	服务端使用：
	Linux下的：Redis、MongoDB、宝塔Linux面板、SVN Server等。
