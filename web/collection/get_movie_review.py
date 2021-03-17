import requests
import json
import datetime
import codecs
import time
from utils.mongodb_model import CollectMovieReviewsDB


# 存储某个电影所有评论
# def get_movie_comments(request):
def get_movie_reviews(id, count):
    result = CollectMovieReviewsDB.objects.filter(reviews_movid_id=id)
    # 若果存在记录，则不再进行爬取，直接return
    if (result and count == len(result)):
        return len(result)

    # total = 0  #搜索总数
    # cat=1001：书籍、cat=1002：电影、cat=1003：音乐
    i = 0
    data = []
    # id = request.GET.get("id")
    # id = 26985916
    start = 0
    # cat = request.GET.get("cat") if request.GET.get("cat") else ''
    # start = request.GET.get("start") if request.GET.get("start") else 0

    while True:
        # https://www.douban.com/j/search?q=%E6%97%B6%E9%97%B4%E7%AE%80%E5%8F%B2&start=0&subtype=item&cat=1002
        url = 'https://api.douban.com/v2/movie/subject/' + str(
            id) + '/reviews?apikey=0df993c66c0c636e29ecbb5344252a4a&count=500&start=' + str(start)
        print(url)
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
            html = requests.get(url, headers=headers, timeout=10)
        except Exception as e:
            print('{"status": 0, "message": "获取失败！", "type": "get_movie_reviews" ,"url": ', url, ' , "movie_id": ',str(id), '_', str(start), '}')
            with codecs.open('record/' + datetime.datetime.now().strftime('%Y-%m-%d') + '_error.txt', 'a+','utf-8') as output:
                output.write('{"status": 0, "message": "获取失败！", "type": "get_movie_reviews", "url": "' + url + '" ,"movie_id": ' + str(id) + '_' + str(start) + '}' + '\n')
            # return '{"status": 0, "message": "获取失败！", "type": "get_movie_reviews", "url": "' + url + '" , "movie_id": ' + str(id) + '_' + str(start) + '}'
            continue
            # break
        if html.status_code == 404:
            print('{"status": 0, "message": "获取失败404！", "type": "get_movie_reviews" ,"url": "', url, '" ,"movie_id": ',str(id), '_', str(start), '}')
            with codecs.open('record/' + datetime.datetime.now().strftime('%Y-%m-%d') + '_error.txt', 'a+','utf-8') as output:
                output.write('{"status": 0, "message": "获取失败404！", "type": "get_movie_reviews", "url": "' + url + '" ,"movie_id": ' + str(id) + '_' + str(start) + '}' + '\n')
            # return '{"status": 0, "message": "获取失败404！", "type": "get_movie_reviews", "url": "' + url + '" , "movie_id": ' + str(id) + '_' + str(start) + '}'
            continue

        htmls = json.loads(html.text)
        comments = htmls['reviews']
        total = htmls['total']
        start += 100

        if len(comments) == 0:
            print('{"status": 1, "message": "已获取完，后无记录！", "type": "get_movie_reviews", "movie_id": ', str(id),
                  '_' + str(start), ', "count": ', str(i), '}')
            return '已获取完，后无记录！' + str(id) + '_' + str(start) + ',' + str(i)

        for index, reviews in enumerate(comments):
            # print(reviews)
            reviews_rating = reviews['rating']['value']  # 评分
            reviews_useful_count = reviews['useful_count']  # 认为有用
            reviews_author_uid = reviews['author']['uid']  # 用户标识
            reviews_author_id = reviews['author']['id']  # 用户id
            reviews_author_name = reviews['author']['name']  # 用户名称
            reviews_movid_id = reviews['subject_id']  # 电影id
            reviews_content = reviews['content']  # 内容
            reviews_id = reviews['id']  # 评论id
            reviews_time = reviews['created_at']  # 评论时间
            reviews_title = reviews['title']  # 评论标题
            reviews_updated = reviews['updated_at']  # 评论更新时间
            reviews_share_url = reviews['share_url']  # 评论分享url
            reviews_summary = reviews['summary']  # 评论简述
            reviews_useless_count = reviews['useless_count']  # 认为无用
            reviews_comments_count = reviews['comments_count']  # 评论数
            i += 1
            sign = CollectMovieReviewsDB.objects.filter(reviews_id=reviews_id).count()
            if sign:
                continue
            # 存储到MongoDB
            CollectMovieReviewsDB.objects.create(reviews_id=int(reviews_id),
                                                 reviews_movid_id=int(reviews_movid_id),
                                                 reviews_rating=int(reviews_rating),
                                                 reviews_useful_count=int(reviews_useful_count),
                                                 reviews_content=str(reviews_content),
                                                 reviews_author_uid=str(reviews_author_uid),
                                                 reviews_author_id=int(reviews_author_id),
                                                 reviews_author_name=str(reviews_author_name),
                                                 reviews_time=str(reviews_time),
                                                 reviews_title=str(reviews_title),
                                                 reviews_updated=str(reviews_updated),
                                                 reviews_share_url=str(reviews_share_url),
                                                 reviews_summary=str(reviews_summary),
                                                 reviews_useless_count=int(reviews_useless_count),
                                                 reviews_comments_count=int(reviews_comments_count),
                                                 )

        if i % 1000 == 0:
            time.sleep(2)

        # if start > total:
        if start > 50:
            break

    print("共收集长评论：", i, "条！")
    return i
    # return HttpResponse('{"status": 1, "message": "获取成功！"}')
    # return render(request, 'index.html', context)
    # print('加载第【{}】页成功'.format(active.text))

# get_movie_reviews('26985916')
