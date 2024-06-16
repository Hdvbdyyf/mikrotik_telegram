from librouteros import connect
from getpass import getpass
import json


class Mikrotik:
    def __init__(self, ipaddr, username, password):
        self.ip = ipaddr
        self.user = username
        self.password = password
        self.con = self.connect()

    def connect(self):
        return connect(username=self.user, password=self.password, host=self.ip)

    def getIpAddresses(self):
        ip_info = self.con(cmd="/ip/address/print")
        a = tuple(ip_info)
        # This also will work, as well as anything else you can do with iterables
        for item in a:
            print(item)

    def getInterfaces(self):
        interfaces = self.con.path('interface')



if __name__ == "__main__":

    mik = Mikrotik(ipaddr='192.168.1.254', username='admin', password='demo') 
    mik.getIpAddresses()