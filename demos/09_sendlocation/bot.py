from telegram import Update, Location
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def send_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    # Reemplaza 'TU_TOKEN' con el token real de tu bot
    app = ApplicationBuilder().token("TU_TOKEN").build()

    # Manejador para el comando /sendlocation
    app.add_handler(CommandHandler("sendlocation", send_location))

    # Inicia el bot en modo polling
    print("Bot iniciado. Usa el comando /sendlocation para recibir una ubicación.")
    app.run_polling()