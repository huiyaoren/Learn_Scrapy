## 目录

* 前言

* 安装
    * 环境
    * Windows 安装
    * Debian / Ubuntu / Deepin 安装
* 基本使用
    * 新建项目
    * 初始化scrapy项目
    * 添加一个基本爬虫
* 进阶使用
    * settings
        * 多线程
    * anti-anti-spider
        * IP proxy
    * url filter
        * bloom filter
        * hyperloglog
* 细节分析
    * Scrapy类
        * 常用属性与方法
        * Request与Response对象
    * Selector
        * XPath选择器
        * CSS选择器
    * Item类
* 总结
* 相关资料
    * 官方文档

## 前言
在本篇中，我假定您已经熟悉并安装了 Python3。 如若不然，请参考 [Python 入门指南](http://www.pythondoc.com/pythontutorial3/index.html) 。

### 关于 Scrapy

> Scrapy是一个为了爬取网站数据，提取结构性数据而编写的应用框架。 可以应用在包括数据挖掘，信息处理或存储历史数据等一系列的程序中。

> 其最初是为了 网络抓取 所设计的， 也可以应用在获取API所返回的数据(例如 Amazon Associates Web Services ) 或者通用的网络爬虫。

### 分布式爬虫架构



## 安装

### 环境
  * Redis 3.2.5
  * Python 3.5.2
  * Scrapy 1.3.3
  * scrapy-redis 0.6.8

### Debian / Ubuntu / Deepin 安装
*安装前你可能需要把 Python3 设置为默认的 Python 解释器，或者使用 virtualenv 搭建一个 Python 的虚拟环境，此处不再赘述。*

#### 安装 Redis
```bash
sudo apt-get install redis-server
```
#### 安装 Scrapy
```bash
sudo apt-get install build-essential libssl-dev libffi-dev python-dev
sudo apt install python3-pip
sudo pip install scrapy scrapy-reids
```
#### 安装 scrapy-redis
```bash
sudo pip install scrapy-reids
```



### Windows 安装

由于目前 Python 实现的一部分第三方模块在 Windows 下并没有可用的安装包，个人并不推荐以 Windows 作为开发环境。

如果你非要这么做，你可能会遇到以下异常：

* ImportError: DLL load failed: %1 不是有效的 Win32 应用程序
    * 这是由于你安装了 64 位的 Python，但却意外安装了 32 位的模块
* Failed building wheel for cryptography
    * 你需要升级你的 pip 并重新安装 cryptography 模块
* ERROR: 'xslt-config' is not recognized as an internal or external command,
operable program or batch file.
    * 你需要从 lxml 的官网下载该模块编译好的 exe 安装包，并用 easy_install 手动进行安装

如果你还没有放弃，以下内容可能会帮到你：
* [Windows上Python3.5安装Scrapy(lxml)](http://www.cnblogs.com/silverbullet11/p/4966608.html)
* [Python爬虫进阶三之Scrapy框架安装配置](http://cuiqingcai.com/912.html)
* [Microsoft Visual C++ Compiler for Python 2.7](https://www.microsoft.com/en-us/download/confirmation.aspx?id=44266)
* [easy_install lxml on Python 2.7 on Windows](http://stackoverflow.com/questions/9453986/easy-install-lxml-on-python-2-7-on-windows)

## 基本使用

### 初始化项目
* 命令行下初始化 Scrapy 项目
```bash
scrapy startproject spider_ebay
```
* 执行后将会生成以下目录结构
```
└── spider_ebay
  ├── spider_ebay
  │   ├── __init__.py
  │   ├── items.py
  │   ├── middlewares.py
  │   ├── pipelines.py
  │   ├── settings.py
  │   └── spiders
  │       └── __init__.py
  └── scrapy.cfg
```

### 创建 Master 爬虫
* 创建文件 ```spider_ebay/spider_ebay/spiders/master.py```
* 代码如下：

```python
# coding: utf-8
from scrapy import Item, Field
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractors import LinkExtractor
from redis import Redis
from time import time
from urllib.parse import urlparse, parse_qs, urlencode


class MasterSpider(RedisCrawlSpider):
    name = 'ebay_master'
    redis_key = 'ebay:start_urls'

    ebay_main_lx = LinkExtractor(allow=(r'http://www.ebay.com/sch/allcategories/all-categories', ))
    ebay_category2_lx = LinkExtractor(allow=(r'http://www.ebay.com/sch/[^\s]*/\d+/i.html',
                                             r'http://www.ebay.com/sch/[^\s]*/\d+/i.html?_ipg=\d+&_pgn=\d+',
                                             r'http://www.ebay.com/sch/[^\s]*/\d+/i.html?_pgn=\d+&_ipg=\d+',))

    rules = (
        Rule(ebay_category2_lx, callback='parse_category2', follow=False),
        Rule(ebay_main_lx, callback='parse_main', follow=False),
    )

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        # self.allowed_domains = filter(None, domain.split(','))
        super(MasterSpider, self).__init__(*args, **kwargs)

    def parse_main(self, response):
        pass
        data = response.xpath("//div[@class='gcma']/ul/li/a[@class='ch']")
        for d in data:
            try:
                item = LinkItem()
                item['name'] = d.xpath("text()").extract_first()
                item['link'] = d.xpath("@href").extract_first()
                yield self.make_requests_from_url(item['link'] + r"?_fsrp=1&_pppn=r1&scp=ce2")
            except:
                pass

    def parse_category2(self, response):
        data = response.xpath("//ul[@id='ListViewInner']/li/h3[@class='lvtitle']/a[@class='vip']")
        redis = Redis()
        for d in data:
            try:
                self._filter_url(redis, d.xpath("@href").extract_first())
            except:
                pass
        try:
            next_page = response.xpath("//a[@class='gspr next']/@href").extract_first()
        except:
            pass
        else:
            new_url = self._build_url(response.url)
            redis.lpush("test:new_url", new_url)

    def _filter_url(self, redis, url, key="ebay_slave:start_urls"):
        is_new_url = bool(redis.pfadd(key + "_filter", url))
        if is_new_url:
            redis.lpush(key, url)

    def _build_url(self, url):
        parse = urlparse(url)
        query = parse_qs(parse.query)
        base = parse.scheme + '://' + parse.netloc + parse.path

        if '_ipg' not in query.keys() or '_pgn' not in query.keys() or '_skc' in query.keys():
            new_url = base + "?" + urlencode({"_ipg": "200", "_pgn": "1"})
        else:
            new_url = base + "?" + urlencode({"_ipg": query['_ipg'][0], "_pgn": int(query['_pgn'][0]) + 1})
        return new_url
```

### 创建 Slave 爬虫
* 创建文件 ```spider_ebay/spider_ebay/spiders/master.py```
* 代码如下：

```python
# coding: utf-8
from scrapy import Item, Field
from scrapy_redis.spiders import RedisSpider

class SlaveSpider(RedisSpider):
    name = "ebay_slave"
    redis_key = "ebay_slave:start_urls"

    def parse(self, response):
        item = ProductItem()
        item["price"] = response.xpath("//span[contains(@id,'prcIsum')]/text()").extract_first()
        item["item_id"] = response.xpath("//div[@id='descItemNumber']/text()").extract_first()
        item["seller_name"] = response.xpath("//span[@class='mbg-nw']/text()").extract_first()
        item["sold"] = response.xpath("//span[@class='vi-qtyS vi-bboxrev-dsplblk vi-qty-vert-algn vi-qty-pur-lnk']/a/text()").extract_first()
        item["cat_1"] = response.xpath("//li[@class='bc-w'][1]/a/span/text()").extract_first()
        item["cat_2"] = response.xpath("//li[@class='bc-w'][2]/a/span/text()").extract_first()
        item["cat_3"] = response.xpath("//li[@class='bc-w'][3]/a/span/text()").extract_first()
        item["cat_4"] = response.xpath("//li[@class='bc-w'][4]/a/span/text()").extract_first()
        yield item
```

## 进阶使用

## 细节分析

## 相关资料