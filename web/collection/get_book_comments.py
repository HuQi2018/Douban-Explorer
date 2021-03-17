import requests
import json
import codecs
import re
import time
import datetime
from bs4 import BeautifulSoup
from utils.mongodb_model import CollectBookCommentsDB


# 存储某个电影所有评论
# def get_movie_comments(request):
def get_book_comments(id):
    result = CollectBookCommentsDB.objects.filter(comments_book_id=id).count()
    # 若果存在记录，则不再进行爬取，直接return
    if (result and result >= 500):#短评只能获取到500条
        return result

    i = 0
    start = 1
    while True:
        tt = int(round(time.time() * 1000))
        # url = 'https://book.douban.com/subject/35030138/comments/new?p=2&_=1587693299777';
        # url = "http://127.0.0.1:8080/try/1/5/4.html"
        url = 'https://book.douban.com/subject/' + str(id) + '/comments/new?p=' + str(start) + '&_=' + str(tt)
        print(url)
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json'}
            html = requests.get(url, headers=headers, timeout=10)
        except Exception as e:
            print('{"status": 0, "message": "获取失败！", "type": "get_book_comments" ,"url": ', url, ' , "book_id": ',str(id), '_', str(start), '}')
            with codecs.open('record/' + datetime.datetime.now().strftime('%Y-%m-%d') + '_error.txt', 'a+','utf-8') as output:
                output.write('{"status": 0, "message": "获取失败！", "type": "get_movie_comments" ,"url": ' + url + ' , "movie_id": ' + str(id) + '_' + str(start) + '}' + '\n')
            continue
        if html.status_code == 404:
            print('{"status": 0, "message": "获取失败404！", "type": "get_book_comments" ,"url": "', url, '" ,"book_id": ',str(id), '_', str(start), '}')
            with codecs.open('record/' + datetime.datetime.now().strftime('%Y-%m-%d') + '_error.txt', 'a+','utf-8') as output:
                output.write('{"status": 0, "message": "获取失败404！", "type": "get_movie_comments" ,"url": "' + url + '" ,"movie_id": ' + str(id) + '_' + str(start) + '}' + '\n')
            continue
        html.encoding = "utf-8"
        htmls = json.loads(html.text)
        # print(htmls)
        content = htmls['content']
        total = htmls['total']
        paginator = htmls['paginator']
        soup = BeautifulSoup(content, features='html.parser')
        if not soup.find(name='div', attrs={'class': 'comment'}):
            break
        for item in soup.find_all(name='div', attrs={'class': 'comment'}):
            comments_id = item.find(name='span', attrs={'class': 'comment-vote'})
            comments_id = comments_id.a['data-cid']
            if not comments_id:
                continue
            # print(comments_id)
            comments_content = item.find(name='span', attrs={'class': 'short'})
            comments_content = comments_content.string
            # print(comments_content)
            vote_count = item.find(name='span', attrs={'class': 'vote-count'})
            vote_count = vote_count.string
            # print(vote_count)
            comment_info = item.find(name='span', attrs={'class': 'comment-info'})
            comment_time = comment_info.contents[len(comment_info.contents) - 2].string
            # print(time)
            author_id = re.search(r'(.*)https://www.douban.com/people/(.*)/(.*)', comment_info.a['href'],
                                  re.M | re.I).group(2)
            # print(author_id)
            author = comment_info.a.string
            # print(author)
            star = comment_info.find(name='span', attrs={'class': re.compile(r'^allstar')})
            if star:
                star_str = star['title']
                # print(star_str)
                star = star['class'][1][-2:]
                # print(star)
            if CollectBookCommentsDB.objects.filter(comments_id=comments_id).first():
                continue
            else:
                i+=1
                CollectBookCommentsDB.objects.create(
                    comments_id=comments_id,
                    comments_book_id=id,
                    comments_rating=star,
                    comments_rating_text=star_str,
                    comments_useful_count=vote_count,
                    comments_content=comments_content,
                    comments_author_id=author_id,
                    comments_author_name=author,
                    comments_time=comment_time)
            # if i % 250 == 0:
            #     time.sleep(2)
        start +=1
        # if start == 26 :
        #     break

    print("共收集短评论：", i, "条！")
    return i
    # return HttpResponse('{"status": 1, "message": "获取成功！"}')
    # return render(request, 'index.html', context)
    # print('加载第【{}】页成功'.format(active.text))

# get_book_comments('3021566')
