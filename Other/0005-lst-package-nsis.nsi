# 官网: https://nsis.sourceforge.io/  用3.08版本，脚本文件格式必须为 utf-8 with BOM
# 使用 Modern 风格界面 那种下一

!include "MUI2.nsh"       # 使用 Modern 风格界面，那种下一步下一步界面。
!include "LogicLib.nsh"   # 逻辑操作符头文件。就是 {If} 那些。
!include "WordFunc.nsh"

#!define PROD_OR_TEST "prod"   # 给生产环境打包，还是测试环境打包
!define PROD_OR_TEST "test"   # 给生产环境打包，还是测试环境打包

#------------------------------------
# 安装包的基本属性设置。
!define PRODUCT_NAME "Myname Smart Tool"
!define PRODUCT_VERSION "3.6.0.3"
!define PRODUCT_PUBLISHER "Myname"
!define PRODUCT_WEB_SITE "https://www.Myname.com"
!define PRODUCT_DIR_REGKEY "Software\Microsoft\Windows\CurrentVersion\App Paths\MynameSmartTool.exe"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM" # HKLM or HKEY_LOCAL_MACHINE
!define PRODUCT_MAIN_EXE "MynameSmartTool.exe"
!define PRODUCT_MAIN_NT_SERVICES_NAME "MynameSmartToolClientNTService"
#---------------------------------

#Unicode true  # 设置为 Unicode 模式，这样界面才可以显示全部的语言。
Name "${PRODUCT_NAME}" # 设定软件的名字。
OutFile "Myname_Smart_Tool_v${PRODUCT_VERSION}_${PROD_OR_TEST}_setup.exe" # 设定编译输出的文件名。
InstallDir "$PROGRAMFILES\Myname\MynameSmartTool" # 设定默认的安装路径。
InstallDirRegKey HKLM "${PRODUCT_DIR_REGKEY}" ""

ShowInstDetails show  # 默认显示安装细节，安装过程中输出的文字信息。
ShowUnInstDetails show  # 默认显示卸载细节，安装过程中输出的文字信息。
AllowRootDirInstall false  # 允许用户在安装路径选择界面选择磁盘的根目录。
RequestExecutionLevel admin  # 设定安装包需要的用户权限，只用于 Vista 以上的版本。设置为 admin 编译出来的 EXE 会带有盾牌小图标。

SetCompressor lzma  # 使用 LZMA 压缩算法，压缩质量比较好。
SetDateSave on # 保存文件日期。

#--------------------------------
# 界面选项，修改界面上的一些元素。
!define MUI_ICON ".\05-InstallationProjectResources\logo.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\orange-uninstall.ico"
#!define MUI_WELCOMEFINISHPAGE_BITMAP "${NSISDIR}\Contrib\Graphics\Wizard\nsis3-metro.bmp" # 设置欢迎和完成界面左侧的图片。

#!define MUI_LICENSEPAGE_CHECKBOX  # 使用复选框来确认安装协议。
#!define MUI_LICENSEPAGE_CHECKBOX_TEXT "$(STR_LicenseAccept)"  # 复选框的文字。
#!define MUI_COMPONENTSPAGE_CHECKBITMAP "check.bmp"  # 选择安装组件界面的复选框图片，可以自定义的。

!define MUI_FINISHPAGE_NOAUTOCLOSE  # 安装完成后不要自动跳过过程界面。
!define MUI_ABORTWARNING  # 中途退出安装时弹出提示。
!define MUI_LANGDLL_ALLLANGUAGES  # 强制显示所有支持的语言。

BrandingText "Provided by Myname"  # 设置分割线上的文字。

#------------------------------------
# 安装包要显示的界面，需要注意的是，界面是按照插入顺序来显示的。
!insertmacro MUI_PAGE_WELCOME # 首先插入的是欢迎界面。
!define MUI_LICENSEPAGE_RADIOBUTTONS
!insertmacro MUI_PAGE_LICENSE ".\05-InstallationProjectResources\license_new.rtf"  # 插入协议确认界面。
!insertmacro MUI_PAGE_DIRECTORY # 插入选择安装路径界面。
!insertmacro MUI_PAGE_INSTFILES # 插入安装过程界面。
!define MUI_FINISHPAGE_RUN "$INSTDIR\MynameSmartTool.exe"
!define MUI_FINISHPAGE_RUN_CHECKED
!insertmacro MUI_PAGE_FINISH  # 插入完成界面。

!insertmacro MUI_UNPAGE_INSTFILES  # 卸载程序显示进度
!insertmacro MUI_UNPAGE_FINISH  # 卸载程序显示安装结束

!insertmacro MUI_LANGUAGE "English" # 简体中文, 会定义 LANG_ENGLISH 变量。必须在最后指定
LangString LAUNCH_TEXT ${LANG_ENGLISH} "Launch the program"

!macro MakeInstallUninstallFunction un
  # 检查主程序exe是否运行
  Function ${un}RunningCheck
    nsProcess::_FindProcess "${PRODUCT_MAIN_EXE}"
    Pop $R0
    StrCmp $R0 0 +1 gocontiune # 0 if found
    MessageBox MB_ICONQUESTION|MB_OKCANCEL|MB_DEFBUTTON2 "${PRODUCT_MAIN_EXE} is running, do you want to close it automatically and continue?" IDOK done_kill IDCANCEL goquit
    done_kill:
      nsProcess::_FindProcess "${PRODUCT_MAIN_EXE}"
      Pop $R0
      StrCmp $R0 0 +1 gocontiune # 0 if found

      nsProcess::_KillProcess "${PRODUCT_MAIN_EXE}"
      Pop $R0
      StrCmp $R0 0 gocontiune +1 # 0 Success
        MessageBox MB_OK "Cannot close the progress: ${PRODUCT_MAIN_EXE}, please close manually and try again."
        Quit
    goquit:
      Quit
    gocontiune:
  FunctionEnd
  
  # 停止运行 windows 服务
  Function ${un}RomveNTServices
    SimpleSC::ExistsService "${PRODUCT_MAIN_NT_SERVICES_NAME}"
    Pop $0 ; returns an errorcode if the service doesn´t exists (<>0)/service exists (0)
    StrCmp $0 0 +1 do_continue
      SimpleSC::ServiceIsRunning "${PRODUCT_MAIN_NT_SERVICES_NAME}"
      Pop $0 ; returns an errorcode (<>0) otherwise success (0)
      Pop $1 ; returns 1 (service is running) - returns 0 (service is not running)
      StrCmp $1 1 +1 do_remove
        DetailPrint "Stopping ${PRODUCT_MAIN_NT_SERVICES_NAME} service..."
        SimpleSC::StopService "${PRODUCT_MAIN_NT_SERVICES_NAME}" 1 30
        Pop $0 ; returns an errorcode (<>0) otherwise success (0)
        StrCmp $0 0 do_remove +1
          Push $0
          SimpleSC::GetErrorMessage
          Pop $0
          DetailPrint "Stopping ${PRODUCT_MAIN_NT_SERVICES_NAME} fails - Reason: $0"
          MessageBox MB_OK|MB_ICONSTOP "Stopping fails - Reason: $0"
      do_remove:
        DetailPrint "Remove ${PRODUCT_MAIN_NT_SERVICES_NAME} service..."
        SimpleSC::RemoveService "${PRODUCT_MAIN_NT_SERVICES_NAME}"
        Pop $0 ; returns an errorcode (<>0) otherwise success (0)
        StrCmp $0 0 do_continue +1
          Push $0
          SimpleSC::GetErrorMessage
          Pop $0
          DetailPrint "Remove ${PRODUCT_MAIN_NT_SERVICES_NAME} fails - Reason: $0"
          MessageBox MB_OK|MB_ICONSTOP "Remove fails - Reason: $0"
    do_continue:
  FunctionEnd
!macroend
!insertmacro MakeInstallUninstallFunction ""
!insertmacro MakeInstallUninstallFunction "un."

# 防止重复运行
Function CheckSingleInstallation
	System::Call 'kernel32::CreateMutexA(i 0, i 0, t "${PRODUCT_NAME}") i .r1 ?e'
	Pop $R0
	StrCmp $R0 0 noprevinst
    MessageBox MB_OK|MB_ICONEXCLAMATION "The install program [${PRODUCT_NAME}] is running!"
    Abort
  noprevinst:
FunctionEnd

# 检查版本号 相等重新安装 大于旧版本需要卸载 小于阻止安装
Function CheckExistsOrUpgrade
  ReadRegStr $0 ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion"
  ReadRegStr $R0 ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString"
  ${VersionCompare} $0 ${PRODUCT_VERSION} $0
  ${If} $R0 != ""
    IntCmp $0 1 old_larger equal new_larger
    old_larger:
      MessageBox MB_OKCANCEL|MB_ICONINFORMATION "There is a higher version of [${PRODUCT_NAME}] installed on the PC. Click 'OK' to remove the existing version." IDOK continue_install
      Quit
    equal:
      MessageBox MB_OKCANCEL|MB_ICONINFORMATION "${PRODUCT_NAME} v${PRODUCT_VERSION} is already installed. Click 'OK' to remove the existing version or 'Cancel' to cancel this upgrade." IDOK continue_install
      Quit
    new_larger:
      goto continue_install
    continue_install:
      ExecWait '$R0 _?=$INSTDIR'
      Delete "$R0"
  ${EndIf}

FunctionEnd

Function UninstallMSI
  # "{502C125C-C695-44AB-9B10-E9507E57138A}"    {213BCCD6-DEB5-4B3D-A009-6DE27A3D387E}
  System::Call 'MSI::MsiEnumRelatedProducts(t "{213BCCD6-DEB5-4B3D-A009-6DE27A3D387E}",i0,i r0,t.r1)i.r2'

  SetRegView 64
  ReadRegStr $R1 HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\$1" "UninstallString"
  SetRegView 32

  StrCmp $R1 "" UninstallMSI_nomsi
    MessageBox MB_YESNO|MB_ICONQUESTION  "A previous version of ${PRODUCT_NAME} was found. It is recommended that you uninstall it first.$\n$\nDo you want to do that now?" IDYES UninstallMSI_yesmsi IDNO +1
      Abort
  UninstallMSI_yesmsi:
      ExecWait '"msiexec.exe" /x $1'
      MessageBox MB_OK|MB_ICONINFORMATION "Click OK to continue upgrading your version of ${PRODUCT_NAME} v${PRODUCT_VERSION}"
  UninstallMSI_nomsi: 
    pop $R1
FunctionEnd

Function .onInit
  !insertmacro MUI_LANGDLL_DISPLAY
  #Debug::Watcher

  Call CheckSingleInstallation
  Call RunningCheck
  Call CheckExistsOrUpgrade
FunctionEnd

Section -MainSection

  Call RomveNTServices

  SetOverwrite ifnewer
  CreateDirectory "$SMPROGRAMS\MynameSmartTool"

  SetOutPath "$INSTDIR\7za"
  File "..\3rdPartyLibraries\7za\7z.dll"
  File "..\3rdPartyLibraries\7za\7z.exe"
  File "..\3rdPartyLibraries\7za\7za.exe"

  SetOutPath "$INSTDIR\drivers\MTK"
  File "..\Installation\03-ConfigurationFileTemplates\drivers\MTK\cdc-acm.cat"
  File "..\Installation\03-ConfigurationFileTemplates\drivers\MTK\cdc-acm.inf"
  SetOutPath "$INSTDIR\drivers\MTK\x64"
  File "..\Installation\03-ConfigurationFileTemplates\drivers\MTK\x64\usb2ser.sys"
  SetOutPath "$INSTDIR\drivers\MTK\x86"
  File "..\Installation\03-ConfigurationFileTemplates\drivers\MTK\x86\usb2ser.sys"
  SetOutPath "$INSTDIR\drivers\QUALCOMM"
  File "..\Installation\03-ConfigurationFileTemplates\drivers\QUALCOMM\Qualcomm.win.1.1_installer_10061.1.exe"
  SetOutPath "$INSTDIR\drivers\SmartClock"
  File "..\Installation\03-ConfigurationFileTemplates\drivers\SmartClock\MynameUsbDriver_autorun_1.1.33_user.exe.zip"

  SetOutPath "$INSTDIR\HWDetection"
  File "..\Installation\03-ConfigurationFileTemplates\HWDetection\MobileAssistant.apk"

  SetOutPath "$INSTDIR\intl"
  File "..\3rdPartyLibraries\Firebird-2.5.4.26856-0_Win32_embed\intl\fbintl.conf"
  File "..\3rdPartyLibraries\Firebird-2.5.4.26856-0_Win32_embed\intl\fbintl.dll"

  SetOutPath "$INSTDIR\LocalConfig"
  File "..\Installation\03-ConfigurationFileTemplates\LocalConfig\Config.xml"
  File "..\Installation\03-ConfigurationFileTemplates\LocalConfig\LocalAppSetting.xml"
  File "..\Installation\03-ConfigurationFileTemplates\LocalConfig\LocalFuncSetting.xml"
  File "..\Installation\03-ConfigurationFileTemplates\LocalConfig\LocalResourceStatus.xml"
  File "..\Installation\03-ConfigurationFileTemplates\LocalConfig\log4net.config"
  File "..\Installation\03-ConfigurationFileTemplates\LocalConfig\log4net_service.config"
  File "..\Installation\03-ConfigurationFileTemplates\LocalConfig\Workflow.xml"

  SetOutPath "$INSTDIR\Resources"
  File "..\Installation\03-ConfigurationFileTemplates\DeviceInfoReader\DeviceInfoReader.apk"

  SetOutPath "$INSTDIR"
  File "..\3rdPartyLibraries\ADB\AdbWinUsbApi.dll"
  File "..\3rdPartyLibraries\ADB\AdbWinApi.dll"
  File "..\3rdPartyLibraries\ADB\adb.exe"
  File "..\3rdPartyLibraries\FastBoot\fastboot.exe"
  File "..\3rdPartyLibraries\Firebird-2.5.4.26856-0_Win32_embed\msvcr80.dll"
  File "..\3rdPartyLibraries\Firebird-2.5.4.26856-0_Win32_embed\msvcp80.dll"
  File "..\3rdPartyLibraries\Firebird-2.5.4.26856-0_Win32_embed\Microsoft.VC80.CRT.manifest"
  File "..\3rdPartyLibraries\Firebird-2.5.4.26856-0_Win32_embed\icuuc30.dll"
  File "..\3rdPartyLibraries\Firebird-2.5.4.26856-0_Win32_embed\icuin30.dll"
  File "..\3rdPartyLibraries\Firebird-2.5.4.26856-0_Win32_embed\icudt30.dll"
  File "..\3rdPartyLibraries\Firebird-2.5.4.26856-0_Win32_embed\firebird.msg"
  File "..\3rdPartyLibraries\Firebird-2.5.4.26856-0_Win32_embed\firebird.conf"
  File "..\3rdPartyLibraries\Firebird-2.5.4.26856-0_Win32_embed\fbembed.dll"
  File "..\3rdPartyLibraries\Firebird-2.5.4.26856-0_Win32_embed\ib_util.dll"
  File "..\3rdPartyLibraries\Interop.SHDocVw.dll"
  File "..\Installation\05-InstallationProjectResources\Language.xlsx"
  File "..\Installation\00-Documents\00-Help\Tools\Myname_Smart_Tool_User_guide.pdf"
  File "..\DataAccessor\LNO_CLIENT.FDB"

  File "..\Bin\zxing.dll"
  File "..\Bin\WebApiClient.JIT.dll"
  File "..\Bin\Utility.dll"
  File "..\Bin\System.Windows.Interactivity.dll"
  File "..\Bin\SmartUtil.dll"
  File "..\Bin\SmartRsd.dll"
  File "..\Bin\SmartDevice.dll"
  File "..\Bin\SmartBase.dll"
  File "..\Bin\ProgrammingToolPlugin.dll"
  File "..\Bin\PdfSharp.dll"
  File "..\Bin\PdfSharp.Charting.dll"
  File "..\Bin\OSDPortalPlugin.dll"
  File "..\Bin\NPOI.OpenXmlFormats.dll"
  File "..\Bin\NPOI.OpenXml4Net.dll"
  File "..\Bin\NPOI.OOXML.dll"
  File "..\Bin\NPOI.dll"
  File "..\Bin\Newtonsoft.Json.dll"
  File "..\Bin\Mono.Posix.dll"
  File "..\Bin\Microsoft.Extensions.Logging.Abstractions.dll"
  File "..\Bin\LSTClientFramework.dll"
  File "..\Bin\log4net.dll"
  File "..\Bin\LibUsbDotNet.dll"
  File "..\Bin\MynameSmartToolWebApiProxy.dll"
  File "..\Bin\MynameSmartToolNTServiceProxy.dll"
  File "..\Bin\Myname.Themes.dll"
  File "..\Bin\KnowledgeBasePlugin.dll"
  File "..\Bin\KillSwitchBase.dll"
  File "..\Bin\ISmart.dll"
  File "..\Bin\ICSharpCode.SharpZipLib.dll"
  File "..\Bin\HwDetectionPlugin.dll"
  File "..\Bin\FirebirdSql.Data.FirebirdClient.dll"
  File "..\Bin\EntityFramework.Firebird.dll"
  File "..\Bin\EntityFramework.dll"
  File "..\Bin\DotNetZip.dll"
  File "..\Bin\DevicesModel.dll"
  File "..\Bin\DeviceManager.dll"
  File "..\Bin\DeviceInfoPlugin.dll"
  File "..\Bin\DataAccessor.dll"
  File "..\Bin\CrachRescureBase.dll"
  File "..\Bin\CountryCodePlugin.dll"
  File "..\Bin\Configurations.dll"
  File "..\Bin\BasicDefinition.dll"
  File "..\Bin\AdaptorManger.dll"
  File "..\Bin\MynameSmartToolSrv.exe"
  File "..\Bin\MynameSmartTool.exe"
  File "..\Bin\MynameSmartToolSrv.exe.config"
  File "..\Bin\MynameSmartTool.exe.config"

  StrCmp ${PROD_OR_TEST} "prod" +1 do_continue
    File "..\Bin\uninst.exe"
  do_continue:

  # service_type:16-在自己的进程中运行的服务  start_type:2-服务自动启动
  DetailPrint "Installing ${PRODUCT_MAIN_NT_SERVICES_NAME} Client service..."
  SimpleSC::InstallService "${PRODUCT_MAIN_NT_SERVICES_NAME}" "MynameSmartTool Client NTService" "16" "2" "$INSTDIR\MynameSmartToolSrv.exe" "" "" "" 
  SimpleSC::SetServiceDescription "${PRODUCT_MAIN_NT_SERVICES_NAME}" "Lst windows services"
  DetailPrint "starting ${PRODUCT_MAIN_NT_SERVICES_NAME} Client service..."
  SimpleSC::StartService "${PRODUCT_MAIN_NT_SERVICES_NAME}" "" 30

  # 开启Windows 共享目录的权限
  DetailPrint "open EnableLinkedConnections..."
  SetRegView 64
  WriteRegDWORD ${PRODUCT_UNINST_ROOT_KEY} "SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" "EnableLinkedConnections" 0x1
  SetRegView 32
SectionEnd

Function .onInstSuccess
FunctionEnd

# 区段名为空、遗漏或者以一个 "-" 开头, 那么它将是一个隐藏的区段, 用户也不能选择禁止它.
Section -AdditionalIcons
  CreateShortCut "$DESKTOP\Myname Smart Tool.lnk" "$INSTDIR\MynameSmartTool.exe"
  CreateShortCut "$SMPROGRAMS\MynameSmartTool\Myname Smart Tool.lnk" "$INSTDIR\MynameSmartTool.exe"
  CreateShortCut "$SMPROGRAMS\MynameSmartTool\Uninstall.lnk" "$INSTDIR\uninst.exe"
SectionEnd

Section -Post
  StrCmp ${PROD_OR_TEST} "test" +1 do_continue
    WriteUninstaller "$INSTDIR\uninst.exe"
  do_continue:

  WriteRegStr HKLM "${PRODUCT_DIR_REGKEY}" "" "$INSTDIR\MynameSmartTool.exe"  # HKLM or HKEY_LOCAL_MACHINE
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\MynameSmartTool.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
SectionEnd

Function un.onInit
  Call un.RunningCheck
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Are you sure you want to completely remove $(^Name) and all of its components?" IDYES +2 IDNO +1
    Abort
FunctionEnd

Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) was successfully removed from your computer."
FunctionEnd

Section Uninstall
  Call un.RomveNTServices

  Delete "$INSTDIR\${PRODUCT_NAME}.url"
  Delete "$INSTDIR\uninst.exe"
  Delete "$INSTDIR\MynameSmartTool.exe.config"
  Delete "$INSTDIR\MynameSmartToolSrv.exe.config"
  Delete "$INSTDIR\MynameSmartTool.exe"
  Delete "$INSTDIR\MynameSmartToolSrv.exe"
  Delete "$INSTDIR\AdaptorManger.dll"
  Delete "$INSTDIR\BasicDefinition.dll"
  Delete "$INSTDIR\Configurations.dll"
  Delete "$INSTDIR\CountryCodePlugin.dll"
  Delete "$INSTDIR\CrachRescureBase.dll"
  Delete "$INSTDIR\DataAccessor.dll"
  Delete "$INSTDIR\DeviceInfoPlugin.dll"
  Delete "$INSTDIR\DeviceManager.dll"
  Delete "$INSTDIR\DevicesModel.dll"
  Delete "$INSTDIR\DotNetZip.dll"
  Delete "$INSTDIR\EntityFramework.dll"
  Delete "$INSTDIR\EntityFramework.Firebird.dll"
  Delete "$INSTDIR\FirebirdSql.Data.FirebirdClient.dll"
  Delete "$INSTDIR\HwDetectionPlugin.dll"
  Delete "$INSTDIR\ICSharpCode.SharpZipLib.dll"
  Delete "$INSTDIR\ISmart.dll"
  Delete "$INSTDIR\Interop.SHDocVw.dll"
  Delete "$INSTDIR\KillSwitchBase.dll"
  Delete "$INSTDIR\KnowledgeBasePlugin.dll"
  Delete "$INSTDIR\Myname.Themes.dll"
  Delete "$INSTDIR\MynameSmartToolNTServiceProxy.dll"
  Delete "$INSTDIR\MynameSmartToolWebApiProxy.dll"
  Delete "$INSTDIR\LibUsbDotNet.dll"
  Delete "$INSTDIR\log4net.dll"
  Delete "$INSTDIR\LSTClientFramework.dll"
  Delete "$INSTDIR\Microsoft.Extensions.Logging.Abstractions.dll"
  Delete "$INSTDIR\Mono.Posix.dll"
  Delete "$INSTDIR\Newtonsoft.Json.dll"
  Delete "$INSTDIR\NPOI.dll"
  Delete "$INSTDIR\NPOI.OOXML.dll"
  Delete "$INSTDIR\NPOI.OpenXml4Net.dll"
  Delete "$INSTDIR\NPOI.OpenXmlFormats.dll"
  Delete "$INSTDIR\OSDPortalPlugin.dll"
  Delete "$INSTDIR\PdfSharp.Charting.dll"
  Delete "$INSTDIR\PdfSharp.dll"
  Delete "$INSTDIR\ProgrammingToolPlugin.dll"
  Delete "$INSTDIR\SmartBase.dll"
  Delete "$INSTDIR\SmartDevice.dll"
  Delete "$INSTDIR\SmartRsd.dll"
  Delete "$INSTDIR\SmartUtil.dll"
  Delete "$INSTDIR\System.Windows.Interactivity.dll"
  Delete "$INSTDIR\Utility.dll"
  Delete "$INSTDIR\WebApiClient.JIT.dll"
  Delete "$INSTDIR\zxing.dll"
  Delete "$INSTDIR\Myname_Smart_Tool_User_guide.pdf"
  Delete "$INSTDIR\Language.xlsx"
  Delete "$INSTDIR\fbembed.dll"
  Delete "$INSTDIR\firebird.conf"
  Delete "$INSTDIR\firebird.msg"
  Delete "$INSTDIR\icudt30.dll"
  Delete "$INSTDIR\icuin30.dll"
  Delete "$INSTDIR\icuuc30.dll"
  Delete "$INSTDIR\Microsoft.VC80.CRT.manifest"
  Delete "$INSTDIR\msvcp80.dll"
  Delete "$INSTDIR\msvcr80.dll"
  Delete "$INSTDIR\ib_util.dll"
  Delete "$INSTDIR\fastboot.exe"
  Delete "$INSTDIR\adb.exe"
  Delete "$INSTDIR\AdbWinApi.dll"
  Delete "$INSTDIR\AdbWinUsbApi.dll"
  Delete "$INSTDIR\Resources\DeviceInfoReader.apk"
  Delete "$INSTDIR\LocalConfig\Workflow.xml"
  Delete "$INSTDIR\LocalConfig\log4net_service.config"
  Delete "$INSTDIR\LocalConfig\log4net.config"
  Delete "$INSTDIR\LocalConfig\LocalResourceStatus.xml"
  Delete "$INSTDIR\LocalConfig\LocalFuncSetting.xml"
  Delete "$INSTDIR\LocalConfig\LocalAppSetting.xml"
  Delete "$INSTDIR\LocalConfig\Config.xml"
  Delete "$INSTDIR\drivers\SmartClock\MynameUsbDriver_autorun_1.1.33_user.exe.zip"
  Delete "$INSTDIR\drivers\QUALCOMM\Qualcomm.win.1.1_installer_10061.1.exe"
  Delete "$INSTDIR\drivers\MTK\x86\usb2ser.sys"
  Delete "$INSTDIR\drivers\MTK\x64\usb2ser.sys"
  Delete "$INSTDIR\drivers\MTK\cdc-acm.inf"
  Delete "$INSTDIR\drivers\MTK\cdc-acm.cat"
  Delete "$INSTDIR\HWDetection\MobileAssistant.apk"
  Delete "$INSTDIR\7za\7za.exe"
  Delete "$INSTDIR\7za\7z.exe"
  Delete "$INSTDIR\7za\7z.dll"
  Delete "$INSTDIR\LNO_CLIENT.FDB"
  Delete "$INSTDIR\intl\fbintl.conf"
  Delete "$INSTDIR\intl\fbintl.dll"

  Delete "$DESKTOP\Myname Smart Tool.lnk"
  Delete "$SMPROGRAMS\MynameSmartTool\Myname Smart Tool.lnk"
  Delete "$SMPROGRAMS\MynameSmartTool\Uninstall.lnk"

  RMDir "$SMPROGRAMS\MynameSmartTool"
  RMDir "$INSTDIR\Resources"
  RMDir "$INSTDIR\intl"
  RMDir "$INSTDIR\LocalConfig"
  RMDir "$INSTDIR\drivers\SmartClock"
  RMDir "$INSTDIR\drivers\QUALCOMM"
  RMDir "$INSTDIR\drivers\MTK\x86"
  RMDir "$INSTDIR\drivers\MTK\x64"
  RMDir "$INSTDIR\drivers\MTK"
  RMDir "$INSTDIR\drivers"
  RMDir "$INSTDIR\HWDetection"
  RMDir /r "$INSTDIR\Operate"
  RMDir "$INSTDIR\7za"
  RMDir "$INSTDIR"

  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  DeleteRegKey HKLM "${PRODUCT_DIR_REGKEY}"
  SetAutoClose true
SectionEnd

