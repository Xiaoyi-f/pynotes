:: 这是注释
@echo off          :: ← 关闭命令显示，脚本第一行必备
echo Hello World   :: ← 显示文本
echo.              :: ← 输出空行（注意有个点）
pause              :: ← 暂停，显示"按任意键继续"
title 我的脚本     :: ← 设置窗口标题
color 0A           :: ← 设置颜色（0背景黑，A前景绿）
cls                :: ← 清屏
echo 操作完成！    :: ← 给用户提示信息

systeminfo :: 查看系统信息
cleanmgr :: 清理磁盘

:: win r 运行框命令 -> services.msc -> mspaint -> cmd ctrl enter开启管理员权限打开cmd

cd                           :: 显示当前目录的完整路径
cd Documents                 :: 进入Documents目录
cd..                         :: 返回上一级目录
cd\                          :: 直接返回C盘根目录
mkdir NewFolder              :: 创建名为NewFolder的新文件夹
rmdir OldFolder /s /q        :: 强制删除OldFolder目录（/s包含子目录，/q不询问确认）

dir                          :: 列出当前目录所有文件和文件夹
dir *.txt                    :: 只列出扩展名为.txt的文件
dir /b                       :: 简洁模式，只显示文件名不显示详细信息
dir /s                       :: 递归列出，包括所有子目录内容
dir /a:h                     :: 显示隐藏文件（/a表示属性，h=hidden）

copy source.txt backup.txt   :: 复制source.txt文件并命名为backup.txt
xcopy source dest /e /i /y   :: 复制整个目录（/e包含空文件夹，/i视为目录，/y覆盖不提示）

move old.txt new.txt         :: 移动文件，也可用于重命名文件
del temp.tmp                 :: 删除temp.tmp文件
del *.log /q                 :: 静默删除所有.log文件（/q不询问确认）
type readme.txt              :: 显示readme.txt文件的文本内容

echo %cd%                    :: 显示当前工作目录的完整路径
echo %~dp0                   :: 显示批处理脚本自身所在的目录路径（重要！）
echo %~nx1                   :: 显示第一个参数的文件名和扩展名部分

set username=张三            :: 创建变量username，值为"张三"（注意：等号两边不能有空格）
echo %username%              :: 使用变量，显示"张三"
set /p choice=请输入选择：    :: 暂停等待用户输入，将输入值存入choice变量
set /a result=10+5*2         :: 进行数学计算，10+5*2=20，结果存入result变量（/a表示算术运算）

echo %date%                  :: 显示当前系统日期，格式：2023/12/25
echo %time%                  :: 显示当前系统时间，格式：14:30:25.45
echo %username%              :: 显示当前登录的用户名
echo %computername%          :: 显示计算机的名称
echo %random%                :: 生成一个0-32767之间的随机整数
echo %errorlevel%            :: 显示上一条命令的退出代码，0表示成功，非0表示失败

:: 判断变量值是否相等
if "%input%"=="yes" echo 您选择了是

:: 判断文件或文件夹是否存在
if exist "C:\test\data.txt" echo 数据文件存在
if not exist "logs\" mkdir logs   :: 如果logs文件夹不存在，则创建它

:: 判断是否提供了命令行参数
if "%1"=="" (
    echo 错误：请提供文件名作为参数
) else (
    echo 正在处理文件：%1
)

:: 使用错误代码判断命令是否执行成功
ping 127.0.0.1 >nul 2>&1 && echo 网络正常 || echo 网络异常

:: 遍历当前目录所有.txt文件
for %%i in (*.txt) do (
    echo 找到文本文件：%%i
)

:: 遍历当前目录所有子文件夹
for /d %%i in (*) do (
    echo 找到文件夹：%%i
)

:: 数字循环，从1到5，每次增加1
for /l %%i in (1,1,5) do (
    echo 当前数字：%%i
)

:: 处理命令的输出结果（逐行处理）
for /f "tokens=*" %%i in ('dir /b') do (
    echo 文件项：%%i
)

:: 定义标签并跳转执行（注意：标签前必须有冒号）
:start_point
echo 这是程序的开始...
goto next_step

:next_step
echo 现在执行下一步...

:: 调用子程序（函数）
call :print_message "你好，世界！"
exit /b 0  :: 主程序结束

:: 子程序（函数）定义
:print_message
echo 消息：%~1  :: %~1表示去掉引号的第一个参数
exit /b        :: 子程序返回

dir > filelist.txt          :: 将dir命令的输出保存到filelist.txt文件（覆盖模式）
dir >> filelist.txt         :: 将dir命令的输出追加到filelist.txt文件（追加模式）
sort < unsorted.txt         :: 从unsorted.txt文件读取内容进行排序

dir >nul                    :: 将正常输出丢弃到空设备（屏幕上不显示）
dir 2>nul                   :: 将错误信息丢弃到空设备（不显示错误）
dir > output.txt 2>&1       :: 将正常输出和错误信息都保存到output.txt文件

ping 127.0.0.1 -n 3 >nul   :: ping本地地址3次，用于制造3秒延迟（>nul不显示输出）
timeout /t 10               :: 等待10秒（Windows 7以上系统支持）

ipconfig                    :: 显示网络配置信息（IP地址、网关等）
netstat -an                 :: 显示所有网络连接和端口监听状态

tasklist                    :: 显示当前正在运行的所有进程列表
taskkill /im notepad.exe /f :: 强制结束所有记事本进程（/im按进程名，/f强制结束）

systeminfo                  :: 显示详细的系统信息（系统版本、内存、补丁等）
ver                         :: 显示简化的Windows版本信息

@echo off
:: 尝试执行需要管理员权限的命令
net session >nul 2>&1
:: 检查上条命令的返回代码，如果不是0表示不是管理员
if %errorlevel% neq 0 (
    echo 需要管理员权限，正在重新以管理员身份运行...
    :: 使用PowerShell重新启动当前脚本并请求管理员权限
    powershell start-process '%~f0' -verb runas
    exit  :: 当前非管理员进程退出
)
:: 从这里开始代码以管理员权限运行
echo 当前已获得管理员权限！

@echo off
:: 显示脚本自身信息
echo 脚本名称：%~nx0  :: %~nx0 = 文件名.扩展名
echo 完整路径：%~f0   :: %~f0 = 完整路径+文件名

:: 处理传入的参数
echo 第一个参数：%~1
echo 第二个参数：%~2
echo 所有参数：%*     :: %* = 所有参数（不包括%0）

:: 判断参数数量
if "%~1"=="" (
    echo 使用方法：%~nx0 [参数1] [参数2]
    exit /b 1  :: 退出并返回错误代码1
)

@echo off
:main_menu
cls  :: 清屏
echo ================================
echo         主菜单
echo ================================
echo 1. 备份文件
echo 2. 清理临时文件
echo 3. 查看系统信息
echo 4. 退出程序
echo.

:: 等待用户输入选择
set /p menu_choice=请输入选择编号（1-4）：
if "%menu_choice%"=="1" goto backup_files
if "%menu_choice%"=="2" goto cleanup_temp
if "%menu_choice%"=="3" goto system_info
if "%menu_choice%"=="4" exit /b 0

:: 如果输入无效，返回菜单
echo 无效的选择，请重新输入！
pause
goto main_menu

:backup_files
echo 正在备份文件...
:: 这里写备份逻辑
pause
goto main_menu


::参数	    说明	             使用示例
::/y	自动回答"Yes"确认	  del /y temp.txt
::/s	包含所有子目录	      dir /s *.txt
::/q	安静模式，不询问	rmdir /s /q old_dir
::/f	强制操作	        taskkill /f /im chrome.exe
::/p	分页显示	        more /p longfile.txt
::/b	简洁格式（无额外信息）	dir /b
::/d	只显示目录	        dir /ad
::/w	宽格式显示	        dir /w

::补充: win + r 输入 services.msc 查看/管理所有服务
::补充: win + r 输入 mspaint 打开画图工具

