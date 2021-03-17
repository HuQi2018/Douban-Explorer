import requests
import json
import time
import datetime
import codecs
import re
from bs4 import BeautifulSoup
from collection.get_music_review import get_music_reviews
from collection.get_music_comments import get_music_comments
from utils.mongodb_model import CollectMusicDB
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
    return (rating_star, comments_count, reviews_count, reading_count, readed_count, wish_count)

# 存储某个电影的信息
# def get_music(request):
def get_music(id):
    if not id :
        return '{"status": 0, "message": "获取失败！请输入参数！", "data": []}'
    result = CollectMusicDB.objects.filter(music_id=id).first()
    url = 'https://douban.uieee.com/v2/music/' + str(id)
    print(url)
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
             'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json'}
        html = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        print('{"status": 0, "message": "获取失败！", "type": "get_music", "url": "' , url , '" ,"music_id": ' , str(id) , '}')
        with codecs.open('record/'+datetime.datetime.now().strftime('%Y-%m-%d')+'_error.txt', 'a+', 'utf-8') as output:
            output.write('{"status": 0, "message": "获取失败！", "type": "get_music", "url": "' + url + '" ,"music_id": ' + str(id) + '}' + '\n')
        return '{"status": 0, "message": "获取失败！", "type": "get_music", "music_id": ' + str(id) + '}'
        # break
    if html.status_code == 404:
        print('{"status": 0, "message": "获取失败404！", "type": "get_music", "url": "' , url + '" ,"music_id": ' , str(id),'}')
        with codecs.open('record/'+datetime.datetime.now().strftime('%Y-%m-%d')+'_error.txt', 'a+', 'utf-8') as output:
            output.write('{"status": 0, "message": "获取失败404！", "type": "get_music", "url": "' + url + '" ,"music_id": ' + str(id) + '\n')
        return '{"status": 0, "message": "获取失败404！", "type": "get_music", "music_id": ' + str(id) + '}'

    htmls = json.loads(html.text)
    id = htmls['id']  # 唯一标识
    title = htmls['title']  # 中文标题
    rating = htmls['rating']['average']  # 评分
    ratings_count = htmls['rating']['numRaters']  # 评分人数
    try:
        pubdate = htmls['attrs']['pubdate']  # 发行时间
    except:
        pubdate = ''
        pass
    images = htmls['image']  # 封面图片
    summary = htmls['summary']  # 简介
    try:
        publisher = htmls['attrs']['publisher']  # 出版者
    except:
        publisher = ''
        pass
    try:
        singer = htmls['attrs']['singer']  # 歌手
    except:
        singer = ''
        pass
    try:
        media = htmls['attrs']['media']  # 介质
    except:
        media = ''
        pass
    try:
        version = htmls['attrs']['version']  # 专辑类型
    except:
        version = ''
        pass
    tags = htmls['tags']  # 标签
    (rating_star, comments_count, reviews_count, reading_count, readed_count, wish_count) = get_search(id)
    print(id)
    # 若果存在记录，则不再进行爬取，直接return
    # if (result):
    #     print(len(result))
    #     return len(result)
    # 存储到MongoDB
    if result :
        result.update(
            music_id=int(id),  # 唯一标识
            title=str(title),  # 中文标题
            rating=str(rating),  # 评分
            ratings_count=int(ratings_count),  # 评分数
            pubdate=str(pubdate),  # 发行时间
            images=str(images),  # 封面图片
            summary=str(summary),  # 简介
            rating_star=str(rating_star),  #评价星级
            comments_count=int(comments_count),  #短评人数
            reviews_count=int(reviews_count),  #长评人数
            reading_count=int(reading_count),  #在读人数
            readed_count=int(readed_count),  #读过人数
            wish_count=int(wish_count),  #想读人数
            publisher=str(publisher),  # 出版者
            singer=str(singer),  # 歌手
            media=str(media),  # 介质
            version=str(version),  # 专辑类型
            tags=str(tags))
    else:
        CollectMusicDB.objects.create(
            music_id=int(id),  # 唯一标识
            title=str(title),  # 中文标题
            rating=str(rating),  # 评分
            ratings_count=int(ratings_count),  # 评分数
            pubdate=str(pubdate),# 发行时间
            images=str(images),  # 封面图片
            summary=str(summary),  # 简介
            rating_star=str(rating_star),  #评价星级
            comments_count=int(comments_count),  #短评人数
            reviews_count=int(reviews_count),  #长评人数
            reading_count=int(reading_count),  #在读人数
            readed_count=int(readed_count),  #读过人数
            wish_count=int(wish_count),  #想读人数
            publisher=str(publisher),  # 出版者
            singer=str(singer),# 歌手
            media=str(media),# 介质
            version=str(version),# 专辑类型
            tags=str(tags))

    get_record_comments = get_music_comments(id)
    time.sleep(2)
    get_record_reviews = get_music_reviews(id)
    time.sleep(2)

    data = str(id)+ "\t记录完成！\t短评："+ str(get_record_comments)+ " 长评："+ str(get_record_reviews)
    print(data)
    return '{"status": 1, "message": "获取成功！", "data": "' + data + '"}'

    # data = str(id) + '\t短评：' + str(get_record_comments) + '\t长评：' + str(get_record_reviews)
    # return data

def main(request):
    id = request.GET.get("id")
    data = get_music(id)
    return HttpResponse(data)
# get_music('35030138')
