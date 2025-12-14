import network
import time
import urequests

class WifiManager:
    def __init__(self, log=True):
        self.log = log
        
        self.__sta_if = network.WLAN(network.STA_IF)
        self.__sta_if.active(False)
        
    def connect(self, ssid, password="", timeout=10):
        if self.isconnected():
            self.console("Already connected:", self.get_ip())
            return True

        self.console(f"Connecting to WiFi: {ssid}")

        self.__sta_if.active(True)
        self.__sta_if.connect(ssid, password)

        start = time.time()

        while not self.isconnected():
            if time.time() - start > timeout:
                if self.log:
                    print()
                self.console("Connection timeout")
                return False

            if self.log:
                print(".", end="")
            time.sleep(0.5)
        
        if self.log:
            print()
        self.console("Connected! IP:", self.get_ip())
        return True

    
    def scan(self):
        self.__sta_if.active(True)
        networks = self.__sta_if.scan()
        
        results = []
        for net in networks:
            ssid = net[0].decode()
            rssi = net[3]
            auth = net[4]
            results.append({
                "ssid": ssid,
                "rssi": rssi,
                "auth": auth
            })

        return results

    def request(self, method, url, **kw):
        allowed_methods = ("HEAD", "GET", "POST", "PUT", "PATCH", "DELETE")
        method = method.upper()
        
        reqs = {
            "HEAD": urequests.head,
            "GET": urequests.get,
            "POST": urequests.post,
            "PUT": urequests.put,
            "PATCH": urequests.patch,
            "DELETE": urequests.delete
        }
        
        if method not in allowed_methods:
            raise Exception(f'Method "{method}" not allowed')
        
        return reqs[method](url, **kw)
        
        
        
    def isconnected(self):
        return self.__sta_if.isconnected()
    
    def get_ip(self):
        if self.isconnected():
            return self.__sta_if.ifconfig()[0]
        return None
    
    def get_mac(self):
        mac = self.__sta_if.config('mac')
        return ':'.join('{:02X}'.format(b) for b in mac)

    def console(self, *args):
        if self.log:
            print("[ WIFI ]", *args)