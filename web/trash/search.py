import requests
from bs4 import BeautifulSoup
import re
import json
from django.http import HttpResponse


def get_search(request):
    # def get_search():

    q = request.GET.get("q")

    if not q:
        return HttpResponse('{"status": 0, "message": "获取失败！请输入正确的参数！", "data": {}}')

    # cat=1001：书籍、cat=1002：电影、cat=1003：音乐
    # https://www.douban.com/j/search?q=%E6%97%B6%E9%97%B4%E7%AE%80%E5%8F%B2&start=0&subtype=item&cat=1002
    url = 'https://www.douban.com/search?q=' + q
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
        html = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        e
        # break
    if html.status_code == 404:
        print("404")
    soup = BeautifulSoup(html.text.encode("utf-8"), features='html.parser')
    soup = soup.find(name='div', attrs={'class': 'result-list'})
    data = []
    # print(soup)
    for item in soup.find_all(name='div', attrs={'class': 'content'}):
        reviews = {}
        matchObj = re.search(r'(.*)dou_search_(.*)\', sid: (.*), qcat(.*)', item.div.h3.a['onclick'], re.M | re.I)
        id = matchObj.group(3)  # 唯一ID
        name = item.div.h3.a.string  # 名称
        # type = item.div.h3.span.string    #类型：[书籍]、[电影]、[音乐]
        type = matchObj.group(2)  # 类型：[书籍]、[电影]、[音乐]
        link = item.div.h3.a['href']  # 跳转链接
        if item.div.div['class'][0] == 'rating-info':
            star = item.div.div.contents[1]['class'][0][-2:]  # 星级
            if item.div.div.contents[3].string == '(评价人数不足)':
                score = item.div.div.contents[3].string  # 评分
                author = item.div.div.contents[5].string  # 作者
            else:
                score = item.div.div.contents[3].string  # 评分
                reviews_count = item.div.div.contents[5].string  # 评价人数
                author = item.div.div.contents[7].string  # 作者
        if item.p:
            brief = item.p.string  # 简述
        reviews['id'] = id
        reviews['name'] = name
        reviews['type'] = type
        reviews['link'] = link
        reviews['star'] = star
        reviews['score'] = score
        reviews['author'] = author
        reviews['reviews_count'] = reviews_count
        reviews['brief'] = brief
        data.append(reviews)
    # print(data)
    data = json.dumps(data)
    return HttpResponse('{"status": 0, "message": "获取成功！", "data": ' + str(data) + '}')
    # return render(request, 'index.html', context)
    # print('加载第【{}】页成功'.format(active.text))

# get_search()
