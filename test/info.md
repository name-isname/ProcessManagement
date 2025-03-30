# AI 时代的软件开发新范式:认知敏捷开发方法
在 AI时代，软件开发已经从传统的“手工编码”转变为“与 A!协作开发"。认知敏捷开发方法(Cognive Agile Development)是一种适应 AI
时代的新型开发范式，它在敏捷开发的基础上，强调了 如何高效利用 AI 进行软件开发，让 AI 成为开发过程中的核心助手。

# 认知敏捷开发的核心理念
1. 以 AI 为核心辅助工具:开发流程围绕 AI 进行优化，减少重复性劳动，提高开发效率。
2. 文档驱动开发(Documentation-Driven Development):先写文档，特别是写给 A|看的文档，确保 A1 能正确理解需求、生成高质
量代码。
3. 先验证核心逻辑，再扩展功能:先从 CLI(命令行工具)开始，确保核心逻辑正确，再扩展到 AP1、前端、移动端等。

4. 基于开源生态优化技术选型:选择 A1训练数据较多、支持较好的技术栈，减少 A| 生成代码的错误率。
5. 快速迭代，验证正确性:利用 A 快速生成、测试和优化代码，确保开发过程敏捷、高效。

# 认知敏捷开发的 8 大步骤
## 1. 需求分析:先写 README
- 不要一上来就让 AI 设计代码，这样容易偏离方向，错误率也高。
- 先编写 README.md，描述项目的基本信息，包括:
    - 项目目标
    - 主要功能
    - 预期技术栈
    - 参考的开源项目（如果有）

## 2. 让 AI生成详细 PRD
- 在 README 的基础上，让 A| 生成 详细的 **PRD(产品需求文档)**
- **注意**:PRD 不是写给产品经理看的，而是写给 AI看的，确保 AI 能理解需求并正确生成代码
- PRD 需要包括:
    1. **项目背景**
    2. **典型用户用例(站在 AI 生成数据库和测试用例的角度编写)**
    3. **技术选型架构**
    4. **核心流程**
    5. **关键技术实现(代码示例)**

## 3.让 A| 生成数据库 Schema
- 基于 PRD，让 Al生成数据库 Schema，包括:
    - 数据库表结构
    - 字段类型
    - 关系定义
    - SQL建表语句
    - 测试数据
- 示例:
```SQL
CREATE TABLE users(
id SERIAL PRIMARY KEY,
emai1 VARCHAR(255)UNIQUE NOT NULL,
password_hash TEXT,
auth_provider VARCHAR(50),
created_at at TIMESTAMP DEFAULT NOW()
);
INSERT INTO users(email, password_hash, auth_provider)
VALUES('test@example.com','hashed password','google');
```
- 验证数据库结构:将 SQL脚本导入数据库，检查是否符合预期。

# 4. 让 AI 生成后端 API
- 先写 CLI(命令行工具)，再扩展 API
- 让 Al 生成后端 API 代码，包括:
    - 核心类、函数
    - API端点(RESTful 或 GraphQL)
    - 认证 & 权限管理
- **示例(CLI 代码)**
```python
import click
import hashlib

@click.command()
@click.option('--email',prompt='Email', help='User email')
@click.option('--password', prompt=True, hide input=True, confirmation prompt=True, help='User password')

def register(email, password):
    password hash = hashlib.sha256(password.encode()).hexdigest()
    print(f"User {email} registered with hash: {password_hash}")

if __name__ == '__main__':
    register()
```
- **确保 CLI 代码正确后，再扩展 API:**
```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/register")
def register(email:str, password: str):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return {"email": email,"password_hash": password_hash}
```

README定方向
AI生产PRD
设计数据库
先CLI再API
生成文档
推导前端需求
AI生成UI
扩展至全平台