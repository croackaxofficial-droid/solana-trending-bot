import logging

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ===========================
# CONFIG
# ===========================

BOT_TOKEN = "8875672879:AAEnWGJO1KkQnKaxcbGiHCAbHbG6csO1524"

PAYMENT_ADDRESS = "0x9Dd701364026d65eFEB7dF610f9a041B5221816C"

# ===========================
# LOGGING
# ===========================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

# ===========================
# STATES
# ===========================

TOKEN_NAME, TOKEN_ADDRESS, PACKAGE, SCREENSHOT, TX_HASH = range(5)

# ===========================
# START
# ===========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "🚀 Welcome to Solana Trending Bot\n\n"
        "Available Commands\n\n"
        "/buy - Buy Promotion\n"
        "/trending - View Packages\n"
        "/support - Contact Support\n"
        "/cancel - Cancel Order"
    )

    await update.message.reply_text(text)

# ===========================
# TRENDING
# ===========================

async def trending(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "🔥 Trending Packages\n\n"
        "🥉 Bronze — 0.5 SOL\n"
        "🥈 Silver — 1 SOL\n"
        "🥇 Gold — 1.5 SOL\n"
        "💎 Diamond — 2 SOL\n\n"
        "Use /buy to place your order."
    )

    await update.message.reply_text(text)

# ===========================
# SUPPORT
# ===========================

async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🛠 Support\n\n@soltrendingsolana_bot"
    )

# ===========================
# BUY
# ===========================

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data.clear()

    await update.message.reply_text(
        "🪙 Enter your Token Name:"
    )

    return TOKEN_NAME

# ===========================
# TOKEN NAME
# ===========================

async def token_name(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["token_name"] = update.message.text

    await update.message.reply_text(
        "📄 Enter your Solana Token Address:"
    )

    return TOKEN_ADDRESS

# ===========================
# TOKEN ADDRESS
# ===========================

async def token_address(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["token_address"] = update.message.text

    keyboard = [
        ["Bronze"],
        ["Silver"],
        ["Gold"],
        ["Diamond"],
    ]

    await update.message.reply_text(
        "📦 Select Your Package:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True,
        ),
    )

    return PACKAGE
    # ===========================
# PACKAGE
# ===========================

async def package(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["package"] = update.message.text

    await update.message.reply_text(
        f"💳 Payment Address\n\n"
        f"{PAYMENT_ADDRESS}\n\n"
        "After payment, please upload your payment screenshot.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return SCREENSHOT


# ===========================
# SCREENSHOT
# ===========================

async def screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.photo:
        await update.message.reply_text(
            "❌ Please upload a valid payment screenshot."
        )
        return SCREENSHOT

    photo = update.message.photo[-1]

    context.user_data["photo_id"] = photo.file_id

    await update.message.reply_text(
        "✅ Screenshot received.\n\n"
        "Now send your Transaction Hash (TX Hash)."
    )

    return TX_HASH


# ===========================
# TX HASH
# ===========================

async def tx_hash(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["tx_hash"] = update.message.text

    order_id = f"ST-{update.effective_user.id}"

    await update.message.reply_text(
        f"🎉 Order Submitted Successfully\n\n"
        f"🆔 Order ID: {order_id}\n"
        f"📦 Package: {context.user_data['package']}\n"
        f"⏳ Status: Pending Verification\n\n"
        "Our team will verify your payment and start your promotion soon."
    )

    return ConversationHandler.END


# ===========================
# CANCEL
# ===========================

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data.clear()

    await update.message.reply_text(
        "❌ Order Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return ConversationHandler.END


# ===========================
# UNKNOWN
# ===========================

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👋 Please use one of these commands:\n\n"
        "/buy\n"
        "/trending\n"
        "/support"
    )


# ===========================
# MAIN
# ===========================

def main():

    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("buy", buy),
        ],
        states={
            TOKEN_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, token_name)
            ],
            TOKEN_ADDRESS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, token_address)
            ],
            PACKAGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, package)
            ],
            SCREENSHOT: [
                MessageHandler(filters.PHOTO, screenshot),
                MessageHandler(filters.TEXT & ~filters.COMMAND, screenshot),
            ],
            TX_HASH: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, tx_hash)
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
        ],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("trending", trending))
    app.add_handler(CommandHandler("support", support))

    app.add_handler(conv_handler)

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            unknown,
        )
    )

    print("✅ Bot Started Successfully")

    app.run_polling()


if __name__ == "__main__":
    main()
