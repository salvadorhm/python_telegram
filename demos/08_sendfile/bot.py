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


async def send_file_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Envía un archivo al usuario que llama al comando /sendfile.
    """
    try:
        # Define la ruta del archivo que se enviará
        filename = 'downloads/documents/ejemplo.txt'  # Reemplaza con la ruta real del archivo

        # Verifica si el archivo existe
        if os.path.exists(filename):
            # Envía el archivo al usuario
            with open(filename, 'rb') as file:
                await context.bot.send_document(chat_id=update.effective_chat.id, document=file)
            await update.message.reply_text("Aquí tienes tu archivo.")
        else:
            await update.message.reply_text("Lo siento, el archivo no existe.")
    except Exception as e:
        print(f"Error al enviar el archivo: {e}")
        await update.message.reply_text("Ocurrió un error al intentar enviar el archivo.")

if __name__ == '__main__':
    # Reemplaza 'TELEGRAM_API_KEY' con el token real de tu bot en el archivo .env
    app = ApplicationBuilder().token(token).build()

    # on different commands - answer in Telegram
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_command))

    # Manejador para el comando /sendfile
    app.add_handler(CommandHandler("sendfile", send_file_command))

    # Inicia el bot en modo polling
    print("Bot iniciado. Usa el comando /sendfile para recibir un archivo.")
    app.run_polling()
