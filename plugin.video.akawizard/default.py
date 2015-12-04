import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os
import shutil
import urllib2,urllib
import re
import extract
import downloader
import time
import subprocess
import platform

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
base='http://167.114.14.194/Kodi/Wizard/tools/'
ADDON=xbmcaddon.Addon(id='plugin.video.akawizard')
INTRO = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.akawizard/Animal.mp4'))  
  
VERSION = "2.0.6"
PATH = "AKA Wizard"


def INTROS():
    xbmcaddon.Addon(id='plugin.video.akawizard').openSettings()
    
    if ADDON.getSetting('intro') == "true":
        xbmcPlayer=xbmc.Player()
        xbmcPlayer.play(INTRO)
        ADDON.setSetting('intro','false')
    else:
        pass
        if ADDON.getSetting('message') == "true":
            intro=xbmcgui.Dialog()
            msg = intro.ok("AKAWIZARD", "[COLOR orange]AUTOMATICALLY INSTALLS THE BUILDS!",
                            "MOST DEVICES REBOOT TO YOUR NEW BUILD",
                            "ENJOY ALL AKA WIZARD BUILDS. THANK-YOU. [/COLOR]")
            if msg == "ok":
                ADDON.setSetting('message','false')
            else:
                pass
        else:
            pass      
    


def CATEGORIES():                      
    link = OPEN_URL('https://github.com/AKODI1/1/blob/master/zips/wizard.txt?raw=true').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        addDir(name,url,1,iconimage,fanart,description)
    setView('movies', 'MAIN')
    
                
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
               
                
def wizard(name,url,description):
    
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    dp = xbmcgui.DialogProgress()
    dp.create("AKAWIZARD","[COLOR red]Downloading.... Please Wait[/COLOR]")
    lib=os.path.join(path, name+'.zip')
    try:
        os.remove(lib)    
    except:
        pass
                       
    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://home'))
    time.sleep(2)
    dp.update(0,"[COLOR red]Downloading.... [COLOR green]DONE![/COLOR]" ,"[COLOR yellow]Extracting Zip.... Please Wait[/COLOR]")
    print '======================================='
    print addonfolder
    print '======================================='
    a = platform.release()
    print str(a)
    win = "0"
    if os.name == "nt":
        print "WINDOWS" 
        if str(a) != "7":
            print "NOT WINDOWS 7"
            win = "1"
            here = xbmc.translatePath(os.path.join('special://home/addons/packages/PARK'))
            try:
                shutil.rmtree(here, ignore_errors=True)
            except:
                pass         
                        
            there = xbmc.translatePath(os.path.join('special://home/addons/packages/PARK/*'))    
                        
            extract.all(lib,here,dp)
            dp.update(0,"[COLOR red]Downloading.... [COLOR green]DONE![/COLOR]", "[COLOR yellow]Extracting Zip.... [COLOR green]DONE![/COLOR]", "[COLOR green]KODI WILL RESTART AUTOMATICALLY.....Please Wait![/COLOR]")         
            subprocess.call('XCOPY '+there + ' ' + addonfolder + ' /S /E /R /C /Y', shell=True)
            ADDON.setSetting('intro','true')
            if addonfolder[-5:] == "TVMC\\":
                subprocess.call('cd \Program Files (x86)\TVMC & taskkill /F /IM TVMC.exe & start TVMC.exe', shell=True)
            elif addonfolder[-5:] == "Kodi\\":
                subprocess.call('cd \Program Files (x86)\Kodi & taskkill /F /IM Kodi.exe & start Kodi.exe', shell=True)
            else:
                pass
        elif str(a) == "7":
            print "WINDOWS 7"
            dp.update(0,"[COLOR red]Downloading.... [COLOR green]DONE![/COLOR]","[COLOR yellow]Extracting Zip.... [COLOR green]PLease Wait[/COLOR]","[COLOR green]KODI WILL REBOOT AUTOMATICALLY.....Please Wait![/COLOR]")
            extract.all(lib,addonfolder,dp)
            ADDON.setSetting('intro','ture')
            if addonfolder[-5:] == "TVMC\\":
                subprocess.call('cd \Program Files (x86)\TVMC & taskkill /F /IM TVMC.exe & start TVMC.exe ', shell=True)
            elif addonfolder[-5:] == "Kodi\\":
                subprocess.call('cd \Program Files (x86)\Kodi & taskkill /F /IM Kodi.exe & start Kodi.exe', shell=True)
            else:
                pass    
        else:
            pass
    else:
        pass                     
    if os.name != "nt":
        if ADDON.getSetting('UNIT') == "1":                    
            print "OE"
            dp.update(0,"[COLOR red]Downloading.... [COLOR green]DONE![/COLOR]","[COLOR yellow]Extracting Zip.... [COLOR green]PLease Wait[/COLOR]","[COLOR green]KODI WILL REBOOT AUTOMATICALLY.....Please Wait![/COLOR]")
            extract.all(lib,addonfolder,dp)
            ADDON.setSetting('intro','true')
            print "NOT WINDOWS"
            subprocess.call('pkill -9 kodi && systemctl start kodi',shell=True)
                
        elif ADDON.getSetting('UNIT') == "2":
            dp.update(0,"[COLOR red]Downloading.... [COLOR green]DONE![/COLOR]","[COLOR yellow]Extracting Zip.... [COLOR green]PLease Wait[/COLOR]","[COLOR green]KODI WILL REBOOT AUTOMATICALLY.....Please Wait![/COLOR]")
            extract.all(lib,addonfolder,dp)
            ADDON.setSetting('intro','true')
            print "NOT WINDOWS"
            os.system("su -c 'reboot'")

        elif ADDON.getSetting('UNIT') == "3":
            dp.update(0,"[COLOR red]Downloading.... [COLOR green]DONE![/COLOR]","[COLOR yellow]Extracting Zip.... [COLOR green]PLease Wait[/COLOR]","[COLOR green]KODI WILL REBOOT AUTOMATICALLY.....Please Wait![/COLOR]")
            extract.all(lib,addonfolder,dp)
            ADDON.setSetting('intro','true')
            print "NOT WINDOWS"
            subprocess.call('pkill -9 kodi && kodi',shell=True)
        elif ADDON.getSetting('UNIT') == "4":
            dp.update(0,"[COLOR red]Downloading.... [COLOR green]DONE![/COLOR]","[COLOR yellow]Extracting Zip.... [COLOR green]PLease Wait[/COLOR]","[COLOR green]KODI WILL REBOOT AUTOMATICALLY.....Please Wait![/COLOR]")
            extract.all(lib,addonfolder,dp)
            ADDON.setSetting('intro','true')
            print "NOT WINDOWS"
            cmd = "killall \-9 \Kodi && open \-a \Kodi"
            os.system(cmd)
        else:
            dialog = xbmcgui.Dialog()
            dialog.ok("AKAWIZARD", "Now Please Press Ok Then UNPLUG UNIT", "[COLOR red]ENJOY ALL AKA WIZARD BUILDS. THANK-YOU. [/COLOR]")
            pass
                
    else:
        dialog = xbmcgui.Dialog()
        dialog.ok("AKAWIZARD", "Now Please Press Ok Then UNPLUG UNIT", "[COLOR red]ENJOY ALL AKA WIZARD BUILDS. THANK-YOU. [/COLOR]")
        pass            
                  
                    
                
def addDir(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
                    
                   
                    
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                            
        return param
                    
                                  
params=get_params()
url=None
name=None
mode=None
iconimage=None
fanart=None
description=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
                    
                    
print str(PATH)+': '+str(VERSION)
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)


def setView(content, viewType):
    # set content type so library shows more views and info
                
    if content:                   
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )
        
      
if mode==None or url==None or len(url)<1:       
        INTROS()
        CATEGORIES()       
        
elif mode==1:
        wizard(name,url,description)
        
                    
                    

                    
xbmcplugin.endOfDirectory(int(sys.argv[1]))


