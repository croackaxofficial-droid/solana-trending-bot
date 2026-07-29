import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

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
        "💰 Buy Promotion\n\nContact: @YOUR_USERNAME"
    )


async def trending(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📈 Trending packages coming soon."
    )


async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛠 Support: @YOUR_USERNAME"
    )


def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN environment variable is missing")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(CommandHandler("trending", trending))
    app.add_handler(CommandHandler("support", support))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
