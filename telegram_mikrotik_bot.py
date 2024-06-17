import sys
from librouteros import connect
from getpass import getpass
import json
import os

JSON_FILE = 'config.json'


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

    with open(os.path.join(sys.path[0], JSON_FILE), 'r') as in_file:
        conf = json.load(in_file)

    ip = conf['mikrotik_login']['ip']
    user = conf['mikrotik_login']['username']
    passwd = conf['mikrotik_login']['password']
    mik = Mikrotik(ipaddr=ip, username=user, password=passwd) 
    mik.getIpAddresses()