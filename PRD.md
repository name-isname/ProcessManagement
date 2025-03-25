# 产品需求文档 (PRD)

## 1. 项目背景
在现代工作环境中，任务管理面临着诸多挑战，如截止期限不合理、任务复杂度高、工作记忆有限等。为了解决这些问题，我们设计了一款以进程为中心的任务管理系统，旨在通过对进程的CRUD操作，帮助用户更有效地管理任务。

## 2. 典型用户用例
- **用例1: 创建新进程**
  - 用户输入进程名称、状态、优先级和详细信息。
  - 系统保存进程并返回成功消息。
- **用例2: 更新进程状态**
  - 用户选择一个进程并修改其状态。
  - 系统更新进程信息并记录日志。
- **用例3: 查询进程**
  - 用户根据优先级或状态查询进程列表。
  - 系统返回符合条件的进程列表。

## 3. 技术选型架构
- **后端**: 使用Python和FastAPI框架，提供RESTful API。
- **数据库**: 使用SQLAlchemy链接SQLite，存储进程数据。
- **前端**: 使用HTML、CSS和JavaScript构建用户界面。

## 4. 核心流程
1. 用户通过前端界面输入进程信息。
2. 前端将数据发送至后端API。
3. 后端处理请求，进行数据库操作。
4. 后端返回结果至前端，更新用户界面。

## 5. 关键技术实现 (代码示例)
```python
# 示例：创建进程的API端点
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Process(BaseModel):
    name: str
    status: str
    priority: str
    details: str = None

@app.post("/process/")
async def create_process(process: Process):
    # 假设这里有数据库操作代码
    return {"message": "Process created successfully", "process": process}