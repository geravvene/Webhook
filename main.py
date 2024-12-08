from fastapi import FastAPI, Request, Header
import httpx

app = FastAPI()

TARGET_WEBHOOK_URL = "https://7l11gvcx-8000.euw.devtunnels.ms/ArendaBot/webhook"  # URL целевого вебхука
SECRET_TOKEN = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # Токен проверки для Telegram

@app.post("/webhook")
async def proxy_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
):

    if x_telegram_bot_api_secret_token != SECRET_TOKEN:
        return {"status": "error", "message": "Invalid secret token"}

    payload = await request.json()

    async with httpx.AsyncClient() as client:
        response = await client.post(
            TARGET_WEBHOOK_URL,
            json=payload,
            headers={"x-telegram-bot-api-secret-token": SECRET_TOKEN},
        )

    # Возвращаем ответ
    if response.status_code == 200:
        return {"status": "success", "message": "Data forwarded"}
    else:
        return {"status": "error", "message": "Failed to forward data"}