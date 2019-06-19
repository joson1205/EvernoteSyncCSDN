#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
import requests
import re
from lxml import etree
import prettytable as pt
from io import BytesIO


class GetNotes(object):
    def __init__(self):
        self.JSESSIONID = None
        self.req_sec = None
        self.userShardId = None
        self.currentUserId = None
        self.listNotebooks = {}
        self.listNotestore = {}
        self.notetags = {}
        self.result = {}
        self.session = self.login()
        self.notebooks()
        while True:
            self.num_1 = input("请输入笔记本名称序号:")
            if self.num_1 in self.listNotebooks.keys():
                self.notestore(self.listNotebooks[self.num_1]["name"])
                break
            else:
                print("输入有误，请重新输入！")
        while True:
            self.num_2 = input("请输入笔记标题序号:")
            if self.num_2 in self.listNotestore.keys():
                self.notecontent(self.listNotestore[self.num_2]["token"])
                break
            else:
                print("输入有误，请重新输入！")

    def login(self):
        login_url = "https://app.yinxiang.com/HeaderLogin.action"
        data = {
            "username": config.Evernote_username,
            "password": config.Evernote_password,
            "login": "",
            "_sourcePage": "qlhPIUFkiwHiMUD9T65RG_YvRLZ-1eYO3fqfqRu0fynRL_1nukNa4gH1t86pc1SP",
            "__fp": "0gFTYmluZ2k3yWPvuidLz-TPR6I9Jhx8"}
        headers = {
            "Host": "app.yinxiang.com",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Origin": "https://app.yinxiang.com",
            "Referer": "https: // app.yinxiang.com / LoggedOut.action",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"}
        session = requests.session()
        response = session.post(login_url, headers=headers, data=data)
        if "localizedMessage" in response.text:
            data = eval(response.text)
            print("Evernote登陆失败:{}".format(data["errors"][0]["localizedMessage"]))
        else:
            print("Evernote登陆成功!")
            cookies = requests.utils.dict_from_cookiejar(response.cookies)
            self.JSESSIONID = cookies["JSESSIONID"]
            self.req_sec = cookies["req_sec"]
            return session

    def notebooks(self):
        home_url = "https://app.yinxiang.com/Home.action"
        headers = {
            "Host": "app.yinxiang.com",
            "Referer": "https://app.yinxiang.com/LoggedOut.action",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
        }
        payload = {
            "username": config.Evernote_username,
            "login": "true",
            "_sourcePage": "qlhPIUFkiwHiMUD9T65RG_YvRLZ-1eYO3fqfqRu0fynRL_1nukNa4gH1t86pc1SP",
            "__fp": "0gFTYmluZ2k3yWPvuidLz-TPR6I9Jhx8"}
        response = self.session.get(home_url, headers=headers, params=payload).text
        self.userShardId = re.findall('(?<=userShardId":").+?(?=")', response)[0]
        self.currentUserId = re.findall('(?<=currentUserId":)\d+', response)[0]
        tags_str = re.findall("(?<=listTags:).+]", response)[0]  # 标签
        notebooks_str = re.findall("(?<=listNotebooks:).+(?=,)", response)[0]  # 笔记本
        tags = eval(tags_str.replace('\\', '').replace('"{', '{').replace('}"', '}'))
        # 标签{token:name,...}
        for tag in tags:
            self.notetags[tag["1"]["str"]] = tag["2"]["str"]
        # 笔记本列表(转嵌套列表)
        Notebooks = {}
        listNotebooks = eval(notebooks_str.replace('\\', '').replace('"{', '{').replace('}"', '}'))
        for item in listNotebooks:
            Notebooks[item["2"]["str"]] = item["1"]["str"]
        i = 1
        for key in Notebooks.keys():
            self.listNotebooks[str(i)] = {}
            self.listNotebooks[str(i)]['name'] = key
            self.listNotebooks[str(i)]['token'] = Notebooks[key]
            i += 1
        print("共获取 {} 个笔记本".format(len(self.listNotebooks)))
        # {1:{},2:{}}
        tb = pt.PrettyTable()
        tb.field_names = ["序号", "笔记本名称"]
        for key in self.listNotebooks.keys():
            tb.add_row([key, self.listNotebooks[key]["name"]])
        print(tb, "\n")

    def notestore(self, bookname):
        url = "https://app.yinxiang.com/shard/{}/enweb/notestore".format(self.userShardId)
        headers = {
            "Host": "app.yinxiang.com",
            "Origin": "https://app.yinxiang.com",
            "Pragma": "no-cache",
            "Referer": "https://app.yinxiang.com/Home.action?login=true",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
            "X-EN-Webclient-CSRF": self.req_sec,
            "X-GWT-Permutation": self.JSESSIONID,
            "X-EN-Webclient-Version": "WEB2.0",
            "X-GWT-Module-Base": "https://app.yinxiang.com/focusclient/"
        }
        # 笔记本最大记录数
        page = 10000
        data = "7|0|11|https://app.yinxiang.com/focusclient/|CA89028168A1400F0E5BA1CB2B1B829D|com.evernote.web.shared.GWTNoteStoreInterface|findNotesMetadata|com.evernote.edam.notestore.NoteFilter/3484559800|I|com.evernote.edam.notestore.NotesMetadataResultSpec/2285571585|[Z/1413617015|{}|Etc/GMT-8||1|2|3|4|4|5|6|6|7|5|8|5|1|1|1|0|0|0|0|0|0|0|0|9|2|0|0|0|0|0|10|11|0|{}|7|8|11|1|0|1|1|0|0|1|0|1|1|0|1|0|1|0|1|0|1|0|1|0|1|".format(
            self.listNotebooks[self.num_1]["token"], page)
        res = self.session.post(url, data=data, headers=headers)
        res_list = eval(res.text[4:])[-3][6:-1]
        data = []
        # 无规则列表清洗
        books_token = [self.listNotebooks[key]["token"] for key in self.listNotebooks.keys()]
        for t in res_list:
            if t in books_token:
                pass
            elif "application/" in t or "desktop." in t:
                pass
            elif "yinxiang" in t or "https://" in t or "http://" in t:
                pass
            elif "image/" in t or 'text/plain' in t:
                pass
            else:
                data.append(t)

        # 匹配笔记token
        k = 1
        while True:
            if len(data) > 1:
                item = re.findall("^[A-Za-z0-9\-]+$", str(data[0]))
                if len(item) == 1 and str(item[0]).count("-") == 4:
                    item = re.findall("^[A-Za-z0-9\-]+$", str(data[1]))
                    if len(item) == 1 and str(item[0]).count("-") == 4:
                        data.remove(data[1])
                    else:
                        self.listNotestore[str(k)] = {}
                        self.listNotestore[str(k)]["token"] = data[0]
                        self.listNotestore[str(k)]["name"] = data[1]
                        data = data[2:]
                        k += 1
                else:
                    data = data[1:]
            else:
                break
        print("# {} # 笔记本下共 {} 条记录:".format(bookname, len(self.listNotestore)))
        tb = pt.PrettyTable()
        tb.field_names = ["序号", "笔记标题"]
        tb.align["笔记标题"] = "l"  # 标题列左对齐
        for key in self.listNotestore.keys():
            tb.add_row([key, self.listNotestore[key]["name"]])
        print(tb, "\n")

    def notecontent(self, token):
        url = "https://app.yinxiang.com/shard/{}/enweb/notestore".format(self.userShardId)
        headers = {
            "Host": "app.yinxiang.com",
            "Origin": "https://app.yinxiang.com",
            "Pragma": "no-cache",
            "Referer": "https://app.yinxiang.com/Home.action",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
            "X-EN-Webclient-CSRF": self.req_sec,
            "X-GWT-Permutation": self.JSESSIONID,
            "X-EN-Webclient-Version": "WEB2.0",
            "X-GWT-Module-Base": "https://app.yinxiang.com/focusclient/"
        }
        payload = "7|0|8|https://app.yinxiang.com/focusclient/|CA89028168A1400F0E5BA1CB2B1B829D|com.evernote.web.shared.GWTNoteStoreInterface|getNoteWithResultSpec|java.lang.String/2004016611|com.evernote.edam.notestore.NoteResultSpec/3324952227|{}|[Z/1413617015|1|2|3|4|2|5|6|7|6|8|8|1|1|1|1|1|0|0|0|0|0|0|0|0|0|0|1|".format(
            token)
        res = self.session.post(url, headers=headers, data=payload)
        # 提取标签
        tags = []
        for key in self.notetags.keys():
            if key in res.text:
                tags.append(self.notetags[key])
        self.result["tags"] = ",".join(tags)

        url = "https://app.yinxiang.com/shard/{}/nl/{}/{}?content=".format(self.userShardId, self.currentUserId, token)
        headers = {
            "Referer": "https://app.yinxiang.com/shard/{}/nl/{}/{}".format(self.userShardId, self.currentUserId, token),
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"}
        res = self.session.post(url, headers=headers)
        html = etree.HTML(res.text)
        contentHTML = html.xpath('//div[@class="note-content"]')
        contentStr = etree.tostring(contentHTML[0])
        contentStr = re.sub('\?resizeSmall.+?(?=")', "", str(contentStr)[2:-3])
        self.result["title"] = self.listNotestore[self.num_2]["name"]
        self.result["content"] = contentStr
        self.noteimage()

    def noteimage(self):
        image = re.findall("https://app\.yinxiang\.com/shard/.+?.(?:jpg|png|gif|jpeg)", str(self.result["content"]))
        img_list = []
        for img in image:
            img_list.append({
                "name": img.split("/")[-1],
                "type": "image/" + img.split(".")[-1],
                "url": img
            })
        for img in img_list:
            res = self.session.get(img["url"])
            img["bytes_content"] = res.content
        self.result["image"] = img_list


class SyncCSDN(object):
    """docstring for SyncCSDN"""

    def __init__(self, **kwargs):
        """params: {'title':'标题','content':'内容','tags':'标签'}"""
        self.session = requests.session()
        self.webUmid_Token = None
        self.login()
        self.draft(kwargs)

    def webUmidToken(self):
        url = "https://ynuf.aliapp.org/service/um.json"
        headers = {
            "Host": "ynuf.aliapp.org",
            "Origin": "https://passport.csdn.net",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
            "Referer": "https://passport.csdn.net/login"
        }
        data = {
            "data": "106!qhImc0clJNmHJx0eHmjz5Frca5nTQzwmUUam0LH0KjRU56cmfbIHMccc6PHCbtyKQfQA1N8EWAU+Xuyg7yt+V9NXG0mMzW0BFpYJC+riRdTamH8qsZkoHBAqUhSdJKV9mEjRP8OAZsfsD3ot7K+8RTpN/jQkgz+1cu01O4rkys/JPfoKzGFPs7OjXROmhvsko4P1l5WHysYGPZ60vga9ObHU5u8Ns+ZUmLFBoCcG/RkSwr/U57bK5FaU4ujc41KSftYSFGTFQiAsf0Rv6muGH7eSTB4joSoLt64OrFT3KtYLyhRvvwvtydgOCb1io1tsTubOrFXuQdYKCMgV9gPAZ/eKZBLroS4s/ulSgGyF/xNU5uMHQAW0xSc6qjUlqCNJUeedl6Ms0TY8aQCQIL2kheNm7u4/osnEKZ0+twjV/dS0qgVbgjcdKsUN9elSwfjn2QIv2jYYY2l5ecGgNM/ZFVkbY8VCCIFJ97CNf8ETEhHuNLAo+xhsoy/aSq9rpyI7DihYN+GCP+LIRZWU7keW0OYp8G+nm77AtLgJ1t895NHP+JrC9Kfrei/yScZFgyBIRVUqooRerPR7lGOYTOIm+x5F+gzFjFFG1EsPL5Jk9mX5+/nvy9hx+ATirXs3QPVKwNAe6A7/KBEynz+/nyuEuMqLPp6nhFlZCPGks0fcdZGFDsmAH5Fm3Rg/Tq9KO/teXeo6dlkzK0dH+tz0yZJcTH4abtMjTkFB0tINS0Ob4DGrq/VI0l4J7kYv0cTBwnyyBQvX3ujnMKVNb7IXt7Evy8PEu8JRbfk9BkzA",
            "xa": "saf-aliyun-com",
            "xt": ""
        }
        res = self.session.post(url, headers=headers, data=data).json()
        self.webUmid_Token = res["tn"]

    def login(self):
        self.webUmidToken()
        url = "https://passport.csdn.net/v1/register/pc/login/doLogin"
        data = {
            "loginType": "1",
            "pwdOrVerifyCode": config.CSDN_password,
            "userIdentification": config.CSDN_username,
            "webUmidToken": self.webUmid_Token
        }
        headers = {
            "Host": "passport.csdn.net",
            "Origin": "https://passport.csdn.net",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
            "Content-Type": "application/json;charset=UTF-8",
            "Referer": "https://passport.csdn.net/login"
        }
        # requests payload 方式传参数,转字符串
        res = self.session.post(url, headers=headers, data=str(data)).json()
        print("CSDN博客登陆状态:{}".format(res["message"]))

    def uploadImage(self, notes, headers):
        if notes["image"]:
            url = "https://mp.csdn.net/UploadImage?shuiyin=2"
            for img in notes["image"]:
                img_file = BytesIO(img["bytes_content"])
                files = {
                    "file": (img["name"], img_file.getvalue(), img["type"])
                }
                res = self.session.post(url, headers=headers, files=files).json()
                if res["result"] == 1:
                    # 替换图片url
                    notes["content"] = notes["content"].replace(img["url"], res["url"])
                    # notes["content"] = str(notes["content"]).replace(img["url"], res["url"])
                    img["bytes_content"] = None

        else:
            pass
        return notes

    # 发布
    def draft(self, notes):
        url = "https://mp.csdn.net/mdeditor/saveArticle"
        headers = {
            "Host": "mp.csdn.net",
            "Origin": "https://mp.csdn.net",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
            "Referer": "https://mp.csdn.net/mdeditor?not_checkout=1"
        }
        notes = self.uploadImage(notes, headers)
        payload = {
            'title': notes['title'],
            'markdowncontent': notes['content'],
            'content': notes['content'],
            'id': '',
            'private': config.CSDN_private,
            'read_need_vip': '',
            'tags': notes['tags'],
            'status': config.CSDN_status,
            'categories': config.CSDN_categories,
            'channel': config.CSDN_channel,
            'type': config.CSDN_article_type,
            'articleedittype': 1,
            'Description': '',
            'csrf_token': ''
        }
        res = self.session.post(url, headers=headers, data=payload).json()
        if res["status"]:
            print("笔记已同步到CSDN博客\n查看链接:{}".format(res["data"]["url"]))
        else:
            print("文章发布失败,原因:{}".format(res["error"]))


def main():
    Evernote = GetNotes()
    SyncCSDN(**Evernote.result)


if __name__ == '__main__':
    main()
