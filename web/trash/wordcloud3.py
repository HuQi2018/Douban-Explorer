# - * - coding: utf - 8 -*-
#fun: 利用jieba分词和wordcloud创建分词与词用

from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt
import jieba
# jieba.load_userdict("txt\userdict.txt")
# 添加用户词库为主词典,原词典变为非主词典
from wordcloud import WordCloud, ImageColorGenerator

# 获取当前文件路径
# __file__ 为当前文件, 在ide中运行此行会报错,可改为
# d = path.dirname('.')
d = path.dirname(__file__)

stopwords = {}
isCN = 1 #默认启用中文分词
back_coloring_path = r"./Image/lufei.jpg" # 设置背景图片路径
text_path = r'./txtdata/keyword_test.txt' #设置要分析的文本路
font_path = r'./fonts\simkai.ttf' # 为matplotlib设置中文字体路径没
stopwords_path = r'./stopword/stopword1893.txt' # 停用词词表
imgname1 = r"./Image/WordCloudDefautColors.png" # 保存的图片名字1(只按照背景图片形状)
imgname2 = r"./Image/WordCloudColorsByImg.png"# 保存的图片名字2(颜色按照背景图片颜色布局生成)

my_words_list = ['一夜爆红'] # 在结巴的词库中添加新词

back_coloring = imread(r"./Image/lufei.jpg")# 设置背景图片-----back_coloring 为3维数组

# 设置词云属性
wc = WordCloud(font_path=font_path,  # 设置字体
               background_color="white",  # 背景颜色
               max_words=2000,  # 词云显示的最大词数
               mask=back_coloring,  # 设置背景图片
               max_font_size=100,  # 字体最大值
               min_font_size=20,
               random_state=42,
               width=1000, height=860, margin=2,# 设置图片默认的大小,但是如果使用背景图片的话,
                                    # 那么保存的图片大小将会按照其大小保存,margin为词语边缘距离
               )

# 添加自己的词库分词，例如词库中没有一夜爆红这个词，我们可以添加：一夜爆红
def add_word(list):
    for items in list:
        jieba.add_word(items)

add_word(my_words_list)

text = open( text_path, encoding='utf-8').read()      #打开文本，获取内容

def jiebaclearText(text):
    mywordlist = []                                #存放最终分词结果
    seg_list = jieba.cut(text, cut_all=False)
    liststr="/ ".join(seg_list)                      #未经处理的文本分词结果列表
    f_stop = open(stopwords_path, encoding='utf-8')     #打开停用词词表
    try:
        f_stop_text = f_stop.read( )                      #获取停用词词表中的内容
    finally:
        f_stop.close( )
    f_stop_seg_list = f_stop_text.split('\n')
    for myword in liststr.split('/'):      #获取初次分词结果中的每一个词
        if not(myword.strip() in f_stop_seg_list) and len(myword.strip())>1:
            mywordlist.append(myword)
    return ''.join(mywordlist)

if isCN:   #开启中文分词
    text = jiebaclearText(text)         #获得中文分词结果

# 生成词云, 可以用generate输入全部文本(wordcloud对中文分词支持不好,建议启用中文分词),
# 也可以我们计算好词频后使用generate_from_frequencies函数
wc.generate(text)
#wc.generate_from_frequencies(txt_freq)
# txt_freq例子为[('词a', 100),('词b', 90),('词c', 80)]

image_colors = ImageColorGenerator(back_coloring)       # 从背景图片生成颜色值

plt.figure()
# 以下代码只显示--------形状与背景图片一致，颜色为默认颜色的词云
plt.imshow(wc)
plt.axis("off")
plt.show()     # 绘制词云
wc.to_file(imgname1)    # 保存图片


# 以下代码显示--------形状与背景图片一致，颜色也与背景图颜色一致的词云
image_colors = ImageColorGenerator(back_coloring)        # 从背景图片生成颜色值
plt.imshow(wc.recolor(color_func=image_colors))
plt.axis("off")
plt.show()
wc.to_file( imgname2)


# 绘制以背景图片为颜色的图片----类似于绘制背景图片
# plt.figure()
# plt.imshow(back_coloring, cmap=plt.cm.gray)
# plt.axis("off")
# plt.show()
# 保存图片