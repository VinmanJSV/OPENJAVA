#!/bin/sh 
# CREATE AUTOSTART FILE
echo "#!/bin/sh" > /storage/.config/autostart.sh && chmod +x /storage/.config/autostart.sh
cat >> /storage/.config/autostart.sh << EOF
sleep 10
/usr/bin/python /storage/.kodi/addons/plugin.video.phstreams/FuckNeulionService.py &
exit 0
EOF
# SET ETC/HOSTS
cat >> /storage/.config/hosts.conf << EOF
127.0.0.1      nlsk.neulion.com
EOF

echo "REMEMBER TO CHANGE WEBSERVER TO PORT 8080"




