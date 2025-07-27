from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import json
import random
import os
import asyncio

TOKEN = os.getenv("BOT_TOKEN", "6288532598:AAEf-5FT5mCBr6D5Pv1iHap3mp9CtB7FE10")

app = FastAPI()
telegram_app = Application.builder().token(TOKEN).build()

def load_azkar():
    try:
        with open("azkar.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return ["سبحان الله", "الحمد لله", "لا إله إلا الله", "الله أكبر"]

def save_user(user_id):
    try:
        with open("rshq.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = []

    if user_id not in data:
        data.append(user_id)
        with open("rshq.json", "w", encoding="utf-8") as f:
            json.dump(data, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = f"@{user.username}" if user.username else user.first_name
    welcome = f"أهلاً وسهلاً أخي الكريم {username} في بوت الأذكار، سيساعدك كثيراً"
    await update.message.reply_text(welcome)

    azkar = load_azkar()
    zekr = random.choice(azkar)
    await update.message.reply_text(zekr)

    save_user(user.id)

telegram_app.add_handler(CommandHandler("start", start))

@app.on_event("startup")
async def on_startup():
    # ✅ الطريقة الصحيحة لتشغيل البوت داخل FastAPI
    asyncio.create_task(telegram_app.initialize())
    asyncio.create_task(telegram_app.start())

@app.post("/")
async def telegram_webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, telegram_app.bot)  # ✅ استخدم البوت من التطبيق نفسه
    await telegram_app.process_update(update)
    return {"ok": True}
