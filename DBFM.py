#-*- encoding:utf-8 -*-
import codecs

__author__ = 'No_Body'

from BeautifulSoup import BeautifulSoup
import urllib, urllib2, cookielib, re, json, eyed3, os
from BaiduMp3down import *

fp=open("songlists.txt",'w')
num=re.compile(r'(\d+)')
songs_dir='songs'
base_url='http://douban.fm/j/mine/playlist?type=n&h=&sid=%s&pt=0.0&channel=0&from=mainsite'
songinfo_url='http://dbfmdb.sinaapp.com/api/song.php?sid=%s'
invalid=['/','\\', ':','*','?','"','<','>','|']

def valid_filename(s):
    return filter(lambda x:x not in invalid, s)

#传入sid 得到歌曲的信息，但是并不包含下载的link，所以只能抛弃了
def get_songs_information(sid):
    opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    urllib2.install_opener(opener)
    detail=json.loads(urllib2.urlopen(songinfo_url%sid).read())

    #本来是想进一步分析得到下载链接的，原来那只是我下载的插件...

    # prereq=urllib2.Request('http://douban.fm?start=%sg%sg' % (sid,detail['ssid']))
    # prereq.add_header("User-Agent", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)")
    # content=urllib2.urlopen(prereq,timeout=20).read()
    # soup=BeautifulSoup(str(content))
    # url=soup.findAll('a',{'title':'点击下载'})
    # print url
    # req=urllib2.Request(base_url % sid)
    # req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')
    # ret=json.loads(urllib2.urlopen(req,timeout=20).read())
    # print len(ret['song'])
    return detail


#本来是准备从豆瓣FM上找到链接下载歌曲的，无奈base_url返回的json都是随机的，并不是对应的歌曲
#无奈之下，只有从百度音乐中搜索并下载歌曲了
def download(song):
    try:
        os.makedirs(songs_dir)
    except:
        pass
    filename='%s-%s.mp3' % (valid_filename(song['artist'].encode('utf-8')), valid_filename(song['title'].encode('utf-8')))

    filepath=os.path.join(songs_dir, filename)   #得到下载路径
    # print filepath
    picname=song['picture'][1+song['picture'].rindex('/'):]
    picpath=os.path.join(songs_dir, picname)
    urllib.urlretrieve(song['picture'].replace('mpic','lpic'), picpath)
    urllib.urlretrieve(song['url'], filepath)

    #eyed3的用法还有待进一步的考证

    # tag=eyed3.Tag()
    # tag.link(filepath)
    # tag.header.setVersion(eyed3.ID3_V2_3)
    # tag.encoding='\x01'
    # tag.setTitle(song['title'])
    # tag.setAlbum(song['albumtitle'])
    # tag.setArtist(song['artist'])
    # tag.setDate(song['public_time'])
    # tag.addImage(3, picpath)
    # os.remove(picpath)
    # tag.update()

#处理html
def html_decode(html):
    import HTMLParser
    return HTMLParser.HTMLParser().unescape(html)


def get(myurl, cookie):
    opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    urllib2.install_opener(opener)
    req=urllib2.Request(myurl)
    req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')
    req.add_header('Cookie', cookie)
    content=urllib2.urlopen(req, timeout=20).read()
    soup=BeautifulSoup(str(content))

    for div in soup.findAll('div', {'class':'info_wrapper'}):
        p=div.find('div',{'class':'song_info'}).findAll('p')
        sid=div.find('div',{'class':'action'})['sid']
        try:
            filename='%s-%s' % (html_decode(p[1].string).encode('utf-8'),html_decode(p[0].string).encode('utf-8'))
            filename=filename.replace('/','&')
            # fp.write(filename+'\n')
            print "song:"+html_decode(p[0].string)+"\nsinger:"+html_decode(p[1].string)+"\nalbum:"+html_decode(p[2].a.string)
            print "song:"+html_decode(p[0].string)+"\nsinger:"+html_decode(p[1].string)+"\nalbum:"+html_decode(p[2].a.string)

            #从百度下载歌曲
            downMusic(filename)
        except:
            print "song..."
        #直接下载未遂的代码
        # mark=False
        # try:
        #     for j in range(9):
        #         songs=get_songs_information(sid)
        #         for song in songs:
        #            if sid==song['sid']:
        #             download(song)
                    # mark=True
                    # break
                # if mark:
                #     print 'succeed!\n\n'
                # else:print 'fail!\n\n'
        # except Exception as e:
        #     print e.message+'\n'


def main():
    url = 'http://douban.fm/mine?start=%d&type=liked'
    #本人的豆瓣cookie
    cookie="""flag="ok"; ac="1365483610"; openExpPan=Y; ck="c2sR"; dbcl2="55618372:JJr127Tjefk";
    bid="Y7DGENdM+7M"; __utma=58778424.985354367.1364552815.1365500439.1365517525.9;
    __utmb=58778424.15.9.1365517853463; __utmc=58778424; __utmz=58778424.1365500431.7.5.utmcsr=douban.com|
    utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=58778424.5561
    """

    #自己查了下 一共是1到8页
    pagestart=1
    pageend=8
    #用cookie登录 从红心列表里面找到歌曲信息
    for i in range(pageend-pagestart+1):
        get(url%((i+pagestart-1)*15), cookie)

if __name__=="__main__":
    main()


