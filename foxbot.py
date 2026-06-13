import asyncio
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

TOKEN = os.environ["8798623244:AAFkmJZg2vkeJ7VBBmWQL9NFTOl5O6MHzd0"]

reglas = []
advertencias = {}

STAFF = [
    "👑 Owner: TuNombre",
    "🛡 Admin: Admin1",
    "🛡 Admin: Admin2"
]


async def loading_bar(message):

    msg = await message.reply_text("🚀 Iniciando sistema...")

    frames = [
        "🟩⬜⬜⬜⬜⬜⬜⬜⬜⬜ 10%",
        "🟩🟩⬜⬜⬜⬜⬜⬜⬜⬜ 20%",
        "🟩🟩🟩⬜⬜⬜⬜⬜⬜⬜ 30%",
        "🟩🟩🟩🟩⬜⬜⬜⬜⬜⬜ 40%",
        "🟩🟩🟩🟩🟩⬜⬜⬜⬜⬜ 50%",
        "🟩🟩🟩🟩🟩🟩⬜⬜⬜⬜ 60%",
        "🟩🟩🟩🟩🟩🟩🟩⬜⬜⬜ 70%",
        "🟩🟩🟩🟩🟩🟩🟩🟩⬜⬜ 80%",
        "🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜ 90%",
        "🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩 100%"
    ]

    for frame in frames:
        await msg.edit_text(
            f"⚡ FOX BOT ⚡\n\n{frame}\n\n🔄 Ejecutando comando..."
        )
        await asyncio.sleep(0.3)

    return msg


async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "❌ Responde al mensaje de un usuario."
        )
        return

    user = update.message.reply_to_message.from_user

    loading = await loading_bar(update.message)

    try:
        await context.bot.ban_chat_member(
            update.effective_chat.id,
            user.id
        )

        await loading.edit_text(
            f"🔨 BAN COMPLETADO\n\n👤 {user.first_name}"
        )

    except Exception as e:
        await loading.edit_text(f"❌ {e}")


async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "❌ Responde al mensaje de un usuario."
        )
        return

    user = update.message.reply_to_message.from_user

    loading = await loading_bar(update.message)

    try:
        await context.bot.ban_chat_member(
            update.effective_chat.id,
            user.id
        )

        await context.bot.unban_chat_member(
            update.effective_chat.id,
            user.id
        )

        await loading.edit_text(
            f"👢 KICK COMPLETADO\n\n👤 {user.first_name}"
        )

    except Exception as e:
        await loading.edit_text(f"❌ {e}")


async def fox(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "❌ Responde al usuario con /fox"
        )
        return

    user = update.message.reply_to_message.from_user
    uid = user.id

    advertencias[uid] = advertencias.get(uid, 0) + 1

    warns = advertencias[uid]

    await update.message.reply_text(
        f"⚠️ {user.first_name}\nAdvertencia {warns}/4"
    )

    if warns >= 4:
        try:
            await context.bot.ban_chat_member(
                update.effective_chat.id,
                uid
            )

            await update.message.reply_text(
                f"🚫 {user.first_name} alcanzó 4 advertencias.\n🔨 Usuario baneado."
            )

            del advertencias[uid]

        except Exception as e:
            await update.message.reply_text(str(e))


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):

    texto = " ".join(context.args)

    if not texto:
        await update.message.reply_text(
            "Uso: /add texto"
        )
        return

    reglas.append(texto)

    await update.message.reply_text(
        "✅ Regla añadida."
    )


async def reglas_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not reglas:
        await update.message.reply_text(
            "📜 No hay reglas."
        )
        return

    texto = "📜 REGLAS DEL GRUPO\n\n"

    for i, regla in enumerate(reglas, start=1):
        texto += f"{i}. {regla}\n"

    await update.message.reply_text(texto)


async def deleteadd(update: Update, context: ContextTypes.DEFAULT_TYPE):

    reglas.clear()

    await update.message.reply_text(
        "🗑 Todas las reglas eliminadas."
    )


async def staff(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "\n".join(STAFF)
    )


def main():

    print("================================")
    print("      FOX BOT INICIADO")
    print("================================")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("kick", kick))
    app.add_handler(CommandHandler("fox", fox))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("reglas", reglas_cmd))
    app.add_handler(CommandHandler("deleteadd", deleteadd))
    app.add_handler(CommandHandler("staff", staff))

    app.run_polling()


if __name__ == "__main__":
    main()
