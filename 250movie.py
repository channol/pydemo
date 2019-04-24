#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# requests

#import sys
#import lxml
#sys.path.append('C:\Program Files\Python36\Lib')
import requests
from lxml import html

def log(*args, **kwargs):
    print(*args, **kwargs)

def movie_log(*args, **kwargs):
    with open('movie.txt', 'a', encoding='utf-8') as f:
        print(*args, file=f, **kwargs)

# object 是祖父类,是系统里的东西
# + __add__
# 在打印一个东西,实际上依次调用
# str(m)
# a.__str__()
# a.__repr__()

# object 里面的str repr 都会打印这样的东西
# 类名 和 内存地址
# <__main__.Fruits object at 0x00000000002DB3400>
# str()人类读取的输出
# repr()机器可读的输出

class Model(object):
    def __repr__(self):
        # 得到实例的类名
        class_name = self.__class__.__name__
        # self.__dict__将实例变成一个字典,字典化
        # item() 将字典变成[(key,value),(),()]
        properties = ('{} = ({})'.format(k, v) for k, v in self.__dict__.items())
        r = '\n<{}:\n {}\n'.format(class_name, '\n '.join(properties))
        return r


# (1,2,3)
# 1\n 2\n 3

class Movie(Model):
    # 初始化
    def __init__(self):
        # 排名
        self.ranking = 0
        # 封面链接
        self.cover_url = ''
        # 评分
        self.rating = 0
        # 电影名字
        self.name = ''
        # 评分人数
        self.number_of_comments = 0


m = Model()
print(m)


def urls_from_douban():
    urls = []
    url = 'https://movie.douban.com/top250?start={}&filter='
    # index 0 25 50 75 100 ...
    for index in range(0, 250, 25):
        u = url.format(index)
        urls.append(u)
    return urls


# print(urls_from_douban())

def movies_from_url(urls):
    all_movie = []
    for u in urls:
        # r 是requests 对象,html里面的东西
        # r 是返回的数据
        r = requests.get(u)
        # page 是bytes 类型
        # 网络上传输数据的都是bytes类型
        page = r.content
        # root 会是一个树形结构
        root = html.fromstring(page)
        # 返回一个列表,里面每个元素都是一个element对象
        movies_divs = root.xpath('//div[@class="item"')
        movies = [movies_from_div(div) for div in movies_divs]
        # extend 扩展列表
        all_movie.extend(movies)
    return all_movie

#将信息归类
def movies_from_div(div):
    #[0] 结果即使只有一个,它也是一个列表,里面一个元素
    movie = Movie()
    movie.ranking = div.xpath('.//div[@class="pic"]/em')[0].text
    movie.cover_url = div.xpath('.//div[@class="pic"]/a/img/@stc')[0]
    names = div.xpath('.//span[@class="title"]/text()')
    movie.name = ''.join(names)
    movie.rating = div.xpath('.//span[@class="rating_num"]')[0].text
    movie.number_of_comments = div.xpath('.//div[@class="star"]/span')[-1].text[-3]
    log('movie', movie)
    return movie

def download_covers(m):
    for m in movies:
        image_url = m.cover_url
        r = requests.get(image_url)
        path = 'covers/' + m.name.split('/')[0] + '.jpg'
        with open(path, 'wb') as f:
            f.write(r.content)
def main():
    urls = urls_from_douban()
    movies = movies_from_url(urls)

    movie_log(movies)
    download_covers(movies)

if __name__ == '__main__':
    main()