# -*- coding: utf-8 -*-

from urllib import request
import re
import datetime
import os


# 请求
def request_url(url, type, path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',

        'Cookie': os.environ['COOKIE']
    }

    # 请求对象 + 响应对象 + 提取内容
    req = request.Request(url=url, headers=headers)
    res = request.urlopen(req)
    html = res.read().decode('utf-8')

    # 解析html
    parse_html(html, type, path)


# 解析html
def parse_html(html, type, path):
    # 正则表达式
    regexp = None
    if type == "Summary":
        regexp = '<td class="td-01 ranktop ranktop\d+">(\d+)?<\/td>\s*<td class=\"td-02\">\s*<a href="(\/weibo\?q=[^"]+)".*?>(.+)<\/a>\s*<span>.* (\d+)<\/span>'
    elif type = "Entertainment":
        regexp = '<td class="td-01 ranktop">(\d+)?<\/td>\s*<td class=\"td-02\">\s*<a href="(\/weibo\?q=[^"]+)".*?>(.+)<\/a>\s*<span>\w*\s*(\d+)<\/span>'

    # 生成正则表达式对象
    pattern = re.compile(regexp, flags=0)

    # r_list:[(rank, url, title, heat), ...] 列表元组
    r_list = pattern.findall(html)

    # 保存markdown文件
    save_md(r_list, type, path)


# 保存markdown文件
def save_md(r_list, type, path):
    timeStr = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    with open(path + "WeiboHotSearch" + type + timeStr + '.md', 'w', encoding='utf-8') as f:
        if type == "Summary":
            f.write(timeStr + " 微博热搜榜\n\n")
        elif type == "Entertainment":
            f.write(timeStr + " 微博文娱热搜榜\n\n")
        for r_info in r_list:
            rank = r_info[0]
            url = 'https://s.weibo.com' + r_info[1]
            title = r_info[2]
            heat = r_info[3]

            row = rank + '. ' + '[' + title + ']' + '(' + url + ')' + '  **' + heat + '**\n'
            f.write(row)


if __name__ == '__main__':
    urlList = [
        {
            "name": "Summary",
            "url": "https://s.weibo.com/top/summary"
        },
        {
            "name": "Entertainment",
            "url": "https://s.weibo.com/top/summary?cate=entrank"
        }
    ]

    # 指定路径下按日期分开保存
    mainPath = r'./data/weiboHotSearch/' + datetime.datetime.now().strftime("%Y-%m-%d") + '/'
    for url in urlList:
        path = mainPath + url.get("name") + "/"
        if not os.path.exists(path):
            os.makedirs(path)
        request_url(url.get("url"), url.get("name"), path)
