#!/usr/bin/env bash
# 用于初次按照或者重置CentOS7 vps服务器

"""
On Server ,Exec Command: 

```sh
wget https://github.com/MrBenWang/MyWroteScripts/blob/master/vps/20190111-install_env_vps_v2.sh -P ~/
chmod a+x install_env_vps.sh
~/install_env_vps.sh [New User Passwd]
```
"""


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

[ -z $1 ] && echo -e "Please input ${red}the parameter(new user passwd).${plain}" && exit 1
[ ! -d /root/.ssh ] && echo -e "Please upload ${red}pub_key for ssh at frist.${plain}" && exit 1

# 检查系统，并且是不是root用户
check_sys_root(){
	[[ $EUID != 0 ]] && echo -e "${Error} 当前账号非ROOT(或没有ROOT权限)，无法继续操作，请使用${Green_background_prefix} sudo su ${Font_color_suffix}来获取临时ROOT权限（执行后会提示输入当前账号的密码）。" && exit 1
}

install_python3(){
	#whereis python	#检查有哪些python
	#yum search python pip
	#yum list installed | grep "python"
	#yum remove tomcat
	yum install epel-release
	yum upgrade  # 更新升级
	yum install python34-pip
	#pip3 install --upgrade pip
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
	init_ssh_config()
}

# ssh 登陆设置
init_ssh_config(){
	cd ~
	mkdir .ssh
	cd .ssh
	cat > ~/.ssh/authorized_keys <<-EOF
public_key
	EOF

	chmod 600 .ssh/authorized_keys # 权限必须是这样
	chmod 700 -R .ssh
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
PS1='\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\W\[\033[00m\]\$ '

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

# 安装配置 v2ray
install_v2ray(){
	# 使用官方 方式，不存在翻墙，很快
	bash <(curl -L -s https://install.direct/go.sh)

	#配置文件自己拷贝 # /etc/v2ray/config.json
	systemctl enable v2ray
	systemctl start v2ray

	# 重新设置防火墙
	firewall-cmd --zone=public --permanent --add-port=8090/tcp
	firewall-cmd --zone=public --permanent --add-port=8080/udp
	firewall-cmd --reload
}


# DenyHosts 不支持systemd或firewalld,
install_Fail2Ban(){
	# fail2ban-client status sshd 	#查看被ban IP，其中sshd为名称
	# fail2ban-client set sshd delignoreip 192.168.111.111  #删除被ban IP
	# tail /var/log/fail2ban.log	#查看日志
	yum -y install fail2ban &> /dev/null
	systemctl enable fail2ban
	systemctl start fail2ban
	echo "finished install fail2ban"
}

# 更新 bbrplus 内核，要最后执行
install_kenal_bbr(){
	wget "https://github.com/cx9208/bbrplus/raw/master/ok_bbrplus_centos.sh" && chmod +x ok_bbrplus_centos.sh && ./ok_bbrplus_centos.sh
	n # no 不重启
	#uname -r
	#lsmod | grep bbr
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

## 检查用户权限
check_sys_root
install_python3
## 更改系统安全配置
change_centos_safe_config
## 自定义系统的参数配置
customize_system
## 安装 v2ray
install_v2ray
## 安装 denyhosts
install_Fail2Ban
## 更新内核，配置 bbr
install_kenal_bbr
reboot_os