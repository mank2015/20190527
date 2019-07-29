import urllib3
import json
from lxml import etree
import random
import threading
import time
import ssl
import requests
import certifi

#多线程
exitFlag = 0


def getImg():
    for i in range(10000):
    #salt = ''.join(random.sample(string.digits, 7))
    
        a = random.sample("0123456789", 7)
        code = ""
        salt = code.join(a)
    
        print('处理工号：'+ salt)
        #get_out_ip()
        #http = urllib3.ProxyManager('https://124.193.37.5:8888/')
        #开起ssl验证
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
        urllib3.disable_warnings()
        headers = {'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.8',
           'Cache-Control': 'max-age=0',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
           'Connection': 'keep-alive',
           'Referer': 'https://m.ke.com'
           #'cert_reqs' : 'CERT_REQUIRED'
           }
        # 这是代理IP
        
        r = http.request('GET', 'https://m.ke.com/cq/fang/agent/100000002' + salt, headers=headers)
        #r = http.request('GET', 'https://m.ke.com/cq/fang/agent/1000000020261493', headers=headers)
        data = str(r.data, 'utf8')
        print(data)
        html = etree.HTML(data)
        result = etree.tostring(html)
        #result = html.xpath('//*')
        print(html)
        # 在xml中定位节点，返回的是一个列
        # 在xml中定位节点，返回的是一个列表
        links = html.xpath("//*[@id='agent-wrapper']/div[1]/div[1]/div/div[1]/img")
        for index in range(len(links)):
    # links[index]返回的是一个字典
            if (index % 2) == 0:
        #        print(links[index].tag)
                print(links[index].attrib)
        #print(links[index].text)
                imgurl = links[index].attrib['src']
                if imgurl == '':
                    print('工号：'+ salt + '没有照片')
                    pass
                else:
                    print(imgurl)
                    imgurl = imgurl[:-12] 
                    print(imgurl)
                    name = html.xpath("//*[@id='agent-wrapper']/div[1]/div[1]/div/div[2]/div[1]/span")
                    for n in range(len(name)):
                    #姓名
                        if (n % 2) == 0:
                            print(name[n].text)
                            name = name[n].text
                            if name == None:
                                print('工号：'+ salt + '没有名字')
                                pass
                            else:
                                print('下载工号：'+ salt + '姓名：'+name)
                                dizhi = html.xpath("//*[@id='agent-wrapper']/div[1]/div[1]/div/div[2]/div[2]/div[1]/span")
                                shangquan = ''
                                for d in range(len(dizhi)):
                                #姓名
                                    if (d % 2) == 0:
                                        print(type(dizhi[d]))
                                        #dizhi = dizhi[d]
                                        if(type(dizhi[d]) == str):
                                            shangquan = dizhi.strip('主营商圈：-') 
                                        else:
                                            pass
                                FileName = "D:/openvc/beike/" + salt +'-'+ name +'-'+ shangquan + ".jpg"
                                # 下载单个imageURL的图片
                                r1 = http.request('GET', imgurl)
                                data1 = r1.data
                                f = open(FileName,'wb+')
                                f.write(data1)
                                f.close()
                                print("第"+str(i)+'次')
def get_out_ip():
    url = r'http://2019.ip138.com/ic.asp'
    r = requests.get(url)
    txt = r.text
    ip = txt[txt.find("[") + 1: txt.find("]")]
    print( ip)
    
#创建线程
threading.current_thread().name
t = threading.Thread(target=getImg, name='Thread1')
t2 = threading.Thread(target=getImg, name='Thread2')
t3 = threading.Thread(target=getImg, name='Thread3')
t4 = threading.Thread(target=getImg, name='Thread4')
#开启线程
t.start()
t2.start()
t3.start()
t4.start()
# thread3.start()
# thread4.start()
# thread5.start()
# thread6.start()
# thread7.start()
# thread8.start()
# thread9.start()
print("Exiting Main Thread")
# # 在xml中定位节点，返回的是一个列表
# links = html.xpath("//*[@id='agent-wrapper']/div[5]/div/a")
# for index in range(len(links)):
#     # links[index]返回的是一个字典
#     if (index % 2) == 0:
#         print(links[index].tag)
#         print(links[index].attrib)
#         print(links[index].text)
