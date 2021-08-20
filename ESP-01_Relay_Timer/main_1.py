#ESP-01_Relay

import random
import struct
import time
from machine import Pin,Timer
from micropython import const
from WAVWifi import WAVWireless
import machine
import socket
import usocket as socket

timer=Timer(1)
ditime = 0
dt=0

class CleanBox:
    def __init__(self, name="WAVDisinfect"):
        self.conn_handle = 0
        self.ditime = 0
        self.p0 = Pin(0, Pin.OUT)
        self.p0.value(1)
        self.lock_open = False

def threadFunction(timer):
    print('ozone is activated')
    global cbox
    global dt
    global ditime
    
    if dt>0:
        cbox.p0.value(0)
        dt=dt-1
        
    else:
        cbox.p0.value(1)
        cbox.ditime = 0
        dt=0
        print('lock closed')          


def wavdisinfect():
    global cbox
    global dt
    cbox = CleanBox()
    w = WAVWireless()
    ret = w.scanAndConnect()
    if ret == False:
        ssid = 'ESP_AP'                   
        password = '12345678'
        global ap
        ap = network.WLAN(network.AP_IF)
        ap.active(True)            
        ap.config(essid=ssid, password=password)
        while ap.active() == False:
          pass
        print('Connection is successful')
        print(ap.ifconfig())
        
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(5)
    
    print('listening on', addr)
     
    while True:
        print("hello")
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        request = str(request)
        print('Content = %s' % request)
        sloc = request.find('/?dtime=')
        print(sloc)
        if sloc > 0 and sloc < 50:
            sub = request[sloc:]
            ss = sub.split(' ')
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall("OK")
            conn.close()
            dt = int(ss[0].replace("/?dtime=",""))
            if dt > 0:
                dt=dt*60
            else:
                cbox.p0.value(1)
                dt = 0
        else:
            apidx = request.find('/?wifiap=')
            if apidx > 0:
                sub = request[apidx:]
                ss = sub.split(' ')
                global apname
                data = ss[0].replace("/?wifiap=","")
                fb=open("wifiap.json","w")
                res = data.split(':')
                fdata = "wifiap:"+res[0]+",password:"+res[1]
                fb.write(fdata)
                print("data write",fdata)
                fb.close()
                conn.send('HTTP/1.1 200 OK\n')
                conn.send('Content-Type: text/html\n')
                conn.send('Connection: close\n\n')
                conn.sendall("OK")
                conn.close()
                global ap
                ap.active(False)
                w = WAVWireless()
                ret = w.scanAndConnect()
                if ret == False:
                    print("Error on wifi connection")

timer.init(period=1000,mode=Timer.PERIODIC,callback=threadFunction)
                
if __name__ == "__main__":
    wavdisinfect()
