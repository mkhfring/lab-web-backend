#!/home/mohamad/.virtualenvs/kiosk_user/bin/python3
#!/usr/bin/python3

import sys
import json
#from websocket import create_connection
import websocket
# sdb1 /dev/disk/by-path/pci-0000:00:14.0-usb-0:3:1.0-scsi-0:0:0:0 add'
print("ok")
# lsblk_command = "lsblk -f |grep media |awk '{print $1 $NF}' |tr -dc 'A-Za-z_1-9/'"

DEVPATH = "/dev/%s" % sys.argv[1]
try:

    # if sys.argv[3] in ["add", "remove"]:

#    ws = create_connection("ws://localhost:9090/")
    ws = websocket.WebSocket()
    ws.connect("ws://0.0.0.0:9989/")
    ws.send(json.dumps(
        {"cmd": 'normal_print', "path": sys.argv[1], "action": sys.argv[2], "from": "usb"}))
    result = ws.recv()
    ws.close()
except Exception as er:
    print("aaaaaaaaaa %s" % str(er))
    pass


# ws = create_connection("ws://localhost:9090/")
# ws.send(json.dumps(
#     {"cmd": sys.argv[1], "path": sys.argv[2], "mount": sys.argv[3], "action": sys.argv[4]}))
# result = ws.recv()
# print("Received '%s'" % result)
# ws.close()
