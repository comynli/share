% 大众点评技术保障
% xueming.li
% May 17, 2013

# Daemon Tools 使用简介

* 什么是Daemon
* 如何实现Daemon
* 如何使用daemon tool 管理daemon
* daemon tools常见错误与排查

# 什么是Daemon

Daemon是unix上的后台进程，通常翻译为守护进程

---------------------------
Daemon的特点：

* Daemon忽略终端相关的信号，例如 `SIGTTOU`,`SIGTTIN`,`SIGTSTP`,`SIGHUP`
* Daemon需要进入后台执行，即父进程为`init`进程。
* Daemon需要脱离控制终端、登录会话和进程组。
* Daemon一般禁止重新打开控制终端
* Daemon一般需要关闭文件描述符，重定向标准输入、输出和错误
* Daemon需要处理SIGCHLD信号，不然会产生僵尸进程


# 如何实现Daemon
详见代码

# 如何使用daemon tool 管理daemon
* supervise
* svc
* svscanboot
* svscan

# daemon tools常见错误与排查