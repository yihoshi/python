实时投票系统技术文档

1. 系统概述
实时投票系统是一个基于现代Web技术栈的应用程序，允许用户参与投票并实时查看投票结果。系统采用前后端分离架构，使用WebSocket实现投票结果的实时推送功能。
功能特点
用户投票界面（单选）
实时投票结果展示（图表+数字）
投票结果实时更新（跨浏览器同步）
防止重复投票（前端限制）

3. 技术栈
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
技术选型说明

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
