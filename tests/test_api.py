from shadowsocks.api import *

if __name__ == '__main__':
    print (start_server("ab111", 8899, "love", "aes-256-cfb"))
    print (start_server("ab1cc", 8923, "love", "aes-256-cfb"))
    print (start_server("ab1ss", 8353, "love", "aes-256-cfb"))
    import os
    import sys

    pid = os.fork()
    if pid > 0:
        print (pid)
        sys.exit(0)
    stop_server("ab111")
