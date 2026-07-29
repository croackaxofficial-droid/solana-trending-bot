from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = 8875672879:AAEnWGJO1KkQnKaxcbGiHCAbHbG6csO1524

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Welcome to Solana Trending Bot!\n\n"
        "The fastest way to discover trending Solana tokens.\n\n"
        "Use /help to see all commands."
    )

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("Bot is running...")
app.run_polling()
