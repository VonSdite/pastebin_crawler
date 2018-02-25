import requests
import pickle
from bs4 import BeautifulSoup

# 得到的proxies形如 [('http', '221.229.18.97:3128')]
# 是一个存放元组的列表

url = 'http://www.ip3366.net/?stype=1&page={page}'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
}
session = requests.Session()

proxies = list()
for page in range(1, 11):
    print('获取第{page}页'.format(page=page))

    res = session.get(url=url.format(page=page), headers=headers)
    res.encoding = 'gb2312'
    soup = BeautifulSoup(res.text, 'lxml')
    tr_set = soup.find('tbody').find_all('tr')

    for tr in tr_set:
        td_set = tr.find_all('td')
        resonse_time = td_set[6].get_text()
        if int(resonse_time[:resonse_time.find('秒')]) < 3:
            continue
        proxies.append((td_set[3].get_text().lower(), td_set[0].get_text() + ':' + td_set[1].get_text()))

with open('proxies.pickle', 'wb') as f:
    pickle.dump(proxies, f)
