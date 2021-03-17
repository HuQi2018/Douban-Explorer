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

# 获取作品信息
def get_search(request):
    # def get_search():

    id = request.GET.get("id")
    type = request.GET.get("type")

    if not id or not type or type not in ['music', 'movie', 'book']:
        return HttpResponse('{"status": 0, "message": "获取失败！请输入正确的参数！", "data": {}}')

    url = 'https://' + str(type) + '.douban.com/subject/' + str(id) + '/'
    # https://movie.douban.com/j/subject_abstract?subject_id=34603816
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
        html = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        return HttpResponse('{"status": 0, "message": "获取失败！' + str(e) + '", "data": {}}')
        # break
    if html.status_code == 404:
        return HttpResponse('{"status": 0, "message": "获取失败，不存在有关信息！", "data": {}}')
    data = {}
    soup = BeautifulSoup(html.text.encode("utf-8"), features='html.parser')
    soup = soup.find(name='div', attrs={'id': 'wrapper'})
    # print(soup.h1.span.string)
    data['type'] = type  # 类型
    data['title'] = soup.h1.span.string  # 标题
    article = soup.find(name='div', attrs={'class': 'subjectwrap'})
    data['article'] = str(article)  # 信息
    sum = soup.find(name='div', attrs={'id': 'link-report'})
    summary = sum.find(name='span', attrs={'class': 'short'})
    if summary:
        summary = str(summary)
    else:
        summary = str(sum)
    data['summary'] = str(summary)  # 简述内容简介
    allSummary = soup.find(name='span', attrs={'class': 'all hidden'})
    data['allSummary'] = str(allSummary)  # 内容简介
    if type == 'book':
        intro = soup.find(text='作者简介')
        if intro:
            try:
                data['info'] = str(intro.parent.parent.next_sibling.next_sibling.div.div.text)  # 作者简介
            except:
                data['info'] = str(intro.parent.parent.next_sibling.next_sibling.span.div.text)  # 作者简介
                pass
        # print(data['info'])
        tag = soup.find(name='div', attrs={'id': 'db-tags-section'})
        tags = [td.a.string for td in tag.div.find_all('span')]
    else:
        tag = soup.find(name='div', attrs={'class': 'tags-body'})
        tags = [td.string for td in tag.find_all('a')]
    data['tags'] = tags #标签

    data = json.dumps(data)
    # return HttpResponse('{"status": 1, "message": "获取成功！", "data": ' + str(data) + ', "url": "' + str(url) + '"}')
    return JsonResponse(json.loads('{"status": 1, "message": "获取成功！", "data": ' + str(data) + ', "url": "' + str(url) + '"}'))
    # return render(request, 'index.html', context)
    # print('加载第【{}】页成功'.format(active.text))

# get_search()
