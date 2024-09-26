from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import os

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
    # Reemplaza 'TU_TOKEN' con el token real de tu bot
    app = ApplicationBuilder().token("TU_TOKEN").build()

    # Manejador para recibir archivos de cualquier tipo
    app.add_handler(MessageHandler(filters.Document.ALL, document_handler))

    # Inicia el bot en modo polling
    print("Bot iniciado. Esperando archivos...")
    app.run_polling()