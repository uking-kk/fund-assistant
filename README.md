# 基金智能助手

基于大语言模型的基金投资问答助手，帮助普通投资者解决"选基金难"的问题。

## 功能特点

- 💬 **智能问答**：基于RAG技术，回答基金基础知识问题
- 📊 **基金查询**：通过API查询基金净值、收益、持仓等信息
- 🎯 **智能推荐**：根据用户偏好推荐合适的基金

## 技术栈

### 前端
- React 18 + Vite
- Tailwind CSS + Framer Motion

### 后端
- Python 3.11 + FastAPI
- LangChain + Chroma（向量数据库）

### AI
- 火山方舟 API（豆包大模型）
- BGE-small-zh（中文向量模型）

## 快速开始

### 环境要求
- Python 3.11+
- Node.js 18+

### 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入你的 API Key

# 启动服务
uvicorn app.main:app --reload --port 8000
```

### 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 访问应用

打开浏览器访问 http://localhost:5173

## 项目结构

```
基金智能助手/
├── backend/                 # 后端代码
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── core/           # 核心逻辑
│   │   ├── services/       # 服务层
│   │   └── knowledge/      # 知识库
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/               # 前端代码
│   ├── src/
│   │   ├── components/     # 组件
│   │   ├── hooks/          # Hooks
│   │   └── lib/            # 工具函数
│   └── package.json
│
└── README.md
```

## API文档

启动后端后访问 http://localhost:8000/docs 查看Swagger文档。

## 部署

支持部署到 Vercel + Railway/Render，详见 `docs/技术架构文档.md`。

## License

MIT
