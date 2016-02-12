# -*- coding: utf-8 -*-
# VinMan_JSV 2016

import os,re,urllib,urllib2,xbmcplugin,xbmcgui,xbmcaddon,xbmc,urlparse,cookielib

thisPlugin = int(sys.argv[1])
base_url = sys.argv[0]
args = urlparse.parse_qs(sys.argv[2][1:])
mode = args.get('mode', None)
addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
ADDON = xbmcaddon.Addon(id='plugin.video.VidTime')
USER = ADDON.getSetting('USER')
PASS = ADDON.getSetting('PASS')
EMAIL = ADDON.getSetting('EMAIL')
REGISTER = ADDON.getSetting('REGISTER')
path = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.VidTime/'))
usdata=xbmc.translatePath(os.path.join('special://userdata/addon_data/plugin.video.VidTime/'))
mediaPath = path +"resources/media/"
fanart = (path + 'fanart.jpg')
icon = (path + 'icon.png')
icon2 = mediaPath+'Search.png'
pager = '1'
cj = cookielib.LWPCookieJar()
cookiepath = (usdata+'cookies.lwp')

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1')]
cookiepath = (usdata+'cookies.lwp')
login_data =urllib.urlencode({'username' : USER,
                              'password' : PASS,
                              'submit' : 'Login'
                              })
register_data =urllib.urlencode({'username' : USER,
                                 'password' : PASS,
                                 'email': EMAIL,
                                 'submit' : 'Register'
                                })
TVSHOWS = None
MOVIES= None

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def REG():
    if os.path.exists(cookiepath):os.remove(cookiepath)
    try:
        req1 = opener.open('http://www.streamlord.com/register.php', register_data)
        source = req1.read()
        req1.close()
        print "REGISTER PAGE"
        line1 = 'Username already used.'
        if re.search(line1 ,source, re.I):
            xbmcgui.Dialog().ok(addonname,line1)
            return
    except:
        pass   
    ADDON.setSetting('REGISTER','false')
        
def choose():
    cats = ['MOVIES','MOVIE GENRES','TV SHOWS','TV SHOWS - RECENTLY UPDATED','SEARCH']
    for name in cats:
        url = build_url({'mode': name})
        li = xbmcgui.ListItem('[B]'+name+'[/B]',iconImage=icon)
        if 'SEARCH' in name:li = xbmcgui.ListItem('[B]'+name+'[/B]',iconImage=icon2)
        li.setProperty('fanart_image', fanart)
        xbmcplugin.addDirectoryItem(handle=thisPlugin,url=url,
                                    listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(thisPlugin)
    
def main(url):
    choice = url
    SITE = opener.open(url)
    REQ = SITE.read()
    SITE.close()
    REQ =REQ.replace('\n','').replace('\t','').replace('\r','').replace('amp;','')

    if  TVSHOWS == False:
        page = re.compile('<ul id="improved">(.+?)</ul>').findall(str(REQ))
        title = re.compile('<a href="(.+?)"><img src="http://www.streamlord.com/(.+?)"></a>').findall(str(page))
    else:
        page = re.compile('<li class="movie">(.+?)</li>').findall(str(REQ))
        title = re.compile('<a href="(.+?)"><img src="(.+?)" ').findall(str(page))
    for t,i in title:
        icon_site = 'http://www.streamlord.com/'+i

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

def login_page():
    try:
        req1 = opener.open('http://www.streamlord.com/login.html', login_data)
        source = req1.read()
        req1.close()
        cj.save(filename=cookiepath, ignore_discard=False, ignore_expires=False)
    except:
        pass
       
def main_page():   
    login_page()            
    try:
        req2 = opener.open('http://www.streamlord.com/index.html')
        source2 = req2.read()
        req2.close()    
    except:
        pass
    logged_in_string = "Log out"
    if re.search(logged_in_string,source2,re.I):
        if not os.path.exists(cookiepath):   
            cj.save(filename=cookiepath, ignore_discard=False, ignore_expires=False)
        else:
            pass
    else:
        if os.path.exists(cookiepath):os.remove(cookiepath)
        ADDON.openSettings()
        return False
    
def search():
    url ='http://www.streamlord.com/search.html'
    SITE = opener.open(url, search_data)
    REQ = SITE.read()
    SITE.close()
    REQ = REQ.split('<div id="movielist"')[1]
    REQ =REQ.replace('\n','').replace('\t','').replace('\r','').replace('amp;','')    
    mort = re.compile('<a href="#"><a href="(.+?)"><img src="(.+?)" /></a>').findall(str(REQ))    
    for name,image in mort:
        li = xbmcgui.ListItem('[B]'+ name +'[/B]',iconImage=image)
        li.setProperty('fanart_image', fanart)
        xbmcplugin.addDirectoryItem(handle=thisPlugin, url=url,
                                    listitem=li, isFolder=True)   
    xbmcplugin.endOfDirectory(thisPlugin)       

def genres():
    icon = mediaPath+'Movie.png'
    req = opener.open('http://www.streamlord.com/index.html')
    source = req.read()
    req.close()
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
    xbmcplugin.endOfDirectory(thisPlugin)   
        
def latest():
    req = opener.open('http://www.streamlord.com/index.html')
    source = req.read()
    req.close()
    source =str(source).replace('\n','').replace('\t','').replace('\r','').replace('amp;','')
    source = source.split('id="tv-serieslist"')[1].split('id="panLeft"')[0]
    Genres = re.compile('href="(watch.+?)"><img src="(.+?)"').findall(source)
    for gurl, thumbs in Genres:
        thumbs = 'http://www.streamlord.com/'+thumbs
        name = re.sub('watch-tvshow-|\.html','',gurl).replace('-',' ').upper().encode('utf-8')
        name = " ".join(name.split(' ')[0:-1])
        url = build_url({'mode': 'TVSHOWS','name':name, 'PAGE':gurl})
        li = xbmcgui.ListItem('[B]'+name+'[/B]',iconImage=thumbs)
        li.setProperty('fanart_image', fanart)
        xbmcplugin.addDirectoryItem(handle=thisPlugin,url=url,
                                    listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(thisPlugin)

if not USER == "" and not REGISTER == 'true':
    main_page()
else:
    ADDON.openSettings()   
if REGISTER == 'true':REG()  
if os.path.exists(cookiepath):
    cj.load(filename=cookiepath, ignore_discard=False, ignore_expires=False)    
else:
    pass

 
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
    SITE = opener.open(url, search_data)
    REQ = SITE.read()
    SITE.close()
    REQ = REQ.split('<div id="movielist"')[1]
    REQ =REQ.replace('\n','').replace('\t','').replace('\r','').replace('amp;','')
    mort = re.compile('<a href="#"><a href="(.+?)"><img src="(.+?)" /></a>').findall(str(REQ))
    if not mort:choose()
    for name,image in mort:
        if ('tv') in name:
            items = re.sub('watch-tvshow-|\.html','',name).replace('-',' ').upper().encode('utf-8')
            items = " ".join(items.split(' ')[0:-1])
            url = build_url({'mode': 'TVSHOWS', 'PAGE': name, 'ICON': image, 'NAME': items})
            li = xbmcgui.ListItem('[B]'+ items +'  ([I]TV SERIES[/I] )[/B]',iconImage=image)
            li.setProperty('fanart_image', fanart)
            xbmcplugin.addDirectoryItem(handle=thisPlugin, url=url,
                                        listitem=li, isFolder=True)           
        elif ('watch-movie') in name:
            items = re.sub('watch-movie-|\.html','',name).replace('-',' ').upper().encode('utf-8')
            items = " ".join(items.split(' ')[0:-1])
            url = build_url({'mode': 'PLAY', 'PAGE': name, 'ICON': image, 'NAME': items})        
            li = xbmcgui.ListItem('[B]'+ items +'[/B]',iconImage=image)
            li.setProperty('fanart_image', fanart)
            xbmcplugin.addDirectoryItem(handle=thisPlugin, url=url,
                                        listitem=li, isFolder=True)            
    xbmcplugin.endOfDirectory(thisPlugin)
    
elif mode[0] == 'PLAY':
    stream_page = args['PAGE'][0]
    thumbnailImage = args['ICON'][0]
    Name = args['NAME'][0]
    url = 'http://www.streamlord.com/'+stream_page
    SITE = opener.open(url)
    REQ = SITE.read()
    SITE.close()
    stream = re.compile('"file": "(.+?)"}]').findall(str(REQ))[1]
    if 'http' in stream:
        pass
    elif not 'http' in stream:
        stream = re.compile('"file": "(.+?)"}]').findall(str(REQ))[0]
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
        print url
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




