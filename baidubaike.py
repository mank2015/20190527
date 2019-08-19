import requests,re
from pyquery import PyQuery as pq

headers = {
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36'
}
#搜索词条
search = "定时器"
r = requests.get("https://baike.baidu.com/item/"+search,headers=headers)
print(r)
html = r.text
#转码
html = html.encode(r.encoding)
html = html.decode("utf-8")
doc = pq(html)
#筛选出secondId,mid
seconds = re.findall(r"c.initialize\({\"secondsKnow\":\[{\"videoSrc\":{.*?\"secondId\":(\d+),\"mid\":\"(.+?)\"",html)
secondId,vedioUrl = seconds[0]
#获取视频段信息
url = "https://baike.baidu.com/api/wikisecond/playurl?secondId="+str(secondId)
r = requests.get(url,headers=headers)
#这一步是选取1280x720分辨率的视频，不过似乎所有分辨率返回的信息是一样的？
hlsUrl = r.json().get("list").get("hlsUrl")
r = requests.get(hlsUrl,headers=headers)
hlsUrl = "https://baikevideo.cdn.bcebos.com/media/"+vedioUrl+"/"+re.findall(r"\n([^#\n].*?)\n\n",r.text)[0]
r =requests.get(hlsUrl,headers=headers)
urls = re.findall(r"\n([^#].*?)\n",r.text)
url_part = "https://baikevideo.cdn.bcebos.com/media/"+vedioUrl+"/"
#爬取ts格式的视频段，写入一个视频文件中
file = open("D:/openvc/"+search+".mp4","ab+")
for url in urls:
    r = requests.get(url_part+url,headers=headers)
    file.write(r.content)
file.close()
