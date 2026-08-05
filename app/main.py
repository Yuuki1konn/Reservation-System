from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text
from app.db.session import engine
from app.routers.auth import router as auth_router
from app.routers.users import router as user_router
from app.routers.resources import router as resource_router
@asynccontextmanager
async def lifespan(app: FastAPI):
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
        print("数据库连接成功")
    yield
    engine.dispose()
    print("数据库连接已关闭")
#FastAPI 类
app = FastAPI(
    title = "预约系统 API",
    description = "基于 FastAPI 开发的预约系统",
    version = "0.1.0",
    lifespan = lifespan
)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(resource_router)
#装饰器 
#在声明类时，会将类的get方法注册为路由，路由的路径为"/",当读取"/"路径时，
# 会调用get方法，返回一个字典，字典中包含一个键值对，键为"message"，值为"预约系统启动成功"
@app.get("/")
def root():
    return {"message": "预约系统启动成功"}
#同上为get方法注册“/health”路由，返回一个字典，字典中包含一个键值对，键为"status"，值为"ok"
@app.get("/health")
def health_check():
    return {"status": "ok"}