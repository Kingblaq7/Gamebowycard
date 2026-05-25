
import os
from PIL import Image, ImageDraw, ImageFont
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

# PASTE YOUR BOT TOKEN HERE
BOT_TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"

# Store users waiting for username
waiting_for_username = set()


# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("🎮 Enter KOL Details", callback_data="enter_kol")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = """
🎮 Welcome to GAME BOWY

Enter the next generation Play-To-Earn universe 🚀

Complete your KOL details and receive your official GAME BOWY creator card instantly.
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
            "Send your Twitter username.\n\nExample:\n@crypto_king"
        )


# HANDLE USERNAME
async def handle_username(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id

    if user_id not in waiting_for_username:
        return

    username = update.message.text

    waiting_for_username.remove(user_id)

    # Open template image
    image = Image.open("templates/card.png")

    draw = ImageDraw.Draw(image)

    # Font
    font = ImageFont.truetype("arial.ttf", 50)

    # Text Position
    x = 220
    y = 500

    # Draw username on card
    draw.text((x, y), username, fill="white", font=font)

    # Save generated image
    output_path = f"{user_id}.png"
    image.save(output_path)

    # Caption message
    caption = f"""
🔥 Welcome to GAME BOWY

Official KOL Creator: {username}

Ready to dominate the battlefield and earn rewards 🚀

#GameBowy #PlayToEarn #GameFi
"""

    # Send generated card
    await update.message.reply_photo(
        photo=open(output_path, "rb"),
        caption=caption
    )

    # Delete generated image
    os.remove(output_path)


# RUN BOT
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_click))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_username))

print("GAME BOWY Bot is running...")
app.run_polling()
