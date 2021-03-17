"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf.urls import url, include
from try_try import redis
from get import wordcloud, get_emotion, search2, search1, search3, count
from collection import get_music,get_movie,get_book,get

urlpatterns = [
    # path(r'admin/', admin.site.urls),             # 默认django管理
    # path(r'set_redis/', redis.index),             # redis设置测试set
    # path(r'get_redis/', redis.order),             # redis设置测试get
    path(r'count/', count.main),                      # 获取数据库内各个集合的数量
    path(r'get/', get.main),                      # 采集数据合集，需给定id、type
    path(r'get_music/', get_music.main),          # 采集音乐数据，需给定id
    path(r'get_movie/', get_movie.main),          # 采集电影数据，需给定id
    path(r'get_book/', get_book.main),            # 采集书籍数据，需给定id
    path(r'wordcloud/', wordcloud.get_wordcloud), # 图片词云，需给定id、type
    # path(r'topic/', topic.main),                  # 话题词云，需给定id、type，非必需n为review个数，默认1个
    path(r'searchAll/', search1.get_search),      # 显示所有的搜索信息，需给定q，非必需cat、start
    path(r'searchPoint/', search2.get_search),    # 显示最多20条信息，即一次爬取，需给定q，非必需cat、start
    path(r'searchId/', search3.get_search),       # 获取作品信息，即详情页，需给定id、type
    path(r'get_emotion/', get_emotion.ChartView.as_view()),     # 情感分析图id、type，非必需n为review个数，默认1个

    url(r'charts/', include('charts.urls')),
    # path(r'try/', tt.index, name='index'),  # 情感分析图id、type，非必需n为review个数，默认1个
]

handler404 = "competition.views.page_not_found"
handler500 = "competition.views.page_error"