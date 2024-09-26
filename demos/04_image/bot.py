from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import os

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
        filename = os.path.join('downloads/images/', "image.jpg")
        
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
    # Reemplaza 'TU_TOKEN' con el token real de tu bot
    app = ApplicationBuilder().token("TU_TOKEN").build()

    # Manejador para recibir imágenes
    app.add_handler(MessageHandler(filters.PHOTO, image_handler))

    # Inicia el bot en modo polling
    print("Bot iniciado. Esperando imágenes...")
    app.run_polling()
