import requests
import json
import time
import datetime
import re
import codecs
from bs4 import BeautifulSoup
from utils.mongodb_model import CollectBookReviewsDB

# 存储某个电影所有评论
# def get_movie_comments(request):
def get_book_reviews(id):
    i = 0

    start = 0

    while True:
        tt = int(round(time.time() * 1000))
        # url = 'http://127.0.0.1:8080/try/1/5/4.html'
        url = 'https://book.douban.com/subject/' + str(id) + '/reviews?sort=time&start=' + str(start) + '&_=' + str(tt)
        print(url)
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json'}
            html = requests.get(url, headers=headers, timeout=10)
        except Exception as e:
            print('{"status": 0, "message": "获取失败！", "type": "get_book_reviews" ,"url": ' , url , ' , "book_id": ' , str(id) , '_' , str(start) , '}')
            with codecs.open('record/'+datetime.datetime.now().strftime('%Y-%m-%d')+'_error.txt', 'a+', 'utf-8') as output:
                output.write('{"status": 0, "message": "获取失败！", "type": "get_book_reviews", "url": "' + url + '" ,"book_id": ' + str(id) + '_' + str(start) + '}' + '\n')
            continue
        if html.status_code == 404:
            print('{"status": 0, "message": "获取失败404！", "type": "get_book_reviews" ,"url": "' , url , '" ,"book_id": ' , str(id) , '_' , str(start) , '}')
            with codecs.open('record/'+datetime.datetime.now().strftime('%Y-%m-%d')+'_error.txt', 'a+', 'utf-8') as output:
                output.write('{"status": 0, "message": "获取失败404！", "type": "get_book_reviews", "url": "' + url + '" ,"book_id": ' + str(id) + '_' + str(start) + '}' + '\n')
            continue

        html.encoding = "utf-8"
        try:
            htmls = json.loads(html.text)
        except Exception as e:
            continue
        reviews = htmls['html']
        # print(reviews)
        count = htmls['count']
        if count == 0:
            break
        soup = BeautifulSoup(reviews, features='html.parser')
        for item in soup.find_all(name='div', attrs={'class': 'review-item'}):
            reviews_id = item['id']
            author = item.find(name='a', attrs={'class': 'name'})
            author_id = re.search(r'(.*)https://www.douban.com/people/(.*)/(.*)', author['href'], re.M | re.I).group(2)
            author = author.string
            reviews_time = item.find(name='span', attrs={'class': 'main-meta'})
            reviews_time = reviews_time.string
            content = item.find(name='div', attrs={'class': 'main-bd'})
            title = content.h2.a.string
            star = item.find(name='span', attrs={'class': re.compile(r'^allstar')})
            # print(star)
            if star:
                star_str = star['title']
                # print(star_str)
                star = star['class'][0][-2:]
                # print(star)
            else:
                star_str = ''
                star = 0
            result = CollectBookReviewsDB.objects.filter(reviews_id=reviews_id).first()
            if result:
                continue
            if reviews_id:
                url = 'https://book.douban.com/j/review/' + reviews_id + '/full'
                try:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                        'X-Requested-With': 'XMLHttpRequest',
                        'Accept': 'application/json'}
                    html = requests.get(url, headers=headers, timeout=10)
                except Exception as e:
                    print('{"status": 0, "message": "获取失败！", "type": "get_book_reviews_all" ,"url": ', url,
                          ' , "book_id": ', str(id), '_', str(start), '}')
                    with codecs.open('record/' + datetime.datetime.now().strftime('%Y-%m-%d') + '_error.txt', 'a+',
                                     'utf-8') as output:
                        output.write(
                            '{"status": 0, "message": "获取失败！", "type": "get_book_reviews_all", "url": "' + url + '" ,"book_id": ' + str(
                                id) + '_' + str(start) + '}' + '\n')
                if html.status_code == 404:
                    print('{"status": 0, "message": "获取失败404！", "type": "get_book_reviews_all" ,"url": "', url,
                          '" ,"book_id": ', str(id), '_', str(start), '}')
                    with codecs.open('record/' + datetime.datetime.now().strftime('%Y-%m-%d') + '_error.txt', 'a+',
                                     'utf-8') as output:
                        output.write(
                            '{"status": 0, "message": "获取失败404！", "type": "get_book_reviews_all", "url": "' + url + '" ,"book_id": ' + str(
                                id) + '_' + str(start) + '}' + '\n')
                if html.status_code == 403:
                    print('{"status": 0, "message": "获取失败403！", "type": "get_book_reviews_all" ,"url": "', url,
                          '" ,"book_id": ', str(id), '_', str(start), '}')
                    with codecs.open('record/' + datetime.datetime.now().strftime('%Y-%m-%d') + '_error.txt', 'a+',
                                     'utf-8') as output:
                        output.write(
                            '{"status": 0, "message": "获取失败403！", "type": "get_book_reviews_all", "url": "' + url + '" ,"book_id": ' + str(
                                id) + '_' + str(start) + '}' + '\n')
                html.encoding = "utf-8"
                try:
                    htmls = json.loads(html.text)
                except Exception as e:
                    continue
                reviews_all = htmls['html']
                useful_count = htmls['votes']['useful_count']
                useless_count = htmls['votes']['useless_count']
            i+=1
            CollectBookReviewsDB.objects.create(
                    reviews_id=reviews_id,
                    reviews_book_id=id,
                    reviews_rating=star,
                    reviews_rating_text=star_str,
                    reviews_useful_count=useful_count,
                    reviews_content=reviews_all,
                    reviews_author_id=author_id,
                    reviews_author_name=author,
                    reviews_time=reviews_time,
                    reviews_title=title,
                    reviews_useless_count=useless_count)
            if i % 500 == 0:
                time.sleep(2)
        start+=count
        # start += 100
        # break

        if start > 50:
            break

    print("共收集长评论：", i, "条！")
    return i
    # return HttpResponse('{"status": 1, "message": "获取成功！"}')
    # return render(request, 'index.html', context)
    # print('加载第【{}】页成功'.format(active.text))

# get_book_reviews('3021566')
