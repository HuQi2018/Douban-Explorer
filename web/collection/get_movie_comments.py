import requests
import json
import datetime
import codecs
import time
from utils.mongodb_model import CollectMovieCommentsDB


# 存储某个电影所有评论
# def get_movie_comments(request):
def get_movie_comments(id, count):
    result = CollectMovieCommentsDB.objects.filter(comments_movid_id=id).count()
    # 若果存在记录，则不再进行爬取，直接return
    if (result and result >= 500):#短评只能获取到500条
        return result

    i = 0
    start = 0

    while True:
        # https://www.douban.com/j/search?q=%E6%97%B6%E9%97%B4%E7%AE%80%E5%8F%B2&start=0&subtype=item&cat=1002
        url = 'https://api.douban.com/v2/movie/subject/' + str(
            id) + '/comments?apikey=0df993c66c0c636e29ecbb5344252a4a&count=500&start=' + str(start)
        print(url)
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
            html = requests.get(url, headers=headers, timeout=10)
        except Exception as e:
            print('{"status": 0, "message": "获取失败！", "type": "get_movie_comments" ,"url": ', url, ' , "movie_id": ',str(id), '_', str(start), '}')
            with codecs.open('record/' + datetime.datetime.now().strftime('%Y-%m-%d') + '_error.txt', 'a+','utf-8') as output:
                output.write('{"status": 0, "message": "获取失败！", "type": "get_movie_comments" ,"url": ' + url + ' , "movie_id": ' + str(id) + '_' + str(start) + '}' + '\n')
            # return '{"status": 0, "message": "获取失败！", "type": "get_movie_comments" ,"url": "' + url + '" , "movie_id": ' + str(id) + '_' + str(start) + '}'
            # break
            continue
        if html.status_code == 404:
            print('{"status": 0, "message": "获取失败404！", "type": "get_movie_comments" ,"url": "', url, '" ,"movie_id": ',str(id), '_', str(start), '}')
            with codecs.open('record/' + datetime.datetime.now().strftime('%Y-%m-%d') + '_error.txt', 'a+','utf-8') as output:
                output.write('{"status": 0, "message": "获取失败404！", "type": "get_movie_comments" ,"url": "' + url + '" ,"movie_id": ' + str(id) + '_' + str(start) + '}' + '\n')
            # return '{"status": 0, "message": "获取失败404！", "type": "get_movie_comments" ,"url": "' + url + '" , "movie_id": ' + str(id) + '_' + str(start) + '}'
            continue

        htmls = json.loads(html.text)
        comments = htmls['comments']
        total = htmls['total']
        start += 100

        if len(comments) == 0:
            print('{"status": 1, "message": "已获取完，后无记录！", "type": "get_movie_comments", "movie_id": ', str(id),
                  '_' + str(start), ', "count": ', str(i), '}')
            return '已获取完，后无记录！' + str(id) + '_' + str(start) + ',' + str(i)

        for index, reviews in enumerate(comments):
            # print(reviews)
            comments_rating = reviews['rating']['value']  # 评分
            comments_useful_count = reviews['useful_count']  # 认为有用
            comments_author_uid = reviews['author']['uid']  # 用户标识
            comments_author_id = reviews['author']['id']  # 用户id
            comments_author_name = reviews['author']['name']  # 用户名称
            comments_movid_id = reviews['subject_id']  # 电影id
            comments_content = reviews['content']  # 内容
            comments_id = reviews['id']  # 评论id
            comments_time = reviews['created_at']  # 评论时间
            sign = CollectMovieCommentsDB.objects.filter(comments_id=comments_id).count()
            if sign:
                continue
            # 存储到MongoDB
            i += 1
            CollectMovieCommentsDB.objects.create(comments_id=int(comments_id),
                                                  comments_movid_id=int(comments_movid_id),
                                                  comments_rating=int(comments_rating),
                                                  comments_useful_count=int(comments_useful_count),
                                                  comments_content=str(comments_content),
                                                  comments_author_uid=str(comments_author_uid),
                                                  comments_author_id=int(comments_author_id),
                                                  comments_author_name=str(comments_author_name),
                                                  comments_time=str(comments_time))

        if i % 1000 == 0:
            time.sleep(2)

        if start > total:
            break

    print("共收集短评论：", i, "条！")
    return i
    # return HttpResponse('{"status": 1, "message": "获取成功！"}')
    # return render(request, 'index.html', context)
    # print('加载第【{}】页成功'.format(active.text))

# get_movie_comments('26985916')
