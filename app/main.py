from fastapi import FastAPI
#FastAPI 类
app = FastAPI(
    title = "预约系统 API",
    description = "基于 FastAPI 开发的预约系统",
    version = "0.1.0",
)
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