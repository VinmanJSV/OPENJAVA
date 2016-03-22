# -*- coding: utf-8 -*-
# VinMan_JSV 2016

import os,re,sys,urllib,urllib2,xbmcplugin,xbmcgui,xbmcaddon,xbmc,urlparse,cookielib,base64
from resources.lib.modules import client
from resources.lib.modules import cloudflare
from resources.lib.modules import control

thisPlugin = int(sys.argv[1])
base_url = sys.argv[0]
args = urlparse.parse_qs(sys.argv[2][1:])
mode = args.get('mode', None)
addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
ADDON = xbmcaddon.Addon(id='plugin.video.VidTime')
path = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.VidTime/'))
usdata=xbmc.translatePath(os.path.join('special://userdata/addon_data/plugin.video.VidTime/'))
mediaPath = path +"resources/media/"
fanart = (path + 'fanart.jpg')
icon = (path + 'icon.png')
icon2 = mediaPath+'Search.png'
SPORT = mediaPath+'sport.png'
ROCK = mediaPath+'Rock.png'
VidToon = mediaPath+'VidToons.png'
CONCERT = mediaPath+'Rock Concert.png'
USTV = mediaPath+'USTV.png'
pager = '1'
plot = None
cj = cookielib.LWPCookieJar()
cookiepath = (usdata+'cookies.lwp')
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1')]

cookie = cloudflare.justcookie('http://www.streamlord.com')

TVSHOWS = None
MOVIES= None

def TEST():
    return 

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)
        
def choose():
    cats = ["MOVIES","MOVIE GENRES","TV SHOWS","TV SHOWS - RECENTLY UPDATED","SEARCH","USTV RIGHT NOW",
            "VIDTOONS","PERCH PICKS - ASSORTED SPORTS", "ROCKS EPIC FAIL", "ROCK CONCERT"]
    for name in cats:
        url = build_url({'mode': name})
        li = xbmcgui.ListItem('[B]'+name+'[/B]',iconImage=icon)
        if 'SEARCH' in name:li = xbmcgui.ListItem('[B]'+name+'[/B]',iconImage=icon2)
        if 'PERCH' in name:li = xbmcgui.ListItem('[B]'+name+'[/B]',iconImage=SPORT)
        if 'ROCKS' in name:li = xbmcgui.ListItem('[B]'+name+'[/B]',iconImage=ROCK)
        if 'CONCERT' in name:li = xbmcgui.ListItem('[B]'+name+'[/B]',iconImage=CONCERT)
        if 'VIDTOONS' in name:li = xbmcgui.ListItem('[B]'+name+'[/B]',iconImage=VidToon)
        if 'USTV' in name:li = xbmcgui.ListItem('[B]'+name+'[/B]',iconImage=USTV)
        li.setProperty('fanart_image', fanart)
        xbmcplugin.addDirectoryItem(handle=thisPlugin,url=url,
                                    listitem=li, isFolder=True)
    try:
        onetime = OPEN_URL('https://www.dropbox.com/s/dpdaw992a92hxdr/XMLEXTRA.xml?raw=true')
        stuff = re.compile('<window>(.+?)</window><base>(.+?)</base><thumbnail>(.+?)</thumbnail>').findall(str(onetime))
        for name, base, thumb in stuff:
            url =build_url({'mode': 'XML', 'base': base})
            li = xbmcgui.ListItem('[B]'+name+'[/B]',iconImage=thumb)
            li.setProperty('fanart_image', fanart)
            xbmcplugin.addDirectoryItem(handle=thisPlugin,url=url,
                                       listitem=li, isFolder=True)
    except:
        pass
    xbmcplugin.endOfDirectory(thisPlugin)
   
   
def main(url):
    choice = url

    REQ = cloudflare.request(url)
   
    REQ =REQ.replace('\n','').replace('\t','').replace('\r','').replace('amp;','')
    if  TVSHOWS == False:
        page = re.compile('<ul id="improved">(.+?)</ul>').findall(str(REQ))
        title = re.compile('<a href="(.+?)"><img src="http://www.streamlord.com/(.+?)"></a>').findall(str(page))
    else:
        page = re.compile('<li.+?class="movie"(.+?)</li>').findall(str(REQ))
        title = re.compile('<a href="(.+?)"><img src=(.+?)width').findall(str(page))
    for t,i in title:
        try:
            icon_site = 'http://www.streamlord.com/'+str(i).replace("\\'",'')+cookie
        except:
            icon_site = 'http://www.streamlord.com/'+str(i).replace("\\'",'')

        if MOVIES:
            items = re.sub('watch-movie-|\.html','',t).replace('-',' ').upper().encode('utf-8')
            items = " ".join(items.split(' ')[0:-1])
            url = build_url({'mode': 'PLAY', 'PAGE': t, 'ICON': icon_site, 'NAME': items})
        else:
            items2 = re.sub('watch-tvshow-|\.html','',t).replace('-',' ').upper().encode('utf-8')
            items = " ".join(items2.split(' ')[0:-1])
            if TVSHOWS:url = build_url({'mode': 'TVSHOWS', 'PAGE': t})
            if not TVSHOWS:
                items = items.replace('EPISODE ','')
                url = build_url({'mode': 'PLAY', 'PAGE': t, 'ICON': icon_site, 'NAME': items})
        li = xbmcgui.ListItem('[B]'+ items +'[/B]',iconImage=icon_site)
        li.setProperty('fanart_image', fanart)
        if TVSHOWS:
            xbmcplugin.addDirectoryItem(handle=thisPlugin, url=url,
                                        listitem=li, isFolder=True)
        else:
            xbmcplugin.addDirectoryItem(handle=thisPlugin, url=url,
                                        listitem=li, isFolder=False)
    
    
    next = re.findall('</span><a href=".+?"> (.+?)  ',str(REQ))
    try:
        if next[0] == 'NEXT':
            url = build_url({'mode': 'NEXT', 'PAGE': pager, 'CHOICE': choice})
            li = xbmcgui.ListItem('[COLOR red][I][B]NEXT[/COLOR][/I][/B]',iconImage=mediaPath+'next.png')
            li.setProperty('fanart_image', fanart)
            xbmcplugin.addDirectoryItem(handle=thisPlugin,url=url,
                                        listitem=li, isFolder=True)
        else:pass
    except:
        pass          
    xbmcplugin.endOfDirectory(thisPlugin)
    
def english(final):
    try:
        x = "MlVPdKNBjIuHvGtF1ocXdEasWZaSeFbNyRtHmJ"
        y =":/."
        fget = x[-1]+x[-11].lower()+x[2]
        rget = x[-12]+x[6]+x[16] 
        this = fget+'.+?'+rget
        getter = re.findall(this,final)[0]
        stage = int(final.index(getter))/5
        work = base64.b64decode(str(final.replace(getter,''))).split('/')
        Solve = True
        S = 1
        while Solve is True:        
            if S<= stage*2:first = base64.b64decode(work[1])
            if S<= stage:sec = base64.b64decode(work[0])
            S = S + 1
            if not S<= stage*2 and not S<= stage: Solve = False
            work =[sec,first]
        answ = work[1]+work[0]
        if answ.startswith (x[-5].lower()+x[-10]):
            begin = (x[-3].lower()+(x[-4]*2)+x[3].lower()+y[0:2]+y[1]+x[7].lower())
            ender = (x[-10]+x[-5].lower())
            killit = (x[-5].lower()+x[-10]+x[-4]+x[-12].lower()+x[-5].lower()+x[4]+x[-11].lower()+x[-3].lower())
            mid = y[2]+x[1]+x[-6]
            url = answ.replace(killit,begin).replace(ender,mid)
        elif answ.startswith ('rtmp') or answ.startswith ('rtsp') or answ.startswith ('plugin'):url = answ
        elif answ.startswith (x[-3].lower()+(x[-4]*2)):url = answ
        elif answ.startswith (x[13].lower()+(x[17]*2)+x[4]):
            killit = (x[13].lower()+(x[17]*2)+x[4])
            begin = (x[-3].lower()+(x[-4]*2)+x[3].lower()+x[-15]+y[0:2]+y[1])
            url = answ.replace(killit,begin)
        else:
            pass
        url = url.replace('/{3,}','//').replace('  ',' ').encode('utf-8')
        #if len(re.search('//',str(url))) != 1: url.split('//').join(url[0],'//',url[1],'/',url[2]) 
        return url
    except:
        return None

def FAN(url):
    fan = 'http://www.streamlord.com/'+str(url)
    
    surl = cloudflare.request(fan)   
    try:
        fanart2 = re.findall("background-image: url\('(.+?)'\)",str(surl))[0]
 
        return fanart2
    except:
        return None    

def genres():
    icon = mediaPath+'Movie.png'
  
    source = cloudflare.request('http://www.streamlord.com/index.html')
 
    source =str(source).replace('\n','').replace('\t','').replace('\r','').replace('amp;','')
    source = source.split('class="dropdown-arrow"')[1].split('id="series-menu"')[0]
    Genres = re.compile('href="(.+?)">(.+?)<').findall(source)
    for gurl, genre in Genres:
        name = genre.upper()
        url = build_url({'mode': 'MOVGEN','name':name, 'url':gurl})
        li = xbmcgui.ListItem('[B]'+name+'[/B]',iconImage=icon)
        li.setProperty('fanart_image', fanart)
        xbmcplugin.addDirectoryItem(handle=thisPlugin,url=url,
                                    listitem=li, isFolder=True)     
    endDir()
    
def latest():
  
    source = cloudflare.request('http://www.streamlord.com/index.html')
        
    source =str(source).replace('\n','').replace('\t','').replace('\r','').replace('amp;','')
    source = source.split('id="tv-serieslist"')[1].split('id="panLeft"')[0]
    Genres = re.compile('href="(watch.+?)"><img src="(.+?)"').findall(source)
    for gurl, thumbs in Genres:
        try:
            thumbs = 'http://www.streamlord.com/'+str(thumbs)+cookie
        except:
            thumbs = 'http://www.streamlord.com/'+thumbs
        name = re.sub('watch-tvshow-|\.html','',gurl).replace('-',' ').upper().encode('utf-8')
        name = " ".join(name.split(' ')[0:-1])
        url = build_url({'mode': 'TVSHOWS','name':name, 'PAGE':gurl})
        li = xbmcgui.ListItem('[B]'+name+'[/B]',iconImage=thumbs)
        li.setProperty('fanart_image', fanart)
        xbmcplugin.addDirectoryItem(handle=thisPlugin,url=url,
                                    listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(thisPlugin)

def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    onetime=response.read()
    response.close()
    onetime = onetime.replace('\n','').replace('\r','')  
    return onetime

def addDirItem(title,icon,fanart,url):
    listitem =xbmcgui.ListItem (title,'','',thumbnailImage=icon)
    listitem.setProperty('fanart_image', fanart)
    xbmcplugin.addDirectoryItem(handle=thisPlugin, url=url,
                                listitem=listitem)
def endDir():
    xbmcplugin.endOfDirectory(thisPlugin)
    
 
if mode is None:
    choose()
    
elif mode[0] == 'MOVIES':
    url = 'http://www.streamlord.com/movies.html?page='+pager
    MOVIES = True
    main(url)

elif mode[0] == "MOVIE GENRES":
    genres()
    
elif mode[0] == "MOVGEN":
    gurl = args['url'][0]
    url = gurl+'?page='+pager
    MOVIES = True
    main(url)
    
elif mode[0] == 'TV SHOWS':
    url = 'http://www.streamlord.com/tvshows.html?page='+pager
    TVSHOWS = True
    MOVIES = False
    main(url)

elif mode[0] == 'TV SHOWS - RECENTLY UPDATED':
    latest()

elif mode[0] == 'SEARCH':
    url ='http://www.streamlord.com/search.html'
    keyboard = xbmc.Keyboard()
    keyboard.setHeading('VIDTIME SEARCH')
    keyboard.doModal()
    if keyboard.isConfirmed(): 
        search = keyboard.getText()
        search = re.sub(r'\W+|\s+','-', search)
    if not keyboard.isConfirmed():
        choose()
    search_data = urllib.urlencode({'search' : search})
  
    REQ = cloudflare.request(url, search_data)
    REQ = REQ.split('<div id="movielist"')[1]
    REQ =REQ.replace('\n','').replace('\t','').replace('\r','').replace('amp;','')
    mort = re.compile('<a href="#"><a href="(.+?)"><img src="(.+?)" /></a>').findall(str(REQ))
    if not mort:choose()
    for name,image in mort:
        if ('tv') in name:
            try:
                image =image+cookie
            except:
                image = image
            items = re.sub('watch-tvshow-|\.html','',name).replace('-',' ').upper().encode('utf-8')
            items = " ".join(items.split(' ')[0:-1])
            url = build_url({'mode': 'TVSHOWS', 'PAGE': name, 'ICON': image, 'NAME': items})
            li = xbmcgui.ListItem('[B]'+ items +'  ([I]TV SERIES[/I] )[/B]',iconImage=image)
            li.setProperty('fanart_image', fanart)
            xbmcplugin.addDirectoryItem(handle=thisPlugin, url=url,
                                        listitem=li, isFolder=True)           
        elif ('watch-movie') in name:
            try:
                image =image+cookie
            except:
                image = image
            items = re.sub('watch-movie-|\.html','',name).replace('-',' ').upper().encode('utf-8')
            items = " ".join(items.split(' ')[0:-1])
            url = build_url({'mode': 'PLAY', 'PAGE': name, 'ICON': image, 'NAME': items})        
            li = xbmcgui.ListItem('[B]'+ items +'[/B]',iconImage=image)  
            li.setProperty('fanart_image', fanart)
            xbmcplugin.addDirectoryItem(handle=thisPlugin, url=url,
                                        listitem=li, isFolder=True)            
    endDir()
  
    
elif mode[0] == 'PLAY':
    stream_page = args['PAGE'][0]
    thumbnailImage = args['ICON'][0]
    Name = args['NAME'][0]
    url = 'http://www.streamlord.com/'+stream_page
  
    REQ = cloudflare.request(url)
    stream = re.compile('true, "file": "(.+?)"}]').findall(str(REQ))
    for i in stream:
        if 'http' in i:
            stream = i
            
        else:pass
    
    stream = re.sub(r'//.+?\.streamlord\.com','//163.172.17.55',stream).encode('utf-8')   
    listitem =xbmcgui.ListItem (Name,'','',thumbnailImage)
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(stream,listitem)
    
elif mode[0] == 'TVSHOWS':
    url = args['PAGE'][0]
    url = 'http://www.streamlord.com/'+url
    TVSHOWS = False
    MOVIES = False
    main(url)
    
elif mode[0] == 'NEXT':
    pager = int(args['PAGE'][0]) + 1
    choice = args['CHOICE'][0]
    pager = str(pager)
    if '?genre' in choice:
        url = choice.split('page=')[0]+'page='+pager
    else:
        url = choice.split('=')[0]+'='+pager
    if re.search('tvshows',str(url),re.I):
        TVSHOWS=True    
    elif re.search('genre',str(url),re.I):
        try:
            sep = url.split('genre-')[1].split('.html?')
            url = 'http://www.streamlord.com/movies.html?genre='+sep[0]+'&'+sep[1]
        except:
            pass
        MOVIES=True
    elif re.search('movies',str(url),re.I):
        MOVIES=True
    else:
        pass
    main(url)

elif mode[0] =="PERCH PICKS - ASSORTED SPORTS" or mode[0] =="ROCKS EPIC FAIL" or mode[0] =="ROCK CONCERT" or mode[0] == "XML":
    
    if "ROCKS" in mode[0]:
        onetime = OPEN_URL('https://www.dropbox.com/s/ibnzr0d4g2ubeyw/Fail.xml?raw=true')
    elif "CONCERT" in mode[0]:
        onetime = OPEN_URL('https://www.dropbox.com/s/rrju6shko3hlg5a/Rock%20Concert.xml?raw=true')
        fanart = re.findall('<fanart>(.+?)</fanart>',str(onetime))[0]
    elif "PERCH" in mode[0]:
        onetime = OPEN_URL('https://www.dropbox.com/s/08u4kw16inm344p/new.xml?raw=true')
    else:
        base = args['base'][0]
        onetime = OPEN_URL(base)
        try:
            fanart = re.findall('<fanart>(.+?)</fanart>',str(onetime))[0]
        except:
            pass
    stuff = re.compile('<title>(.+?)</title><link>(.+?)</link><thumbnail>(.+?)</thumbnail>').findall(str(onetime))
    
    for title, url, icon in stuff:
        
        if not ('http') in url and not ('plugin') in url and not ('rtmp') in url and not ('rstp') in url and not ('base64') in url and len(url) > 2:
            url = english(url)
        if ('base64') in url:
            url = base64.b64decode(url[8:-1])
        if ('youtube') in url and not 'plugin' in url:
            url = build_url({'mode': 'YouTube', 'url':url})
        if ('sawlive') in url:
            url = build_url({'mode': 'sawlive', 'name':title, 'icon':icon, 'url':url})
        if ('p2pcast') in url:
            url = build_url({'mode': 'P2P', 'name':title, 'icon':icon, 'url':url})
        if ('sublink') in url:
            links = re.findall('<sublink>(.+?)</sublink>',str(url))
            for item in links:
                url = item
                addDirItem(title,icon,fanart,url)
                
        else:
            pass
        addDirItem(title,icon,fanart,url)    
    endDir()
    
elif mode[0] =="YouTube":
    url = args['url'][0]
    try:
        xbmc.executebuiltin('PlayMedia(plugin://plugin.video.youtube/play/?video_id='+ url.split('v=')[1]+')')
    except:
        pass
elif mode[0] == "P2P":
    url = args['url'][0]
    Name = args['name'][0]
    thumbnailImage = args['icon'][0]
    from resources.lib.resolvers import p2pcast
    stream = p2pcast.resolve(url)
    listitem =xbmcgui.ListItem (Name,'','',thumbnailImage)
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(stream,listitem)

elif mode[0] == "sawlive":
    url = args['url'][0]
    Name = args['name'][0]
    thumbnailImage = args['icon'][0]
    from resources.lib.resolvers import sawlive
    stream = sawlive.resolve(url)
    listitem =xbmcgui.ListItem (Name,'','',thumbnailImage)
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(stream,listitem)

elif mode[0] =="USTV RIGHT NOW":
    from resources.lib.indexers import ustv
    ustv.RIGHT()
    
elif mode[0] =="VIDTOONS":
    from resources.lib.indexers import vidtoons
    vidtoons.VidToon()
    
elif mode[0] =="VCartoonCraze":
    image = args['image'][0]
    fanart = args['fanart'][0]
    from resources.lib.indexers import vidtoons
    vidtoons.VCartoonCraze(image,fanart)
    
elif mode[0] =="VAnime":
    image = args['image'][0]
    fanart = args['fanart'][0]
    from resources.lib.indexers import vidtoons
    vidtoons.VAnime(image,fanart)

elif mode[0] =="VAalpha": 
    image = args['image'][0]
    fanart = args['fanart'][0]
    from resources.lib.indexers import vidtoons
    vidtoons.VAalpha(image,fanart)

elif mode[0]=="VCalpha":
    image = args['image'][0]
    fanart = args['fanart'][0]
    from resources.lib.indexers import vidtoons
    vidtoons.VCalpha(image,fanart)

elif mode[0]=="VAgenres":
    image = args['image'][0]
    fanart = args['fanart'][0]
    from resources.lib.indexers import vidtoons
    vidtoons.VAgenres(image,fanart)
    
elif mode[0]=="VCgenres":
    image = args['image'][0]
    fanart = args['fanart'][0]
    from resources.lib.indexers import vidtoons    
    vidtoons.VCgenres(image,fanart)

elif mode[0]=="VCcat":
    url = args['url'][0]
    image = args['image'][0]
    fanart = args['fanart'][0]
    from resources.lib.indexers import vidtoons
    vidtoons.VCcat(url, image, fanart)
    
elif mode[0]=="VAcat":
    url = args['url'][0]
    image = args['image'][0]
    fanart = args['fanart'][0]
    from resources.lib.indexers import vidtoons    
    vidtoons.VAcat(url, image, fanart)

elif mode[0]=="VCpart":
    url = args['url'][0]
    image = args['image'][0]
    fanart = args['fanart'][0]
    from resources.lib.indexers import vidtoons
    vidtoons.VCpart(url, image, fanart)
    
elif mode[0]=="VApart":
    url = args['url'][0]
    image = args['image'][0]
    fanart = args['fanart'][0]
    from resources.lib.indexers import vidtoons    
    vidtoons.VApart(url, image, fanart)

elif mode[0]=="VCsearch":
    image = args['image'][0]
    fanart = args['fanart'][0]
    from resources.lib.indexers import vidtoons
    vidtoons.VCsearch(image, fanart)
    
elif mode[0]=="VAsearch":
    image = args['image'][0]
    fanart = args['fanart'][0]
    from resources.lib.indexers import vidtoons    
    vidtoons.VAsearch(image, fanart)

elif mode[0]=="VAstream":
    url = args['url'][0]
    from resources.lib.indexers import vidtoons
    vidtoons.VAstream(url)
    
elif mode[0]=="VCstream":
    url = args['url'][0]
    from resources.lib.indexers import vidtoons    
    vidtoons.VCstream(url)
