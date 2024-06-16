from librouteros import connect
from getpass import getpass
import json

ip_address = ["192.168.1.254"]
user = 'admin'
passw = getpass()
for ip in ip_address:
    api = connect(username=user, password=passw, host=ip)
    ip_info = api(cmd="/ip/address/print")
    a = tuple(ip_info)
    # This also will work, as well as anything else you can do with iterables
    for item in a:
        print(item)


interfaces = api.path('interface')

#for item in interfaces:
    #print(item)