nvm是一个管理node版本的工具，建议下载使用
首先自行换源 --> AI
nvm list available 查看可以安装的版本
nvm install 版本号 
nvm list 查看已经安装过的版本
nvm use 版本号 使用对应版本
nvm uninstall 版本号 删除对应版本
node项目都需要有 package.json 以即 package-lock.json 作为项目的配置文件
JS/TS需要使用ESModule，需要在package.json中将type属性设置为'module'
import export 机制 -> export default 只能一个模块最多一个，此外的export都需要使用{}(花括号)阔起
npm init 初始化项目的配置文件
npm install 优先从package-lock.json安装包，若没有则会依照package.json安装，并且创建lock配置文件
--save 安装到dependencies --save-dev 安装到devDependencies -> 写入本地package.json
-g 全局安装
npm install 包名@版本号  
npm list 查看当前项目安装的包 -g 查看全局安装的包
npm uninstall 包 卸载包
npm config get registry --> 查看当前配置的源 --> 换源问AI
npx --> 专门为终端执行包设计的工具


