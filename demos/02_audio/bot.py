from telegram import Update,ForceReply
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
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


async def audio_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Maneja la recepción de archivos de audio y los guarda en la carpeta 'downloads/audios/'.
    """
    try:
        # Muestra un mensaje en la consola indicando que se ha recibido un audio
        print("Recibiendo audio...")
        
        # Obtiene el usuario que envió el mensaje
        user_data = update.message.from_user
        print(f"Audio recibido de: {user_data.first_name} {user_data.last_name} ({user_data.username})")

        # Obtiene el archivo de audio desde el mensaje
        audio_file = await context.bot.get_file(update.message.audio.file_id)

        print(f"FILE_ID: {update.message.audio.file_id}")
        
        # Define el nombre y la ruta donde se guardará el archivo
        # El nombre del archivo se genera con el ID del audio para evitar duplicados
        filename = os.path.join('downloads/audios/', f"{update.message.audio.file_id}.ogg")
        
        # Crea la carpeta si no existe
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Descarga el archivo de audio en la ruta especificada
        await audio_file.download_to_drive(filename)
        
        # Responde al usuario confirmando la recepción del archivo
        await update.message.reply_text("Audio recibido y guardado correctamente.")
        
        print(f"Audio guardado en: {filename}")
    except Exception as e:
        print(f"Error al recibir el audio: {e}")
        await update.message.reply_text("Ocurrió un error al guardar el audio.")


if __name__ == '__main__':
    # Crea la aplicación con el token de tu bot
    app = ApplicationBuilder().token(token).build()

    # on different commands - answer in Telegram
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_command))

    # Manejador para recibir audios
    app.add_handler(MessageHandler(filters.AUDIO, audio_handler))

    # Inicia el bot en modo polling
    print("Bot iniciado.")
    app.run_polling()
