#
# @Date        : 2020-09-02 17:51:24
# @LastEditors : anlzou
# @Github      : https://github.com/anlzou
# @LastEditTime: 2020-09-02 18:40:49
# @FilePath    : \stars-list\stars-list.py
# @Describe    :
#

import requests
from requests_html import HTMLSession

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
}

'''
    data[0]:types
    data[1]:types_url
    list_title:project name
    list_title_url:project url
    list_text:project brief introduction
'''
data = []
github_url = "https://github.com"
session = HTMLSession()

list_title = []
list_title_url = []
list_text = []


def get_title_and_text(url):
    resp = session.get(url, headers=headers)
    url = resp.html.xpath('//div[@class="BtnGroup"]/a[@rel="nofollow"]/@href')
    button = resp.html.xpath(
        '//div[@class="BtnGroup"]/a[@rel="nofollow"]/text()')

    if len(url) == 0 or (len(url) == 1 and button[0] == "Next"):
        title = resp.html.xpath(
            '//div[@class="d-inline-block mb-1"]/h3/a/@href')
        title_url = [github_url + i for i in title]
        text = resp.html.xpath('//div[@class="py-1"]/p/text()')
        text = [j.replace("\n      ", "")
                for j in [i.replace("\n        ", "") for i in text]]

        list_title.append(title)
        list_title_url.append(title_url)
        list_text.append(text)

    elif len(pages_next) == 2:
        title = resp.html.xpath(
            '//div[@class="d-inline-block mb-1"]/h3/a/@href')
        title_url = [github_url + i for i in title]
        text = resp.html.xpath('//div[@class="py-1"]/p/text()')
        text = [j.replace("\n      ", "")
                for j in [i.replace("\n        ", "") for i in text]]

        list_title.append(title)
        list_title_url.append(title_url)
        list_text.append(text)

        resp = session.get(pages_next[1], headers=headers)
        pages_next = resp.html.xpath(
            '//div[@class="BtnGroup"]/a[@rel="nofollow"]/@href')
        get_title_and_text(resp)


def get_types(username):
    stars_url = "https://github.com/" + username + "?tab=stars"
    resp = session.get(stars_url, headers=headers)

    # 获取类型
    types = resp.html.xpath('//ul[@class="filter-list"]/li/a/text()')
    types_result = [k.replace("  ", "") for k in [j.replace(
        "\n      ", "") for j in [i.replace("\n        ", "") for i in types]]]
    types_result = types_result[4:]  # 去掉多余

    # 获取类型链接
    urls = resp.html.xpath('//ul[@class="filter-list"]/li/a/@href')
    urls_result = urls[4:]  # 去掉多余

    return types_result, urls_result


def makeMarkdown():
    name = "## Stars-List"
    text = "> A curated list of my GitHub stars! Generated by [stars-list](https://github.com/anlzou/stars-list)"
    details_head_contents = "<details><summary>Contents</summary>"
    details_head_List = "<details><summary>List</summary>"
    datails_font = "</details>"

#     添加Contents
    md_text = name+"\n"+text+"\n\n"+details_head_contents+"\n\n"
    for i in range(len(data[0])):
        li = "- [" + str(data[0][i]) + "](##" + str(data[0][i]) + ")\n"
        md_text += li
    md_text += datails_font+"\n\n"

#     添加List
    md_text += details_head_List+"\n\n"
    for i in range(len(list_title)):
        li_title = "## " + str(data[0][i]) + "\n"
        li_text = ""
        for j in range(len(list_title[i])):
            li_text += "- [" + str(list_title[i][j][1:]) + \
                "](" + str(list_title_url[i][j]) + ")"
            if len(str(list_text[i][j])) != 0:
                li_text += " - "
                li_text += str(list_text[i][j]) + "\n"
        md_text += li_title
        md_text += li_text
    md_text += datails_font

    md_file = open('StarsList.md', mode='w+', encoding='utf-8')
    md_file.write(md_text)
    md_file.close()


def run(username):
    type_data = get_types(username)
    for i in type_data:
        data.append(i)

#     每个类型的页面
    for url in data[1]:
        get_title_and_text(url)

#     生成markdown文件
    makeMarkdown()
    print("finish")


if __name__ == '__main__':
    username = input("input your github username: ")
    print("wait a moment...")
    run(username)
