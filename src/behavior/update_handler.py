from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram._update import Update
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, MessageHandler, filters, \
    CallbackQueryHandler

from src.data_init import logger
from src.models.user import User, ChangeUserRequest
from src.services.init import user_api

CHANGE_KEY, CHANGE_VALUE = range(2)


async def update_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    reply_markup = ReplyKeyboardMarkup([["Nickname", "Full Name"], ["Description"]], one_time_keyboard=True)

    await update.message.reply_text(
        "Выберите поле, которое хотите измененить:",
        reply_markup=reply_markup
    )

    return CHANGE_KEY

async def update_key_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    context.user_data["key"] = update.message.text

    await update.message.reply_text(
        "Введите новое значение:",
        reply_markup=ReplyKeyboardRemove()
    )


    return CHANGE_VALUE

async def update_value_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    chUser = ChangeUserRequest(
        update.message.from_user.id,
        None,
        None,
        None
    )

    if context.user_data["key"] == "Nickname":
        chUser.nick = update.message.text
    elif context.user_data["key"] == "Full Name":
        chUser.fullName = update.message.text
    elif context.user_data["key"] == "Description":
        chUser.description = update.message.text
    else:
        await update.message.reply_text(
            "Неизвестное значение",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    res = await user_api.change(chUser)

    if res is not None:
        await update.message.reply_text(
            "Данные обновлены",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await update.message.reply_text(
            "Что-то пошло не так! Попробуйте еще раз!"
        )


    return ConversationHandler.END


async def cancel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:


    return ConversationHandler.END


def update_builder() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[
            CommandHandler("change", update_callback)
        ],
        states={
            CHANGE_KEY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, update_key_callback),
            ],
            CHANGE_VALUE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, update_value_callback)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel_callback)]
    )
