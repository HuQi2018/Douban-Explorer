import ast
import re
import pandas as pd
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Pie,Bar,Line,Scatter,Grid,Bar3D,Timeline, Tab
from pyecharts.faker import Faker
from pyecharts.commons.utils import JsCode
from utils.mongodb_model import CollectMusicCommentsDB,CollectMusicReviewsDB,CollectMusicDB\
    ,CollectMusicCommentsDB,CollectMusicReviewsDB,CollectMusicDB,\
    CollectBookCommentsDB,CollectBookReviewsDB,CollectBookDB
import redis
from utils.redis_pool import POOL
import json
from random import randrange

from django.http import HttpResponse
from rest_framework.views import APIView


# Create your views here.
def response_as_json(data):
    json_str = json.dumps(data)
    response = HttpResponse(
        json_str,
        content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def json_response(data, code=200):
    data = {
        "code": code,
        "msg": "success",
        "data": data,
    }
    return response_as_json(data)


def json_error(error_string="error", code=500, **kwargs):
    data = {
        "code": code,
        "msg": error_string,
        "data": {}
    }
    data.update(kwargs)
    return response_as_json(data)


JsonResponse = json_response
JsonError = json_error

def music_rating(id,num):
    # 评分统计、评分的音乐数（rating--》average）
    if not id:
        return (0,0)
    result = CollectMusicDB.objects.aggregate([
                                            {"$match":{'music_id':int(id)}},
                                            {'$sample': {'size': int(num)}},
                                            {"$project": {"rating_star": 1}},
                                            {"$sort": {"music_id": -1}}])
    if not result:
        return (0,0)
    num = 0
    for i in result:
        genre = ast.literal_eval(i['rating_star'])
        num += 1
    return (genre,num)

def music_rating_pie(id,num) -> Pie:
    (genre,num) = music_rating(id,num)
    if genre == 0:
        return 0
    c = (
        #     Pie(init_opts=opts.InitOpts(width="", height="", bg_color=""))
        Pie()
        .add(
            series_name="音乐评分",
            data_pair=[list(z) for z in zip(["评分5", "评分4", "评分3", "评分2", "评分1"], list(map(float, genre)))],
            center=["45%", "50%"],
            radius=["40%", "55%"],
            label_opts=opts.LabelOpts(
                is_show=True,
                position="outside",
                formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}%  {per|{d}%}  ",
                background_color="#eee",
                border_color="#aaa",
                border_width=1,
                border_radius=4,
                rich={
                    "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                    "abg": {
                        "backgroundColor": "#e3e3e3",
                        "width": "100%",
                        "align": "right",
                        "height": 22,
                        "borderRadius": [4, 4, 0, 0],
                    },
                    "hr": {
                        "borderColor": "#aaa",
                        "width": "100%",
                        "borderWidth": 0.5,
                        "height": 0,
                    },
                    "b": {"fontSize": 16, "lineHeight": 33},
                    "per": {
                        "color": "#eee",
                        "backgroundColor": "#334455",
                        "padding": [2, 4],
                        "borderRadius": 2,
                    },
                },
            ),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="音乐评分分布",
                subtitle="数据量：" + str(num),
                #                                   pos_left="center",
                pos_left="38%",
                #                                   pos_top="20",
                #                                   title_textstyle_opts=opts.TextStyleOpts(color="#fff"),
            ),
            legend_opts=opts.LegendOpts(is_show=True,
                                        pos_top="20",
                                        type_="scroll",
                                        pos_left="85%",
                                        orient="vertical"
                                        ),
            toolbox_opts=opts.ToolboxOpts(is_show=True,pos_left="95%",
                                          feature={
                                              "dataZoom": {"yAxisIndex": "none"},
                                              "restore": {},
                                              "saveAsImage": {},
                                          }, ),
        )
        .set_series_opts(
            tooltip_opts=opts.TooltipOpts(
                trigger="item", formatter="{a} <br/>{b}: {c}% ({d}%)"
            ),
            #         label_opts=opts.LabelOpts(color="rgba(1, 1, 1, 0.3)"),
        )
        .dump_options_with_quotes()
    )
    return c

def music_rating_bar(id, num) -> Bar:
    (genre,num) = music_rating(id, num)
    if genre == 0:
        return 0
    c = (
        Bar()
        .add_xaxis(["评分5", "评分4", "评分3", "评分2", "评分1"])
        .add_yaxis("音乐评分占比", list(map(float, genre)),
                       )
        .set_global_opts(title_opts=opts.TitleOpts(title="音乐评分分布", subtitle="数据量：" + str(num),),
                             xaxis_opts=opts.AxisOpts(name="评分"),
                             yaxis_opts=opts.AxisOpts(name_gap=50,name_rotate=90,name_location="center",name="占比"),
                             toolbox_opts=opts.ToolboxOpts(is_show=True,
                                                           #                                         orient="vertical",
                                                           pos_left="95%",
                                                           feature={
                                                               "dataZoom": {"yAxisIndex": "none"},
                                                               "dataView": {},
                                                               "magicType": {
                                                                   "show": True,
                                                                   "title": "切换",
                                                                   "type": ['line', 'bar'],
                                                                   # 启用的动态类型，包括'line'（切换为折线图）, 'bar'（切换为柱状图）, 'stack'（切换为堆叠模式）, 'tiled'（切换为平铺模式）
                                                               },
                                                               "restore": {},
                                                               "saveAsImage": {},
                                                           },
                                                           ),
                             )
        .dump_options_with_quotes()
    )
    return c

def music_comments_rating(id,num):
    # 评论时间与评分的关系（单个喜好关系）
    if not id:
        return (0,0,0)
    result = CollectMusicCommentsDB.objects.aggregate([
                                            {"$match":{'comments_music_id':int(id)}},
                                            {'$sample': {'size': int(num)}},
                                            {"$project": {"comments_rating": 1,"comments_time": 1}},
                                            {"$sort": {"comments_time": -1}}])
    if not result:
        return (0,0,0)
    rating = list()
    times = list()
    num = 0
    # quarter = list()
    for i in result:
        rating.append(i['comments_rating'])
        times.append(i['comments_time'][:10])
        # year = i['comments_time'][0:4]
        # month = int(i['comments_time'][5:7])
        # if month >= 1 and month <= 3:
        #     quarter.append(year + '-' + '1')
        # elif month >= 4 and month <= 6:
        #     quarter.append(year + '-' + '2')
        # elif month >= 7 and month <= 9:
        #     quarter.append(year + '-' + '3')
        # elif month >= 10 and month <= 12:
        #     quarter.append(year + '-' + '4')
        num += 1
    # print(rating)
    # print(times)
    # print(quarter)
    index = np.arange(len(rating))
    data = pd.DataFrame(data={'评分': rating, '天': times}, index=index)
    data = data.groupby(by="天", as_index=False).mean()
    rt = list(map(float, np.around(data['评分'].values,2)))
    qu = data['天'].values
    return (rt,qu,num)

def music_comments_rating_line(id, num) -> Line:
    (rt,qu,num) = music_comments_rating(id, num)
    if rt == 0:
        return 0
    l1 = (
        Line()
        .add_xaxis(xaxis_data=qu)
        .add_yaxis(
            series_name="评分",
            y_axis=rt,
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                    opts.MarkPointItem(type_="min", name="最小值"),
                ]
            ),
            markline_opts=opts.MarkLineOpts(
                data=[opts.MarkLineItem(type_="average", name="平均值")]
            ),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="评论时间季度与评分的关系",subtitle="数据量：" + str(num),),
            tooltip_opts=opts.TooltipOpts(trigger="axis", is_show=True),
            axispointer_opts=opts.AxisPointerOpts(
                is_show=True, link=[{"xAxisIndex": "all"}]
            ),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
            toolbox_opts=opts.ToolboxOpts(is_show=True,
                                          #                                         orient="vertical",
                                          pos_left="95%",
                                          feature={
                                              "dataZoom": {"yAxisIndex": "none"},
                                              "dataView": {},
                                              "magicType": {
                                                  "show": True,
                                                  "title": "切换",
                                                  "type": ['line', 'bar'],
                                                  # 启用的动态类型，包括'line'（切换为折线图）, 'bar'（切换为柱状图）, 'stack'（切换为堆叠模式）, 'tiled'（切换为平铺模式）
                                              },
                                              "restore": {},
                                              "saveAsImage": {},
                                          },
                                          ),
            xaxis_opts=opts.AxisOpts(name="评论时间季度", type_="category", boundary_gap=False),
            yaxis_opts=opts.AxisOpts(name_gap=50,name_rotate=90,name_location="center",name="评分"),
        )
        .dump_options_with_quotes()
    )
    return l1


def musics_rating(id,num):
    # 评分统计、评分的音乐数（rating--》average）
    result = CollectMusicDB.objects.aggregate([
        # {"$match":{'status':{'$ne':0}}},
        {'$sample': {'size': int(num) }},
        {"$project": {"rating": 1}},
        {"$sort": {"music_id": -1}}])
    if not result:
        return (0,0,0)
    rating = dict({})
    num = 0
    for i in result:
        average = str(round(float(i['rating']), 1))
        if not average == '0.0':
            #         if float(average) < 9:#所有小于9的数据都进行区间数据合并
            ck = int(average[-1:])
            if ck in [0, 1, 2]:
                average = average[:-1] + '0'
            elif ck in [3, 4, 5, 6]:
                average = average[:-1] + '5'
            elif ck in [7, 8, 9]:
                average = average[:-1] + '0'
                average = str(float(average) + 1)
            if average not in rating:
                rating[average] = 1
            else:
                rating[average] += 1
        num += 1
    # print(rating)
    # 使用pandas排序
    rating = pd.DataFrame(data={'rating': list(rating.keys()), 'num': list(rating.values())},
                          index=np.arange(len(rating))).sort_values(by='rating')
    key = list(rating['rating'].values)
    val = list(rating['num'].values)
    return (key,val,num)

def musics_rating_pie(id,num) -> Pie:
    (key,val,num) = musics_rating(id,num)
    if key == 0:
        return 0
    # print(key)
    c = (
        Pie()
        .add(
            series_name="评分 音乐数",
            data_pair=[list(z) for z in zip([x + '分' for x in key], map(str, val))],
            center=["45%", "50%"],
            label_opts=opts.LabelOpts(
                is_show=True,
            ),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="各评分的音乐数",
                                                       pos_left="38%", subtitle="数据量：" + str(num),),
                             legend_opts=opts.LegendOpts(is_show=True,
                                                         pos_top="20",
                                                         type_="scroll",
                                                         pos_left="85%",
                                                         orient="vertical"
                                                         ),
                             toolbox_opts=opts.ToolboxOpts(is_show=True,pos_left="95%",
                                                           feature={
                                                               "dataZoom": {"yAxisIndex": "none"},
                                                               "dataView": {},
                                                               "restore": {},
                                                               "saveAsImage": {},
                                                           },
                                                           ),
                             )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}  ({d}%)"))
        .dump_options_with_quotes()
    )
    # c.render_notebook()
    # print(c)
    return c

def musics_rating_bar(id,num) -> Bar:
    (key,val,num) = musics_rating(id,num)
    if key == 0:
        return 0
    c = (
        Bar()
        .add_xaxis([x + '分' for x in key])
        .add_yaxis("音乐数", list(map(str, val)))
        .set_global_opts(title_opts=opts.TitleOpts(title="各评分的音乐数", subtitle="数据量：" + str(num),),
                             yaxis_opts=opts.AxisOpts(name_gap=50,name_rotate=90,name_location="center",name="音乐数（个）"),
                             xaxis_opts=opts.AxisOpts(name="评分"),
                             toolbox_opts=opts.ToolboxOpts(is_show=True,
                                                           #                                         orient="vertical",
                                                           pos_left="95%",
                                                           feature={
                                                               "dataZoom": {"yAxisIndex": "none"},
                                                               "dataView": {},
                                                               "magicType": {
                                                                   "show": True,
                                                                   "title": "切换",
                                                                   "type": ['line', 'bar'],
                                                                   # 启用的动态类型，包括'line'（切换为折线图）, 'bar'（切换为柱状图）, 'stack'（切换为堆叠模式）, 'tiled'（切换为平铺模式）
                                                               },
                                                               "restore": {},
                                                               "saveAsImage": {},
                                                           },
                                                           ),
                            )
        .dump_options_with_quotes()
    )
    return c


def musics_pubdate(id,num):
    # 发行时间数（取月份：pubdate/pubdates）
    result = CollectMusicDB.objects.aggregate([
                                            # {"$match":{'music_id':int(id)}},
                                            {'$sample': {'size': int(num)}},
                                            {"$project": {"pubdate": 1}},
                                            {"$sort": {"pubdate": -1}}])
    if not result:
        return (0,0,0)
    time = list()
    times = dict({})
    num = 0
    for i in result:
        try:
            pubdate = ast.literal_eval(i['pubdate'])
        except:
            continue
            pass
        if not pubdate:
            continue
        pubdate = pubdate[0]
        if len(pubdate) == 7:
            pubdate = pubdate + "-01"
        elif len(pubdate) == 4:
            pubdate = pubdate + "-01-01"
        elif len(pubdate) == 9:
            pubdate = pubdate[:-1] + "0" + pubdate[-1:]
        elif len(pubdate) == 0:
            continue
        date_all = re.findall(r"(\d{4}-\d{1,2}-\d{1,2})", pubdate)
        if not date_all:  # 去除不完整的数据
            continue
        pubdate = date_all[0]
        time.append(pubdate)
        num += 1
    time.sort()
    for i in time:
        if str(i) not in times:
            times[str(i)] = 1
        else:
            times[str(i)] += 1
    return (time,times,num)

def musics_pubdate_scatter(id, num) -> Scatter:
    (time,times,num) = musics_pubdate(id, num)
    if time == 0:
        return 0
    x_data = list(map(str, times.keys()))
    y_data = list(map(str, times.values()))

    c = (
        Scatter()  # init_opts=opts.InitOpts(width="1600px", height="1000px")
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(
            series_name="音乐数",
            y_axis=y_data,
            symbol_size=20,
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_series_opts()
        .set_global_opts(
            title_opts=opts.TitleOpts(title="音乐发行趋势", subtitle="数据量：" + str(num),),
            xaxis_opts=opts.AxisOpts(
                splitline_opts=opts.SplitLineOpts(is_show=True),
                name="音乐发行时间"
            ),
            yaxis_opts=opts.AxisOpts(
                #             type_="value",
                name="音乐数量",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
            visualmap_opts=opts.VisualMapOpts(type_="size", max_=5, min_=1),
            toolbox_opts=opts.ToolboxOpts(is_show=True,pos_left="95%",
                                          feature={
                                              "dataZoom": {"yAxisIndex": "none"},
                                              "dataView": {},
                                              "restore": {},
                                              "saveAsImage": {},
                                          },
                                          ),
        )
        .dump_options_with_quotes()
    )
    return c


def musics_year(id,num):
    #历年音乐产量、发行时间数
    result = CollectMusicDB.objects.aggregate([
                                            # {"$match":{'music_id':int(id)}},
                                            {'$sample': {'size': int(num)}},
                                            {"$project": {"pubdate": 1}},
                                            {"$sort": {"music_id": -1}}])
    if not result:
        return (0,0,0)
    year = dict({})
    num = 0
    for i in result:
        try:
            date_all = re.findall(r"(\d{4})", str(ast.literal_eval(i['pubdate'])[0]))
        except:
            continue
            pass
        if not date_all:  # 去除不完整的数据
            continue
        date_all = date_all[0]
        if str(date_all) not in year:
            year[str(date_all)] = 1
        else:
            year[str(date_all)] += 1
        num += 1
    #     countries.append(i['countries'])
    # print(year)

    year = pd.DataFrame(data={'year': list(year.keys()), 'num': list(year.values())},
                        index=np.arange(len(year))).sort_values(by='year')
    key = list(year['year'].values)
    val = list(year['num'].values)
    return (key,val,num)

def musics_year_pie(id, num) -> Pie:
    (key,val,num) = musics_year(id, num)
    if key == 0:
        return 0
    c = (
        Pie()
        .add(
            series_name="历年音乐产量",
            data_pair=[list(z) for z in zip([x + '年' for x in list(map(str, key))], list(map(str, val)))],
            center=["45%", "50%"],
            label_opts=opts.LabelOpts(
                is_show=True,
            ),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="历年音乐产量",
                                                       pos_left="38%",subtitle="数据量：" + str(num), ),
                             legend_opts=opts.LegendOpts(is_show=True,
                                                         pos_top="20",
                                                         type_="scroll",
                                                         pos_left="85%",
                                                         orient="vertical"
                                                         ),
                             toolbox_opts=opts.ToolboxOpts(is_show=True,pos_left="95%",
                                                           feature={
                                                               "dataZoom": {"yAxisIndex": "none"},
                                                               "dataView": {},
                                                               "restore": {},
                                                               "saveAsImage": {},
                                                           },
                                                           ),
                             )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}  ({d}%)"))
        .dump_options_with_quotes()
    )
    return c

def musics_year_bar(id, num) -> Bar:
    (key,val,num) = musics_year(id, num)
    if key == 0:
        return 0
    c = (
        Bar()
        .add_xaxis([x + '年' for x in key])
        .add_yaxis("音乐数", list(map(str, val)))
        .set_global_opts(title_opts=opts.TitleOpts(title="历年音乐产量", subtitle="数据量：" + str(num),),
                             yaxis_opts=opts.AxisOpts(name_gap=50,name_rotate=90,name_location="center",name="音乐数（个）"),
                             xaxis_opts=opts.AxisOpts(name="年份"),
                             toolbox_opts=opts.ToolboxOpts(is_show=True,
                                                           #                                         orient="vertical",
                                                           pos_left="95%",
                                                           feature={
                                                               "dataZoom": {"yAxisIndex": "none"},
                                                               "dataView": {},
                                                               "magicType": {
                                                                   "show": True,
                                                                   "title": "切换",
                                                                   "type": ['line', 'bar'],
                                                                   # 启用的动态类型，包括'line'（切换为折线图）, 'bar'（切换为柱状图）, 'stack'（切换为堆叠模式）, 'tiled'（切换为平铺模式）
                                                               },
                                                               "restore": {},
                                                               "saveAsImage": {},
                                                           },
                                                           ),
                             )
        .dump_options_with_quotes()
    )
    return c


def musics_genres(id,num):
    #音乐类型（genres）
    result = CollectMusicDB.objects.aggregate([
                                            # {"$match":{'music_id':int(id)}},
                                            {'$sample': {'size': int(num)}},
                                            {"$project": {"tags": 1}},
                                            {"$sort": {"music_id": -1}}])
    if not result:
        return (0,0,0)
    genres = dict({})
    num = 0
    for i in result:
        yy = ast.literal_eval(i['tags'])
        for ck in yy:
            ck = ck['name']
            if str(ck) not in genres:
                genres[str(ck)] = 1
            else:
                genres[str(ck)] += 1
        num += 1
    genres = pd.DataFrame(data={'genres': list(genres.keys()), 'num': list(genres.values())},
                          index=np.arange(len(genres))).sort_values(by='num', ascending=False)
    key = list(genres['genres'].values)[:20]
    val = list(genres['num'].values)[:20]
    return (key,val,num)

def musics_genres_pie(id, num) -> Pie:
    (key,val,num) = musics_genres(id, num)
    if key == 0:
        return 0
    c = (
        Pie()
        .add(
            series_name="不同标签的音乐数量",
            data_pair=[list(z) for z in zip(key, list(map(str, val)))],
            center=["45%", "50%"],
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="不同标签的音乐数量",
                                                       pos_left="38%", subtitle="数据量：" + str(num),),
                             legend_opts=opts.LegendOpts(is_show=True,
                                                         pos_top="20",
                                                         type_="scroll",
                                                         pos_left="85%",
                                                         orient="vertical"
                                                         ),
                             toolbox_opts=opts.ToolboxOpts(is_show=True,pos_left="95%",
                                                           feature={
                                                               "dataZoom": {"yAxisIndex": "none"},
                                                               "dataView": {},
                                                               "restore": {},
                                                               "saveAsImage": {},
                                                           },
                                                           ),
                             )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}  ({d}%)"))
        .dump_options_with_quotes()
    )
    return c

def musics_genres_bar(id, num) -> Bar:
    (key,val,num) = musics_genres(id, num)
    if key == 0:
        return 0
    c = (
        Bar()
        .add_xaxis(list(map(str, key)))
        .add_yaxis("音乐数", list(map(str, list(map(str, val)))))
        .set_global_opts(title_opts=opts.TitleOpts(title="不同标签的音乐数量", subtitle="数据量：" + str(num),),
                             yaxis_opts=opts.AxisOpts(name_gap=50,name_rotate=90,name_location="center",name="音乐数（个）"),
                             xaxis_opts=opts.AxisOpts(name="音乐类型"),
                             toolbox_opts=opts.ToolboxOpts(is_show=True,
                                                           #                                         orient="vertical",
                                                           pos_left="95%",
                                                           feature={
                                                               "dataZoom": {"yAxisIndex": "none"},
                                                               "dataView": {},
                                                               "magicType": {
                                                                   "show": True,
                                                                   "title": "切换",
                                                                   "type": ['line', 'bar'],
                                                                   # 启用的动态类型，包括'line'（切换为折线图）, 'bar'（切换为柱状图）, 'stack'（切换为堆叠模式）, 'tiled'（切换为平铺模式）
                                                               },
                                                               "restore": {},
                                                               "saveAsImage": {},
                                                           },
                                                           ),
                             )
        .dump_options_with_quotes()
    )
    return c


def musics_star_pubdate(id,num):
    #发行时间与评分的关系
    result = CollectMusicDB.objects.aggregate([
                                            # {"$match":{'music_id':int(id)}},
                                            {'$sample': {'size': int(num)}},
                                            {"$project": {"rating": 1,"pubdate": 1}},
                                            {"$sort": {"music_id": -1}}])
    if not result:
        return (0,0,0)
    rating = list()
    times = list()
    num = 0
    for i in result:
        rat = i['rating']
        if not rat:
            continue
        try:
            pubdate = ast.literal_eval(i['pubdate'])
        except:
            continue
            pass
        if not pubdate:
            continue
        pubdate = pubdate[0]
        if len(pubdate) == 7:
            pubdate = pubdate + "-01"
        elif len(pubdate) == 4:
            pubdate = pubdate + "-01-01"
        elif len(pubdate) == 9:
            pubdate = pubdate[:-1] + "0" + pubdate[-1:]
        elif len(pubdate) == 0:
            continue
        date_all = re.findall(r"(\d{4}-\d{1,2}-\d{1,2})", pubdate)
        if not date_all:  # 去除不完整的数据
            continue
        pubdate = date_all[0]
        times.append(pubdate)
        rating.append(rat)
        num+=1
    data = pd.DataFrame(data={'rating': list(rating), 'times': list(times)}, index=np.arange(len(rating))).sort_values(
        by='times')
    val = list(data['rating'].values)
    key = list(data['times'].values)
    return (key,val,num)

def musics_star_pubdate_scatter(id, num) -> Scatter:
    (key,val,num) = musics_star_pubdate(id, num)
    if key == 0:
        return 0
    x_data = list(map(str, key))
    y_data = list(map(float, val))
    c = (
        Scatter()  # init_opts=opts.InitOpts(width="1600px", height="1000px")
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
            series_name="评分",
            y_axis=y_data,
            #         symbol_size=20,
            label_opts=opts.LabelOpts(is_show=False),
        )
            .set_series_opts()
            .set_global_opts(
            title_opts=opts.TitleOpts(title="发行时间与评分的关系", subtitle="数据量：" + str(num),),
            xaxis_opts=opts.AxisOpts(
                #             type_="value",
                type_='time',
                name="发行时间",
                splitline_opts=opts.SplitLineOpts(is_show=True),
                #             max_=10,
                #             min_=min(y_data)-1

            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                name="评分",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                max_=10,
                min_=min(y_data) - 1
            ),
            tooltip_opts=opts.TooltipOpts(
                is_show=True, trigger="item", formatter="发行时间 评分 <br/>{c}分"
            ),
            visualmap_opts=opts.VisualMapOpts(
                max_=10,
                range_color=[
                    "#313695",
                    "#4575b4",
                    "#74add1",
                    "#abd9e9",
                    "#e0f3f8",
                    "#ffffbf",
                    "#fee090",
                    "#fdae61",
                    "#f46d43",
                    "#d73027",
                    "#a50026",
                ],
            ),
            toolbox_opts=opts.ToolboxOpts(is_show=True,pos_left="95%",
                                          feature={
                                              "dataZoom": {"yAxisIndex": "none"},
                                              "dataView": {},
                                              "restore": {},
                                              "saveAsImage": {},
                                          },
                                          ),
        )
        .dump_options_with_quotes()
    )
    return c


def musics_star_comments_count(id,num):
    #评论数与评分的关系（散点图，所有）
    result = CollectMusicDB.objects.aggregate([
                                            # {"$match":{'music_id':int(id)}},
                                            {'$sample': {'size': int(num)}},
                                            {"$project": {"rating": 1,"comments_count": 1,"reviews_count": 1}},
                                            {"$sort": {"music_id": -1}}])
    if not result:
        return (0,0,0,0)
    rating = list()
    counts = list()
    num = 0
    for i in result:
        rat = i['rating']
        if not rat:
            continue
        count = i['comments_count']
        counts.append(count)
        rating.append(rat)
        num += 1

    data = pd.DataFrame(data={'rating': list(rating), 'counts': list(counts)},
                        index=np.arange(len(rating))).sort_values(by='rating', ascending=True)
    key = list(data['rating'].values)
    val = list(data['counts'].values)
    maxx = max(val)
    return (key,val,maxx,num)

def musics_star_comments_count_scatter(id, num) -> Scatter:
    (key,val,maxx,num) = musics_star_comments_count(id, num)
    if key == 0:
        return 0
    x_data = list(map(float, key))
    y_data = list(map(int, val))
    c = (
        Scatter()  # init_opts=opts.InitOpts(width="1600px", height="1000px")
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
            series_name="评论数",
            y_axis=y_data,
            #         symbol_size=20,
            label_opts=opts.LabelOpts(is_show=False),
        )
            .set_series_opts()
            .set_global_opts(
            title_opts=opts.TitleOpts(title="评论数与评分的关系", subtitle="数据量：" + str(num),),
            xaxis_opts=opts.AxisOpts(
                # 坐标轴类型。可选：
                # 'value': 数值轴，适用于连续数据。
                # 'category': 类目轴，适用于离散的类目数据，为该类型时必须通过 data 设置类目数据。
                # 'time': 时间轴，适用于连续的时序数据，与数值轴相比时间轴带有时间的格式化，在刻度计算上也有所不同，
                # 例如会根据跨度的范围来决定使用月，星期，日还是小时范围的刻度。
                # 'log' 对数轴。适用于对数数据。
                type_="value",
                name="评分",
                splitline_opts=opts.SplitLineOpts(is_show=True),
                max_=10,
                min_=min(x_data) - 1

            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                name="评论数",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            #         tooltip_opts=opts.TooltipOpts(is_show=True),
            tooltip_opts=opts.TooltipOpts(
                trigger="item", formatter="评分 评论数 <br/>{c}条"
            ),
            visualmap_opts=opts.VisualMapOpts(
                #             type_="size",
                max_=int(maxx),
                #             min_=0,
                range_color=[
                    "#313695",
                    "#4575b4",
                    "#74add1",
                    "#abd9e9",
                    "#e0f3f8",
                    "#ffffbf",
                    "#fee090",
                    "#fdae61",
                    "#f46d43",
                    "#d73027",
                    "#a50026",
                ],
            ),
            toolbox_opts=opts.ToolboxOpts(is_show=True,pos_left="95%",
                                          feature={
                                              "dataZoom": {"yAxisIndex": "none"},
                                              "dataView": {},
                                              "restore": {},
                                              "saveAsImage": {},
                                          },
                                          ),
        )
        .dump_options_with_quotes()
    )
    return c

class ChartView(APIView):
    def get(self, request, *args, **kwargs):

        conn = redis.Redis(connection_pool=POOL)
        id = request.GET.get("id")
        num = request.GET.get("num")
        if not num:
            num = 5000
        typ = request.GET.get("typ")
        nochache = request.GET.get("nochache")
        redis_key = typ + '_' + id + num
        data = conn.get(redis_key)

        if not data or nochache == '1':
            if typ == 'musics_rating_pie':
                data = musics_rating_pie(id, num)
            elif typ == 'musics_rating_bar':
                data = musics_rating_bar(id, num)
            elif typ == 'music_rating_pie':
                data = music_rating_pie(id, num)
            elif typ == 'music_rating_bar':
                data = music_rating_bar(id, num)
            elif typ == 'music_comments_rating_line':
                data = music_comments_rating_line(id, num)
            elif typ == 'musics_pubdate_scatter':
                data = musics_pubdate_scatter(id, num)
            elif typ == 'musics_year_pie':
                data = musics_year_pie(id, num)
            elif typ == 'musics_year_bar':
                data = musics_year_bar(id, num)
            # elif typ == 'musics_countries_pie':
            #     data = musics_countries_pie(id, num)
            # elif typ == 'musics_countries_bar':
            #     data = musics_countries_bar(id, num)
            # elif typ == 'musics_languages_pie':
            #     data = musics_languages_pie(id, num)
            # elif typ == 'musics_languages_bar':
            #     data = musics_languages_bar(id, num)
            elif typ == 'musics_genres_pie':
                data = musics_genres_pie(id, num)
            elif typ == 'musics_genres_bar':
                data = musics_genres_bar(id, num)
            # elif typ == 'musics_star_num_bar3d':
            #     data = musics_star_num_bar3d(id, num)
            # elif typ == 'musics_star_durations_scatter':
            #     data = musics_star_durations_scatter(id, num)
            elif typ == 'musics_star_pubdate_scatter':
                data = musics_star_pubdate_scatter(id, num)
            elif typ == 'musics_star_comments_count_scatter':
                data = musics_star_comments_count_scatter(id, num)
            else:
                data = '{"msg":"参数错误，或信息不存在","code":"404"}'
            print("redis存储")
            conn.set(redis_key, data)
            conn.expire(redis_key, 60*60*24)


        if data == 0:
            data = '{"msg":"参数错误，或信息不存在","code":"404"}'
        return JsonResponse(json.loads(data))

class IndexView(APIView):
    def get(self, request, *args, **kwargs):
        return HttpResponse(content=open('./templates/charts.html').read())






