from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import os

async def video_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Maneja la recepción de videos y los guarda en la carpeta 'downloads/videos/'.
    """
    try:
        # Muestra un mensaje en la consola indicando que se ha recibido un video
        print("Recibiendo video...")
        
        # Obtiene el usuario que envió el mensaje
        user_data = update.message.from_user
        print(f"Video recibido de: {user_data.first_name} {user_data.last_name} ({user_data.username})")
        
        # Obtiene el archivo de video desde el mensaje
        video_file = await context.bot.get_file(update.message.video.file_id)
        
        # Define el nombre y la ruta donde se guardará el archivo
        # El nombre del archivo se genera con el ID del video para evitar duplicados
        filename = os.path.join('downloads/videos/', f"{update.message.video.file_id}.mp4")
        
        # Crea la carpeta si no existe
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Descarga el archivo de video en la ruta especificada
        await video_file.download_to_drive(filename)
        
        # Responde al usuario confirmando la recepción del archivo
        await update.message.reply_text("Video recibido y guardado correctamente.")
        
        print(f"Video guardado en: {filename}")
    except Exception as e:
        print(f"Error al recibir el video: {e}")
        await update.message.reply_text("Ocurrió un error al guardar el video.")

if __name__ == '__main__':
    # Reemplaza 'TU_TOKEN' con el token real de tu bot
    app = ApplicationBuilder().token("TU_TOKEN").build()

    # Manejador para recibir archivos de video
    app.add_handler(MessageHandler(filters.VIDEO, video_handler))

    # Inicia el bot en modo polling
    print("Bot iniciado. Esperando videos...")
    app.run_polling()
