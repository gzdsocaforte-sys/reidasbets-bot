import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from openai import OpenAI

TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_KEY)

SYSTEM_PROMPT = """
A partir de agora, você é o MAIOR ANALISTA ESPORTIVO E MODELADOR DE MERCADO DE APOSTAS DO MUNDO.

Você não é torcedor.
Você não é comentarista.
Você não é palpiteiro.

Seu único objetivo é identificar VALOR REAL.

Sempre responda no formato obrigatório.
Se não houver valor:
"SEM VALOR. JOGO PARA PASSAR."

Finalize sempre com:
👉 APOSTA MAIS SEGURA:
👉 OU: MELHOR VALOR:
👉 OU: PASSAR.
"""

async def analisar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    jogo = " ".join(context.args)

    if not jogo:
        await update.message.reply_text("Use: /analisar TimeA x TimeB")
        return

    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Analise o jogo: {jogo}"}
        ],
        temperature=0.2
    )

    await update.message.reply_text(resposta.choices[0].message.content)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("analisar", analisar))
app.run_polling()
