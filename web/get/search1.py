import requests
from bs4 import BeautifulSoup
import re
import json
from django.http import HttpResponse


# Create your views here.
def response_as_json(data):
    json_str = json.dumps(data)
    response = HttpResponse(
        json_str,
        content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def json_response(data, code=200):
    data = {
        "code": code,
        "msg": "success",
        "data": data,
    }
    return response_as_json(data)


def json_error(error_string="error", code=500, **kwargs):
    data = {
        "code": code,
        "msg": error_string,
        "data": {}
    }
    data.update(kwargs)
    return response_as_json(data)


JsonResponse = json_response
JsonError = json_error

# 显示所有的搜索信息
def get_search(request):
    # def get_search():

    # total = 0  #搜索总数
    # cat=1001：书籍、cat=1002：电影、cat=1003：音乐
    i = 0
    data = []
    q = request.GET.get("q")
    cat = request.GET.get("cat") if request.GET.get("cat") else ''
    start = request.GET.get("start") if request.GET.get("start") else 0

    while True:
        # https://www.douban.com/j/search?q=%E6%97%B6%E9%97%B4%E7%AE%80%E5%8F%B2&start=0&subtype=item&cat=1002
        # url = 'https://www.douban.com/j/search?q=%E5%83%8F%E6%88%91%E8%BF%99%E6%A0%B7%E7%9A%84%E4%BA%BA&start='+str(start)+'&subtype=item&cat=1003'
        url = 'https://www.douban.com/j/search?q=' + str(q) + '&start=' + str(start) + '&subtype=item&cat=' + str(cat)
        # url = 'http://127.0.0.1:8080/try/1/5/1.txt'
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
            html = requests.get(url, headers=headers, timeout=10)
        except Exception as e:
            return HttpResponse('{"status": 0, "message": "获取失败！' + str(e) + '", "data": [], "total": -1}')
            # break
        if html.status_code == 404:
            return HttpResponse('{"status": 0, "message": "获取失败！", "data": [], "total": -1}')
        # soup = BeautifulSoup(html.text.encode("utf-8"), features='html.parser')
        # soup = soup.find(name='div', attrs={'class': 'result-list'})

        htmls = json.loads(html.text)
        total = htmls['total']
        start = int(start) + htmls['limit']
        if total == -1 or total == 0:  #
            return HttpResponse('{"status": 1, "message": "获取成功！", "data": [], "total": '+str(total)+'}')
        # print(soup['items'][0])
        for index, items in enumerate(htmls['items']):
            soup = BeautifulSoup(items.encode("utf-8"), features='html.parser')
            # print(index,"：",items)
            for item in soup.find_all(name='div', attrs={'class': 'content'}):
                reviews = {}
                try:
                    type_text = item.div.h3.span.string  # 类型：[书籍]、[电影]、[音乐]
                except:
                    type_text = ''
                    pass
                if type_text not in ['[书籍]', '[电影]', '[音乐]']:
                    continue
                matchObj = re.search(r'(.*)dou_search_(.*)\', sid: (.*), qcat(.*)', item.div.h3.a['onclick'],
                                     re.M | re.I)
                id = matchObj.group(3)  # 唯一ID
                name = item.div.h3.a.string  # 名称
                type = matchObj.group(2)  # 类型
                star = ''
                score = ''
                author = ''
                reviews_count = ''
                brief = ''
                link = ''
                if type in ['music', 'movie', 'book']:
                    link = item.div.h3.a['href']  # 跳转链接
                    if item.div.div['class'][0] == 'rating-info':
                        star = item.div.div.contents[1]['class'][0][-2:]  # 星级
                        score = item.div.div.contents[3].string  # 评分
                        size = len(item.div.div.contents)
                        if (score != '(评价人数不足)' and score != '(目前无人评价)') and size > 7:
                            reviews_count = item.div.div.contents[5].string  # 评价人数
                            author = item.div.div.contents[7].string  # 作者
                        elif size > 5:
                            author = item.div.div.contents[5].string  # 作者
                    if item.p:
                        brief = item.p.string  # 简述
                    reviews['id'] = id
                    reviews['i'] = i
                    i += 1
                    reviews['name'] = name
                    reviews['type'] = type
                    reviews['link'] = link
                    reviews['star'] = star
                    reviews['score'] = score
                    reviews['author'] = author
                    reviews['reviews_count'] = reviews_count
                    reviews['brief'] = brief
                    data.append(reviews)
        more = htmls['more']
        if not more:
            break
    # print(data)
    data = json.dumps(data)
    return JsonResponse(json.loads('{"status": 1, "message": "获取成功！", "data": ' + str(data) + '}'))
    # return HttpResponse('{"status": 1, "message": "获取成功！", "data": ' + str(data) + '}')
    # return render(request, 'index.html', context)
    # print('加载第【{}】页成功'.format(active.text))

# get_search()
