from fastapi import FastAPI
import uvicorn
from get_data import common_rpc_call
from models import RpcParam
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 허용할 출처 목록
    allow_credentials=True,
    allow_methods=["*"],  # 허용할 HTTP 메서드
    allow_headers=["*"],  # 허용할 HTTP 헤더
)
@app.get("/")
async def root():
    return {"message": "EGI FAST API"}


@app.post("/api/post")
async def call_database(models: RpcParam):
    print(models)
    result = common_rpc_call(models)
    return result

def serve():
    uvicorn.run(
        app="main:app",
        timeout_keep_alive=10,
        host='0.0.0.0',
        port=10900,
        log_level="info"
    )

if __name__ == "__main__":
    serve()