import json
import time
import requests
from bs4 import BeautifulSoup
import re
import os
from tqdm import tqdm

#文件命名去除非法字符
def remove_illegal_characters(filename):
    # 匹配非法字符
    illegal_chars = r'[\\/:*?"<>|]'
    # 将非法字符替换为空
    new_filename = re.sub(illegal_chars, '', filename)
    return new_filename

#文件命名获取
def get_title_by_index(index_num):
    url = 'http://www.jko0.com/play/' + index_num + '-1-' + str(1) + '.html'
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')
    title1 = soup.select_one('head title')
    title = remove_illegal_characters(str(title1))
    return title


#"https:\\\/\\\/top.1080pzy.co\\\/202312\\\/2\d\\\/(.*?)\\\/video\\/index.m3u8"

hash_video = re.compile('"url":"https:\\\/\\\/top.1080pzy.co\\\/\d\d\d\d\d\d\\\/\d\d\\\/(.*?)\\\/video',re.I|re.S)
hash_url1 = re.compile('"url":"https:\\\/\\\/top.1080pzy.co\\\/(.*?)\\\/\d\d\\\/',re.I|re.S)
hash_url2 = re.compile('"url":"https:\\\/\\\/top.1080pzy.co\\\/\d\d\d\d\d\d\\\/(.*?)\\\/',re.I|re.S)

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0'
}
hash_video_res = []
hash_url_res2 = []
hash_url_res1 = []
index_num = input('输入url后面的数字>>>> ')
video_num = int(input('输入电视剧剧集>>>> ')) + 1

def get_elements_url(hash_url_res1:list ,hash_url_res2:list ,hash_video_res:list ,index_num:str ,video_num:int):
    for i in range(1, video_num):
        url = 'http://www.jko0.com/play/' + index_num + '-1-' + str(i) + '.html'
        html = requests.get(url,headers=headers)

        hash_video_res.append(hash_video.findall(html.text))
        hash_url_res2.append(hash_url2.findall(html.text))
        hash_url_res1.append(hash_url1.findall(html.text))

#爬虫获取需要拼接url的基本元素，根据hash和服务器对应视频的文件名

get_elements_url(hash_url_res1,hash_url_res2,hash_video_res,index_num,video_num)

get_title_by_index(index_num)


for i in range(1,video_num):
    index = i-1
    url = 'https://top.1080pzy.co/' + str(hash_url_res1[index]).replace('[','').replace(']','').replace('\'','').replace('\'','') + '/' + str(hash_url_res2[index]).replace('[','').replace(']','').replace('\'','').replace('\'','') + '/' + str(hash_video_res[index]).replace('[','').replace(']','').replace('\'','').replace('\'','') + '/video/1000k_0X720_64k_25/hls/index.m3u8'
    print(url)
    with open('E:\\video\\video' + str(hash_video_res[index]) + '.txt','w',encoding='utf8') as f_write_down:
        f_write_down.write(requests.get(url,headers=headers).text)

    with open('E:\\video\\video_clear' + str(hash_video_res[index]) + '.txt','w',encoding='utf8') as f_write_down_clear:
        with open('E:\\video\\video' + str(hash_video_res[index]) + '.txt','r',encoding='utf8') as f_read_down:
            lines = f_read_down.readlines()
            for line in lines:
                if line.startswith('#'):
                    continue
                else:
                    f_write_down_clear.write(line)
    print('下载格式存储完毕')

for i in range(1, video_num):
    with open('E:\\video\\video_clear' + str(hash_video_res[index]) + '.txt', 'r',encoding='utf8') as f_read_down_clear:
        lines1 = f_read_down_clear.readlines()
        total_lines = len(lines1)  # 获取总行数，用于进度条
        with open('E:\\video\\video_' + str(title1) + ' 第 ' + str(i) + '集' + '.mp4', 'ab') as f_write_down_video:
            for line1 in tqdm(lines1, total=total_lines, desc="Downloading video segment", ncols=100):
                url = line1
                f_write_down_video.write(requests.get(url,headers=headers).content)
                time.sleep(0.5)
    print("下载" + str(title1) + ' 第 ' + str(i) + '集' + '成功')













