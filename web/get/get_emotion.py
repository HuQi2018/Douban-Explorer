from snownlp import SnowNLP
from django.http import HttpResponse
from django.template import loader
from pyecharts import options as opts
from pyecharts.charts import Pie
from utils.mongodb_model import CollectMovieDB,CollectMovieCommentsDB,CollectMovieReviewsDB,\
    CollectMusicDB,CollectMusicCommentsDB,CollectMusicReviewsDB\
    ,CollectBookDB,CollectBookCommentsDB,CollectBookReviewsDB
import redis
from utils.redis_pool import POOL
from rest_framework.views import APIView
import json
from collection import get_music,get_movie,get_book
import ast

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

def StartoSentiment(star):
    score = int(star)
    if score >= 3:
        return 1
    # elif score < 3:
    #     return -1
    else:
        return 0

def get_collection(typ,id,n):
    if typ == 'movie':
        # result = CollectMovieDB.objects.aggregate([
        #     {"$match": {'movie_id': int(id)}},
        #     {'$sample': {'size': 1}},
        #     {"$project": {"title": 1}},
        #     {"$sort": {"movie_id": -1}}])
        # result1 = CollectMovieCommentsDB.objects.aggregate([
        #     {"$match": {'comments_movid_id': int(id)}},
        #     # {'$sample': {'size': int(n)}},
        #     {"$project": {"comments_content": 1, "comments_rating": 1}},
        #     {"$sort": {"comments_movid_id": -1}}])
        # result2 = CollectMovieReviewsDB.objects.aggregate([
        #     {"$match": {'reviews_movid_id': int(id)}},
        #     {'$sample': {'size': int(n)}},
        #     {"$project": {"reviews_content": 1, "reviews_rating": 1}},
        #     {"$sort": {"reviews_movid_id": -1}}])
        result = CollectMovieDB.objects(movie_id=id).order_by("movie_id").only('title').limit(1)
        result1 = CollectMovieCommentsDB.objects(comments_movid_id=id).order_by("comments_movid_id").only('comments_content', 'comments_rating')
        result2 = CollectMovieReviewsDB.objects(reviews_movid_id=id).order_by("reviews_movid_id").only('reviews_content', 'reviews_rating').limit(int(n))

    elif typ == 'music':
        # result = CollectMusicDB.objects.aggregate([
        #     {"$match": {'music_id': int(id)}},
        #     {'$sample': {'size': 1}},
        #     {"$project": {"title": 1}},
        #     {"$sort": {"music_id": -1}}])
        # result1 = CollectMusicCommentsDB.objects.aggregate([
        #     {"$match": {'comments_music_id': int(id)}},
        #     # {'$sample': {'size': int(n)}},
        #     {"$project": {"comments_content": 1, "comments_rating": 1}},
        #     {"$sort": {"comments_music_id": -1}}])
        # result2 = CollectMusicReviewsDB.objects.aggregate([
        #     {"$match": {'reviews_music_id': int(id)}},
        #     {'$sample': {'size': int(n)}},
        #     {"$project": {"reviews_content": 1, "reviews_rating": 1}},
        #     {"$sort": {"reviews_music_id": -1}}])
        result = CollectMusicDB.objects(music_id=id).order_by("music_id").only('title').limit(1)
        result1 = CollectMusicCommentsDB.objects(comments_music_id=id).order_by("comments_music_id").only('comments_content', 'comments_rating')
        result2 = CollectMusicReviewsDB.objects(reviews_music_id=id).order_by("reviews_music_id").only('reviews_content', 'reviews_rating').limit(int(n))
    elif typ == 'book':
        # result = CollectBookDB.objects.aggregate([
        #     {"$match": {'book_id': int(id)}},
        #     {'$sample': {'size': 1}},
        #     {"$project": {"title": 1}},
        #     {"$sort": {"book_id": -1}}])
        # result1 = CollectBookCommentsDB.objects.aggregate([
        #     {"$match": {'comments_book_id': int(id)}},
        #     # {'$sample': {'size': int(n)}},
        #     {"$project": {"comments_content": 1, "comments_rating": 1}},
        #     {"$sort": {"comments_book_id": -1}}])
        # result2 = CollectBookReviewsDB.objects.aggregate([
        #     {"$match": {'reviews_book_id': int(id)}},
        #     {'$sample': {'size': int(n)}},
        #     {"$project": {"reviews_content": 1, "reviews_rating": 1}},
        #     {"$sort": {"reviews_book_id": -1}}])
        result = CollectBookDB.objects(book_id=id).order_by("book_id").only('title').limit(1)
        result1 = CollectBookCommentsDB.objects(comments_book_id=id).order_by("comments_music_id").only('comments_content', 'comments_rating')
        result2 = CollectBookReviewsDB.objects(reviews_book_id=id).order_by("reviews_music_id").only('reviews_content', 'reviews_rating').limit(int(n))
    else:
        return (0,0,0)
    if not result1:
        if typ == 'movie':
            data = get_movie.get_movie(id)
        elif typ == 'music':
            data = get_music.get_music(id)
        elif typ == 'book':
            data = get_book.get_book(id)
        else:
            return (0,0,0)
        if ast.literal_eval(data)['status'] == 0:
            return (0,0,0)
        else:
            (result, result1, result2) = get_collection(typ, id, n)
    return (result,result1,result2)

def img(id, typ,n):
    # print(type)
    # 保存评论文件
    if not n:
        n=1

    (result,result1,result2) = get_collection(typ, id, n)
    # print(result,result1,result2)
    if not result:
        return 0
    reviews = []
    sentiment = []
    for txt in result1:
        sentiment.append(StartoSentiment(txt['comments_rating']))
        reviews.append(txt['comments_content'])
    for txt in result2:
        sentiment.append(StartoSentiment(txt['reviews_rating']))
        reviews.append(txt['reviews_content'])
    for i in result:
        title = i['title']
        break
    # (reviews, sentiment) = CollectReivew(id, 10, typ)
    numOfRevs = len(list(sentiment))
    if (numOfRevs == 0):
        return 0

    positive = 0.0
    negative = 0.0
    accuracy = 0.0
    # 利用snownlp逐条分析每个评论的情感
    for i in range(numOfRevs):
        if len(reviews[i])==0:
            continue
        sent = SnowNLP(reviews[i])
        predict = sent.sentiments
        if predict >= 0.5:
            positive += 1
            if sentiment[i] == 1:
                accuracy += 1
        else:
            negative += 1
            if sentiment[i] == 0:
                accuracy += 1

    # 绘制饼状图
    # 定义饼状图的标签
    labels = ['积极评论', '消极评论']
    # 每个标签占的百分比
    # ratio = ["%.2f%%" % ((positive / numOfRevs) * 100), "%.2f%%" % ((negative / numOfRevs) * 100)]
    ratio = [positive, negative]
    accur = str("%.2f%%" % ((accuracy / numOfRevs) * 100))
    # ratio = ["%.2f" % ((positive / numOfRevs) * 100), "%.2f" % ((negative / numOfRevs) * 100)]
    # print(ratio)
    # print([positive, negative])
    # print('情感预测精度为: ' + str("%.2f%%" % ((accuracy/numOfRevs) * 100)))
    # pie = Pie(title, "情感分析图    情感预测精度为: " + str("%.2f%%" % ((accuracy/numOfRevs) * 100)), title_pos='center', width=550)
    # pie.add("评论情感", labels, ratio, is_legend_show=True, is_label_show=True, legend_pos='left')
    # return pie
    return get_emotion_pie(labels,ratio,accur,title)

def get_emotion_pie(labels,ratio,accur,title) -> Pie:
    title = str(title)+"——评论情感"
    c = (
        Pie(init_opts=opts.InitOpts(width="550px"))
        .add(
            series_name="评论情感",
            data_pair=[list(z) for z in zip([x + '分' for x in labels], map(str, ratio))],
            #         center=["35%", "50%"],
            label_opts=opts.LabelOpts(
                is_show=True,
            ),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title=title,
                                                       pos_left="center",
                                                       subtitle="情感分析图    情感预测精度为: " + accur),
                             legend_opts=opts.LegendOpts(is_show=True,
                                                         pos_top="20",
                                                         type_="scroll",
                                                         pos_left="70%",
                                                         orient="vertical"
                                                         ),
                             toolbox_opts=opts.ToolboxOpts(is_show=True,
                                                           pos_left="90%",
                                                           feature={
                                                               "dataZoom": {"yAxisIndex": "none"},
                                                               "dataView": {},
                                                               "restore": {},
                                                               "saveAsImage": {},
                                                           },
                                                           orient="vertical"
                                                           ),
                             )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}  ({d}%)"))
        .dump_options_with_quotes()
    )
    return c

class ChartView(APIView):
    def get(self, request, *args, **kwargs):
        id = request.GET.get("id") if request.GET.get("id") else ''
        typ = request.GET.get("type") if request.GET.get("type") else ''
        n = request.GET.get("n") if request.GET.get("n") else ''
        nochache = request.GET.get("nochache")

        conn = redis.Redis(connection_pool=POOL)
        redis_key = 'emotion' + typ + '_' + id + n
        data = conn.get(redis_key)
        if not data or nochache == '1':
            if id and typ in ['movie', 'book', 'music']:
                data = img(id, typ, n)
                print("redis存储")
                conn.set(redis_key, data)
                conn.expire(redis_key, 60 * 60 * 24)
            else:
                data = "{'msg':'参数错误，或信息不存在','code':404}"

        if data == 0:
            return JsonResponse("{'data':'参数错误，或信息不存在','code':404}")
        return JsonResponse(json.loads(data))

