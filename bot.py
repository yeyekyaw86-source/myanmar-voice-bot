import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import re

# Log setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# သင်္ကေတတွေဖယ်ပြီး စာသားကို သန့်စင်တဲ့ function
def clean_text(text: str) -> str:
    # URL detect
    url_pattern = re.compile(r'(https?://[^\s]+)')
    urls = url_pattern.findall(text)

    # URL မဟုတ်တဲ့ စာတွေထဲက သင်္ကေတတွေဖယ်
    cleaned = re.sub(r'[^A-Za-z0-9\u1000-\u109F\s:/._-]', '', text)

    # အရမ်းရှည်တဲ့ URL တွေကို domain name လောက်သာထား
    processed_urls = []
    for url in urls:
        if len(url) > 40:
            domain = re.findall(r'https?://([^/]+)/?', url)
            if domain:
                processed_urls.append(domain[0])
            else:
                processed_urls.append(url)
        else:
            processed_urls.append(url)

    # အကြောင်းအရာပြန်ပေါင်း
    return " ".join(cleaned.split()) + " " + " ".join(processed_urls)

# မက်ဆေ့ချ်လက်ခံပြီး voice ဖိုင်နဲ့အတူပြန်ပေးမယ့် handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    if not user_text:
        return

    # စာကို သန့်စင်
    cleaned_text = clean_text(user_text)

    # သန့်စင်ပြီးစာကို အဖြစ်အပျက်အနည်းဆုံးထပ်ပေါင်းပြီး ပြန်ပို့
    await update.message.reply_text(cleaned_text)

if __name__ == "__main__":
    # အကိုရဲ့ Telegram Bot Token ကို ဒီမှာထည့်ပါ
    TOKEN = "8319996943:AAGUDW5LbNwksHyWKO-aFxADgrwn_QWglI4"

    app = ApplicationBuilder().token(TOKEN).build()

    # စာတိုင်းကို handle_message နဲ့ဆောင်ရွက်
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()
