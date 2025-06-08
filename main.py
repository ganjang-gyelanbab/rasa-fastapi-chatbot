from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware  # 👈 이 줄 추가
import requests

app = FastAPI()

# 👇 여기가 바로 그 CORS 설정 영역!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 또는 ["https://너의-netlify주소.netlify.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(req: Request):
    data = await req.json()
    message = data.get("message", "")
    sender = data.get("sender", "user")
    print("📨 사용자 메시지:", message)

    try:
        response = requests.post(
            "http://localhost:5005/webhooks/rest/webhook",
            json={
                "sender": sender,
                "message": message
            }
        )
        rasa_response = response.json()
        print("🤖 Rasa 응답:", rasa_response)
        return rasa_response
    except Exception as e:
        print("❌ 에러:", str(e))
        return {"error": str(e)}

