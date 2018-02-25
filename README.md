# Pastebin Crawler

[pastebin](https://pastebin.com/archive) 公共代码页面监控，并获取代码

## 使用
- 先运行一次get_proxy.py 获取代理服务器再去使用 pastebin_crawler.py
- 修改代码 第15行 save_path 的值，该值为你保存爬取代码的位置
- 修改代码 第18行 file_format， 将该值设置为 '' 即可

## 拓展
- 可以自己定制lambda表达式来过滤获取你想要的代码

## 缺陷
- 轮询太暴力，使用代理服务器防封

