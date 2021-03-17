import ast

# from utils.mongodb_model import CollectMovieCommentsDB,CollectMovieDB
# # result1 = CollectMovieCommentsDB.objects(comments_movid_id='1291546').only('comments_content', 'comments_rating').limit(1)
# result1 = CollectMovieDB.objects(movie_id='1849031').order_by("movie_id")
# print(ast.literal_eval(result1[0]['images']))
# tt = ast.literal_eval(result1[0]['images'])
# print(tt['large'])
# print(result1[0]['comments_id'])
# print(result1[0]['comments_rating'])
# .read()
# import requests
# import json
# url = 'https://book.douban.com/subject/26435510/comments/new?p=1&_=1588176677253'
# print(url)
# headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
#         'X-Requested-With': 'XMLHttpRequest',
#         'Accept': 'application/json'}
# html = requests.get(url, headers=headers, timeout=10)
# html.encoding = "utf-8"
# htmls = json.loads(html.text)
# print(htmls)

# import mongoengine
# import datetime
# mongoengine.disconnect()
# mongoengine.connect('test',host='127.0.0.1',port=27017) # 连接的数据库名称
# #mongoengine.connect('test')
# # 测试
#
# class CollectMovieDB(mongoengine.Document):
#     movie_id = mongoengine.IntField(default=0)  # 唯一标识
#     original_title = mongoengine.StringField(default='')  # 原始标题
#     title = mongoengine.StringField(default='')  # 中文标题
#     rating = mongoengine.StringField(default='')  # 评分
#     ratings_count = mongoengine.IntField(default=0)  # 评分数
#     pubdate = mongoengine.StringField(default='')  # 上映日期
#     pubdates = mongoengine.StringField(default='')  # 上映日期2
#     year = mongoengine.IntField(default=0)  # 年份
#     countries = mongoengine.StringField(default='')  # 制片国家/地区
#     mainland_pubdate = mongoengine.StringField(default='')  # 主要上映日期
#     aka = mongoengine.StringField(default='')  # 又名
#     tags = mongoengine.StringField(default='')  # 标签
#     durations = mongoengine.StringField(default='')  # 时长
#     genres = mongoengine.StringField(default='')  # 类型
#     videos = mongoengine.StringField(default='')  # 短视频
#     wish_count = mongoengine.StringField(default='')  # 想看
#     reviews_count = mongoengine.IntField(default=0)  # 短评数
#     comments_count = mongoengine.IntField(default=0)  # 评论数
#     collect_count = mongoengine.IntField(default=0)  # 收藏
#     images = mongoengine.StringField(default='')  # 封面图片
#     photos = mongoengine.StringField(default='')  # 照片
#     languages = mongoengine.StringField(default='')  # 语言
#     writers = mongoengine.StringField(default='')  # 作者
#     actor = mongoengine.StringField(default='')  # 演员
#     summary = mongoengine.StringField(default='')  # 简介
#     directors = mongoengine.StringField(default='')  # 导演
#     record_time = mongoengine.StringField(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
#
# result = CollectMovieDB.objects.filter(movie_id=10551473).first()
# if result :
#     print(result)

#         .dump_options_with_quotes()
#     )
#     return c
#
# def movies_rating_bar(id, num) -> Bar:
#     genre = movies_rating(id, num)
#     if genre == 0:
#         return 0

# def movies_rating(id,num):
#     if not num:
#         num = 500000
#     if not id:
#         return 0
#     result = CollectMovieDB.objects.aggregate([
#                                             # {"$match":{'movie_id':int(id)}},
#                                             {'$sample': {'size': int(num)}},
#                                             {"$project": {"rating": 1}},
#                                             {"$sort": {"movie_id": -1}}])
#     if not result:
#         return 0
#
# def movies_rating_pie(id,num) -> Pie:

from PIL import Image, ImageDraw, ImageFont
import codecs as cs

def genFontImage(font, char):
    size = font.size
    image = Image.new('1', (size, size))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), char, font=font, fill='#ff0000')
    return image



if __name__ == '__main__':
    size = 500
    font = ImageFont.truetype('../file/汉仪中楷简.ttf', size)
    hans = '神'

    for han in hans[:10]:
        image = genFontImage(font,han)
        image.save(str(hans.index(han))+'.png')
