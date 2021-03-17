import re
import jieba
import gensim
from gensim import corpora, models
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from django.shortcuts import HttpResponse
from utils.mongodb_model import CollectMovieDB,CollectMovieCommentsDB,CollectMovieReviewsDB,\
    CollectMusicDB,CollectMusicCommentsDB,CollectMusicReviewsDB\
    ,CollectBookDB,CollectBookCommentsDB,CollectBookReviewsDB
from io import BytesIO
import base64
import redis
from utils.redis_pool import POOL


def SentenceSegmentation(text):
    """
    给定一段文本，将文本分割成若干句子
    这里简单使用句号、问号、感叹号及换行符进行分割
    """
    sentences = re.split(u'[\n。？！]', text)
    sentences = [sent for sent in sentences if len(sent) > 0]  # 去除只包含\n或空白符的句子
    return sentences

def LoadStopWords(stopfile):
    """
    载入停用词文件
    """
    stop_words = set()  # 保存停用词集合
    fin = open(stopfile, 'r', encoding='utf-8', errors='ignore')
    for word in fin.readlines():
       stop_words.add(word.strip())
    fin.close()
    return stop_words

def WordSegmentation(text, stop_words):
    """
            利用jieba分词工具进行词分割
            同时过滤掉文本中的停用词
            """
    jieba_list = jieba.cut(text)
    word_list = []
    for word in jieba_list:
        if word not in stop_words:
            word_list.append(word)
    return word_list

def TopicModeling(n,id,typ):
    """
            将读入的文本利用话题模型LDA进行处理
            得出每个话题及每个话题中对应的概率最高的词
            """
    if not n:
        n=1
    document = []
    texts = []
    stop_words = LoadStopWords('file/stopwords.txt')

    if typ == 'movie':
        title = CollectMovieDB.objects.aggregate([
                                            {"$match":{'movie_id':int(id)}},
                                            {'$sample': {'size': 1}},
                                            {"$project": {"title": 1}},
                                            {"$sort": {"movie_id": -1}}])
        result1 = CollectMovieCommentsDB.objects.aggregate([
                                            {"$match":{'comments_movid_id':int(id)}},
                                            # {'$sample': {'size': int(n)}},
                                            {"$project": {"comments_content": 1}},
                                            {"$sort": {"comments_movid_id": -1}}])
        result2 = CollectMovieReviewsDB.objects.aggregate([
                                            {"$match":{'reviews_movid_id':int(id)}},
                                            {'$sample': {'size': int(n)}},
                                            {"$project": {"reviews_content": 1}},
                                            {"$sort": {"reviews_movid_id": -1}}])
        for txt in result1:
            tt = jieba.cut(txt['comments_content'].strip())
            for item in tt:
                if (not item in stop_words) and (not len(item.strip()) == 0):
                    document.append(item)
            texts.append(document)
        for txt in result2:
            tt = jieba.cut(txt['reviews_content'].strip())
            for item in tt:
                if (not item in stop_words) and (not len(item.strip()) == 0):
                    document.append(item)
            texts.append(document)
    elif typ == 'music':
        title = CollectMusicDB.objects.aggregate([
                                            {"$match":{'music_id':int(id)}},
                                            {'$sample': {'size': 1}},
                                            {"$project": {"title": 1}},
                                            {"$sort": {"music_id": -1}}])
        result1 = CollectMusicCommentsDB.objects.aggregate([
                                            {"$match":{'comments_music_id':int(id)}},
                                            # {'$sample': {'size': int(n)}},
                                            {"$project": {"comments_content": 1}},
                                            {"$sort": {"comments_music_id": -1}}])
        result2 = CollectMusicReviewsDB.objects.aggregate([
                                            {"$match":{'reviews_music_id':int(id)}},
                                            {'$sample': {'size': int(n)}},
                                            {"$project": {"reviews_content": 1}},
                                            {"$sort": {"reviews_music_id": -1}}])
        for txt in result1:
            tt = jieba.cut(txt['comments_content'].strip())
            for item in tt:
                if (not item in stop_words) and (not len(item.strip()) == 0):
                    document.append(item)
            texts.append(document)
        for txt in result2:
            tt = jieba.cut(txt['reviews_content'].strip())
            for item in tt:
                if (not item in stop_words) and (not len(item.strip()) == 0):
                    document.append(item)
            texts.append(document)
    elif typ == 'book':
        title = CollectBookDB.objects.aggregate([
                                            {"$match":{'book_id':int(id)}},
                                            {'$sample': {'size': 1}},
                                            {"$project": {"title": 1}},
                                            {"$sort": {"book_id": -1}}])
        result1 = CollectBookCommentsDB.objects.aggregate([
                                            {"$match":{'comments_book_id':int(id)}},
                                            # {'$sample': {'size': int(n)}},
                                            {"$project": {"comments_content": 1}},
                                            {"$sort": {"comments_book_id": -1}}])
        result2 = CollectBookReviewsDB.objects.aggregate([
                                            {"$match":{'reviews_book_id':int(id)}},
                                            {'$sample': {'size': int(n)}},
                                            {"$project": {"reviews_content": 1}},
                                            {"$sort": {"reviews_book_id": -1}}])
        for txt in result1:
            tt = jieba.cut(txt['comments_content'].strip())
            for item in tt:
                if (not item in stop_words) and (not len(item.strip()) == 0):
                    document.append(item)
            texts.append(document)
        for txt in result2:
            tt = jieba.cut(txt['reviews_content'].strip())
            for item in tt:
                if (not item in stop_words) and (not len(item.strip()) == 0):
                    document.append(item)
            texts.append(document)
    else:
        return "该评论不存在，或参数有误！"

    if not title:
        return "该评论不存在，或参数有误！"

    # 利用gensim将载入的文本文件构造成词-词频(term-frequency)矩阵
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    # 将词题（term-frequency）矩阵作为输入，利用LDA进行话题分析
    lda = gensim.models.ldamodel.LdaModel(corpus, num_topics=1, id2word=dictionary, passes=20)
    topics = []
    for tid in range(n):
        wordDict = {}
        # 选出每个话题中具有代表性的前15个词
        topicterms = lda.show_topic(tid, topn=30)
        for item in topicterms:
            (w, p) = item
            # 由于LDA保留的每个词属于该话题的概率值p
            # 该概率值本身较小，这里为了方便可视化，将概率p进一步放大
            wordDict[w] = (p * 100) ** 2
        topics.append(wordDict)
    return topics

def GenWordCloud(wordDict):
    """
            利用词云工具Word Cloud为每个话题生成词云
            """
    # 由于原始WordCloud不支持中文，这里需要载入中文字体文件simsun.ttc
    cloud = WordCloud(font_path='file/simkai.ttf', background_color='white', max_words=300, max_font_size=40,
                      random_state=42)
    wordcloud = cloud.generate_from_frequencies(wordDict)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    # plt.show()
    sio = BytesIO()
    plt.savefig(sio, format='png')
    data = base64.encodebytes(sio.getvalue()).decode()
    plt.close()
    return data

def main(request):
    id = request.GET.get("id")  if request.GET.get("id") else ''
    typ = request.GET.get("type") if request.GET.get("type") else ''
    n = request.GET.get("n") if request.GET.get("n") else ''
    nochache = request.GET.get("nochache")
    conn = redis.Redis(connection_pool=POOL)
    redis_key = 'topic' + typ + '_' + id + n
    data = conn.get(redis_key)

    if not data or nochache == '1':
        # id = 1292052
        # numOfTopics = 1 #设置话题数目为3
        topics = TopicModeling(n, id, typ)
        if topics == 0 or not id or not typ:
            return HttpResponse("")
        print(topics)
        data = GenWordCloud(topics[0])
        # GenWordCloud(topics[0])

        print("redis存储")
        conn.set(redis_key, data)
        conn.expire(redis_key, 60 * 60 * 24)
    else:
        data = str(data).replace('\\n', '')[2:][:-1]
    return HttpResponse(
        '<img src="data:image/png;base64,' + data + '" style="height: 400px;width: 450px;border: 2px solid;">')
    # for i in range(numOfTopics):

# main()