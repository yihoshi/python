实时投票系统技术文档
1. 系统概述
实时投票系统是一个基于现代Web技术栈的应用程序，允许用户参与投票并实时查看投票结果。系统采用前后端分离架构，使用WebSocket实现投票结果的实时推送功能。

功能特点
用户投票界面（单选）
实时投票结果展示（图表+数字）
投票结果实时更新（跨浏览器同步）
防止重复投票（前端限制）
2. 技术栈
前端
​​框架​​：Vue 3
​​构建工具​​：Vite
​​图表库​​：Chart.js + vue-chartjs
​​网络通信​​：Axios (REST), WebSocket API (实时)
后端
​​框架​​：FastAPI (Python)
​​数据库​​：MySQL
​​ORM​​：SQLAlchemy
​​实时通信​​：WebSocket
开发工具
​​数据库管理​​：MySQL Workbench
​​API测试​​：Postman 或 curl
​​版本控制​​：Git
3. 系统架构图
+-----------------+       +-----------------+       +-----------------+
|                 |       |                 |       |                 |
|   Vue 3 前端    |<----->|   FastAPI 后端  |<----->|     MySQL       |
|   (Vite)        | HTTP  |   (Python)      |       |     数据库      |
|                 |       |                 |       |                 |
+--------+--------+       +--------+--------+       +-----------------+
         |                          |
         | WebSocket (实时更新)     |
         +--------------------------+
4. API接口说明
基础URL
http://localhost:8000

1. 获取投票问卷
​​端点​​：GET /api/poll

​​响应示例​​：

{
  "id": 1,
  "title": "您最喜欢的编程语言是什么？",
  "options": [
    {
      "id": 1,
      "text": "Python",
      "votes": 5
    },
    {
      "id": 2,
      "text": "JavaScript",
      "votes": 3
    },
    // ...其他选项
  ]
}
2. 提交投票
​​端点​​：POST /api/poll/vote

​​请求体​​：

{
  "option_id": 1
}
​​响应示例​​：

{
  "message": "投票成功",
  "option_id": 1,
  "votes": 6
}
3. WebSocket 实时更新
​​端点​​：ws://localhost:8000/ws/poll

​​消息格式​​：

{
  "poll_id": 1,
  "title": "您最喜欢的编程语言是什么？",
  "options": [
    {"id": 1, "text": "Python", "votes": 5},
    {"id": 2, "text": "JavaScript", "votes": 3},
    // ...其他选项
  ]
}
5. 实时推送机制
技术实现
使用 WebSocket 协议实现全双工通信
后端维护一个 WebSocket 连接管理器
当投票发生时，后端广播更新到所有连接的客户端
工作流程
前端页面加载时建立 WebSocket 连接
用户提交投票后，后端更新数据库
后端查询最新投票结果
后端通过 WebSocket 广播更新到所有客户端
前端接收更新并刷新界面
6. 数据库设计
表结构
​​polls 表（问卷）​​

字段	类型	描述
id	INT	主键
title	VARCHAR(255)	问卷标题
created_at	TIMESTAMP	创建时间
​​options 表（选项）​​

字段	类型	描述
id	INT	主键
poll_id	INT	外键，关联问卷
text	VARCHAR(255)	选项文本
votes	INT	当前票数
关系
一个问卷有多个选项（1:N）
每个选项属于一个问卷
7. 安装与运行
环境要求
Python 3.8+
Node.js 16+
MySQL 8.0+
安装步骤
​​克隆仓库​​
git clone https://github.com/yourusername/realtime-voting.git
cd realtime-voting
​​初始化后端环境​​
运行 init_backend.bat (Windows)
根据提示输入 MySQL 凭据
脚本将：
创建 Python 虚拟环境
安装后端依赖
配置环境变量
初始化数据库
​​启动项目​​
运行 run.bat (Windows)
脚本将：
启动后端服务 (http://localhost:8000)
启动前端开发服务器 (http://localhost:5173)
手动启动
​​后端​​

cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
​​前端​​

cd frontend
npm install
npm run dev
8. 测试方法
​​打开两个浏览器窗口​​ 访问 http://localhost:5173
​​在左侧窗口投票​​ 选择任意选项提交
​​观察右侧窗口​​ 应实时更新投票结果
​​在右侧窗口投票​​ 选择另一个选项
​​观察左侧窗口​​ 应实时更新投票结果
9. 项目结构
realtime-voting/
├── backend/                  # 后端代码
│   ├── app/                  # FastAPI应用
│   │   ├── __init__.py
│   │   ├── main.py           # 主应用
│   │   ├── database.py        # 数据库连接
│   │   ├── models.py         # 数据模型
│   │   ├── schemas.py        # Pydantic模型
│   │   ├── crud.py           # 数据库操作
│   │   └── websocket.py      # WebSocket管理
│   ├── requirements.txt      # 依赖列表
│   └── .env                  # 环境变量
│
├── frontend/                 # 前端代码
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/       # Vue组件
│   │   │   └── PollChart.vue # 图表组件
│   │   ├── services/         # API服务
│   │   │   ├── api.js        # REST API服务
│   │   │   └── websocket.js  # WebSocket服务
│   │   ├── App.vue           # 主组件
│   │   └── main.js           # 入口文件
│   ├── package.json
│   └── vite.config.js        # Vite配置
│
├── init.sql                  # 数据库初始化脚本
├── init_backend.bat          # 后端初始化脚本
└── run.bat                   # 项目启动脚本
10. 技术选型说明
前端选型
​​Vue 3​​：提供响应式数据绑定和组件化开发
​​Vite​​：极速的开发服务器启动和热重载
​​Chart.js​​：轻量级图表库，满足数据可视化需求
后端选型
​​FastAPI​​：高性能Python框架，自带API文档生成
​​SQLAlchemy​​：成熟的Python ORM，支持多种数据库
​​WebSocket​​：低延迟实时通信协议，适合投票场景
数据库选型
​​MySQL​​：成熟的关系型数据库，满足事务性需求
11. 演示截图
投票界面
![alt text](image.png)
实时更新演示（两个窗口）
![alt text](image-1.png)
![alt text](image-2.png)
API文档
![alt text](image-3.png)
12. 注意事项
​​数据库安全​​：生产环境不要使用root用户
​​投票限制​​：当前仅前端限制重复投票，生产环境应增加后端验证
​​跨域问题​​：开发环境已配置CORS，生产环境应指定具体域名
​​性能优化​​：高并发场景下应考虑使用Redis缓存投票结果
​​WebSocket连接​​：生产环境应考虑使用WebSocket负载均衡
