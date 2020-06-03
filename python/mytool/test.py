#!/usr/bin/python3.7

ipfile = "/etc/ansible/1040pnode.txt"
DEFAULTPORT = int(32200)


iplist = []
with open(ipfile, "r") as fp:
   for line in fp:
      lineList=line.split()
      ip = lineList[0]
      if len(lineList) == 1:
          port = DEFAULTPORT
      else:
          port = int(lineList[1])

      iplist.append({ip:port})
print(iplist)



alist = [('115.238.122.213', 32200), ('115.238.122.218', 32201)]
for i in alist:
    print(i[0],i[1])