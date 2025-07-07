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


async def location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Maneja la recepción de ubicaciones y las guarda en un archivo de texto
    en la carpeta 'downloads/locations/'.
    """
    try:
        # Muestra un mensaje en la consola indicando que se ha recibido una ubicación
        print("Recibiendo ubicación...")
        
        # Obtiene el usuario que envió el mensaje
        user_data = update.message.from_user
        print(f"Ubicación recibida de: {user_data.first_name} {user_data.last_name} ({user_data.username})")
        
        # Obtiene la ubicación del mensaje
        location = update.message.location
        
        # Define la ruta del archivo de texto donde se guardará la ubicación
        filename = os.path.join('downloads/locations/', 'ubicaciones.txt')
        
        # Crea la carpeta si no existe
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Abre el archivo en modo append y guarda la ubicación
        with open(filename, 'a') as f:
            f.write(f"Usuario: {user_data.username} - Latitud: {location.latitude}, Longitud: {location.longitude}\n")
        
        # Responde al usuario confirmando la recepción de la ubicación
        await update.message.reply_text("Ubicación recibida y guardada correctamente.")
        
        print(f"Ubicación guardada en: {filename}")
    except Exception as e:
        print(f"Error al recibir la ubicación: {e}")
        await update.message.reply_text("Ocurrió un error al guardar la ubicación.")

if __name__ == '__main__':
    # Reemplaza 'TELEGRAM_API_KEY' con el token real de tu bot en el archivo .env
    app = ApplicationBuilder().token(token).build()

    # on different commands - answer in Telegram
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_command))

    # Manejador para recibir ubicaciones
    app.add_handler(MessageHandler(filters.LOCATION, location_handler))

    # Inicia el bot en modo polling
    print("Bot iniciado. Esperando ubicaciones...")
    app.run_polling()
