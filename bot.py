import os

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = "8927128908:AAFrTO8mjIcujJf6juLw96zQmCyAEe6mS1Q"

waiting_for_username = set()


# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("🎮 Enter KOL Details", callback_data="enter_kol")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = """
🎮 Welcome to GAME BWOY

Enter the next generation Play-To-Earn universe 🚀

Complete your KOL details and receive your official GAME BWOY creator card instantly.
"""

    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup
    )


# BUTTON CLICK
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "enter_kol":

        waiting_for_username.add(query.from_user.id)

        await query.message.reply_text(
            "Send your Twitter username.\n\nExample:\nphoenix"
        )


# HANDLE USERNAME
async def handle_username(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id

    if user_id not in waiting_for_username:
        return

    username = update.message.text.lower().replace("@", "").strip()

    waiting_for_username.remove(user_id)

    image_path = f"templates/{username}.png"

    # Check if card exists
    if not os.path.exists(image_path):

        await update.message.reply_text(
            "❌ No creator card found for this username."
        )

        return

    caption = f"""
🔥 Welcome to GAME BWOY

Official KOL Creator: @{username}

Ready to dominate the battlefield and earn rewards 🚀

#GameBwoy #PlayToEarn #GameFi
"""

    # Send creator card
    await update.message.reply_photo(
        photo=open(image_path, "rb"),
        caption=caption
    )


# RUN BOT
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_click))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_username))

print("GAME BWOY Bot is running...")
app.run_polling()
