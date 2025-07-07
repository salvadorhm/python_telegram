import logging
from telegram import ForceReply, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv
import os

load_dotenv()
token=os.getenv("TELEGRAM_API_KEY")

logging.basicConfig(
    filename='bot.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)

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

async def image_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Maneja la recepción de imágenes y las guarda en la carpeta 'downloads/images/'.
    """
    try:
        # Muestra un mensaje en la consola indicando que se ha recibido una imagen
        print("Recibiendo imagen...")
        
        # Obtiene el usuario que envió el mensaje
        user_data = update.message.from_user
        print(f"Imagen recibida de: {user_data.first_name} {user_data.last_name} ({user_data.username})")
        
        # Obtiene el archivo de imagen con la mejor resolución (la última en la lista)
        photo_file = await context.bot.get_file(update.message.photo[-1].file_id)
        print(f"FILE_ID: {update.message.photo[-1].file_id}")
        
        # Define el nombre y la ruta donde se guardará el archivo
        # El nombre del archivo se genera con el ID de la imagen para evitar duplicados
        filename = os.path.join('downloads/images/', f"{update.message.photo[-1].file_id}.jpg")
        
        # Crea la carpeta si no existe
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Descarga el archivo de imagen en la ruta especificada
        await photo_file.download_to_drive(filename)
        
        # Responde al usuario confirmando la recepción del archivo
        await update.message.reply_text("Imagen recibida y guardada correctamente.")
        
        print(f"Imagen guardada en: {filename}")
    except Exception as e:
        print(f"Error al recibir la imagen: {e}")
        await update.message.reply_text("Ocurrió un error al guardar la imagen.")

if __name__ == '__main__':
    # Reemplaza 'TELEGRAM_API_KEY' con el token real de tu bot en el archivo .env
    app = ApplicationBuilder().token(token).build()

    # on different commands - answer in Telegram
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_command))

    # Manejador para recibir imágenes
    app.add_handler(MessageHandler(filters.PHOTO, image_handler))

    # Inicia el bot en modo polling
    print("Bot iniciado. Esperando imágenes...")
    app.run_polling()
