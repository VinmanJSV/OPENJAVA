# -*- coding: utf-8 -*-



data={"APL":"7D928ANIMUSTVNOW","BRAVO":"34046BRAVUSTVNOW","TOON":"C01E6CARTUSTVNOW",
      "ESPN":"15E33ESPNUSTVNOW","CNN":"A4E91CNN0USTVNOW","CNBC":"D2036CNBCUSTVNOW",
      "USA":"C7069USA0USTVNOW","SYFY":"AF6A3SYFYUSTVNOW","HISTORY":"04107HISTUSTVNOW",
      "DSC":"9BC4DDISCUSTVNOW","COMEDY":"5F4F3COMEUSTVNOW","TNT":"A7CA7TNT0USTVNOW",
      "WLYHUSTVNOW":"CW","WHTM":"A4EB6WHTMUSTVNOW","WPMT":"D5267WPMTUSTVNOW",
      "FX":"D120AFX00USTVNOW","WPSU":"4D4B0WPSUUSTVNOW","FOOD":"8D6BAFOODUSTVNOW",
      "TBS":"4431BTBS0USTVNOW","NIK":"7D839NICKUSTVNOW","WHP":"B7356WHP0USTVNOW",
      "WGAL":"1F797WGALUSTVNOW","AETV":"FD166AETVUSTVNOW","LIFE":"EF5CELIFEUSTVNOW",
      "SPIKETV":"B94D4SPIKUSTVNOW","FNC":"DD21DFOXNUSTVNOW","NGC":"54650NATGUSTVNOW",
      "WHVLLD":"08868WHVLUSTVNOW","AMC":"7BDE7AMC0USTVNOW"
      }



import cookielib
import os
import re
import urllib, urllib2
import sys
import xbmcaddon,xbmcplugin,xbmcgui,xbmc

ADDON = xbmcaddon.Addon(id='plugin.video.VidTime')
USER = ADDON.getSetting('USER')
PASS = ADDON.getSetting('PASS')
thisPlugin = int(sys.argv[1])
fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.VidTime/resources/media/USTV.jpg'))
stream_type = 'rtmp'
quality = '3'

def TEST():
    return

class Ustvnow:
    __BASE_URL = 'http://lv2.ustvnow.com'
    def __init__(self, user, password):
        self.user = USER
        self.password = PASS
                  
    def get_channels(self, quality=1, stream_type='rtmp'):
        self._login()
        html = self._get_html('iphone_ajax', {'tab': 'iphone_playingnow', 
                                              'token': self.token})
        drop = urllib2.urlopen('https://www.dropbox.com/s/jmqo041hwpftywq/newchannel.xml?raw=true')
        b = drop.readlines()
        drop.close()
        channels = []
 
        for channel in re.finditer('<div id="content_(.+?)" class="panel" noback="noback" title="">.+?src="' + 
                                   '(.+?)".+?class="nowplaying_item">(.+?)' +
                                   '<\/td>.+?class="nowplaying_itemdesc".+?' +
                                   '<\/a>(.+?)<\/td>.+?href="(.+?)"',
                                   html, re.DOTALL):
            name, icon, title, plot, url = channel.groups()
            if not url.startswith('http'):
                try:
                    now = {'title': title, 'plot': plot.strip()}
                    fake = icon.split('images/')[1][:-4]
                    url = '%s%s%d' % (stream_type, url[4:-1], quality)
                    url = url[:-17]
                  
                    for data in b:
                        if str(fake) in data:
                            doer = re.findall('".+?": "(.+?)"',data)[0]
                        else:pass
                 
                    url = url+doer+str(quality+1)
                    if "WHVL" in url: url = url[:-1]+str(quality-1)                     
                    if not re.search(str(fake),str(channels)):
                        try: channels.append({'name': fake, 'url': url, 
                                       'icon': icon, 'now': now})
                        except:pass                 
                except:pass
            
        return channels 
            

    def _build_url(self, path, queries={}):
        if queries:
            query = build_query(queries)
            print query
            print '%s/%s?%s' % (self.__BASE_URL, path, query) 
            return '%s/%s?%s' % (self.__BASE_URL, path, query) 
        else:
            return '%s/%s' % (self.__BASE_URL, path)

    def _fetch(self, url, form_data=False):
        if form_data:
            req = urllib2.Request(url, form_data)
        else:
            req = url
        try:
            response = urllib2.urlopen(url)
            return response
        except urllib2.URLError, e:
            return False
        
    def _get_html(self, path, queries={}):
        html = False
        url = self._build_url(path, queries)

        response = self._fetch(url)
        if response:
            html = response.read()
        else:
            html = False
        return html

    def _login(self):
        self.token = None
        self.cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        
        urllib2.install_opener(opener)
        url = self._build_url('iphone_login', {'username': self.user, 
                                               'password': self.password})
        response = self._fetch(url)
        #response = opener.open(url)
        for cookie in self.cj:
            if cookie.name == 'token':
                self.token = cookie.value


def build_query(queries):
    return '&'.join([k+'='+urllib.quote(str(v)) for (k,v) in queries.items()])

def addDirItem(title,icon,fanart,url):
    listitem =xbmcgui.ListItem (title,'','',thumbnailImage=icon)
    listitem.setProperty('fanart_image', fanart)
    xbmcplugin.addDirectoryItem(handle=thisPlugin, url=url,
                                listitem=listitem)
def endDir():
    xbmcplugin.endOfDirectory(thisPlugin)

def RIGHT():
    if not USER =="":   
        ustv = Ustvnow(USER, PASS)
        channels = ustv.get_channels(int(quality), stream_type)

        for c in channels:
            print c
            title = c['now']['title']
            url = c['url']
            icon = c['icon']
            title = re.sub('[^\w\-_\. ]', '', title)
            title = title.replace(' amp ', ' and ')
            addDirItem(title,icon,fanart,url)
        endDir()

    else:
        ADDON.openSettings()
