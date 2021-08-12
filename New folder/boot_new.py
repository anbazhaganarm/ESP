try:
 import usocket as socket        

except:
 import socket

import network            
import esp
from time import sleep
from machine import Pin

esp.osdebug(None)
import gc
gc.collect()
j=0
flag=0
def station():
    print("station function")
    ssid ='ArginAnbu'
    password ='Anbu8122'

    station = network.WLAN(network.STA_IF)

    station.active(True)
    station.connect(ssid, password)

    #while station.isconnected() == False:
    sleep(10)
    if station.isconnected() == True:
        print('Station Mode Connection successfull')
        print(station.ifconfig())
        led = Pin(2, Pin.OUT)
        return True
    else:
        return False
    
if j == False:
    print('AP Mode Connection successfull')
    #station.active(False)
    
    ssid = 'ESP_AP'                   
    password = '12345678'
    
    ap = network.WLAN(network.AP_IF)
    ap.active(True)            
    ap.config(essid=ssid, password=password)

    while ap.active() == False:
      pass
    print('Connection is successful')
    print(ap.ifconfig())
    
    
def web_page():
    
    ''' print("web page load")
    html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
    <body><h1>Welcome to NEEVEE!</h1></body></html>"""
    return html'''
    html = """<html><head> <title>ESP Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
    h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
    border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
    .button2{background-color: #4286f4;}</style></head><body> <h1>ESP Web Server</h1> 
    <p>GPIO state: <strong></strong></p><p><a href="/?check"><button class="button">Check Wifi</button></a></p>
    </body></html>"""
    return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
s.bind(('', 80))
s.listen(5)
    
while True:
    print("Hello")
    conn, addr = s.accept()
    print("waiting")
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request=str(request)
        
    print('Content = %s' % str(request))
    sta = request.find('/?check')
    #led_off = request.find('/?led=off')
    if(sta == 6):
        flag=station()
    response = web_page()
    conn.send(response)
    conn.close()
    if flag == True:
        print("loop will end")
        break;
          