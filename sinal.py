import random
import asyncio
import os
from datetime import datetime, timedelta
from telegram import Bot
from telegram import __version__ as ptb_version

# --- CONFIGURAÇÕES ---
BOT_TOKEN = "7401293219:AAFDt9G2wlozVa1zNGU-A50Uj9R1yCh3zE8"
CHAT_ID = "-4935359876"

# Intervalos possíveis entre sinais (minutos)
INTERVALOS = [3, 5, 6, 7, 8, 10, 12]

# Caminho do arquivo de comando
ARQUIVO_COMANDO = "comando.txt"

# Mensagens de presença (mais engajamento)
MENSAGENS_PRESENCA = [
    "Bot ativo ✅",
    "Estamos buscando sinais... 🔎",
    "Analisando os padrões da plataforma... 🚀",
    "Fique ligado, Estamos com os padrões definidos e alinhados. ⏱️",
    "Atenção! Sinais a caminho... 👀",
]

# --- FUNÇÕES ---
async def enviar_mensagem(bot: Bot, texto: str):
    await bot.send_message(chat_id=CHAT_ID, text=texto)

def gerar_horario_futuro(minutos: int) -> str:
    futuro = datetime.now() + timedelta(minutes=minutos)
    return futuro.strftime("%H:%M")

def gerar_sinal() -> str:
    escolha = random.choice([50, 100])
    minutos = random.choice([3, 5, 10, 13, 15])
    link = "raspadinhatri.com"
    if escolha == 50:
        return f"""
APOSTA EM POTENCIAL {link.upper()}

RASPADINHA DE R$ 50 (DOBRO DE CHANCE) ✅
Lucro em Potencial 📈
Em {minutos} Minutos ⏰ ({gerar_horario_futuro(minutos)})
Acesse: {link}
"""
    else:
        return f"""
APOSTA EM POTENCIAL {link.upper()}

RASPADINHA DE R$ 100 (TRIPLO DE CHANCE) ✅
Lucro em Potencial 📈
Em {minutos} Minutos ⏰ ({gerar_horario_futuro(minutos)})
Acesse: {link}
"""

async def checar_comando(bot: Bot):
    """Verifica o arquivo comando.txt e envia mensagem instantânea se houver algo escrito"""
    if os.path.exists(ARQUIVO_COMANDO):
        with open(ARQUIVO_COMANDO, "r", encoding="utf-8") as f:
            texto = f.read().strip()
        if texto:
            await enviar_mensagem(bot, texto)
            # Limpa o arquivo após enviar
            with open(ARQUIVO_COMANDO, "w", encoding="utf-8") as f:
                f.write("")

async def bot_loop():
    bot = Bot(token=BOT_TOKEN)
    enviados_especiais = 0

    while True:
        agora = datetime.now()
        hora = agora.hour

        # 1️⃣ Checa comandos manuais a cada ciclo
        await checar_comando(bot)

        # 2️⃣ Mensagem de presença (intervalo 1-2 min)
        mensagem_presenca = random.choice(MENSAGENS_PRESENCA)
        await enviar_mensagem(bot, mensagem_presenca)
        await asyncio.sleep(random.randint(60, 120))  # 1 a 2 minutos

        if 8 <= hora < 24:
            # 3️⃣ Sinais reais dentro do horário normal
            intervalo = random.choice(INTERVALOS)
            await asyncio.sleep(intervalo * 60)
            await enviar_mensagem(bot, gerar_sinal())
        else:
            # 4️⃣ Sinais especiais da madrugada
            if enviados_especiais < 3 and random.random() < 0.05:
                msg = f"""
🌙 SINAL ESPECIAL DA MADRUGADA 🌙

{gerar_sinal()}
"""
                await enviar_mensagem(bot, msg)
                enviados_especiais += 1
