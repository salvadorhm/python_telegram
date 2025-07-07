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
    await update.message.reply_text("Este bot puede realizar las siguientes acciones:")


async def echo_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


async def document_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Maneja la recepción de archivos y los guarda en la carpeta 'downloads/documents/'.
    """
    try:
        # Muestra un mensaje en la consola indicando que se ha recibido un archivo
        print("Recibiendo archivo...")
        
        # Obtiene el usuario que envió el mensaje
        user_data = update.message.from_user
        print(f"Archivo recibido de: {user_data.first_name} {user_data.last_name} ({user_data.username})")
        
        # Obtiene el archivo enviado
        document = update.message.document
        
        # Define la ruta donde se guardará el archivo
        # Se utiliza el nombre original del archivo enviado por el usuario
        filename = os.path.join('downloads/documents/', document.file_name)
        
        # Crea la carpeta si no existe
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Descarga el archivo en la ruta especificada
        file = await context.bot.get_file(document.file_id)
        await file.download_to_drive(filename)
        
        # Responde al usuario confirmando la recepción del archivo
        await update.message.reply_text(f"Archivo '{document.file_name}' recibido y guardado correctamente.")
        
        print(f"Archivo guardado en: {filename}")
    except Exception as e:
        print(f"Error al recibir el archivo: {e}")
        await update.message.reply_text("Ocurrió un error al guardar el archivo.")

if __name__ == '__main__':
    # Reemplaza 'TELEGRAM_API_KEY' con el token real de tu bot en el archivo .env
    app = ApplicationBuilder().token(token).build()

    # on different commands - answer in Telegram
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_command))

    # Manejador para recibir archivos de cualquier tipo
    app.add_handler(MessageHandler(filters.Document.ALL, document_handler))

    # Inicia el bot en modo polling
    print("Bot iniciado. Esperando archivos...")
    app.run_polling()
