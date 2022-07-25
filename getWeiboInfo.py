import csv

from bs4 import BeautifulSoup
import requests
import re
from pyquery import PyQuery as pq 
import json
import MySQLdb
# url="https://www.runoob.com/python/python-json.html"
# data={
#     'name':'germey',
#     'age':22
# }
# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
# }
# r=requests.get(url,headers=headers)

# pattern = re.compile('"title":"(.*?)","description":"(.*?)","url":"(.*?)"', re.S)

# titles = re.findall(pattern, r.text)
# # for res in titles:
# #     print(res[1],res[2],res[0])
# print(titles[0])

# print(r.text)



# soup=BeautifulSoup(r.text,'lxml')
# # print(soup.find_all(name='a'))
# for ul in soup.find_all(name='a'):
#     if ul.string !=None:
#         tem=ul.attrs['href']
#         mathch_str=re.match('.*?/.*?/.*',tem)
#         if mathch_str!=None:
#             # print(mathch_str.group())
#             integ=re.match('^/.*',mathch_str.group())
#             if integ!=None:
#                 print("网站:https://www.runoob.com"+str(integ.group()))
#             else:
#                 print("网站:{}".format(mathch_str.group()))
def getPage(page):
    url="https://m.weibo.cn/api/container/getIndex?"
    params={
        'containerid':'102803',
        'openApp':'0',
        'since_id':page
    }
    headers={
        'Accept': 'application/json, text/plain, */*',
        'MWeibo-Pwa': '1',
        'Referer': 'https://m.weibo.cn/',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'X-XSRF-TOKEN': 'fb01ea',
        'cookie': '_T_WM=53261302214; MLOGIN=0; XSRF-TOKEN=fb01ea; WEIBOCN_FROM=1110106030; mweibo_short_token=b64669a7f3; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D102803%26uicode%3D20000174'
    }
    try:
        response=requests.get(url,headers=headers,params=params)
        if response.status_code==200:
            return response.json()
        else:
            print('status:',response.status_code)
    except requests.ConnectionError as err:
        print('erro',err.args)

def parsePage(json):
    if json:
        items=json.get('data').get('cards')
        for item in items:
            item=item.get('mblog')
            weibo={}
            weibo['attitudes_count']=item.get('attitudes_count')        #点赞数
            weibo['comments_count']=item.get('comments_count')          #评论数
            # weibo['region_name']=item.get('region_name')                #位置
            weibo['text']=re.sub('\n','',pq(item.get('text')).text())              #文本内容，包含html格式文本,使用re.sub去除\n
            item=item.get('user')
            # weibo['avatar_hd']=item.get('avatar_hd')                    #头像图片url
            if item==None :
                return None
            if item.get('description')==None or item.get('followers_count')==None or item.get('screen_name')==None :
                return None
            weibo['description']=item.get('description')                #博主描述
            weibo['followers_count']=item.get('followers_count')        #粉丝数
            weibo['screen_name']=item.get('screen_name')                #博主名称
            yield weibo

if __name__ == '__main__':  
    db = MySQLdb.connect("localhost", "root", "123456", "spy",charset='utf8mb4', )
    cursor=db.cursor()
    # cursor.execute("INSERT INTO `spy`.`weibo` (`attitudes_count`, `comments_count`, `text`, `description`, `followers_count`, `screen_name`) VALUES ('1', '1', '1', '1', '1', '1')")
    with open('data.csv','w+',encoding='utf-8') as file:
        fieldnames=['attitudes_count','comments_count','text','description','followers_count','screen_name']
        # writer=csv.writer(file) 
        # writer.writerow(['点赞数','评论数','文本','博主描述','博主名称'])
        writer=csv.DictWriter(file,fieldnames=fieldnames)
        for page in range(1, 11):  
            json = getPage(page)  
            results = parsePage(json)
            if results!=None: 
                for result in results: 
                    # writer.writerow([result['attitudes_count'],result['comments_count'],result['text'],result['description'],result['screen_name']])
                    
                    # temp=re.match('{\'attitudes_count\': .*?, \'comments_count\': .*?, \'text\': \'.*?\', \'description\': \'.*?\', \'followers_count\': \'.*?\', \'screen_name\': \'.*?\'}',str(result))
                    # if temp!=None:
                    #     writer.writerow(result)
                    #     print(str(result))
                    writer.writerow(result)
                    print(result)
                    sql="INSERT INTO `spy`.`weibo`(`attitudes_count`,`comments_count`,`text`,`description`,`followers_count`,`screen_name`) \
        VALUES('%s', '%s', '%s', '%s', '%s','%s' );" % (str(result['attitudes_count']),str(result['comments_count']),str(result['text']),str(result['description']),str(result['followers_count']),str(result['screen_name']))  
                    cursor.execute(sql)
                    db.commit()
    db.close()


