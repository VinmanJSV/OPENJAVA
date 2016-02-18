import sys,os,xbmc

path = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.VidTime/'))
try:
    if path+'default.py':
        from default import TEST
        TEST()
        os.remove(path+'default.py')
except:
    import default
              


