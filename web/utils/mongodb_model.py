import mongoengine
import datetime

# 测试
class CollectReivewDB(mongoengine.Document):
    num = mongoengine.IntField(default=0)
    type = mongoengine.StringField(default='movie')
    comment = mongoengine.StringField(default='')
    star = mongoengine.StringField(default='')
    record_time = mongoengine.StringField(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# 正式
class CollectMovieCommentsDB(mongoengine.Document):
    comments_id = mongoengine.IntField(default=0)
    comments_movid_id = mongoengine.IntField(default=0)
    comments_rating = mongoengine.IntField(default=0)
    comments_useful_count = mongoengine.IntField(default=0)
    comments_content = mongoengine.StringField(default='')
    comments_author_uid = mongoengine.StringField(default='')
    comments_author_id = mongoengine.IntField(default=0)
    comments_author_name = mongoengine.StringField(default='')
    comments_time = mongoengine.StringField(default='')
    record_time = mongoengine.StringField(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


class CollectMovieReviewsDB(mongoengine.Document):
    reviews_id = mongoengine.IntField(default=0)
    reviews_movid_id = mongoengine.IntField(default=0)
    reviews_rating = mongoengine.IntField(default=0)
    reviews_useful_count = mongoengine.IntField(default=0)
    reviews_content = mongoengine.StringField(default='')
    reviews_author_uid = mongoengine.StringField(default='')
    reviews_author_id = mongoengine.IntField(default=0)
    reviews_author_name = mongoengine.StringField(default='')
    reviews_time = mongoengine.StringField(default='')
    reviews_title = mongoengine.StringField(default='')
    reviews_updated = mongoengine.StringField(default='')
    reviews_share_url = mongoengine.StringField(default='')
    reviews_summary = mongoengine.StringField(default='')
    reviews_useless_count = mongoengine.IntField(default=0)
    reviews_comments_count = mongoengine.IntField(default=0)
    record_time = mongoengine.StringField(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


class CollectMovieDB(mongoengine.Document):
    movie_id = mongoengine.IntField(default=0)  # 唯一标识
    original_title = mongoengine.StringField(default='')  # 原始标题
    title = mongoengine.StringField(default='')  # 中文标题
    rating = mongoengine.StringField(default='')  # 评分
    ratings_count = mongoengine.IntField(default=0)  # 评分数
    pubdate = mongoengine.StringField(default='')  # 上映日期
    pubdates = mongoengine.StringField(default='')  # 上映日期2
    year = mongoengine.IntField(default=0)  # 年份
    countries = mongoengine.StringField(default='')  # 制片国家/地区
    mainland_pubdate = mongoengine.StringField(default='')  # 主要上映日期
    aka = mongoengine.StringField(default='')  # 又名
    tags = mongoengine.StringField(default='')  # 标签
    durations = mongoengine.StringField(default='')  # 时长
    genres = mongoengine.StringField(default='')  # 类型
    videos = mongoengine.StringField(default='')  # 短视频
    wish_count = mongoengine.StringField(default='')  # 想看
    reviews_count = mongoengine.IntField(default=0)  # 短评数
    comments_count = mongoengine.IntField(default=0)  # 评论数
    collect_count = mongoengine.IntField(default=0)  # 收藏
    images = mongoengine.StringField(default='')  # 封面图片
    photos = mongoengine.StringField(default='')  # 照片
    languages = mongoengine.StringField(default='')  # 语言
    writers = mongoengine.StringField(default='')  # 作者
    actor = mongoengine.StringField(default='')  # 演员
    summary = mongoengine.StringField(default='')  # 简介
    directors = mongoengine.StringField(default='')  # 导演
    record_time = mongoengine.StringField(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


class CollectTop250MovieDB(mongoengine.Document):
    movie_id = mongoengine.IntField(default=0)
    movie_title = mongoengine.StringField(default='')
    movie_original_title = mongoengine.StringField(default='')
    movie_rating = mongoengine.StringField(default='')
    movie_year = mongoengine.IntField(default=0)
    movie_pubdates = mongoengine.StringField(default='')
    movie_directors = mongoengine.StringField(default='')
    movie_genres = mongoengine.StringField(default='')
    movie_actor = mongoengine.StringField(default='')
    movie_durations = mongoengine.StringField(default='')
    movie_collect_count = mongoengine.IntField(default=0)
    movie_mainland_pubdate = mongoengine.StringField(default='')
    movie_images = mongoengine.StringField(default='')
    record_time = mongoengine.StringField(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


class CollectMusicCommentsDB(mongoengine.Document):
    comments_id = mongoengine.IntField(default=0)
    comments_music_id = mongoengine.IntField(default=0)
    comments_rating = mongoengine.IntField(default=0)
    comments_rating_text = mongoengine.StringField(default='')
    comments_useful_count = mongoengine.IntField(default=0)
    comments_content = mongoengine.StringField(default='')
    comments_author_id = mongoengine.StringField(default='')
    comments_author_name = mongoengine.StringField(default='')
    comments_time = mongoengine.StringField(default='')
    record_time = mongoengine.StringField(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


class CollectMusicReviewsDB(mongoengine.Document):
    reviews_id = mongoengine.IntField(default=0)
    reviews_music_id = mongoengine.IntField(default=0)
    reviews_rating = mongoengine.IntField(default=0)
    reviews_rating_text = mongoengine.StringField(default='')
    reviews_useful_count = mongoengine.IntField(default=0)
    reviews_content = mongoengine.StringField(default='')
    reviews_author_id = mongoengine.StringField(default='')
    reviews_author_name = mongoengine.StringField(default='')
    reviews_time = mongoengine.StringField(default='')
    reviews_title = mongoengine.StringField(default='')
    reviews_useless_count = mongoengine.IntField(default=0)
    reviews_comments_count = mongoengine.IntField(default=0)
    record_time = mongoengine.StringField(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# class CollectMusicDB(mongoengine.Document):
#     music_id=mongoengine.IntField(default=0)  # 唯一标识
#     title=mongoengine.StringField(default='')  # 中文标题
#     rating=mongoengine.StringField(default='')  # 评分
#     ratings_count=mongoengine.IntField(default=0)  # 评分数
#     pubdate=mongoengine.StringField(default='')  # 发行时间
#     images=mongoengine.StringField(default='')  # 封面图片
#     summary=mongoengine.StringField(default='')  # 简介
#     publisher=mongoengine.StringField(default='')  # 出版者
#     singer=mongoengine.StringField(default='')  # 歌手
#     media=mongoengine.StringField(default='')  # 介质
#     version=mongoengine.StringField(default='')  # 专辑类型
#     tags=mongoengine.StringField(default='')  # 标签
#     record_time = mongoengine.StringField(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

class CollectMusicDB(mongoengine.Document):
    music_id=mongoengine.IntField(default=0)  # 唯一标识
    title=mongoengine.StringField(default='')  # 中文标题
    rating=mongoengine.StringField(default='')  # 评分
    ratings_count=mongoengine.IntField(default=0)  # 评分数
    pubdate=mongoengine.StringField(default='')  # 发行时间
    images=mongoengine.StringField(default='')  # 封面图片
    summary=mongoengine.StringField(default='')  # 简介
    publisher=mongoengine.StringField(default='')  # 出版者
    singer=mongoengine.StringField(default='')  # 歌手
    media=mongoengine.StringField(default='')  # 介质
    version=mongoengine.StringField(default='')  # 专辑类型
    tags=mongoengine.StringField(default='')  # 标签
    rating_star = mongoengine.StringField(default='')  #评价星级
    comments_count = mongoengine.IntField(default=0)  #短评人数
    reviews_count = mongoengine.IntField(default=0)  #长评人数
    reading_count = mongoengine.IntField(default=0)  #在读人数
    readed_count = mongoengine.IntField(default=0)  #读过人数
    wish_count = mongoengine.IntField(default=0)  #想读人数
    record_time = mongoengine.StringField(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

class CollectBookCommentsDB(mongoengine.Document):
    comments_id = mongoengine.IntField(default=0)
    comments_book_id = mongoengine.IntField(default=0)
    comments_rating = mongoengine.IntField(default=0)
    comments_rating_text = mongoengine.StringField(default='')
    comments_useful_count = mongoengine.IntField(default=0)
    comments_content = mongoengine.StringField(default='')
    comments_author_id = mongoengine.StringField(default='')
    comments_author_name = mongoengine.StringField(default='')
    comments_time = mongoengine.StringField(default='')
    record_time = mongoengine.StringField(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


class CollectBookReviewsDB(mongoengine.Document):
    reviews_id = mongoengine.IntField(default=0)
    reviews_book_id = mongoengine.IntField(default=0)
    reviews_rating = mongoengine.IntField(default=0)
    reviews_rating_text = mongoengine.StringField(default='')
    reviews_useful_count = mongoengine.IntField(default=0)
    reviews_content = mongoengine.StringField(default='')
    reviews_author_id = mongoengine.StringField(default='')
    reviews_author_name = mongoengine.StringField(default='')
    reviews_time = mongoengine.StringField(default='')
    reviews_title = mongoengine.StringField(default='')
    reviews_useless_count = mongoengine.IntField(default=0)
    reviews_comments_count = mongoengine.IntField(default=0)
    record_time = mongoengine.StringField(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

class CollectBookDB(mongoengine.Document):
    book_id = mongoengine.IntField(default=0)  # 唯一标识
    title = mongoengine.StringField(default='')  # 中文标题
    author = mongoengine.StringField(default='')  # 作者
    origin_title = mongoengine.StringField(default='')  # 原始标题
    pubdate = mongoengine.StringField(default='')  # 出版时间
    images = mongoengine.StringField(default='')  # 封面图片
    summary = mongoengine.StringField(default='')  # 书简介
    rating = mongoengine.IntField(default=0)  #评分
    rating_count = mongoengine.IntField(default=0)  #评价人数
    rating_star = mongoengine.StringField(default='')  #评价星级
    comments_count = mongoengine.IntField(default=0)  #短评人数
    reviews_count = mongoengine.IntField(default=0)  #长评人数
    reading_count = mongoengine.IntField(default=0)  #在读人数
    readed_count = mongoengine.IntField(default=0)  #读过人数
    wish_count = mongoengine.IntField(default=0)  #想读人数
    publisher = mongoengine.StringField(default='')  # 出版商
    isbn10 = mongoengine.StringField(default='')  # ISBN10
    isbn13 = mongoengine.StringField(default='')  # ISBN13
    author_intro = mongoengine.StringField(default='')  # 作者简介
    ebook_price = mongoengine.StringField(default='')  # 电子书价格
    price = mongoengine.StringField(default='')  # 电子书价格
    series = mongoengine.StringField(default='')  # 系列
    pages = mongoengine.IntField(default=0)  # 页数
    translator = mongoengine.StringField(default='')  # 翻译人
    binding = mongoengine.StringField(default='')  # 出版类型
    tags = mongoengine.StringField(default='')  # 标签
    record_time = mongoengine.StringField(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# class CollectBookDB(mongoengine.Document):
#     book_id = mongoengine.IntField(default=0)  # 唯一标识
#     title = mongoengine.StringField(default='')  # 中文标题
#     author = mongoengine.StringField(default='')  # 作者
#     origin_title = mongoengine.StringField(default='')  # 原始标题
#     pubdate = mongoengine.StringField(default='')  # 出版时间
#     images = mongoengine.StringField(default='')  # 封面图片
#     summary = mongoengine.StringField(default='')  # 书简介
#     publisher = mongoengine.StringField(default='')  # 出版商
#     isbn10 = mongoengine.StringField(default='')  # ISBN10
#     isbn13 = mongoengine.StringField(default='')  # ISBN13
#     author_intro = mongoengine.StringField(default='')  # 作者简介
#     ebook_price = mongoengine.StringField(default='')  # 电子书价格
#     price = mongoengine.StringField(default='')  # 电子书价格
#     series = mongoengine.StringField(default='')  # 系列
#     pages = mongoengine.IntField(default=0)  # 页数
#     translator = mongoengine.StringField(default='')  # 翻译人
#     binding = mongoengine.StringField(default='')  # 出版类型
#     tags = mongoengine.StringField(default='')  # 标签
#     record_time = mongoengine.StringField(default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))