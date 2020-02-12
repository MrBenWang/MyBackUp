# 在centos7 安装 mysql5.7

``` shell
wget https://dev.mysql.com/get/mysql57-community-release-el7-11.noarch.rpm
sudo rpm -Uvh mysql57-community-release-el7-11.noarch.rpm
yum repolist all | grep mysql
yum install mysql-community-server
systemctl start mysqld 
systemctl status mysqld

sudo grep 'temporary password' /var/log/mysqld.log  #查看mysql 临时密码
mysql -uroot -p  # 输入查看到的密码
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'mysql@2020';
mysql> SHOW VARIABLES LIKE 'validate_password%';  #修改密码策略
mysql> SET global validate_password_policy=LOW;

mysql> USE mysql; -- 切换到 mysql DB
mysql> SELECT User, Host FROM user; -- 查看现有用户及允许连接的主机
mysql> GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'mysql@2020' WITH GRANT OPTION; #允许远程连接
mysql> flush privileges;

#修改 mysql 配置项
nano /ect/my.cnf
character_set_server=utf8
init_connect='SET NAMES utf8'
port=12306

systemctl restart mysqld

#开启防火墙
firewall-cmd --list-ports
firewall-cmd --zone=public --add-port=12306/tcp --permanent
firewall-cmd --reload
```

--脚本生成表
CREATE DATABASE DB_TEST;
USE DB_TEST;
source MySQL.sql;
