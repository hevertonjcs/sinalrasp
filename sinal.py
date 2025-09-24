import random
import asyncio
from datetime import datetime, timedelta
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# --- CONFIGURAÇÕES ---
BOT_TOKEN = "7401293219:AAFDt9G2wlozVa1zNGU-A50Uj9R1yCh3zE8"
CHAT_ID = "-4935359876"

INTERVALOS = [3, 5, 6, 7, 8, 10, 12, 25, 30]

# Mensagens de presença/atividade com variações
MENSAGENS_PRESENCA = [
    "Bot ativo ✅",
    "Analisando padrões… 🔎",
    "Analisando últimos ganhadores… 📊",
    "Preparando próximo sinal… ⏱️",
    "Monitorando oportunidades de Raspadinha… 💡",
    "Verificando tendências do dia… 📈",
    "Buscando padrões de vitória… 🏆",
    "Analisando estatísticas recentes… 📊",
    "Acompanhando apostas vencedoras… 💰",
    "Calculando melhores probabilidades… 🔍",
]

# Mensagens de /b (busca/análise)
MENSAGENS_BUSCA = [
    "Estou analisando padrões agora 🔎",
    "Buscando sinais com maior potencial 📊",
    "Verificando últimos ganhadores 🏆",
    "Calculando oportunidades de Raspadinha 💰",
    "Monitorando estatísticas atuais 📈",
    "Preparando próximo sinal estratégico ⏱️",
    "Buscando padrões de vitória recentes 🔍",
    "Analisando tendências do dia… 🧐",
    "Processando dados e padrões atuais 📊",
    "Verificando probabilidades e chances 💡",
]

# Guardar o último sinal em memória
ultimo_sinal = ""

# --- FUNÇÕES ---
def gerar_horario_futuro(minutos: int) -> str:
    futuro = datetime.now() + timedelta(minutes=minutos)
    return futuro.strftime("%H:%M")

def gerar_sinal() -> str:
    global ultimo_sinal
    escolha = random.choice([50, 100])
    minutos = random.choice([3, 5, 10, 13, 15])
    link = "raspadinhatri.com"
    if escolha == 50:
        sinal = f"""
APOSTA EM POTENCIAL {link.upper()}

RASPADINHA DE R$ 50 (DOBRO DE CHANCE) ✅
Lucro em Potencial 📈
Em {minutos} Minutos ⏰ ({gerar_horario_futuro(minutos)})
Acesse: {link}
"""
    else:
        sinal = f"""
APOSTA EM POTENCIAL {link.upper()}

RASPADINHA DE R$ 100 (TRIPLO DE CHANCE) ✅
Lucro em Potencial 📈
Em {minutos} Minutos ⏰ ({gerar_horario_futuro(minutos)})
Acesse: {link}
"""
    ultimo_sinal = sinal
    return sinal

# --- Handlers de comandos ---
async def comando_sinal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(gerar_sinal())

async def comando_last(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if ultimo_sinal:
        await update.message.reply_text(ultimo_sinal)
    else:
        await update.message.reply_text("Ainda não foi enviado nenhum sinal.")

async def comando_b(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = random.choice(MENSAGENS_BUSCA)
    await update.message.reply_text(msg)

# --- Loop de presença e sinais automáticos ---
async def loop_atividade(bot: Bot):
    enviados_especiais = 0
    while True:
        agora = datetime.now()
        hora = agora.hour

        # Mensagens de presença a cada 1-2 minutos
        mensagem_presenca = random.choice(MENSAGENS_PRESENCA)
        await bot.send_message(chat_id=CHAT_ID, text=mensagem_presenca)
        await asyncio.sleep(random.randint(60, 120))

        if 8 <= hora < 24:
            # Sinais automáticos
            intervalo = random.choice(INTERVALOS)
            await asyncio.sleep(intervalo * 60)
            await bot.send_message(chat_id=CHAT_ID, text=gerar_sinal())
        else:
            # Sinais especiais da madrugada (3 vezes)
            if enviados_especiais < 3 and random.random() < 0.05:
                msg = f"""
🌙 SINAL ESPECIAL DA MADRUGADA 🌙

{gerar_sinal()}
"""
                await bot.send_message(chat_id=CHAT_ID, text=msg)
                enviados_especiais += 1

# --- INÍCIO ---
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    bot = app.bot

    # Comandos
    app.add_handler(CommandHandler("sinal", comando_sinal))
    app.add_handler(CommandHandler("last", comando_last))
    app.add_handler(CommandHandler("b", comando_b))

    # Loop de presença e sinais
    async def start_loop():
        await loop_atividade(bot)

    asyncio.create_task(start_loop())

    # Rodar o bot
    app.run_polling()
