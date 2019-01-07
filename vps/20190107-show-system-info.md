# 一些系统 信息

## 系统信息(硬件)

dmidecode       #系统信息，汇总
dmidecode|grep "System Information" -A9|egrep  "Manufacturer|Product|Serial"        #查看服务器型号、序列号
dmidecode |grep -A16 "System Information$"      #查看主板型号
dmidecode -t bios       #查看BIOS信息
dmidecode -t memory       #查看内存槽及内存条
dmesg | grep -i Ethernet        #查看网卡信息
lspci | head -10        #查看pci信息，即主板所有硬件槽信息

## 系统信息(软件)

uname -a        #版本
hostname        #计算机名
env             #环境变量
uptime          #当前时间，运行了多久，多少个用户，平均系统负载时间
cat /proc/loadavg       #直接查看平均负载情况。【0.00 0.01 0.05 4/524 7152】 除了前3个数字表示平均进程数量外，后面的1个分数，分母表示系统进程总数，分子表示正在运行的进程数；最后一个数字表示最近运行的进程ID

w       #活动用户
id root     #用户信息

## cpu

cat /proc/cpuinfo       #cpu信息  
lscpu       #容易读的cpu信息 来自 /proc/cpuinfo
cat /proc/cpuinfo| grep "physical id"| sort| uniq| wc -l        # "physical id"物理CPU个数；"cpu cores"物理CPU中core的个数；"processor"逻辑CPU的个数  

## memory

cat /proc/meminfo       #内存信息  
awk '$3=="kB"{if ($2>1024**2){$2=$2/1024**2;$3="GB";} else if ($2>1024){$2=$2/1024;$3="MB";}} 1' /proc/meminfo | column -t      #单位显示更友好  
free -h        #内存运行信息，友好方式；实际可用内存：buffers+cached+free  
free -hl        #最低内存的统计信息

## disk

lsblk           #硬件硬盘分区信息
fdisk -l        #挂载 磁盘信息
mount | column -t       #挂在分区情况
df -hT          #硬盘使用情况
swapon -s       #所有交换分区

## 网卡信息

lspci       #硬件网卡信息
ip link show        #系统的所有网络接口
ip -s link          #统计数据
ip addr            #所有网络接口的属性
ethtool eth0        #某个网络接口的详细信息
route -n            #查看路由表
firewall-cmd --list-all     #端口信息

## 进程信息

ps -ef      #所有进程
ps -aux     #进程占用CPU,内存情况
top     #实时显示进程状态
