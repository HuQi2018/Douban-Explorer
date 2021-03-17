from io import BytesIO
import base64
from snownlp import SnowNLP
from matplotlib import pyplot as plt
from django.shortcuts import render
from trash.get_comment import CollectReivew

'''
豆瓣电影评论的情感分析
'''
def img(id,type):
    # print(type)
    # 保存评论文件
    # outfile = 'review.txt'
    (reviews, sentiment) = CollectReivew(id, 10, '' ,type)
    print(reviews,'：' , sentiment)
    numOfRevs = len(sentiment)

    if numOfRevs == 0 :
        return '0'

    positive = 0.0
    negative = 0.0
    accuracy = 0.0
    # 利用snownlp逐条分析每个评论的情感
    for i in range(numOfRevs):
        sent = SnowNLP(reviews[i])
        predict = sent.sentiments
        if predict >= 0.5:
            positive += 1
            if sentiment[i] == 1:
                accuracy += 1
        else:
            negative += 1
            if sentiment[i] == 0:
                accuracy += 1

    # 绘制饼状图
    # 定义饼状图的标签
    labels = ['Positive Reviews', 'Negetive Reviews']
    # 每个标签占的百分比
    ratio = [positive / numOfRevs, negative / numOfRevs]
    print(ratio)
    colors = ['red', 'yellowgreen']
    # PlotPie(ratio, labels, colors)

    plt.figure(figsize=(6, 8))
    explode = (0.05, 0)

    patches, l_text, p_text = plt.pie(ratio, explode=explode, labels=labels, colors=colors,
                                      labeldistance=1.1, autopct='%3.1f%%', shadow=False,
                                      startangle=90, pctdistance=0.6)

    # 画饼状图
    plt.axis('equal')
    plt.legend()
    # plt.show()
    # 转成图片的步骤
    sio = BytesIO()
    plt.savefig(sio, format='png')
    data = base64.encodebytes(sio.getvalue()).decode()
    return data
    plt.close()

def get(request):

    context = {}
    context['title'] = 'Hello World!'
    context['message'] = 'This is message'
    context['condition2'] = True
    id = request.GET.get("id")
    type = request.GET.get("type")
    if id and type in ['movie','book','music']:
        context['img'] = img(id,type)
    return render(request, 'index.html', context)

