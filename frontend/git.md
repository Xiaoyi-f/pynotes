# IDEA自带git工具基本使用：
    1.将改动文件添加到暂存区
    2.输入提交信息之后提交到本地仓库
    3.提交之后推送到远程仓库

# [工作区]  --git add-->  [暂存区]  --git commit-->  [本地仓库]  --git push-->  [远程仓库]
# 不要存放视频/音频文件/超过100mb的文件
# 基本命令:
cd 对应目录
git init
git clone <url> 
git checkout -b branch_name 
git pull <别名> <分支>
git status 

[//]: # (git branch )
# 分支
[//]: # (git branch -d <分支名>)

git add . 
git commit -m 'commit_sentence'
git push -u <别名> <分支>
git remote -v 
git remote add <别名> <url>
git remote rm <别名>
git merge <分支>

# 合并分支注意点: 若提示CONFLICT则表明发生冲突,需要自行解决冲突之后再提交

# Eslint配置->解决行尾序列符不一问题
rules: {
  "prettier/prettier": ["error", { endOfLine: "auto" }]
}

# 多余子git问题->解决git提交问题
删除子目录的子.git文件
git rm -r --cached 子目录 # --cached一定要开

# 设置代理
git config --global https.proxy http://127.0.0.1:[代理端口]

