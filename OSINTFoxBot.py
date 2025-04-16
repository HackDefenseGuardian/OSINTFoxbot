from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os
import requests

# ----------------------------------------------------------
# Cargar variables de entorno desde el archivo .env usando python-dotenv.
# Asegúrate de tener un archivo .env con la variable TELEGRAM_BOT_TOKEN.
# ----------------------------------------------------------
load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# ----------------------------------------------------------
# Comando: /help – Muestra todos los comandos disponibles
# ----------------------------------------------------------
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
🧠 *OSINTFoxBot - Comandos Disponibles*:

🔍 _Información por IP:_
/ipinfo <ip> – Muestra datos de geolocalización y proveedor.

📧 _Reputación de correos:_
/emailrep <email> – Analiza el correo con emailrep.io.

📄 _Información general:_ 
/help – Muestra esta ayuda.
/start – Mensaje de bienvenida.

🛠️ _Próximamente:_
/whois <dominio> – Consulta información WHOIS.
/hibp <email> – Verifica si un correo fue filtrado.
/dox <usuario> – Recopila info básica de un usuario.

_Escribe un comando seguido de un valor. Ejemplo:_
/ipinfo 8.8.8.8
/emailrep ejemplo@gmail.com
"""
    await update.message.reply_markdown(help_text)

# ----------------------------------------------------------
# Comando: /start – Invoca el comando /help para mostrar el menú al usuario.
# ----------------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await help_command(update, context)

# ----------------------------------------------------------
# Comando: /ipinfo <ip> – Obtiene información de geolocalización y proveedor usando ipinfo.io.
# ----------------------------------------------------------
async def ipinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Debes proporcionar una IP. Ej: /ipinfo 8.8.8.8")
        return

    ip = context.args[0]
    url = f"https://ipinfo.io/{ip}/json"
    try:
        response = requests.get(url)
        data = response.json()
        msg = "\n".join([f"{k}: {v}" for k, v in data.items()])
        await update.message.reply_text(msg)
    except Exception:
        await update.message.reply_text("Error obteniendo datos.")

# ----------------------------------------------------------
# Comando: /emailrep <correo> – Obtiene la reputación de un correo usando emailrep.io.
# ----------------------------------------------------------
async def emailrep(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Debes proporcionar un correo. Ej: /emailrep ejemplo@gmail.com")
        return

    email = context.args[0]
    url = f"https://emailrep.io/{email}"
    headers = {"User-Agent": "OSINTFoxBot"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 429:
            await update.message.reply_text("Límite de peticiones alcanzado. Intenta más tarde.")
            return
        data = response.json()
        msg = "\n".join([f"{k}: {v}" for k, v in data.items()])
        await update.message.reply_text(msg)
    except Exception:
        await update.message.reply_text("Error obteniendo información del correo.")

# ----------------------------------------------------------
# Configuración principal del bot:
# Se crea la aplicación, se añaden los handlers de los comandos y se inicia el bot en modo polling.
# ----------------------------------------------------------
if __name__ == '__main__':
    # Construir la aplicación del bot con el token
    application = ApplicationBuilder().token(TOKEN).build()

    # Registro de comandos con sus respectivos handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("ipinfo", ipinfo))
    application.add_handler(CommandHandler("emailrep", emailrep))

    # Inicia el bot y se queda en ejecución usando run_polling(), que maneja internamente el bucle de eventos
    application.run_polling()
