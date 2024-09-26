from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import os

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
    # Reemplaza 'TU_TOKEN' con el token real de tu bot
    app = ApplicationBuilder().token("TU_TOKEN").build()

    # Manejador para recibir ubicaciones
    app.add_handler(MessageHandler(filters.LOCATION, location_handler))

    # Inicia el bot en modo polling
    print("Bot iniciado. Esperando ubicaciones...")
    app.run_polling()