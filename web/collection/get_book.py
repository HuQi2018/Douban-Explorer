import requests
import json
import time
import datetime
import re
from bs4 import BeautifulSoup
import codecs
from collection.get_book_review import get_book_reviews
from collection.get_book_comments import get_book_comments
from utils.mongodb_model import CollectBookDB
from django.http import HttpResponse

#额外信息爬取函数
def get_search(id):
    id = str(id)
    url = 'https://book.douban.com/subject/' + id + '/'
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
        html = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        pass
    soup = BeautifulSoup(html.text.encode("utf-8"), features='html.parser')
    rating_num = soup.find(name='strong', attrs={'class': 'rating_num'})
    try:
        rating = re.findall(r'\d+', rating_num.string)[0]  # 评分
    except:
        rating = 0
        pass
    rating_people = soup.find(name='a', attrs={'class': 'rating_people'})
    try:
        rating_count = re.findall(r'\d+', rating_people.span.string)[0]  # 评价人数
    except:
        rating_count = 0
        pass
    rating_per = soup.find_all(name='span', attrs={'class': 'rating_per'})
    if rating_per:
        rating_star = list()
        for i in rating_per:
            rating_star.append(i.string[:-1])  # 评价星级
    else:
        rating_star = ['', '', '', '', '', '']
    comments_count = soup.find(name='a', attrs={'href': 'https://book.douban.com/subject/' + id + '/comments/'})
    try:
        comments_count = re.findall(r'\d+', comments_count.string)[0]  # 短评人数
    except:
        comments_count = 0
        pass
    reviews_count = soup.find(name='a', attrs={'href': 'reviews'})
    try:
        reviews_count = re.findall(r'\d+', reviews_count.string)[0]  # 长评人数
    except:
        reviews_count = 0
        pass
    reading_count = soup.find(name='a', attrs={'href': 'https://book.douban.com/subject/' + id + '/doings'})
    try:
        reading_count = re.findall(r'\d+', reading_count.string)[0]  # 在读人数
    except:
        reading_count = 0
        pass
    readed_count = soup.find(name='a', attrs={'href': 'https://book.douban.com/subject/' + id + '/collections'})
    try:
        readed_count = re.findall(r'\d+', readed_count.string)[0]  # 读过人数
    except:
        readed_count = 0
        pass
    wish_count = soup.find(name='a', attrs={'href': 'https://book.douban.com/subject/' + id + '/wishes'})
    try:
        wish_count = re.findall(r'\d+', wish_count.string)[0]  # 想读人数
    except:
        wish_count = 0
        pass
    return (rating, rating_count, rating_star, comments_count, reviews_count, reading_count, readed_count, wish_count)

# 存储某个电影的信息
# def get_book(request):
def get_book(id):
    if not id :
        return '{"status": 0, "message": "获取失败！请输入参数！", "data": []}'
    result = CollectBookDB.objects.filter(book_id=id).first()
    url = 'https://douban.uieee.com/v2/book/' + str(id)
    print(url)
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
             'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json'}
        html = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        print('{"status": 0, "message": "获取失败！", "type": "get_book", "url": "' , url , '" ,"book_id": ' , str(id) , '}')
        with codecs.open('record/'+datetime.datetime.now().strftime('%Y-%m-%d')+'_error.txt', 'a+', 'utf-8') as output:
            output.write('{"status": 0, "message": "获取失败！", "type": "get_book", "url": "' + url + '" ,"book_id": ' + str(id) + '}' + '\n')
        return '{"status": 0, "message": "获取失败！", "type": "get_book", "book_id": ' + str(id) + '}'
        # break
    if html.status_code == 404:
        print('{"status": 0, "message": "获取失败404！", "type": "get_book", "url": "' , url + '" ,"book_id": ' , str(id),'}')
        with codecs.open('record/'+datetime.datetime.now().strftime('%Y-%m-%d')+'_error.txt', 'a+', 'utf-8') as output:
            output.write('{"status": 0, "message": "获取失败404！", "type": "get_book", "url": "' + url + '" ,"book_id": ' + str(id) + '\n')
        return '{"status": 0, "message": "获取失败404！", "type": "get_book", "book_id": ' + str(id) + '}'

    htmls = json.loads(html.text)
    id = htmls['id']  # 唯一标识
    title = htmls['title']  # 中文标题
    author = htmls['author']  # 作者
    origin_title = htmls['origin_title']  # 原始标题
    pubdate = htmls['pubdate']  # 出版时间
    images = htmls['image']  # 封面图片
    summary = htmls['summary']  # 书简介
    publisher = htmls['publisher']  # 出版商
    isbn10 = htmls['isbn10']  # ISBN10
    try:
        isbn13 = htmls['isbn13']  # ISBN13
    except:
        isbn13 = ''
        pass
    author_intro = htmls['author_intro']  # 作者简介
    try:
        ebook_price = htmls['ebook_price']  # 电子书价格
    except:
        ebook_price = ''
        pass
    price = htmls['price']  # 电子书价格
    try:
        series = htmls['series']  # 系列
    except:
        series = ''
        pass
    try:
        pages = re.findall(r'\d+', htmls['pages'])[0]  # 页数
    except:
        pages = 0
        pass
    if pages == '':
        pages = 0
    translator = htmls['translator']  # 翻译人
    binding = htmls['binding']  # 出版类型
    tags = htmls['tags']  # 标签
    (rating, rating_count, rating_star, comments_count, reviews_count, reading_count, readed_count, wish_count) = get_search(id)
    print(id)
    # 若果存在记录，则不再进行爬取，直接return
    # if (result):
    #     print(len(result))
    #     return len(result)
    # 存储到MongoDB
    if result :
        result.update(
            book_id=int(id),  # 唯一标识
            title=str(title),  # 中文标题
            author=str(author),  # 作者
            origin_title=str(origin_title),  # 原始标题
            pubdate=str(pubdate),  # 出版时间
            images=str(images),  # 封面图片
            summary=str(summary),  # 书简介
            rating=int(rating),  # 评分
            rating_count=int(rating_count),  # 评价人数
            rating_star=str(rating_star),  # 评价星级
            comments_count=int(comments_count),  # 短评人数
            reviews_count=int(reviews_count),  # 长评人数
            reading_count=int(reading_count),  # 在读人数
            readed_count=int(readed_count),  # 读过人数
            wish_count=int(wish_count),  # 想读人数
            publisher=str(publisher),  # 出版商
            isbn10=str(isbn10),  # ISBN10
            isbn13=str(isbn13),  # ISBN13
            author_intro=str(author_intro),  # 作者简介
            ebook_price=str(ebook_price),  # 电子书价格
            price=str(price),  # 电子书价格
            series=str(series),  # 系列
            pages=int(pages),  # 页数
            translator=str(translator),  # 翻译人
            binding=str(binding),  # 出版类型
            tags=str(tags))  # 标签
    else:
        CollectBookDB.objects.create(
            book_id=int(id),  # 唯一标识
            title=str(title),  # 中文标题
            author=str(author),  # 作者
            origin_title=str(origin_title),  # 原始标题
            pubdate=str(pubdate),  # 出版时间
            images=str(images),  # 封面图片
            summary=str(summary),  # 书简介
            rating=int(rating),  # 评分
            rating_count=int(rating_count),  # 评价人数
            rating_star=str(rating_star),  # 评价星级
            comments_count=int(comments_count),  # 短评人数
            reviews_count=int(reviews_count),  # 长评人数
            reading_count=int(reading_count),  # 在读人数
            readed_count=int(readed_count),  # 读过人数
            wish_count=int(wish_count),  # 想读人数
            publisher=str(publisher),  # 出版商
            isbn10=str(isbn10),  # ISBN10
            isbn13=str(isbn13),  # ISBN13
            author_intro=str(author_intro),  # 作者简介
            ebook_price=str(ebook_price),  # 电子书价格
            price=str(price),  # 电子书价格
            series=str(series),  # 系列
            pages=int(pages),  # 页数
            translator=str(translator),  # 翻译人
            binding=str(binding),  # 出版类型
            tags=str(tags))  # 标签

    get_record_comments = get_book_comments(id)
    time.sleep(2)
    get_record_reviews = get_book_reviews(id)
    time.sleep(2)

    data = str(id)+ "\t记录完成！\t短评："+ str(get_record_comments)+ " 长评："+ str(get_record_reviews)
    print(data)
    return '{"status": 1, "message": "获取成功！", "data": "' + data + '"}'


def main(request):
    id = request.GET.get("id")
    data = get_book(id)
    return HttpResponse(data)
# get_book('3021566')
