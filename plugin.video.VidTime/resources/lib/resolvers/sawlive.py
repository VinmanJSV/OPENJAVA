# -*- coding: utf-8 -*-

import re,urllib,urlparse,base64
from resources.lib.modules import client
from resources.lib.modules import jsunpack

def TEST():
    return

def resolve(url):
    
        try:        
                page = re.compile('//(.+?)/(?:embed|v)/([0-9a-zA-Z-_]+)').findall(url)[0]
                page = 'http://%s/embed/%s' % (page[0], page[1])
                
                try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
                except: referer = page
                
                result = client.request(page, referer=referer)
                unpacked = ''
                packed = result.split('\n')
                
                for i in packed: 
                    try: unpacked += jsunpack.unpack(i)
                    except: pass
                result += unpacked
                result = urllib.unquote_plus(result)
                vars = re.compile('var (.+?=".+?");').findall(str(result))
                for item in vars:
                        var = item.split('=')
                
                result = re.sub('\s\s+', ' ', result)
                url = client.parseDOM(result, 'iframe', ret='src')[-1]
                url = url.replace(' ', '').split("'")[0]      
                try:
                        ch = re.compile('ch=""(.+?)""').findall(str(result))[0]
                except:
                        ch = re.compile("ch='(.+?)'").findall(str(result))[0]
                try:
                        sw = re.compile(" sw='(.+?)'").findall(str(result))[0]
                except:
                        sw = re.compile(' sw=""(.+?)""').findall(str(result))[0]

                if ' ' in sw:
                        for item in vars:
                                var = item.replace('"','').replace("'",'').split('=')
                                sw = re.sub(var[0], var[1], str(sw))
                        sw = sw.replace(' ','')
                if ' ' in ch:
                        for item in vars:
                                var = item.replace('"','').replace("'",'').split('=')
                                ch = re.sub(var[0], var[1], str(ch))
                        ch = ch.replace(' ','')
                if len(str(ch)) > len(str(sw)):url = str(url)+str(sw)+'/'+str(ch)
                if len(str(sw)) > len(str(ch)):url = str(url)+str(ch)+'/'+str(sw)

                result = client.request(url, referer=referer)
                
                #file = re.compile("'file'.+?'(.+?)'").findall(result)[0]
                file = re.compile("\('file',(.+?)\)").findall(result)[0]
                file = urllib.unquote_plus(file)
                var2= re.compile("var (.+?) = '(.+?)';").findall(result)
                strm = re.compile("\('streamer', (.+?)\)").findall(result)[0]
                strm =strm.replace("'",'').replace('"','')
                for name, parts in var2:
                        name = name.replace("'",'').replace('"','')
                        parts = parts.replace("'",'').replace('"','')
                        if (name) in file:file = file.replace(name,parts)
                        print file
                        if (name) in strm: strm = parts
                file = file.replace(' ','').replace('"','').replace("'","")

                try:
                    if not file.startswith('http'): raise Exception()
                    url = client.request(file, output='geturl')
                    if not '.m3u8' in url: raise Exception()
                    url += '|%s' % urllib.urlencode({'User-Agent': client.agent(), 'Referer': file})
                    return url
                    
                except:
                    pass

                #strm = re.compile("'streamer'.+?'(.+?)'").findall(result)[0]
                swf = re.compile("SWFObject\('(.+?)'").findall(result)[0]
                
                url = '%s playpath=%s swfUrl=%s pageUrl=%s live=1 timeout=30' % (strm, file, swf, url)
                return url
          
        except:
                return

