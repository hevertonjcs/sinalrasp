import random
import asyncio
from datetime import datetime, timedelta
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.error import BadRequest

# --- CONFIGURAÇÕES ---
BOT_TOKEN = "7401293219:AAFDt9G2wlozVa1zNGU-A50Uj9R1yCh3zE8"
CHAT_ID = "-4935359876"
INTERVALOS = [3, 5, 6, 7, 8, 10]

# Mensagens de presença/atividade
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

# Frases adicionais para sinais (variações internas)
FRASES_SINAL = [
    "Não perca esta chance! 💎",
    "Confira e aproveite a oportunidade! 🚀",
    "Potencial de lucro alto! 📈",
    "Sinal baseado nos últimos padrões vencedores 🔍",
    "Risco calculado, aposta estratégica 🏆",
    "Atenção! Pode ser um grande vencedor 💰",
]

# Guardar o último sinal
ultimo_sinal = ""

# --- FUNÇÕES ---
def gerar_horario_futuro(minutos: int) -> str:
    futuro = datetime.now() + timedelta(minutes=minutos)
    return futuro.strftime("%H:%M")

def gerar_sinal() -> str:
    global ultimo_sinal
    escolha = random.choice([50, 100])
    minutos = random.choice([3, 5, 10, 13, 15])
    frase_extra = random.choice(FRASES_SINAL)
    link = "raspadinhatri.com"
    if escolha == 50:
        sinal = f"""
APOSTA EM POTENCIAL {link.upper()}

RASPADINHA DE R$ 50 (DOBRO DE CHANCE) ✅
Lucro em Potencial 📈
Em {minutos} Minutos ⏰ ({gerar_horario_futuro(minutos)})
{frase_extra}
Acesse: {link}
"""
    else:
        sinal = f"""
APOSTA EM POTENCIAL {link.upper()}

RASPADINHA DE R$ 100 (TRIPLO DE CHANCE) ✅
Lucro em Potencial 📈
Em {minutos} Minutos ⏰ ({gerar_horario_futuro(minutos)})
{frase_extra}
Acesse: {link}
"""
    ultimo_sinal = sinal
    return sinal

async def enviar_se_apenas_adm(update: Update, context: ContextTypes.DEFAULT_TYPE, func):
    """Executa a função apenas se o usuário for administrador do grupo"""
    try:
        chat_member = await update.effective_chat.get_member(update.effective_user.id)
        if chat_member.status in ["administrator", "creator"]:
            await func(update, context)
        else:
            await update.message.reply_text("Apenas administradores podem usar este comando.")
    except BadRequest:
        await update.message.reply_text("Não foi possível verificar permissões.")

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

# --- FUNÇÃO PRINCIPAL ---
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Comandos restritos a admins
    app.add_handler(CommandHandler("sinal", lambda u, c: enviar_se_apenas_adm(u, c, comando_sinal)))
    app.add_handler(CommandHandler("start", lambda u, c: enviar_se_apenas_adm(u, c, lambda u2, c2: asyncio.create_task(loop_atividade(app.bot)))))
    app.add_handler(CommandHandler("stop", lambda u, c: enviar_se_apenas_adm(u, c, lambda u2, c2: asyncio.get_event_loop().stop())))
    
    # Comandos liberados
    app.add_handler(CommandHandler("last", comando_last))
    app.add_handler(CommandHandler("b", comando_b))
    
    # Rodar polling
    await app.run_polling()

# --- EXECUTAR BOT ---
if __name__ == "__main__":
    asyncio.run(main())
