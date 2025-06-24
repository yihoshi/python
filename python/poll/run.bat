@echo off
setlocal

:: 启动后端
start cmd /k "cd backend && venv\Scripts\activate && uvicorn app.main:app --reload --port 8000"

:: 启动前端
start cmd /k "cd frontend && npm install && npm run dev"

endlocal