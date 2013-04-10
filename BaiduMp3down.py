#-*- encoding:utf-8 -*-
__author__ = 'No_Body'

from BeautifulSoup import BeautifulSoup
import urllib, urllib2, cookielib, re, json, os

base_url='http://music.baidu.com/search?key=%s'
base_down='http://music.baidu.com%s/download'
base_link='http://music.baidu.com'
songs_dir='songs'
fp=open("fail.txt",'w')

def downMusic(songName):
    #搜索字符串 注意 空格要用+替换 一开始没注意 导致有些歌名包含空格的没下载下来
    url=base_url % songName.replace(" ","+")
    req=urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')
    content=urllib2.urlopen(req,timeout=20).read()
    soup=BeautifulSoup(content)

    #取第一个链接进行下载
    song_id=soup.findAll("span",{'class':'song-title'})[0].find('a')['href']
    down_url=base_down % song_id  #下载页面的url
    req1=urllib2.Request(down_url)
    req1.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')
    content1=urllib2.urlopen(req1,timeout=20).read()
    soup1=BeautifulSoup(content1)

    song_link=soup1.findAll("div",{"id":"down_btn_group"})[0].find('a')['href']#找到下载链接字符串
    down_link=base_link + song_link  #下载的链接
    filename=songName+".mp3"        #构造文件名
    filepath=os.path.join(songs_dir, filename)   #构造下载路径

    print down_link
    print filepath
    try:
        urllib.urlretrieve(down_link,filepath.decode('utf-8'))   #下载歌曲
        print "succeed!"
    except:
        print "fail!"
        fp.write(filename+'\n')

if __name__=="__main__":
    downMusic("Eminem / Rihanna-Love The Way You Lie")   #测试
