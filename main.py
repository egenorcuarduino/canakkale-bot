import time
import requests
from telegram import Bot

TELEGRAM_TOKEN = "7951485448:AAEq7JmWfwjKR_Fk4MyNy6TKC9BvtpzdxRo"
TELEGRAM_CHAT_ID = 5691962682

INSTAGRAM_USERNAMES = [
    "tevkil", "tevkil_", "tevkilbirgi", "tevkiliniz", "tevkilat", "tevkil.comm"
]

LAST_POSTS = {}

def send_telegram_message(message):
    bot = Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

def check_instagram():
    for username in INSTAGRAM_USERNAMES:
        url = f"https://www.instagram.com/{username}/?__a=1&__d=dis"
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code == 200:
                data = response.json()
                latest_post = data["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]
                caption = latest_post["edge_media_to_caption"]["edges"][0]["node"]["text"]
                post_id = latest_post["id"]
                if username not in LAST_POSTS or LAST_POSTS[username] != post_id:
                    LAST_POSTS[username] = post_id
                    if "çanakkale" in caption.lower():
                        post_url = f"https://instagram.com/p/{latest_post['shortcode']}"
                        send_telegram_message(f"{username} adlı hesap Çanakkale kelimesi geçen yeni bir gönderi paylaştı:\n{post_url}")
        except Exception as e:
            print(f"Hata oluştu: {e}")

while True:
    check_instagram()
    time.sleep(60)  # Her 1 dakikada bir kontrol eder
