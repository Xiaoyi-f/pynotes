"""
python基础教学
>>> __author__ = "XiaoYi --NieJianbing"
>>> __description__ = "快速入门掌握python基础"
>>> __email__ = "15779544219@163.com"
>>> __license__ = "不开源，无协议，依照法律条纹实现协议"
>>> __copyright__ = "源码文件作者 派小翊 --聂坚兵 保留所有权力以即版权，禁止未经允许传播/商用"
>>> __all__ = []
>>> YI_TEAM = ['YiTeam是作者组织的一个工作室', '专注python全栈开发', '专注AI开发', '专注逆向爬虫开发', '专注数据分析', '申请加入请联系wechat: CodingAlgorithmYT']
>>> for i in range(len(YI_TEAM)):
...    print(YI_TEAM[i])
"""

"""
1.下载安装与基本使用 
浏览器搜索python官网下载对应系统的security安全版本python --> 3.10.xxx
配置系统环境变量 -> 为了使得我们可以随时打开系统的终端使用python的命令解释器 -> 系统设置搜索"环境变量" -> 配置Path环境变量，将需要全局搜寻的路径添加进去即可
使用包管理工具pip 
pip --version
pip install package[==版本号](pip默认不区分包名大小写，但是建议统一使用对应官方说明的名字) -> 安装包
pip uninstall package -> 卸载包
pip list -> 查看已经安装过的所有包
pip config list -> 查看配置好的源
pip config set (按照 pip config list 给出的形式把那个'='替换为空格 换行则重新再执行一次对应的pip config set ...命令)
pip freeze > requirements.txt -> 将当前环境的包列表冻结版本信息并保存到requirements.txt文件中
pip install -r requirements.txt -> 启动请求安装模式并且从版本列表文件requirements.txt安装
pip show package -> 查看某个包的详细信息
推荐官方高级命令行解释器: pip install ipython 
推荐IDE -> Pycharm 
Pycharm推荐插件:
    BlackConnect
    CMD Support
    CodeGlance Pro
    Indent Rainbow
    Inspection Lens
    Lingma -Alibaba
    Material Theme UI Lite
    Rainbow Brackets Lite - Free
    Translation
Pycharm基本使用:
    配置按键映射 -> ctrl d 删除当前行
    ctrl z 撤销操作 
    ctrl shift z 反撤销操作 
    F11 给当前行贴标签
    ctrl shift F10 运行对应文件
    alt F12 打开终端 
    shift enter 直接下开一行
    顶部tab文件栏通过鼠标上下滚轮可以滚动
开发辅助工具:
    AI --> 辅助开发必会
    Xshell --> 远程终端连接软件
    Xftp --> 本地机与虚拟/远程机资源交互软件
    Navicat --> 图形化数据库操作软件
    Postman/Apipost --> 接口测试软件
    WattToolkit/Clash --> VPN
    typora --> MarkDown笔记软件
"""
