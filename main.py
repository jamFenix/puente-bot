from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
import os

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_name = os.getenv("SESSION_NAME")
grupo_id = int(os.getenv("GRUPO_ID"))
bot_real = os.getenv("BOT_REAL")

comandos_validos = [
    "/dni", "/dnif", "/dnid", "/dnifd", "/nm", "/actan", "/actam", "/actad", "/mpfn", 
    "/mpfnv", "/antpdf", "/rqpdf", "/denuncias", "/ant", "/rq", "/antpenver", "/antpolver",
    "/antjudver", "/renadespdf", "/rqv", "/rqvpdf", "/detenciones", "/sunarp", "/sunarpdf",
    "/pla", "/partida", "/tive", "/biv", "/tivep", "/dnivir", "/dnive", "/antpenal", "/antpol",
    "/antjud", "/c4", "/c4w", "/c4t", "/licencia", "/agv", "/migrapdf", "/tel", "/telp",
    "/bitel", "/claro", "/ag", "/hogar", "/fam", "/tra", "/sunedu", "/mine", "/afp",
    "/finan", "/sbs", "/co", "/dir", "/sunat", "/trabajadores", "/sueldos", "/migra",
    "/yape", "/plin", "/mtc", "/cedulav", "/cedulab", "/cedulae", "/nmv"
]

frases_bloqueo = [
    "bienvenido a fenixbot",
    "/register",
    "visualizar la lista de comandos",
    "visualizar el perfil de tu cuenta",
    "visualizar los planes o rangos",
    "puedes contactar con northon",
    "fenixdata.net",
    "canal oficial",
    "@northonc",
    "hola, que tal"
]

app = Client(session_name, api_id=api_id, api_hash=api_hash)
ya_se_envio_start = False

def contiene_frases_bloqueadas(texto: str) -> bool:
    texto_limpio = texto.lower()
    return any(f in texto_limpio for f in frases_bloqueo)

@app.on_message(filters.chat(grupo_id) & filters.text)
async def reenviar_comando(client: Client, message: Message):
    global ya_se_envio_start
    texto = message.text.strip()
    if not texto:
        return

    comando = texto.split()[0].lower()
    if comando in comandos_validos:
        try:
            if not ya_se_envio_start:
                await client.send_message(bot_real, "/start")
                await asyncio.sleep(2)
                ya_se_envio_start = True
                print("🚀 /start enviado")

            await client.send_message(bot_real, texto)
            print(f"↪️ Comando reenviado: {texto}")
        except Exception as e:
            print(f"⚠️ Error: {e}")
    else:
        print(f"❌ Comando no válido: {texto}")

@app.on_message(filters.chat(bot_real))
async def manejar_respuesta(client: Client, message: Message):
    contenido = message.text or message.caption or ""

    if contiene_frases_bloqueadas(contenido):
        print("⛔ Mensaje de bienvenida detectado y bloqueado")
        return

    try:
        if message.text:
            await client.send_message(grupo_id, message.text)
            print("✅ Texto reenviado al grupo")
        elif message.media:
            await message.copy(grupo_id)
            print("📸 Media reenviada")
    except Exception as e:
        print(f"❗Error al reenviar: {e}")

print("🤖 Bot puente escuchando...")
app.run()
