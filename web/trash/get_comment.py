from bs4 import BeautifulSoup
import requests
import re
import time
from utils.mongodb_model import CollectReivewDB
import ast


def StartoSentiment(star):
    '''
    将评分转换为情感标签，简单起见
    我们将大于或等于三星的评论当做正面评论
    小于三星的评论当做负面评论
    '''
    score = int(star[-2])
    if score >= 3:
        return 1
    # elif score < 3:
    #     return -1
    else:
        return 0


def CollectReivew(id, n, type):
    result = CollectReivewDB.objects.filter(num=id)

    # 若果存在记录，则不再进行爬取，直接return
    if (result and result[0].type == type):
        # print(result[0].num)
        return (ast.literal_eval(result[0].comment), ast.literal_eval(result[0].star))

    # 初始url，加勒比海盗5的链接
    url = 'https://' + type + '.douban.com/subject/' + id + '/'
    if type == 'movie':
        i = 0
    else:
        i = 1
    '''
    收集给定电影url的前n条评论
    '''
    reviews = []
    sentiment = []
    urlnumber = 1
    while urlnumber < n:
        url = url + 'comments/new?start=' + str(urlnumber) + '&limit=20&sort=new_score'
        print('要收集的电影评论网页为：' + url)

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
            html = requests.get(url, headers=headers, timeout=10)
        except Exception as e:
            break
        if html.status_code == 404 or html.status_code == 301:
            print(html.status_code)
            return ([], [])
        soup = BeautifulSoup(html.text.encode("utf-8"), features='html.parser')
        htm_type = soup.find(name='a', attrs={'class': re.compile(r'nav-login')})
        matchObj = re.search(r'(.*)source=(.*)', htm_type['href'], re.M | re.I)

        if matchObj.group(2) != type  :
            return ([], [])

        # print(soup)
        # 通过正则表达式匹配评论和评分
        for item in soup.find_all(name='span', attrs={'class': re.compile(r'^allstar')}):
            sentiment.append(StartoSentiment(item['class'][i]))

        # for item in soup.find_all(name='p', attrs={'class': ''}):
        for item in soup.find_all(name='span', attrs={'class': 'short'}):
            # if str(item).find('class="short"') < 0:
            r = str(item.string).strip()
            reviews.append(r)

        urlnumber = urlnumber + 22
        time.sleep(3)

    # 存储到MongoDB
    CollectReivewDB.objects.create(num=id, type=str(type), comment=str(reviews), star=str(sentiment))

    # with codecs.open(outfile, 'w', 'utf-8') as output:
    #     for i in range(len(sentiment)):
    #         output.write(reviews[i] + '\t' + str(sentiment[i]) + '\n')
    # print(reviews,sentiment)
    return (list(reviews), list(sentiment))

    # 定义一个方法来写入mongodb数据库
    # def mongodb_write(self):
    #     data = self.movie_dataframe()
    #     data_columns = list(data.columns)
    #     # 首先连接数据库
    #     client = MongoClient(host="127.0.0.1", port=27017)
    #     # 连接数据库中的某个集合,这里如果原本没有这个数据库或者是集合，就会自动创建
    #     collection = client['test_python']['movie_data']
    #     i = 0
    #     for j in list(data.values):
    #         l = list(j)
    #         data_list = {"_id":i,data_columns[0]: l[0], data_columns[1]: l[1], data_columns[2]: l[2], data_columns[3]: l[3],
    #                      data_columns[4]: l[4], data_columns[5]: l[5], data_columns[6]: l[6],data_columns[7]:l[7]}
    #         collection.insert_one(data_list)
    #         i +=1
    #     print("写入成功")
