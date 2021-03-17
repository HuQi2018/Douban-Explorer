import requests
import json
from django.http import HttpResponse
import time
import datetime
import codecs
from collection.get_movie_review import get_movie_reviews
from collection.get_movie_comments import get_movie_comments
from utils.mongodb_model import CollectMovieDB


# 存储某个电影的信息
def get_movie(id):

    if not id :
        return '{"status": 0, "message": "获取失败！请输入参数！", "data": []}'
    result = CollectMovieDB.objects.filter(movie_id=id).first()

    url = 'https://api.douban.com/v2/movie/subject/' + str(id) + '?apikey=0df993c66c0c636e29ecbb5344252a4a'
    print(url)
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
        html = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        print('{"status": 0, "message": "获取失败！", "type": "get_movie", "url": "' , url , '" ,"movie_id": ' , str(id) , '}')
        with codecs.open('record/'+datetime.datetime.now().strftime('%Y-%m-%d')+'_error.txt', 'a+', 'utf-8') as output:
            output.write('{"status": 0, "message": "获取失败！", "type": "get_movie", "url": "' + url + '" ,"movie_id": ' + str(id) + '}' + '\n')
        return '{"status": 0, "message": "获取失败！", "type": "get_movie", "movie_id": ' + str(id) + '}'
        # break
    if html.status_code == 404:
        print('{"status": 0, "message": "获取失败404！", "type": "get_movie", "url": "' , url + '" ,"movie_id": ' , str(id) , '}')
        with codecs.open('record/'+datetime.datetime.now().strftime('%Y-%m-%d')+'_error.txt', 'a+', 'utf-8') as output:
            output.write('{"status": 0, "message": "获取失败404！", "type": "get_movie", "url": "' + url + '" ,"movie_id": ' + str(id) + '}' + '\n')
        return '{"status": 0, "message": "获取失败404！", "type": "get_movie", "movie_id": ' + str(id) + '}'

    htmls = json.loads(html.text)
    id = htmls['id']  # 唯一标识
    original_title = htmls['original_title']  # 原始标题
    title = htmls['title']  # 中文标题
    rating = htmls['rating']  # 评分
    ratings_count = htmls['ratings_count']  # 评分数
    pubdate = htmls['pubdate']  # 上映日期
    pubdates = htmls['pubdates']  # 上映日期2
    year = htmls['year']  # 年份
    countries = htmls['countries']  # 制片国家/地区
    mainland_pubdate = htmls['mainland_pubdate']  # 主要上映日期
    aka = htmls['aka']  # 又名
    tags = htmls['tags']  # 标签
    durations = htmls['durations']  # 时长
    genres = htmls['genres']  # 类型
    videos = htmls['videos']  # 短视频
    wish_count = htmls['wish_count']  # 想看
    reviews_count = htmls['reviews_count']  # 短评数
    comments_count = htmls['comments_count']  # 评论数
    collect_count = htmls['collect_count']  # 收藏
    images = htmls['images']  # 封面图片
    photos = htmls['photos']  # 照片
    languages = htmls['languages']  # 语言
    writers = htmls['writers']  # 作者
    actor = htmls['casts']  # 演员
    summary = htmls['summary']  # 简介
    directors = htmls['directors']  # 导演
    print(id)
    # 若果存在记录，则不再进行爬取，直接return
    # if (result):
    #     print(len(result))
    #     return len(result)

    if result :
        result.update(
            movie_id=int(id),  # 唯一标识
            original_title=str(original_title),  # 原始标题
            title=str(title),  # 中文标题
            rating=str(rating),  # 评分
            ratings_count=int(ratings_count),  # 评分数
            pubdate=str(pubdate),  # 上映日期
            pubdates=str(pubdates),  # 上映日期2
            year=int(year),  # 年份
            countries=str(countries),  # 制片国家/地区
            mainland_pubdate=str(mainland_pubdate),  # 主要上映日期
            aka=str(aka),  # 又名
            tags=str(tags),  # 标签
            durations=str(durations),  # 时长
            genres=str(genres),  # 类型
            videos=str(videos),  # 短视频
            wish_count=str(wish_count),  # 想看
            reviews_count=int(reviews_count),  # 短评数
            comments_count=int(comments_count),  # 评论数
            collect_count=int(collect_count),  # 收藏
            images=str(images),  # 封面图片
            photos=str(photos),  # 照片
            languages=str(languages),  # 语言
            writers=str(writers),  # 作者
            actor=str(actor),  # 演员
            summary=str(summary),  # 简介
            directors=str(directors))  # 导演
    else:
    # 存储到MongoDB
        CollectMovieDB.objects.create(
            movie_id=int(id),  # 唯一标识
            original_title=str(original_title),  # 原始标题
            title=str(title),  # 中文标题
            rating=str(rating),  # 评分
            ratings_count=int(ratings_count),  # 评分数
            pubdate=str(pubdate),  # 上映日期
            pubdates=str(pubdates),  # 上映日期2
            year=int(year),  # 年份
            countries=str(countries),  # 制片国家/地区
            mainland_pubdate=str(mainland_pubdate),  # 主要上映日期
            aka=str(aka),  # 又名
            tags=str(tags),  # 标签
            durations=str(durations),  # 时长
            genres=str(genres),  # 类型
            videos=str(videos),  # 短视频
            wish_count=str(wish_count),  # 想看
            reviews_count=int(reviews_count),  # 短评数
            comments_count=int(comments_count),  # 评论数
            collect_count=int(collect_count),  # 收藏
            images=str(images),  # 封面图片
            photos=str(photos),  # 照片
            languages=str(languages),  # 语言
            writers=str(writers),  # 作者
            actor=str(actor),  # 演员
            summary=str(summary),  # 简介
            directors=str(directors))  # 导演
    get_record_comments = get_movie_comments(id, comments_count)
    time.sleep(3)
    get_record_reviews = get_movie_reviews(id, reviews_count)
    time.sleep(3)

    print(id,"\t记录完成！", "短评：",get_record_comments ,"：" ,comments_count , "   长评：", get_record_reviews ,"：" ,reviews_count)
    data = str(id) + '\t短评：' + str(get_record_comments) + ':' + str(comments_count) + '\t长评：' + str(get_record_reviews) + ':' + str(reviews_count)
    return '{"status": 1, "message": "获取成功！", "data": "' + data + '"}'


def main(request):
    id = request.GET.get("id")
    data = get_movie(id)
    return HttpResponse(data)

# return HttpResponse('{"status": 1, "message": "获取成功！"}')
# return render(request, 'index.html', context)
# print('加载第【{}】页成功'.format(active.text))

# get_movie('26985916')
