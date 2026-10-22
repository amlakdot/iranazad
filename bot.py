import os
import json
import requests
from datetime import datetime

# خواندن از Environment Variables (Secrets)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")
CONFIG_URL = os.environ.get("CONFIG_URL")

# بررسی وجود مقادیر
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN تنظیم نشده است!")
if not CHANNEL_ID:
    raise ValueError("❌ CHANNEL_ID تنظیم نشده است!")
if not CONFIG_URL:
    raise ValueError("❌ CONFIG_URL تنظیم نشده است!")

def get_configs():
    """دانلود فایل کانفیگ و شمارش تعداد کانفیگ‌ها"""
    print(f"در حال دانلود از: {CONFIG_URL}")
    response = requests.get(CONFIG_URL, timeout=30)
    response.raise_for_status()
    content = response.text

    # شمارش خطوط غیرخالی که کانفیگ هستند
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    config_count = sum(
        1 for line in lines
        if line.startswith(("vless://", "vmess://", "ss://", "trojan://", "hysteria://", "hy2://"))
    )

    return content, config_count

def send_document(content: str, config_count: int):
    """آپلود فایل به کانال تلگرام با کپشن و دکمه"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"

    # کپشن با فرمت HTML
    caption = (
        f"تعداد کانفیگ ها: <b>{config_count}</b>\n\n"
        f'<a href="https://t.me/xixtot/96">آموزش استفاده از فایل</a>\n\n'
        f"هر ۵ ساعت مجموعه کانفیگ فعال"
    )

    # دکمه شیشه‌ای
    reply_markup = {
        "inline_keyboard": [
            [
                {
                    "text": "🕊ایران آزاد",
                    "url": "https://t.me/XIXVPN"
                }
            ]
        ]
    }

    # اسم فایل ارسالی در تلگرام
    filename = "@XIXVPN ایران آزاد 🕊.txt"

    files = {
        "document": (filename, content.encode("utf-8"), "text/plain")
    }

    data = {
        "chat_id": CHANNEL_ID,
        "caption": caption,
        "parse_mode": "HTML",
        "reply_markup": json.dumps(reply_markup)
    }

    response = requests.post(url, data=data, files=files, timeout=60)
    response.raise_for_status()
    result = response.json()

    if not result.get("ok"):
        raise Exception(f"Telegram API error: {result}")

    print(f"✅ فایل با موفقیت ارسال شد. تعداد کانفیگ: {config_count}")
    return result

def main():
    print(f"[{datetime.now()}] شروع کار...")
    try:
        content, count = get_configs()
        print(f"تعداد کانفیگ پیدا شده: {count}")
        send_document(content, count)
    except Exception as e:
        print(f"❌ خطا: {e}")
        raise

if __name__ == "__main__":
    main()
