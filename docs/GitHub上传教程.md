# GitHub上传教程

## 第一步：打开PowerShell

1. 按 `Win + X`
2. 选择 **Windows PowerShell** 或 **终端**

## 第二步：执行以下命令

```powershell
# 1. 进入项目目录
cd "d:\AIE55期课程文件合计\个人项目\基金智能助手"

# 2. 查看当前状态（确认文件已添加）
git status

# 3. 提交代码到本地仓库
git add .
git commit -m "Initial commit: 基金智能助手"

# 4. 查看提交结果
git log --oneline
```

## 第三步：在GitHub创建仓库

1. 打开浏览器，访问 https://github.com/new
2. 填写信息：
   - **Repository name**: `fund-assistant`
   - **Description**: `基金智能助手 - 基于大模型的基金投资问答系统`
   - 选择 **Public**
   - **不要勾选** "Add a README file"
   - **不要勾选** ".gitignore"
   - **不要勾选** "license"
3. 点击绿色按钮 **Create repository**

## 第四步：关联并推送

创建仓库后，GitHub会显示一些命令。**忽略它们**，直接执行：

```powershell
# 关联远程仓库
git remote add origin https://github.com/uking-kk/fund-assistant.git

# 设置主分支
git branch -M main

# 推送代码到GitHub
git push -u origin main
```

## 第五步：验证

1. 刷新你的GitHub页面
2. 访问 https://github.com/uking-kk/fund-assistant
3. 应该能看到所有代码文件

---

## 常见问题

### Q: git push 报错 "fatal: 'origin' already exists"

执行：
```powershell
git remote remove origin
git remote add origin https://github.com/uking-kk/fund-assistant.git
git push -u origin main
```

### Q: git push 报错 "fatal: Authentication failed"

需要登录GitHub：
1. 执行 `git config --global user.name "你的用户名"`
2. 执行 `git config --global user.email "你的邮箱"`
3. 可能需要输入GitHub密码或Token

### Q: 如何获取GitHub Token？

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 勾选 `repo` 权限
4. 生成后复制Token
5. 在push时输入Token作为密码

---

## 完整命令汇总

```powershell
# === 完整流程 ===

# 1. 进入目录
cd "d:\AIE55期课程文件合计\个人项目\基金智能助手"

# 2. 配置用户信息（如果没配置过）
git config --global user.name "uking-kk"
git config --global user.email "你的邮箱"

# 3. 添加文件
git add .

# 4. 提交
git commit -m "Initial commit: 基金智能助手"

# 5. 关联远程仓库（先在GitHub创建仓库）
git remote add origin https://github.com/uking-kk/fund-assistant.git

# 6. 推送
git branch -M main
git push -u origin main
```

执行完这些命令后，访问 https://github.com/uking-kk/fund-assistant 就能看到你的项目了！
