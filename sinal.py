import random
import asyncio
import os
from datetime import datetime, timedelta
from telegram import Bot
from telegram import __version__ as ptb_version

# --- CONFIGURAÇÕES ---
BOT_TOKEN = "7401293219:AAFDt9G2wlozVa1zNGU-A50Uj9R1yCh3zE8"
CHAT_ID = "-4935359876"

# Intervalos possíveis entre sinais (em minutos)
INTERVALOS = [3, 5, 6, 7, 8, 10, 12, 25, 30]

# Caminho do arquivo de comando
ARQUIVO_COMANDO = "comando.txt"

# --- FUNÇÕES ---
async def enviar_busca(bot: Bot):
    await bot.send_message(chat_id=CHAT_ID, text="🔎 Buscando SINAL PREMIADO...")

def gerar_horario_futuro(minutos: int) -> str:
    futuro = datetime.now() + timedelta(minutes=minutos)
    return futuro.strftime("%H:%M")

def gerar_sinal() -> str:
    escolha = random.choice([50, 100])
    minutos = random.choice([3, 5, 10, 13, 15])
    if escolha == 50:
        return f"""
APOSTA EM POTENCIAL RASPADINHATRI.COM

RASPADINHA DE R$ 50 (DOBRO DE CHANCE) ✅
Lucro em Potencial 📈
Em {minutos} Minutos ⏰ ({gerar_horario_futuro(minutos)})
"""
    else:
        return f"""
APOSTA EM POTENCIAL RASPADINHATRI.COM

RASPADINHA DE R$ 100 (TRIPLO DE CHANCE) ✅
Lucro em Potencial 📈
Em {minutos} Minutos ⏰ ({gerar_horario_futuro(minutos)})
"""

async def enviar_sinal(bot: Bot):
    msg = gerar_sinal()
    await bot.send_message(chat_id=CHAT_ID, text=msg)

async def checar_comando(bot: Bot):
    """Verifica o arquivo comando.txt e envia mensagem instantânea se houver algo escrito"""
    if os.path.exists(ARQUIVO_COMANDO):
        with open(ARQUIVO_COMANDO, "r", encoding="utf-8") as f:
            texto = f.read().strip()
        if texto:
            await bot.send_message(chat_id=CHAT_ID, text=texto)
            # Limpa o arquivo após enviar
            with open(ARQUIVO_COMANDO, "w", encoding="utf-8") as f:
                f.write("")

# --- LOOP PRINCIPAL ---
async def bot_loop():
    bot = Bot(token=BOT_TOKEN)
    enviados_especiais = 0

    while True:
        agora = datetime.now()
        hora = agora.hour

        # Checa comandos a cada ciclo
        await checar_comando(bot)

        if 8 <= hora < 24:
            # Dentro do horário normal
            await enviar_busca(bot)
            await asyncio.sleep(60)

            # Sinal real
            intervalo = random.choice(INTERVALOS)
            await asyncio.sleep(intervalo * 60)
            await enviar_sinal(bot)
        else:
            # Fora do horário → sinais especiais
            if enviados_especiais < 3 and random.random() < 0.05:
                msg = f"""
🌙 SINAL ESPECIAL DA MADRUGADA 🌙

{gerar_sinal()}
"""
                await bot.send_message(chat_id=CHAT_ID, text=msg)
                enviados_especiais += 1
            await asyncio.sleep(60)

# --- INÍCIO ---
if __name__ == "__main__":
    print(f"Rodando bot com python-telegram-bot v{ptb_version}")
    asyncio.run(bot_loop())
