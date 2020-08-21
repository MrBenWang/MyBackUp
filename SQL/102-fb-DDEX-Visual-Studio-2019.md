# Visual-Studio-2019 安装 Firebird DDEX

由于 Visual-Studio-2019 没有对应的 Firebird DDEX 需要自己来生成。  
Failure [INSTALL_FAILED_SHARED_USER_INCOMPATIBLE: Package couldn't be installed in /data/app/com.lenovo.st.deviceinforeader-1: Package com.lenovo.st.deviceinforeader has no signatures that match those in shared user android.uid.system; ignoring!]  

参考资料：  
the database for design purposes(DDEX Provider) are not installed for provider 'FirebirdSql.Data.FirebirdClient'
[《How to install DDEX Firebird Provider in Microsoft Visual Studio 2017》](http://onlineservicetools.com/en_US/how-to-install-ddex-firebird-provider-in-microsoft-visual-studio-2017/)

## 参数替换

1. `16.0_79b7ce62_Config` 来自于 `C:\Users\zhenglong.wang\AppData\Local\Microsoft\VisualStudio` 文件夹下的 `16.0_79b7ce62` 文件夹；(11处需替换)
2. `CodeBase` 后面的参数，要选择对应的 `FirebirdSql.VisualStudio.DataTools.dll` 的绝对路径；(1处需替换)

其他的 Guid 为固定的值，不用管。  

## 安装vs2019 DDEXProvider

引用原文 [《Installing DDEX provider for Firebird into Visual Studio 2017 》](https://www.tabsoverspaces.com/233604-installing-ddex-provider-for-firebird-into-visual-studio-2017)  

Open `regedit` and load the `privateregistry.bin` file using the `File > Load Hive...` menu and load it i.e. into `HKEY_USERS` under some name. I’ll use `VS2017PrivateRegistry` here. Take a copy of `FirebirdDDEXProvider64.reg` (or `FirebirdDDEXProvider32.reg`) and change the registry paths `HKEY_CURRENT_USER\Software\Microsoft\VisualStudio\14.0_Config to HKEY_USERS\VS2017PrivateRegistry\Software\Microsoft\VisualStudio\15.0_<something>_Config`. Don’t forget to properly change the `%Path%` variable too in this file. At the end, it might look like this.

## 我的 FirebirdDDEXProvider64.reg

```shell
Windows Registry Editor Version 5.00

[HKEY_USERS\VS2019PrivateRegistry\Software\Microsoft\VisualStudio\16.0_79b7ce62_Config\DataSources\{2979569E-416D-4DD8-B06B-EBCB70DE7A4E}]
@="Firebird Data Source"



[HKEY_USERS\VS2019PrivateRegistry\Software\Microsoft\VisualStudio\16.0_79b7ce62_Config\DataSources\{2979569E-416D-4DD8-B06B-EBCB70DE7A4E}\SupportingProviders\{92421248-F044-483A-8237-74C7FBC62971}]

[HKEY_USERS\VS2019PrivateRegistry\Software\Microsoft\VisualStudio\16.0_79b7ce62_Config\DataProviders\{92421248-F044-483A-8237-74C7FBC62971}]
@=".NET Framework Data Provider for Firebird"
"DisplayName"="Provider_DisplayName, FirebirdSql.VisualStudio.DataTools.Properties.Resources"
"ShortDisplayName"="Provider_ShortDisplayName, FirebirdSql.VisualStudio.DataTools.Properties.Resources"
"Description"="Provider_Description, FirebirdSql.VisualStudio.DataTools.Properties.Resources"
"CodeBase"="C:\\Program Files (x86)\\FirebirdDDEX\\FirebirdSql.VisualStudio.DataTools.dll"
"InvariantName"="FirebirdSql.Data.FirebirdClient"
"Technology"="{77AB9A9D-78B9-4ba7-91AC-873F5338F1D2}"



[HKEY_USERS\VS2019PrivateRegistry\Software\Microsoft\VisualStudio\16.0_79b7ce62_Config\DataProviders\{92421248-F044-483A-8237-74C7FBC62971}\SupportedObjects]


[HKEY_USERS\VS2019PrivateRegistry\Software\Microsoft\VisualStudio\16.0_79b7ce62_Config\DataProviders\{92421248-F044-483A-8237-74C7FBC62971}\SupportedObjects\DataConnectionSupport]
@="FirebirdSql.VisualStudio.DataTools.FbDataConnectionSupport"

[HKEY_USERS\VS2019PrivateRegistry\Software\Microsoft\VisualStudio\16.0_79b7ce62_Config\DataProviders\{92421248-F044-483A-8237-74C7FBC62971}\SupportedObjects\DataConnectionProperties]
@="FirebirdSql.VisualStudio.DataTools.FbDataConnectionProperties"



[HKEY_USERS\VS2019PrivateRegistry\Software\Microsoft\VisualStudio\16.0_79b7ce62_Config\DataProviders\{92421248-F044-483A-8237-74C7FBC62971}\SupportedObjects\DataConnectionUIControl]
@="FirebirdSql.VisualStudio.DataTools.FbDataConnectionUIControl"

[HKEY_USERS\VS2019PrivateRegistry\Software\Microsoft\VisualStudio\16.0_79b7ce62_Config\DataProviders\{92421248-F044-483A-8237-74C7FBC62971}\SupportedObjects\DataSourceInformation]
@="FirebirdSql.VisualStudio.DataTools.FbDataSourceInformation"



[HKEY_USERS\VS2019PrivateRegistry\Software\Microsoft\VisualStudio\16.0_79b7ce62_Config\DataProviders\{92421248-F044-483A-8237-74C7FBC62971}\SupportedObjects\DataObjectSupport]
@="FirebirdSql.VisualStudio.DataTools.FbDataObjectSupport"



[HKEY_USERS\VS2019PrivateRegistry\Software\Microsoft\VisualStudio\16.0_79b7ce62_Config\DataProviders\{92421248-F044-483A-8237-74C7FBC62971}\SupportedObjects\DataViewSupport]
@="FirebirdSql.VisualStudio.DataTools.FbDataViewSupport"

[HKEY_USERS\VS2019PrivateRegistry\Software\Microsoft\VisualStudio\16.0_79b7ce62_Config\Services\{AEF32AEC-2167-4438-81FF-AE6603341536}]
@="{8d9358ba-ccc9-4169-9fd6-a52b8aee2d50}"
"Name"="Firebird Provider Object Factory"
```

## 总结

看了下 `DDEXProvider-3.0.2.0-src.7z` 里面的安装部分 `reg_files` 文件夹下面，目前只针对了 VS2005 、 VS2008 、 VS2010 、 VS2012 、 VS2013 、 VS2015 这六个 vs 版本 `*.reg` 文件。所以需要自己来实现新的 `FirebirdDDEXProvider64.reg` 。  

注册表中的 `VS2017PrivateRegistry` 类似于一个模板性质，使用完成后，可以删除。
