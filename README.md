# spider

> 这是一些爬虫项目，欢迎大家clone学习，交流分享。
>
> * common：一些从0开始写，没有用框架和其他工具的项目
> * selenium：一些基于selenium工具进行编写的爬虫项目
> * scrapy：基于scrapy框架进行编写的爬虫项目

这篇文章介绍了爬虫的一些基础知识[爬虫基础知识_冰山一树Sankey的博客-CSDN博客](https://blog.csdn.net/m0_59464010/article/details/123253811)

## common

### baidu_images.py

爬取百度图片，网址：[百度图片-发现多彩世界 (baidu.com)](https://image.baidu.com/)



### careers_tencent.py

爬取腾讯招聘的，网址：[腾讯招聘 (tencent.com)](https://careers.tencent.com/home.html)



### douban_movies.py

爬取豆瓣电影的榜单，网址：[豆瓣电影排行榜 (douban.com)](https://movie.douban.com/chart)



### gushiwen.py

爬取古诗文网的古诗，包括诗名，作者，诗词，网址：[唐诗三百首全集_古诗文网 (gushiwen.cn)](https://so.gushiwen.cn/gushi/tangshi.aspx)



### kan_2345.py

爬取2345影院的电影，包括电影名字，演员，以及评分，网址：[VIP电影大全,好看的VIP电影高清在线观看 - 2345影视](https://kan.2345.com/vip/list/--movie--0---1.html)



### lianjia.py

爬取北京的链家二手房的，其网址：[北京二手房房源_北京二手房出售|买卖|交易信息(北京链家) (lianjia.com)](https://bj.lianjia.com/ershoufang/)



### mca_gov.py

爬取民政部，目标：

1、抓取最新中华人民共和国县以上行政区划代码
2、建立增量爬虫 - 网站有更新时抓取，否则不抓
3、所抓数据存到数据库，按照层级关系分表存储 - 省、市、县表

网址：[中华人民共和国民政部 (mca.gov.cn)](http://www.mca.gov.cn/article/sj/xzqh/2020/)



### tieba_images_videos

爬取百度贴吧的各种图片和视频，文章爬取爬取相对简单点，这里就没有爬了

网址：[百度贴吧——全球领先的中文社区 (baidu.com)](https://tieba.baidu.com/)



### proxies_86

爬取了86代理网的免费IP并进行测试可用性，存到自己的代理IP池

具体可去我写的这篇文章[如何建立自己的代理IP池,减少爬虫被封的几率](https://www.cnblogs.com/bingshanyishu/p/15959270.html)

## selenium

这篇文章讲了一些selenium的一些概念和使用方法[ selenium在爬虫中的使用_冰山一树Sankey的博客-CSDN博客](https://blog.csdn.net/m0_59464010/article/details/123254759)

### douyu_spider.py

爬取斗鱼网的各个直播间的房间名，直播类型，主播，人气以及直播间首页图

网址：[游戏直播_全部游戏直播_斗鱼直播 (douyu.com)](https://www.douyu.com/directory/all)

### get_crop_image.py

这里呢，不属于爬虫，介绍了如何通过selenium去截取网页上的验证码，后续可通过机器学习破解



### maoyan_spider.py

猫眼top100榜单加上了一些反爬策略，使用一般方式去爬取需要先破解反爬，而使用selenium则不用，selenium的优势就再这个例子中体现出来。

网址：[TOP100榜 - 猫眼电影 - 一网打尽好电影 (maoyan.com)](https://www.maoyan.com/board/4?timeStamp=1646288656064&channelId=40011&index=6&signKey=c766c26af0af881dba7425484092ebb0&sVersion=1&webdriver=false)



### qq_space_log_in.py

运用selenium模拟登录QQ空间



## scrapy

这篇文章介绍了爬虫框架的基本使用，参数配置等[爬虫框架Scrapy_冰山一树Sankey的博客-CSDN博客](https://blog.csdn.net/m0_59464010/article/details/123254840)

### DaoMu

盗墓笔记的爬虫，爬取了所有的盗墓笔记的小说

网址：[盗墓笔记-盗墓笔记小说全集-盗墓笔记电影电视剧-南派三叔作品 (daomubiji.com)](https://www.daomubiji.com/)

包括：
盗墓笔记1：七星鲁王
盗墓笔记2：秦岭神树
盗墓笔记3：云顶天宫
盗墓笔记4：蛇沼鬼城
盗墓笔记5：迷海归巢
盗墓笔记6：阴山古楼
盗墓笔记7：邛笼石影
盗墓笔记8：大结局
盗墓笔记2015年更新



### Douban

爬取豆瓣电影榜单Top250

网址：[豆瓣电影 Top 250 (douban.com)](https://movie.douban.com/top250?start=0&filter=)



### Lianjia

爬取了链家二手房，不过是基于scrapy框架的，可与[lianjia.py](#lianjia.py)进行对比学习



### So

爬取360图片中的美女图片，喜欢美女的，可取运行体验

网址：[美女_360图片 (so.com)](https://image.so.com/z?ch=beauty)



### Tencent

爬取腾讯招聘，内容和[#careers_tencent.py](#careers_tencent.py)一样，网址：[腾讯招聘 (tencent.com)](https://careers.tencent.com/home.html)



### Youdao

破解网易翻译的，破解后可基于本地直接翻译文本

