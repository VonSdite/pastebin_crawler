# -*- coding: utf-8 -*-
# @Author   : Sdite
# @DateTime : 2018-02-25 00:49:10

import requests
import threading
import os
import time
from bs4 import BeautifulSoup

# 这是你保存pastebin代码的路径，记得修改
save_path = 'E:/1Code/TestRepositories/pastebin_save/'

# 因为我主要获取c/c++，所以我这里加上了文件扩展名为.cpp， 如果不过滤代码的话，就将该变量赋值为空串，即 ''
file_format = '.cpp'    

base_url = 'https://pastebin.com'       # pastebin的url
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
}
session = requests.Session()


def get_code(archive, code_fliter=lambda code: True):
    '''
    获取pastebin代码的函数

    Args: 
        archive: 这是pastebin每个页面的标号，形式同'/hGsXPdqY'的字符串
        code_fliter: 一个lambda表达式，可以用来过滤得到你想要的类型代码

    Returns: 
        None
        获取到的代码会保存在你设置好的 save_path 中，以archive命名
    '''
    try:
        html = session.get(url=base_url + archive, headers=headers).text
        soup = BeautifulSoup(html, 'lxml')
        code = soup.find('textarea', attrs={
                         'id': 'paste_code', 'class': 'paste_code', 'name': 'paste_code'}).get_text()
    except:
        print('获取代码过程中出现异常')
        return

    if code_fliter(code):
        # 使用code_filter来获取你想要的代码
        with open(save_path + archive[1:] + file_format, 'w', encoding='utf-8') as f:
            f.write(code)


def monitor(code_fliter=lambda code: True):
    '''
    pastebin监控，采用轮询来检测是否有新的代码被上传

    Args: 
        code_fliter: 一个lambda表达式，可以用来过滤得到你想要的类型代码(在开线程时使用)
    '''
    while True:
        links = []          # 一个临时缓存，用于判断是否有新的代码上传

        times = 0

        try:
            html = session.get(url=base_url + '/archive', headers=headers).text
        except:
            print('网络异常')
            break

        soup = BeautifulSoup(html, 'lxml')
        tr_list = soup.find_all('tr')[1:]   # 代码链接都在tr标签中，且是从第二个tr标签开始

        try:
            for tr in tr_list:
                try:
                    a = tr.td.a                     # 代码链接在tr标签的td标签的a标签中
                    if 'href' in a.attrs:
                        link = a.attrs['href']

                        if link not in links:
                            # 判断该代码链接是否已存在
                            links.append(link)

                            # 开线程去获取代码
                            threading.Thread(target=get_code, args=(link, code_fliter)).start()
                            times += 1
                            if times <= 50:
                                # 最开始页面就有49条链接，需要sleep避免太快开线程了
                                # 后续轮询就没有那么多链接了， 所以不需要sleep了
                                time.sleep(1)  # 避免开线程太快导致cpu资源被消耗过多
                except:
                    print('获取代码链接中发生一次错误...')
        except:
            print('获取代码失败...')

if __name__ == '__main__':
    # 这里以获取c/c++代码为例
    monitor(code_fliter=lambda code: code.find('#include') != -1)
