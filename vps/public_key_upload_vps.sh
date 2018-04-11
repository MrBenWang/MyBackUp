#!/usr/bin/env bash
# 在客户端生成 私钥，然后上传到服务器，配置好ssh

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

red="\033[0;31m"
green="\033[0;32m"
plain="\033[0m"

[ -z $1 ] && echo -e "Please input ${red}the parameter(vps ip) ${plain}" && exit 1

# 生成公钥
[ -f ~/.ssh/id_rsa ] && rm -rf ~/.ssh
ssh-keygen -t rsa -f ~/.ssh/id_rsa -N ''

# 上传公钥给服务器
ssh-copy-id root@$1 && echo -e "upload id_rsa ${green}success${plain} " || echo -e "upload public_key ${red}failure${plain}"
