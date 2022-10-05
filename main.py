from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup

import Constants as keys
from telegram.ext import *
from translate import Translator

print("Bot started...")


def start_command(update, context):
    update.message.reply_text('Type /help to get help!')


def help_command(update, context):
    update.message.reply_text('This Bot will translate all your messages.')
    update.message.reply_text('/translate -> start the translation ans select language')
    update.message.reply_text('Just type to translate automatically')


# show InlineKeyboard to select language
def select_lang(update: Update, context: CallbackContext) -> None:
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Select your language", reply_markup=reply_markup)


# language options
keyboard = [
    [
        InlineKeyboardButton("English", callback_data="English"),
        InlineKeyboardButton("Spanish", callback_data="Spanish"),
        InlineKeyboardButton("French", callback_data="French"),
        InlineKeyboardButton("Russian", callback_data="Russian"),
        InlineKeyboardButton("Portuguese", callback_data="Portuguese"),
        InlineKeyboardButton("Hindi", callback_data="Hindi"),
    ]
]

# store the to language
lang = ""


# how to deal with click on language
def button(update: Update, context: CallbackContext) -> None:
    global lang
    lang = update.callback_query.data.lower()
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text=f"{query.data} has been selected for translation! You can start translating your text!")


# translate from german to selected language
def lang_translator(user_input):
    translator = Translator(from_lang="german", to_lang=lang)
    translation = translator.translate(user_input)
    return translation


# standard method to respond
def reply(update, context):
    user_input = update.message.text
    update.message.reply_text(lang_translator(user_input))


def error(update, context):
    print(f"Update {update} caused error {context.error}")


def main():
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher
    # setup all commands
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("translate", select_lang))
    dp.add_handler(CallbackQueryHandler(button))

    # setup translation
    dp.add_handler(MessageHandler(Filters.text, reply))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


main()
