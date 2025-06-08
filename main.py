from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 나중에 보안상 도메인 제한해도 돼요
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
            json={"sender": sender, "message": message}
        )
        rasa_response = response.json()
        print("🤖 Rasa 응답:", rasa_response)
        return rasa_response
    except Exception as e:
        print("❌ 에러:", str(e))
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
