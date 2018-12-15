# 不同操作系统间，CRLR-LR ，涉及到GIT的问题。

在仓库的根目录下建一个文件 `.gitattributes`  
在 github 我是用的是 `*.js -text`  

```text
*         text=auto
# These files are text and should be normalized (convert crlf => lf)
*.cs      text
*.xaml    text
*.csproj  text
*.sln     text
*.tt      text
*.ps1     text
*.cmd     text
*.msbuild text
*.md      text

# Images should be treated as binary
# (binary is a macro for -text -diff)
*.png     binary
*.jepg    binary

*.sdf     binary
```

text 设置的时候，转换自动转换到对应平台的换行符；行号高的设置会覆盖行号低的设置

- text      自动完成标准化与转换
- -text     不执行标准化与转换
- text=auto 根据 Git 决定是否需要执行标准化与转化
- 不设置     使用core.autocrlf配置决定是否执行标准化与转换

eol

- eol=lf 强制完成标准化，不执行转换（相当于指定转换为LF格式）
- eol=crlf 强制完成标准化，指定转换为CRLF格式

binary

- binary 二进制文件不参与标准化与转换

- 不设置 由 Git 决定是否为二进制文件

eol=lf 强制完成标准化，不执行转换（相当于指定转换为LF格式）
eol=crlf 强制完成标准化，指定转换为CRLF格式
