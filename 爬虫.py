from re import sub
from os import getenv
from jieba import cut
from requests import get
from bs4.element import Tag
from bs4 import BeautifulSoup as Bs
from matplotlib import pyplot as plt
from wordcloud import WordCloud as Wc
from urllib.parse import unquote as uq

agents = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 '
    'OPR/26.0.1656.60',
    'Opera/8.0 (Windows NT 5.1; U; en)',
    'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 '
    'Safari/534.16',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 '
    'Safari/536.11',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 '
    'LBBROWSER',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X '
    'MetaSr 1.0',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X '
    'MetaSr 1.0) ',
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; "
    ".NET CLR 3.0.04506)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 "
    "Safari/535.20"]


def search():
    while True:
        while True:  # 循环直到输入了正确的选项
            type_ = input("读书（b）or 影视（m）or 随便（c）：")
            if type_ != "b" and type_ != "m" and type_ != "c":
                print("输入错误\a")
                continue
            else:
                break
        key_word = input("想要搜索些什么？：")

        header = {"user-agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)"}
        if type_ == "b":
            s_page = get("https://www.douban.com/search?cat=1001&q=%s" % uq(key_word), headers=header)
        elif type_ == "m":
            s_page = get("https://www.douban.com/search?cat=1002&q=%s" % uq(key_word), headers=header)
        else:
            s_page = get("https://www.douban.com/search?q=%s" % uq(key_word), headers=header)

        s_page.encoding = s_page.apparent_encoding
        s_page = Bs(s_page.text, "html5lib")

        c_list = s_page.findAll("div", class_="content")
        if not c_list:
            print("未搜索到结果")
            continue
        else:
            n = 0
            links = []
            for t in c_list:  # type: Tag
                n += 1
                try:
                    if t.div.h3.span.string == "[电影]" or t.div.h3.span.string == "[书籍]":
                        print("=+" * 20)
                        print(str(n) + "、" + t.div.h3.a.string, end="")
                        if type_ == "c":
                            print(t.div.h3.span.string)

                        text = sub(r"[\n ]+", " ", t.div.div.text)
                        print(text)
                        links.append(t.find("a").attrs["href"])
                except:
                    continue

            if len(links) == 0:
                print("未搜索到结果")
                continue
        break

    while True:
        try:
            choose = int(input("选择一个选项，输入这个选项的序号："))

            scope = len(links)
            if 1 <= choose <= scope:
                return links[choose - 1]
            else:
                raise ValueError

        except ValueError:
            print("输入错误")
            continue


def spider(url: str):
    global agents

    header = {"user-agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)"}
    print("正在解析 URL...")
    url = get(url, headers=header).url  # 使用浏览器浏览参数 url 时出现了 302 重定向，获取重定向后的地址

    while True:
        print("选择爬取评论的类型")
        type_ = input("好（h） or 一般（m） or 差（l） or 全部（a）：")
        if type_ != "h" and type_ != "m" and type_ != "l" and type_ != "a":
            print("选择错误")
            continue
        else:
            if type_ != "a":
                url += "comments?percent_type=%s&" % type_
            else:
                url += "comments?"
            break

    print("开始爬取评论...")
    words = ""
    name = ""
    for i in range(20):
        crawl_url = url + "start=" + str(i * 20)
        page = get(crawl_url, headers={"user-agent": agents[i]})
        page.encoding = "utf-8"
        page = Bs(page.text, "html5lib")
        comments = page.findAll("span", class_="short")
        for t in comments:  # type: Tag
            words += t.string

        if name == "":
            name = page.find("title").string.strip()

    print("开始写入文件...")
    with open(f"{name}.txt", "w", encoding="utf-8") as file_obj:
        file_obj.write(words)

    print("开始分词...")
    words = " ".join(cut(words))

    print("开始生成词云...")
    sys_drive = getenv("SystemDrive")
    cloud = Wc(background_color="white", width=2000, height=2000,
               font_path=f"{sys_drive}/Windows/Fonts/STZHONGS.TTF")  # 字体文件路径可能需要修改
    cloud.generate(words)
    cloud.to_file(f"{name}.webp")

    plt.imshow(cloud)
    plt.axis("off")
    print("完成！")
    plt.show()


if __name__ == "__main__":
    while True:
        link = search()
        spider(link)
