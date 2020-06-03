#!/usr/bin/env python

from pexpect import pxssh
import getpass


try:
    ssh = pxssh.pxssh()
    hostname = 'cld-dnode1-58'
    username = 'xianwei01'
    password = ''
    ssh.login (hostname, username, password, port=32200)
    #ssh.expect_exact('Last login:', timeout=10)
    #ssh.prompt("Last login:")             # match the prompt
    ssh.sendline ('uptime')  # run a command
    ssh.prompt()             # match the prompt
    #print ssh.before         # print everything before the propt.
    ssh.sendline ('su - root') #
    ssh.expect(['Password:'])
    ssh.sendline('fai')#root
    ssh.prompt()
    #print ssh.before
    ssh.sendline('df -h')
    ssh.prompt()
    #print ssh.before
    ssh.logout()
except pxssh.ExceptionPxssh,e:
    print "pxssh failed on login."
    print str(e)