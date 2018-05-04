#!/usr/bin/env bash
# 用于初次按照或者重置CentOS7 vps服务器

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

red="\033[0;31m"
green="\033[0;32m"
yellow="\033[0;33m"
plain="\033[0m"
# 用户名,密码
readonly my_name_pwd=("zhenglong" $1)
# 更改ssh 端口为
readonly my_ssh_port=8822
# 端口数组
readonly myports=8880 
# 密码数组，对端口对应
readonly mypwds="zhenglong"

[ -z $1 ] && echo -e "Please input ${red}the parameter(new user passwd).${plain}" && exit 1
[ ! -d /root/.ssh ] && echo -e "Please upload ${red}pub_key for ssh at frist.${plain}" && exit 1
yum -y -q install epel-release

# 检查系统，并且是不是root用户
check_sys_root(){
	[[ $EUID != 0 ]] && echo -e "${Error} 当前账号非ROOT(或没有ROOT权限)，无法继续操作，请使用${Green_background_prefix} sudo su ${Font_color_suffix}来获取临时ROOT权限（执行后会提示输入当前账号的密码）。" && exit 1

	if [[ -f /etc/redhat-release ]]; then
		release="centos"
	elif cat /etc/issue | grep -q -E -i "debian"; then
		release="debian"
	elif cat /etc/issue | grep -q -E -i "ubuntu"; then
		release="ubuntu"
	elif cat /etc/issue | grep -q -E -i "centos|red hat|redhat"; then
		release="centos"
	elif cat /proc/version | grep -q -E -i "debian"; then
		release="debian"
	elif cat /proc/version | grep -q -E -i "ubuntu"; then
		release="ubuntu"
	elif cat /proc/version | grep -q -E -i "centos|red hat|redhat"; then
		release="centos"
    fi
}

# Disable selinux
disable_selinux(){
    if [ -s /etc/selinux/config ] && grep "SELINUX=enforcing" /etc/selinux/config; then
        sed -i "s/SELINUX=enforcing/SELINUX=disabled/g" /etc/selinux/config
        setenforce 0
    fi
}

# 安装配置shadowsocks
install_config_shadowsocks_go(){
	#判断是否已经安装，go 和 git
	if [ $(yum list installed git golang | egrep "^git|^golang" | wc -l) -lt 3 ]; then
		echo "begin install golang"
		yum install go -y -q
		echo "finished install golang"
		yum install git -y -q
		echo "finished install git"
	fi

	if [ ! -f /root/go/bin/go-shadowsocks2 ] ;then
		go get -u github.com/shadowsocks/go-shadowsocks2
		echo "finished install go-shadowsocks2"
	fi

	if [ $(systemctl list-units | grep "shadowsocks.service" |wc -l) -gt 0 ]; then
		systemctl stop shadowsocks.service && systemctl disable shadowsocks.service
	fi
	create_ss_service
	systemctl start shadowsocks.service && systemctl enable shadowsocks.service
	echo "finished create shadowsocks.service"

	# 重新设置防火墙
	echo "open port:${myports}  pwd:${mypwds}"
	if [ $(firewall-cmd --query-port=${myports}/tcp) == "no" ]; then
		firewall-cmd --zone=public --permanent --add-port=${myports}/tcp
		firewall-cmd --zone=public --permanent --add-port=${myports}/udp
		firewall-cmd --reload
	fi

	echo "added in ${myports}/tcp ${myports}/udp firewall-cmd "
}
create_ss_service(){
	# 服务配置文件
	readonly server_config_path="/etc/systemd/system/shadowsocks.service"
	[ -f ${server_config_path} ] && rm -f ${server_config_path}
	cat > ${server_config_path}<<-EOF
[UNIT]
Description=shadowsocks Service

[Service]
Type=simple
ExecStart=/root/go/bin/go-shadowsocks2 -s ss://AEAD_CHACHA20_POLY1305:${mypwds}@:${myports} -verbose

[Install]
WantedBy=multi-user.target
EOF
}

# 更新linux内核到 4.x 可以开启bbr
install_kenal_bbr(){
	if [ $(uname -r | cut -d '.' -f1) -lt 4 ];then
		# 更新系统核心
		rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org
		rpm -Uvh http://www.elrepo.org/elrepo-release-7.0-2.el7.elrepo.noarch.rpm
		yum --enablerepo=elrepo-kernel install kernel-ml -y &> /dev/null
		echo "finished install kernel 4.x"
		rpm -qa | grep kernel
		grub2-set-default 1

		# 更改配置文件
		echo 'net.core.default_qdisc=fq' | tee -a /etc/sysctl.conf
		echo 'net.ipv4.tcp_congestion_control=bbr' | tee -a /etc/sysctl.conf
		echo "finished set bbr"	
	else 
		#检查 是否更新成功
		sysctl -p
		sysctl -n net.ipv4.tcp_congestion_control
		lsmod | grep bbr
	fi
}

# 安装DenyHosts
install_denyhosts(){
	yum install denyhosts -y &> /dev/null
	sed -i "s/root@localhost/${my_name_pwd[0]}@localhost/g" /etc/denyhosts.conf
	systemctl start denyhosts
	systemctl enable denyhosts
	echo "finished install denyhosts"
}

# 增加系统安全性
change_centos_safe_config(){
	# 不要以Root权限登陆
	id ${my_name_pwd[0]} > /dev/null 2>&1
	if [ $? -eq 0 ]; then
		echo -e "[ Input user(${my_name_pwd[0]}) exist] \n"
	else 
		useradd ${my_name_pwd[0]}
		echo ${my_name_pwd[1]} | passwd --stdin ${my_name_pwd[0]}
		usermod -aG wheel ${my_name_pwd[0]}
		# 复制ssh的参数
		cp -r /root/.ssh /home/${my_name_pwd[0]}/
		chown -R ${my_name_pwd[0]}:${my_name_pwd[0]} /home/${my_name_pwd[0]}
		echo "add user:${my_name_pwd[0]} passwd: ${my_name_pwd[1]}"
	fi

	# 更改ssh 端口 ,在匹配的下一行添加
	if [ -z $(grep ^Port /etc/ssh/sshd_config) ]; then
		sed -i "/^#Port 22/a\Port ${my_ssh_port}" /etc/ssh/sshd_config > /dev/null
		firewall-cmd --zone=public --permanent --add-port=${my_ssh_port}/tcp
		firewall-cmd --reload
		echo "changed shh_port: ${my_ssh_port}"
	fi

	# 禁止root远程登录，有则替换为no，没有则下一行添加no
	sed -i "s/^PermitRootLogin yes\|^#PermitRootLogin yes/PermitRootLogin no/g" /etc/ssh/sshd_config
	# 普通用户可以使用密码登录
	sed -i "s/^PasswordAuthentication no\|^#PasswordAuthentication yes/PasswordAuthentication yes/g" /etc/ssh/sshd_config
	# sed -i "s/^PermitRootLogin yes|/PermitRootLogin no/g" /etc/ssh/sshd_config \
	# || sed -i "/^#PermitRootLogin yes/a\PermitRootLogin no" /etc/ssh/sshd_config 

	echo "chenged sshd_config"
	systemctl restart sshd

	
}

# 自定义系统配置
customize_system(){
	# 修改时区
	timedatectl set-timezone Asia/Shanghai
	# wheel组 sudo不需要密码
	sed -i 's/^%wheel.*/%wheel ALL=(ALL) NOPASSWD: ALL/g' /etc/sudoers
	# wheel组 su 不需要密码
	sed -i 's/^#auth\s\+sufficient\s\+pam_wheel.so\s\+trust\s\+use_uid/auth sufficient pam_wheel.so trust use_uid/g' /etc/pam.d/su

	# 别名设置
	cat > /etc/profile.d/alias.sh <<-EOF
PS1='\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\W\[\033[00m\]\\$ '

alias cp='cp -i'
alias mv='mv -i'
alias rm='rm -i'

alias ls='ls --color=auto'
alias ll='ls -al'
alias lm='ls -al | more'
alias dir='dir --color=auto'
alias vdir='vdir --color=auto'

alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'

alias mkcd='function _mkcd(){ mkdir \$@ && cd \$@; }; _mkcd'
alias cdl='function _cdl() { cd \$@ && pwd; ls -alF; }; _cdl'
	EOF
}

# 更新python 到 3.x
update_python_to_3x(){
	sudo apt-get install python3-pip
	sudo pip-3.3 install pylint
}

reboot_os() {
	# 清除 历史指令
	history -c
	# 清除登录失败记录
	echo > /var/log/btmp

    echo -e "${green}Info:${plain} The system needs to reboot."
    read -p "Do you want to restart system? [y/n]" is_reboot
    if [[ ${is_reboot} == "y" || ${is_reboot} == "Y" ]]; then
        reboot
    else
        echo -e "${green}Info:${plain} Reboot has been canceled..."
        exit 0
    fi
}

## 更改系统安全配置
change_centos_safe_config
## 自定义系统的参数配置
customize_system
## 安装go-shadowsocks2
install_config_shadowsocks_go
## 安装 denyhosts
install_denyhosts
## 更新内核，配置 bbr
#install_kenal_bbr
#reboot_os