from telegram import ForceReply, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)



if __name__ == "__main__":
    # Reemplaza 'TU_TOKEN' con el token real de tu bot
    app = ApplicationBuilder().token("TU_TOKEN").build()

    # on different commands - answer in Telegram
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Inicia el bot en modo polling
    print("Bot iniciado.")
    app.run_polling()
