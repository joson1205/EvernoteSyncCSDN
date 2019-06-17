# EvernoteSyncCSDN
通过抓包分析,然后模拟请求的方式获取数据,同步到CSDN博客上,并非API.
不采用API的原因主要是因为两个方面:
1.印象笔记官方的API申请后只能通过沙盒环境测试用,没办法直接获取到实际数据;可以申请临时API,不过有效期只有7天.API的接口只支持Python2,很遗憾,本人已经放弃使用.
2.CSDN API 官方已经关闭,没找到入口

## 依赖库
```python
pip install configparser
pip install requests
pip install lxml
pip install prettytable
```
## 配置config.ini
```
[Evernote_Setting]
username = username
password = password

[CSDN_Setting]
username = username
password = password
# 0:直接发布,2:存到草稿箱
status = 0
# 文章类型:original(原创),repost(转载),translated(翻译)
article_type = original
# 个人分类,不存在则新增
categories = Python
# 博客分类,默认(程序人生),16:编程语言,6:数据库,36:咨询
channel = 33
# true:私密文章,留空则表示公开,false无效
private =
```
## 使用
```python
python setup.py
```
## 已知Bug
1.图片同步后无法显示
2.笔记标签信息暂时未获取到
3.单个笔记本目录下最多显示1w条笔记,超过可自行修改



