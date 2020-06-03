#!/usr/bin/env bas

#

### BEGIN INIT INFO

# Provides:          lbc
# Required-Start:    $remote_fs $network $time $syslog
# Required-Stop:     $remote_fs $network $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: LBC VIP
# Description:       Script for add LBC VIP
### END INIT INFO
#Author: IGI
#Update: 20180427


# vip list

#VIP="10.200.75.182"
conf="/home/cld/conf/cld.cfg"
VIP=$(awk -F= '/kmastervip/{print $NF}' ${conf})
if [ -z "${VIP}" ];then
    echo "kmaster VIP address is NULL"
    exit 1
fi


do_start() {
    for ip in $VIP
            do
                # add vip to tunnel
                /sbin/ip addr add ${ip}/32 brd $ip scope global dev tunl0
                ipset add MY_IPS ${ip}
        #modify mss, define in fwrule
        #iptables -I OUTPUT 1 -s $ip/32 -p tcp -m tcp --tcp-flags SYN,RST,ACK SYN,ACK -j TCPMSS --set-mss 1440
    done
    /sbin/ifconfig tunl0 up
    # enable arp ignore
    echo "1" >/proc/sys/net/ipv4/conf/tunl0/arp_ignore
    echo "2" >/proc/sys/net/ipv4/conf/tunl0/arp_announce
    echo "0" >/proc/sys/net/ipv4/conf/tunl0/rp_filter
    echo "1" >/proc/sys/net/ipv4/conf/all/arp_ignore
    echo "2" >/proc/sys/net/ipv4/conf/all/arp_announce
    echo "0" >/proc/sys/net/ipv4/conf/all/rp_filter
    echo "RealServer Start OK"
}

do_stop() {
    for ip in $VIP
            do
                # remove vip from realserver lo
                /sbin/ip addr del ${ip}/32 dev tunl0
    done
    /sbin/ifconfig tunl0 down

    # disable arp ignore
    echo "0" >/proc/sys/net/ipv4/conf/tunl0/arp_ignore
    echo "0" >/proc/sys/net/ipv4/conf/tunl0/arp_announce
    echo "1" >/proc/sys/net/ipv4/conf/tunl0/rp_filter
    echo "0" >/proc/sys/net/ipv4/conf/all/arp_ignore
    echo "0" >/proc/sys/net/ipv4/conf/all/arp_announce
    echo "1" >/proc/sys/net/ipv4/conf/all/rp_filter
    echo "RealServer Stoped"
}

do_status() {
    ip addr list tunl0
    sysctl net.ipv4.conf.tunl0.arp_ignore net.ipv4.conf.tunl0.arp_announce net.ipv4.conf.tunl0.rp_filter net.ipv4.conf.all.arp_ignore net.ipv4.conf.all.arp_announce net.ipv4.conf.all.rp_filter
}

case $1 in
            start)
                do_start
                ;;
            stop)
                do_stop
                ;;
            status)
                do_status
                ;;
            *)
                echo "Usage: $0 [start|stop|status]"
        ;;
esac