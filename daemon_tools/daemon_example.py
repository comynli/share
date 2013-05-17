#!/usr/bin/python
# encoding=utf-8

import sys
import os
import signal
import posix

def daemon(func, *args, **kwargs):
    # 忽略进程
    signal.signal(signal.SIGTTOU, signal.SIG_IGN) # SIGTTOU 后台进程写控制终端
    signal.signal(signal.SIGTTIN, signal.SIG_IGN) # SIGTTIN 后台进程读控制终端
    signal.signal(signal.SIGTSTP, signal.SIG_IGN) # SIGTSTP 终端挂起
    signal.signal(signal.SIGHUP, signal.SIG_IGN)  # SIGHUP  进程组长发送的终止进程

    try:
        # 退出父进程
        if os.fork() > 0:
            os._exit(0) 
    except OSError, error:
        print 'fork #1 failed: %d (%s)' % (error.errno, error.strerror)
        os._exit(1)

    # 切换工作目录
    os.chdir('/')
    # 脱离控制终端、登录会话和进程组
    os.setsid()
    # 设置umask
    os.umask(0)

    # 禁止进程重新打开控制终端, 二次fork实现，结束第一子进程，第二子进程继续（第二子进程不再是会话组长）
    try:
        if os.fork() > 0:
            os._exit(0)
    except OSError, error:
        print 'fork #1 failed: %d (%s)' % (error.errno, error.strerror)
        os._exit(1)

    # 关闭打开的文件描述符， 输入 输出和错误除外
    os.closerange(3, posix.sysconf('SC_OPEN_MAX'))

    # 重定向 输入、输出和错误
    null_in = open('/dev/null').fileno()
    null_out = open('/dev/null', 'w').fileno()
    os.dup2(sys.stdin.fileno(), null_in)
    os.dup2(sys.stdout.fileno(), null_out)
    os.dup2(sys.stderr.fileno(), null_out)

    # 处理SIGCHLD信号
    signal.signal(signal.SIGCHLD, handlerSIGCHLD)

    # 实际处理
    func(*args, **kwargs)


def handlerSIGCHLD():
    os.waitpid(-1, os.WNOHANG)

def funzioneDemo():
    import time

    fd = open('/tmp/demone.log', 'a')
    while True:
        fd.write(time.ctime()+'\n')
        fd.flush()
        time.sleep(2)
    fd.close()

if __name__ == '__main__':
    daemon(funzioneDemo)
