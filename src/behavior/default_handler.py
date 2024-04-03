from telegram._update import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, MessageHandler, filters, \
    CallbackQueryHandler

from src.data_init import logger, WEBUI_BASE_URL
from src.models.user import User
from src.services.init import user_api

REGISTRATION_NAME, REGISTRATION_DESCRIPTION, REGISTRATION_END = range(3)


async def registration_nickname_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    i = update.message.from_user.id
    registration = await user_api.auth(i)

    if registration is None:
        await update.message.reply_text(
            "Начнем регистрацию! Введите свой nickname:"
        )
        return REGISTRATION_NAME
    else:
        await update.message.reply_text(
            "Вы уже зарегистрированы.\n" +
            f"Ваш tgId: {i}.\n" +
            "Создать новую заявку можно по ссылке:\n"
        )
        await update.message.reply_text(
            f"https://{WEBUI_BASE_URL}/new_trip_registration?tg_id={i}"
        )

        return ConversationHandler.END


async def registration_fio_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["nick"] = update.message.text

    await update.message.reply_text(
        "Введите свой ФИО:"
    )

    return REGISTRATION_DESCRIPTION


async def registration_description_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["full_name"] = update.message.text

    await update.message.reply_text(
        "Расскажите о себе - чем увлекаетесь, интересуетесь:"
    )

    return REGISTRATION_END


async def registration_end_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["description"] = update.message.text
    nick = context.user_data["nick"]
    i = update.message.from_user.id
    res = await user_api.create_user(
        User(
            context.user_data["nick"],
            context.user_data["full_name"],
            context.user_data["description"],
            update.message.from_user.username,
            i
        ))

    if res is not None:
        logger.info(
            f"User[nickname={nick}] successfully registered")

        await update.message.reply_text(
            "Вы зарегистрированы.\n" +
            f"Ваш tgId: {i}.\n" +
            "Создать новую заявку можно по ссылке:\n"
        )
        await update.message.reply_text(
            f"https://{WEBUI_BASE_URL}/new_trip_registration?tg_id={i}"
        )
    else:
        logger.info(
            f"User[nickname={nick}] error when register")

        await update.message.reply_text(
            "Что-то пошло не так! Попробуйте еще раз!"
        )

    return ConversationHandler.END

async def cancel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    return ConversationHandler.END

def default_builder() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[
            MessageHandler(filters.TEXT & ~filters.COMMAND, registration_nickname_callback),
            CommandHandler("start", registration_nickname_callback)
        ],
        states={
            REGISTRATION_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, registration_fio_callback)
            ],
            REGISTRATION_DESCRIPTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, registration_description_callback)
            ],
            REGISTRATION_END: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, registration_end_callback)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel_callback)]
    )
