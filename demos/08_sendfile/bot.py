from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

async def send_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Envía un archivo al usuario que llama al comando /sendfile.
    """
    try:
        # Define la ruta del archivo que se enviará
        filename = 'downloads/documents/ejemplo.txt'  # Reemplaza con la ruta real del archivo

        # Verifica si el archivo existe
        if os.path.exists(filename):
            # Envía el archivo al usuario
            with open(filename, 'rb') as file:
                await context.bot.send_document(chat_id=update.effective_chat.id, document=file)
            await update.message.reply_text("Aquí tienes tu archivo.")
        else:
            await update.message.reply_text("Lo siento, el archivo no existe.")
    except Exception as e:
        print(f"Error al enviar el archivo: {e}")
        await update.message.reply_text("Ocurrió un error al intentar enviar el archivo.")

if __name__ == '__main__':
    # Reemplaza 'TU_TOKEN' con el token real de tu bot
    app = ApplicationBuilder().token("TU_TOKEN").build()

    # Manejador para el comando /sendfile
    app.add_handler(CommandHandler("sendfile", send_file))

    # Inicia el bot en modo polling
    print("Bot iniciado. Usa el comando /sendfile para recibir un archivo.")
    app.run_polling()