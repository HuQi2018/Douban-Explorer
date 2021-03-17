
from wordcloud import WordCloud
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
# from scipy.misc import imread
from imageio import imread
import jieba
import json
from utils.mongodb_model import CollectMovieDB,CollectMovieCommentsDB,CollectMovieReviewsDB,\
    CollectMusicDB,CollectMusicCommentsDB,CollectMusicReviewsDB\
    ,CollectBookDB,CollectBookCommentsDB,CollectBookReviewsDB
from io import BytesIO
import base64
from django.shortcuts import HttpResponse
# import pygame
import random
import redis
from utils.redis_pool import POOL
from collection import get_music,get_movie,get_book
import ast
from PIL import Image, ImageDraw, ImageFont


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


# def get_word(txt):
    # pygame.init()
    # tt = int(hex(ord(txt)))
    # word = chr(ord(txt))
    # font = pygame.font.Font("file/汉仪中楷简.ttf", 650)
    # rtext = font.render(word, True, (0, 0, 0), (255, 255, 255))
    # pygame.image.save(rtext, "file/chinese/"+ word + ".png")

def get_word(char):
    size = ImageFont.truetype('file/simkai.ttf', 500).size
    image = Image.new('1', (size, size))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), char, font=ImageFont.truetype('file/simkai.ttf', size), fill='#ff0000')
    image.save("file/chinese/"+ str(char) + ".png")
    # return image

def get_collection(typ,id):
    if typ == 'movie':
        title = CollectMovieDB.objects.filter(movie_id=id)
        result1 = CollectMovieCommentsDB.objects(comments_movid_id=id).order_by("comments_movid_id").only(
            'comments_content')
        result2 = CollectMovieReviewsDB.objects(reviews_movid_id=id).order_by("reviews_movid_id").only(
            'reviews_content')
    elif typ == 'music':
        title = CollectMusicDB.objects.filter(music_id=id)
        result1 = CollectMusicCommentsDB.objects(comments_music_id=id).order_by("comments_music_id").only(
            'comments_content')
        result2 = CollectMusicReviewsDB.objects(reviews_music_id=id).order_by("reviews_music_id").only(
            'reviews_content')
    elif typ == 'book':
        title = CollectBookDB.objects.filter(book_id=id)
        result1 = CollectBookCommentsDB.objects(comments_book_id=id).order_by("comments_book_id").only(
            'comments_content')
        result2 = CollectBookReviewsDB.objects(reviews_book_id=id).order_by("reviews_book_id").only(
            'reviews_content')
    else:
        return (0,0,0)
    j = 0
    for i in result1:
        j = 1
    if j == 0:
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
            (result, result1, result2) = get_collection(typ, id)
    return (title, result1, result2)

def get_wordcloud(request):
    id = request.GET.get("id")
    typ = request.GET.get("type")
    nochache = request.GET.get("nochache")

    conn = redis.Redis(connection_pool=POOL)
    redis_key = 'wordcloud' + typ + '_' + id
    data = conn.get(redis_key)
    if not data or nochache == '1':

        (title, result1, result2) = get_collection(typ, id)
        if title == 0:
            return HttpResponse("该评论不存在，或参数有误！")

        reviews = []
        for txt in result1:
            reviews.append(txt['comments_content'])
        for txt in result2:
            reviews.append(txt['reviews_content'])

        if not title:
            return HttpResponse("该评论不存在，或参数有误！")
        for i in title:
            title = str(i['title'])
            break
        # 结巴分词
        wordlist = jieba.cut(str(reviews), cut_all=True)
        wl = " ".join(wordlist)
        # print(wl)#输出分词之后的txt
        word = title[random.randint(0, (len(title) - 1))]
        get_word(word)
        # print(wl)
        # 设置词云
        wc = WordCloud(background_color="white",  # 设置背景颜色
                       mask=imread('file/chinese/' + word + '.png'),  # 设置背景图片
                       max_words=300,  # 设置最大显示的字数
                       font_path="file/simkai.ttf",  # 设置为楷体 常规
                       # stopwords = sw,
                       # 设置中文字体，使得词云可以显示（词云默认字体是“DroidSansMono.ttf字体库”，不支持中文）
                       max_font_size=40,  # 设置字体最大值
                       # min_font_size=20,  # 设置字体最大值
                       random_state=30,  # 设置有多少种随机生成状态，即有多少种配色方案
                       )
        myword = wc.generate(wl)  # 生成词云

        # 展示词云图
        plt.imshow(myword)
        plt.axis("off")
        # plt.show()
        # 转成图片的步骤
        sio = BytesIO()
        plt.savefig(sio, format='png')
        data = base64.encodebytes(sio.getvalue()).decode()
        plt.close()

        print("redis存储")
        conn.set(redis_key, data)
        conn.expire(redis_key, 60 * 60 * 24)
    else:
        data = str(data).replace('\\n', '')[2:][:-1]
    # print(data)
    return JsonResponse(data)
    # return HttpResponse('<img src="data:image/png;base64,' + data + '" style="height: 450px;width: 450px;border: 2px solid;object-fit: cover;">')
