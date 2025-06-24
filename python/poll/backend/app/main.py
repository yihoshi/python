from fastapi import FastAPI, Depends, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import crud, schemas, models, database
from .database import get_db, engine
from .websocket import manager  # 导入manager实例
import json
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建数据表
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="实时投票系统API",
    description="一个实时投票系统后端API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 根路由 - 显示欢迎信息和API文档链接
@app.get("/", tags=["Root"])
def read_root():
    logger.info("根路由被访问")
    return {
        "message": "欢迎使用实时投票系统API",
        "documentation": "访问 /docs 查看API文档",
        "endpoints": {
            "GET /api/poll": "获取投票数据",
            "POST /api/poll/vote": "提交投票",
            "WebSocket /ws/poll": "订阅实时投票更新"
        }
    }

# 健康检查
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "服务运行正常"}

# RESTful API
@app.get("/api/poll", response_model=schemas.PollBase, tags=["投票"])
def get_poll_data(db: Session = Depends(get_db)):
    logger.info("获取投票数据请求")
    poll = crud.get_poll(db, poll_id=1)
    if not poll:
        logger.error("投票问卷未找到")
        raise HTTPException(status_code=404, detail="投票问卷未找到")
    return poll

@app.post("/api/poll/vote", tags=["投票"])
async def submit_vote(option_id: int, db: Session = Depends(get_db)):
    logger.info(f"收到投票请求，选项ID: {option_id}")
    updated_option = crud.increment_vote(db, option_id)
    if not updated_option:
        logger.error(f"选项未找到: {option_id}")
        raise HTTPException(status_code=404, detail="选项未找到")
    
    # 广播投票更新
    poll_data = crud.get_poll(db, poll_id=1)
    
    # 使用 await 调用异步方法
    await manager.broadcast(json.dumps({
        "poll_id": poll_data.id,
        "options": [
            {"id": opt.id, "text": opt.text, "votes": opt.votes}
            for opt in poll_data.options
        ]
    }))
    
    return {"message": "投票提交成功", "option_id": option_id}

# WebSocket 端点
@app.websocket("/ws/poll")
async def websocket_endpoint(websocket: WebSocket):
    logger.info("新的WebSocket连接")
    # 使用导入的manager实例
    await manager.connect(websocket)
    try:
        # 当客户端连接时，立即发送当前投票数据
        db = next(database.get_db())
        poll_data = crud.get_poll(db, poll_id=1)
        if poll_data:
            await websocket.send_text(json.dumps({
                "poll_id": poll_data.id,
                "options": [
                    {"id": opt.id, "text": opt.text, "votes": opt.votes}
                    for opt in poll_data.options
                ]
            }))
        else:
            logger.warning("未找到投票数据")
            
        # 保持连接打开
        while True:
            await websocket.receive_text()
    except Exception as e:
        logger.error(f"WebSocket错误: {e}")
    finally:
        manager.disconnect(websocket)
        logger.info("WebSocket连接关闭")