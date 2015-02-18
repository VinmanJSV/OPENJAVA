import sys
import subprocess
subprocess.call("chmod +x /storage/.kodi/addons/plugin.program.prometheusjava/autophs.sh", shell=True)
subprocess.call("/storage/.kodi/addons/plugin.program.prometheusjava/autophs.sh", shell=True)

import xbmcaddon
import xbmcgui
addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
 

line1 = "INSTALLED Java on OpeneELEC PROMETHEUS KODI ONLY!!!!!"
line2 = "ALL NECESARY FILES FOR PHEONIX HOCKEY....DONE!!!!"
line3 = "REBOOT AND ENJOY!!"

xbmcgui.Dialog().ok(addonname, line1, line2, line3)
