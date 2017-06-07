# 基于 Scrapy-redis 的分布式爬虫设计

## 目录

* 安装
  * 环境
  * Windows 安装
  * Debian / Ubuntu / Deepin 安装
* 基本使用
    * 新建项目
    * 初始化scrapy项目
    * 添加一个基本爬虫
* 进阶使用
    * 多线程
    * anti-anti-spider
    * IP proxy
    * url 去重
        * bloom filter
        * hyperloglog
* Scrapy 细节分析
    * Scrapy类
        * 常用属性与方法
        * Request与Response对象
    * Selector
        * XPath选择器
        * CSS选择器
    * Item类
* 相关资料
    * 官方文档

## 安装
