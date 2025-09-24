import logging
import random
import asyncio
from datetime import datetime, timedelta
from telegram import Bot

# --- CONFIGURAÇÕES ---
BOT_TOKEN = "7401293219:AAFDt9G2wlozVa1zNGU-A50Uj9R1yCh3zE8"
CHAT_ID = "-4935359876"

# Intervalos possíveis entre sinais (em minutos)
INTERVALOS = [3, 5, 6, 7, 8, 10, 12, 25, 30]

bot = Bot(token=BOT_TOKEN)

logging.basicConfig(level=logging.INFO)

# Função para gerar um horário futuro
def gerar_horario_futuro(minutos):
    agora = datetime.now()
    futuro = agora + timedelta(minutes=minutos)
    return futuro.strftime("%H:%M")

# Função para criar um sinal
def gerar_sinal():
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

# Loop principal
async def rodar_bot():
    enviados_especiais = 0
    while True:
        agora = datetime.now()
        hora = agora.hour

        # Dentro do horário normal (08h–00h)
        if 8 <= hora < 24:
            # Enquanto não sai sinal → manda "Buscando..."
            await bot.send_message(chat_id=CHAT_ID, text="🔎 Buscando SINAL PREMIADO...")
            await asyncio.sleep(60)

            # Decide intervalo do próximo sinal
            intervalo = random.choice(INTERVALOS)
            await asyncio.sleep(intervalo * 60)

            msg = gerar_sinal()
            await bot.send_message(chat_id=CHAT_ID, text=msg)

        else:
            # Fora do horário → pode rolar até 3 sinais especiais
            if enviados_especiais < 3 and random.random() < 0.05:  # 5% de chance por minuto
                msg = f"""
🌙 SINAL ESPECIAL DA MADRUGADA 🌙

{gerar_sinal()}
"""
                await bot.send_message(chat_id=CHAT_ID, text=msg)
                enviados_especiais += 1
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(rodar_bot())
