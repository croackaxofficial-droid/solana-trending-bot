import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    ConversationHandler,
    filters,
)

TOKEN_NAME, TOKEN_ADDRESS, WEBSITE, TWITTER, TELEGRAM, PACKAGE = range(6)

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
🚀 Welcome to Solana Trending Bot!

🔥 Fastest way to promote your Solana token.

📈 Available Commands:
/buy - Buy promotion
/trending - View packages
/support - Contact support

💎 Let's make your token trend!
"""
    await update.message.reply_text(text)


async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💰 Buy Promotion\n\nContact: @soltrendingsolana_bot"
    )


async def trending(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
📈 SOL TRENDING PACKAGES

🥉 Bronze — $29
✅ 2 Story Posts
✅ 1 Permanent Post

🥈 Silver — $59
✅ 4 Story Posts
✅ 2 Permanent Posts
✅ Faster Promotion

🥇 Gold — $99
✅ Daily Promotion
✅ Priority Listing
✅ Maximum Reach

💎 Diamond — $199
✅ Premium Promotion
✅ Highest Priority
✅ Dedicated Support

💰 To order your package:
/buy
"""
    await update.message.reply_text(text)


async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛠 Support: @soltrendingsolana_bot"
    )
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Please use these commands:\n\n"
        "/buy - Buy Promotion\n"
        "/trending - View Packages\n"
        "/support - Contact Support"
    )

def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN environment variable is missing")

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("buy", buy))
app.add_handler(CommandHandler("trending", trending))
app.add_handler(CommandHandler("support", support))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

print("Bot is running...")
app.run_polling()

if __name__ == "__main__":
    main()
