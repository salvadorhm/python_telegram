from telegram import ForceReply, Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from dotenv import load_dotenv
import os

load_dotenv()
token=os.getenv("TELEGRAM_API_KEY")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Este bot puede realizar las siguientes acciones:")


async def echo_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


async def send_location_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Envía una ubicación al usuario que llama al comando /sendlocation.
    """
    try:
        # Define la latitud y longitud de la ubicación que deseas enviar
        latitude = 40.7128  # Ejemplo: Nueva York
        longitude = -74.0060  # Ejemplo: Nueva York

        # Envía la ubicación al usuario
        await context.bot.send_location(chat_id=update.effective_chat.id, latitude=latitude, longitude=longitude)
        await update.message.reply_text("Aquí tienes la ubicación enviada.")
    except Exception as e:
        print(f"Error al enviar la ubicación: {e}")
        await update.message.reply_text("Ocurrió un error al intentar enviar la ubicación.")

if __name__ == '__main__':
    # Reemplaza 'TELEGRAM_API_KEY' con el token real de tu bot en el archivo .env
    app = ApplicationBuilder().token(token).build()

    # on different commands - answer in Telegram
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_command))

    # Manejador para el comando /sendlocation
    app.add_handler(CommandHandler("sendlocation", send_location_command))

    # Inicia el bot en modo polling
    print("Bot iniciado. Usa el comando /sendlocation para recibir una ubicación.")
    app.run_polling()
