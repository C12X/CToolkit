
# CToolkit

---
　　CToolkit是一款面向安全行业从业者的渗透测试工具集系统，由三大功能模块组成：资产整理、漏洞利用、笔记，主要实现了主机开放端口及服务信息的收集，已知web应用漏洞的利用，以及测试过程中的有用信息记录，涵盖了渗透测试的几个重要的步骤。
## Install & Launch
>以下命令均在命令行完成

安装python3所需模块

```
pip install -r requirements.txt
```

安装nmap

```
apt install nmap
```

安装及运行celery

```
apt install celery
celery worker -A celery_runner -l info
```

安装及运行mongodb

```
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6
```

```
echo "deb [ arch=amd64,arm64 ] http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
```

```
apt update
```

```
apt install -y mongodb-org
```

```
service mongod start
```

安装redis

```
apt install redis-server
service redis-server start
```

修改manage.py的绑定ip地址

```
manager.add_command("server", Server(host="指定主机"))
```

启动Flask

```
python3 manage.py server
```

最后浏览器访问http://主机:5000/即可

## Modules

### 0x01 Projects ###
>资产整理是针对目标网络主机的信息收集，探测并记录主机开放的端口及服务，信息收集是渗透测试的第一步，如果在前期没有收集到足够多的信息，将会影响到渗透测试的后续操作，端口及开放服务信息是渗透测试过程中的重要突破口。本系统将会实现对目标主机的开放端口服务及信息的扫描功能。

### 0x02 Vulnerability ###
>漏洞利用是利用已知的应用漏洞，对目标web应用可能存在的利用点进行检测与利用，检测并成功利用漏洞，是渗透测试出报告的重要凭据，根据对应web应用漏洞的通性，利用相同的有效载荷可以对相同web应用系统进行检测。本系统将会实现web应用漏洞有效载荷的存储与利用，用以检测多种web应用系统的漏洞。

### 0x03 Note ###
>随手笔记是在记录渗透测试过程中有用信息的模块，针对手动测试过程中发现的多种潜在可利用线索进行记录（包括图片与文字），需要随时做好笔记，方便更深入检测工作的进行。本系统将使用WYSIWYG（所见即所得）编辑器作为随手笔记模块对渗透测试过程中发现的有用信息进行记录。