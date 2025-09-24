import random
import inspect
from datetime import datetime, timedelta
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.error import BadRequest
import asyncio

BOT_TOKEN = "7401293219:AAFDt9G2wlozVa1zNGU-A50Uj9R1yCh3zE8"
CHAT_ID = "-4935359876"
INTERVALOS = [2, 3, 4, 5, 6]  # mais rápido

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

MENSAGENS_BUSCA = [
    "Estou analisando padrões agora 🔎",
    "Buscando sinais com maior potencial 📊",
    "Verificando últimos ganhadores 🏆",
    "Calculando oportunidades de Raspadinha 💰",
    "Monitorando estatísticas atuais 📈",
    "Preparando próximo sinal garantido ⏱️",
    "Buscando padrões de vitória recentes 🔍",
    "Analisando tendências do dia… 🧐",
    "Processando dados e padrões atuais 📊",
    "Verificando probabilidades e chances 💡",
]

FRASES_SINAL = [
    "Não perca esta chance! Ganho Garantido 💎",
    "Confira e aproveite a oportunidade de ganhar de verdade! 🚀",
    "Potencial de lucro alto garantido! 📈",
    "Sinal Garantido baseado nos últimos padrões vencedores 🔍",
    "Risco calculado, aposta estratégica e garantida 🏆",
    "Atenção! Pode ser um grande vencedor garantido 💰",
]

ultimo_sinal = ""
loop_rodando = False
ultimo_aviso_fixado = None  # guarda o ID do aviso fixado


def gerar_horario_futuro(minutos: int) -> str:
    futuro = datetime.now() + timedelta(minutes=minutos)
    return futuro.strftime("%H:%M")


def gerar_sinal() -> str:
    global ultimo_sinal
    escolha = random.choice([50, 100])
    minutos = random.choice([2, 3, 4, 5])
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


def enviar_se_apenas_adm(func):
    """Decorator para restringir comandos a administradores"""
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            chat_member = await update.effective_chat.get_member(update.effective_user.id)
            if chat_member.status in ["administrator", "creator"]:
                if inspect.iscoroutinefunction(func):
                    return await func(update, context)
                else:
                    return func(update, context)
            else:
                await update.message.reply_text("❌ Apenas administradores podem usar este comando.")
        except BadRequest:
            await update.message.reply_text("⚠️ Não foi possível verificar permissões.")
    return wrapper


@enviar_se_apenas_adm
async def comando_sinal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(gerar_sinal())


@enviar_se_apenas_adm
async def start_loop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global loop_rodando
    if not loop_rodando:
        loop_rodando = True
        asyncio.create_task(loop_atividade(context.bot))
        await update.message.reply_text("🤖 Bot ativado e em operação!")
    else:
        await update.message.reply_text("⚠️ O bot já está em execução.")


@enviar_se_apenas_adm
async def stop_loop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global loop_rodando
    loop_rodando = False
    await update.message.reply_text("❌ Bot desativado.")


async def comando_last(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if ultimo_sinal:
        await update.message.reply_text(ultimo_sinal)
    else:
        await update.message.reply_text("Ainda não foi enviado nenhum sinal.")


async def comando_b(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = random.choice(MENSAGENS_BUSCA)
    await update.message.reply_text(msg)


@enviar_se_apenas_adm
async def comando_aviso(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lê comando.txt, envia e fixa. Substitui aviso anterior fixado."""
    global ultimo_aviso_fixado
    try:
        with open("comando.txt", "r", encoding="utf-8") as f:
            conteudo = f.read().strip()

        if not conteudo:
            await update.message.reply_text("⚠️ O arquivo comando.txt está vazio.")
            return

        # envia aviso
        sent = await context.bot.send_message(chat_id=CHAT_ID, text=conteudo)

        # desfixa o anterior se existir
        if ultimo_aviso_fixado:
            try:
                await context.bot.unpin_chat_message(chat_id=CHAT_ID, message_id=ultimo_aviso_fixado)
            except Exception:
                pass  # ignora se já não estiver fixado

        # fixa o novo
        try:
            await context.bot.pin_chat_message(chat_id=CHAT_ID, message_id=sent.message_id, disable_notification=True)
            ultimo_aviso_fixado = sent.message_id
        except Exception as e:
            await update.message.reply_text(f"⚠️ Aviso enviado, mas não consegui fixar: {e}")

    except FileNotFoundError:
        await update.message.reply_text("❌ O arquivo comando.txt não foi encontrado.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Erro ao ler comando.txt: {e}")


async def loop_atividade(bot: Bot):
    global loop_rodando
    while loop_rodando:
        try:
            # Mensagem de presença
            mensagem_presenca = random.choice(MENSAGENS_PRESENCA)
            await bot.send_message(chat_id=CHAT_ID, text=mensagem_presenca)
            await asyncio.sleep(random.randint(30, 60))

            # Sinal
            sinal = gerar_sinal()
            await bot.send_message(chat_id=CHAT_ID, text=sinal)

            intervalo = random.choice(INTERVALOS)
            await asyncio.sleep(intervalo * 60)

        except Exception as e:
            print(f"Erro no loop principal: {e}")
            await bot.send_message(chat_id=CHAT_ID, text="⚠️ Ocorreu um erro no loop, tentando continuar...")
            await asyncio.sleep(5)


# Handler global de erros
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Erro detectado: {context.error}")
    if isinstance(update, Update) and update.effective_chat:
        try:
            await update.effective_chat.send_message("⚠️ Ocorreu um erro inesperado, mas estou me recuperando.")
        except Exception:
            pass


if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Comandos restritos
    app.add_handler(CommandHandler("sinal", comando_sinal))
    app.add_handler(CommandHandler("start", start_loop))
    app.add_handler(CommandHandler("stop", stop_loop))
    app.add_handler(CommandHandler("aviso", comando_aviso))

    # Comandos liberados
    app.add_handler(CommandHandler("last", comando_last))
    app.add_handler(CommandHandler("b", comando_b))

    # Handler global de erros
    app.add_error_handler(error_handler)

    app.run_polling()

