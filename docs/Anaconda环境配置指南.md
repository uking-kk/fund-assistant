# 基金智能助手 - Anaconda环境配置指南

> 本文档教你如何使用Anaconda配置Python环境，适合Windows用户。

---

## 一、安装Anaconda

### 1.1 下载Anaconda

1. 访问官网：https://www.anaconda.com/download
2. 选择 Windows 版本下载
3. 下载完成后双击安装

### 1.2 安装步骤

```
1. 欢迎界面 → Next
2. 许可协议 → I Agree
3. 安装类型 → Just Me (推荐)
4. 安装路径 → 默认或自定义（记住这个路径）
5. 高级选项 → 勾选 "Add Anaconda to my PATH"（方便命令行使用）
6. Install → 等待安装完成
```

### 1.3 验证安装

打开 **Anaconda Prompt** 或 **PowerShell**：

```powershell
# 检查conda版本
conda --version
# 输出示例: conda 23.7.4

# 检查Python版本
python --version
# 输出示例: Python 3.11.5
```

---

## 二、创建项目环境

### 2.1 创建虚拟环境

```powershell
# 进入项目目录
cd "d:\AIE55期课程文件合计\个人项目\基金智能助手\backend"

# 创建名为 fund-assistant 的虚拟环境，Python版本3.11
conda create -n fund-assistant python=3.11 -y

# 看到 Proceed ([y]/n)? 输入 y 回车
```

### 2.2 激活环境

```powershell
# 激活虚拟环境
conda activate fund-assistant

# 成功后，命令行前面会显示 (fund-assistant)
# 例如: (fund-assistant) D:\AIE55期课程文件合计\个人项目\基金智能助手\backend>
```

### 2.3 验证环境

```powershell
# 检查当前Python路径
where python
# 应该显示 Anaconda环境下的Python路径

# 检查已安装的包
conda list
```

---

## 三、安装项目依赖

### 3.1 安装依赖

```powershell
# 确保在虚拟环境中
conda activate fund-assistant

# 进入backend目录
cd "d:\AIE55期课程文件合计\个人项目\基金智能助手\backend"

# 安装依赖
pip install -r requirements.txt
```

### 3.2 常见安装问题

#### 问题1: pip安装速度慢

```powershell
# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 问题2: chromadb安装失败

```powershell
# 先安装依赖
pip install chromadb==0.4.22 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 问题3: sentence-transformers安装慢

```powershell
# 这个包比较大，耐心等待
pip install sentence-transformers==2.3.1 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 四、配置环境变量

### 4.1 创建.env文件

```powershell
# 在backend目录下
cd "d:\AIE55期课程文件合计\个人项目\基金智能助手\backend"

# 复制模板
copy .env.example .env
```

### 4.2 编辑.env文件

用记事本或VS Code打开 `.env` 文件：

```
# 火山方舟API配置
ARK_API_KEY=你的API密钥
ARK_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
ARK_MODEL=doubao-seed-2-0-pro-260215

# 向量模型配置
EMBEDDING_MODEL=BAAI/bge-small-zh-v1.5
CHROMA_PERSIST_DIR=./chroma_db

# CORS配置
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

---

## 五、启动项目

### 5.1 启动后端

```powershell
# 1. 激活环境
conda activate fund-assistant

# 2. 进入backend目录
cd "d:\AIE55期课程文件合计\个人项目\基金智能助手\backend"

# 3. 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

看到以下输出表示成功：

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 5.2 测试后端

打开浏览器访问：
- http://localhost:8000 → 看到 {"message": "基金智能助手 API", "version": "1.0.0"}
- http://localhost:8000/docs → Swagger API文档

---

## 六、常用命令

### 6.1 环境管理

```powershell
# 查看所有环境
conda env list

# 激活环境
conda activate fund-assistant

# 退出环境
conda deactivate

# 删除环境（如果需要重建）
conda remove -n fund-assistant --all
```

### 6.2 包管理

```powershell
# 查看已安装的包
conda list

# 安装新包
pip install 包名

# 卸载包
pip uninstall 包名

# 导出依赖
pip freeze > requirements.txt
```

### 6.3 启动命令

```powershell
# 开发模式（带热重载）
uvicorn app.main:app --reload --port 8000

# 生产模式
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 七、VS Code配置（推荐）

### 7.1 选择Python解释器

1. 打开VS Code
2. 打开项目文件夹
3. 按 `Ctrl+Shift+P`
4. 输入 `Python: Select Interpreter`
5. 选择 `fund-assistant` 环境的Python

### 7.2 安装推荐插件

- Python (Microsoft)
- Pylance
- Python Debugger

---

## 八、完整启动流程

```powershell
# === 启动后端 ===
# 1. 打开 Anaconda Prompt 或 PowerShell
# 2. 激活环境
conda activate fund-assistant

# 3. 进入backend目录
cd "d:\AIE55期课程文件合计\个人项目\基金智能助手\backend"

# 4. 启动后端
uvicorn app.main:app --reload --port 8000

# === 启动前端（新开一个终端）===
# 1. 打开新的 PowerShell
# 2. 进入frontend目录
cd "d:\AIE55期课程文件合计\个人项目\基金智能助手\frontend"

# 3. 安装依赖（首次）
npm install

# 4. 启动前端
npm run dev

# 5. 打开浏览器访问 http://localhost:5173
```

---

## 九、常见问题

### Q1: conda命令找不到？

**解决**：
1. 使用 Anaconda Prompt 而不是普通CMD
2. 或者添加环境变量：将 `C:\Users\你的用户名\anaconda3\Scripts` 添加到PATH

### Q2: 激活环境失败？

```powershell
# 初始化conda
conda init powershell

# 重启PowerShell后再试
conda activate fund-assistant
```

### Q3: 端口被占用？

```powershell
# 查看8000端口占用
netstat -ano | findstr :8000

# 结束占用进程（PID是上面查到的数字）
taskkill /PID 进程号 /F
```

### Q4: 如何更新依赖？

```powershell
conda activate fund-assistant
pip install --upgrade -r requirements.txt
```
