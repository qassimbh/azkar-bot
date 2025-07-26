from fastapi import FastAPI, Request
import json
import random
import asyncio
import os
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, ContextTypes
from telegram.ext import Application

TOKEN = "6288532598:AAEf-5FT5mCBr6D5Pv1iHap3mp9CtB7FE10"
bot = Bot(token=TOKEN)
app = FastAPI()

dispatcher = Dispatcher(bot=bot, update_queue=None, workers=1, use_context=True)

def load_azkar():
    with open("azkar.json", "r", encoding="utf-8") as f:
        return json.load(f)

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
    await context.bot.send_message(chat_id=update.effective_chat.id, text=welcome)

    azkar = load_azkar()
    zekr = random.choice(azkar)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=zekr)

    save_user(update.effective_user.id)

dispatcher.add_handler(CommandHandler("start", start))

@app.post("/")
async def telegram_webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, bot)
    dispatcher.process_update(update)
    return {"ok": True}