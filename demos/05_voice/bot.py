from telegram import ForceReply, Update
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
    await update.message.reply_text("Help!")


async def echo_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Maneja la recepción de mensajes de voz y los guarda en la carpeta 'downloads/voices/'.
    """
    try:
        # Muestra un mensaje en la consola indicando que se ha recibido un mensaje de voz
        print("Recibiendo mensaje de voz...")
        
        # Obtiene el usuario que envió el mensaje
        user_data = update.message.from_user
        print(f"Mensaje de voz recibido de: {user_data.first_name} {user_data.last_name} ({user_data.username})")
        
        # Obtiene el archivo de mensaje de voz desde el mensaje
        voice_file = await context.bot.get_file(update.message.voice.file_id)
        
        # Define el nombre y la ruta donde se guardará el archivo
        # El nombre del archivo se genera con el ID del mensaje de voz para evitar duplicados
        filename = os.path.join('downloads/voices/', f"{update.message.voice.file_id}.ogg")
        
        # Crea la carpeta si no existe
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Descarga el archivo de mensaje de voz en la ruta especificada
        await voice_file.download_to_drive(filename)
        
        # Responde al usuario confirmando la recepción del archivo
        await update.message.reply_text("Mensaje de voz recibido y guardado correctamente.")
        
        print(f"Mensaje de voz guardado en: {filename}")
    except Exception as e:
        print(f"Error al recibir el mensaje de voz: {e}")
        await update.message.reply_text("Ocurrió un error al guardar el mensaje de voz.")

if __name__ == '__main__':
    # Reemplaza 'TELEGRAM_API_KEY' con el token real de tu bot en el archivo .env
    app = ApplicationBuilder().token(token).build()

    # on different commands - answer in Telegram
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))

    # Manejador para recibir mensajes de voz
    app.add_handler(MessageHandler(filters.VOICE, voice_handler))

    # Inicia el bot en modo polling
    print("Bot iniciado. Esperando mensajes de voz...")
    app.run_polling()
