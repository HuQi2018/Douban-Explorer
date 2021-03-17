import os
import pygame

chinese_dir = 'chinese'
if not os.path.exists(chinese_dir):
    os.mkdir(chinese_dir)

pygame.init()
# start,end = (0x4E00, 0x9FA5) # 汉字编码范围
# start,end = (0x795e, 0x795f) # 汉字编码范围
# for codepoint in range(int(start), int(end)):
word = chr(0x795e)
font = pygame.font.Font("fzxkjw_0.ttf", 500)
# 当前目录下要有微软雅黑的字体文件msyh.ttc,或者去c:\Windows\Fonts目录下找
# 64是生成汉字的字体大小
rtext = font.render(word, True, (0, 0, 0), (255, 255, 255))
pygame.image.save(rtext, os.path.join(chinese_dir, word + ".png"))
