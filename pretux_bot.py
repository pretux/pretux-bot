#!venv/bin/python3
# pylint: disable=C0116,W0613


import email
import logging
import notion
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    Filters,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
)
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Stages
BOLSA, CHECK, PENDENCIAS = range(3)

# Callback data
SCHOLARSHIP, EMAIL_PENDENCY, CHECK_PENDENCY, RESTART, EMAIL, CONFIRMATION, YES_CONFIRM, NO_CONFIRM = range(8)
global action_email

def start(update: Update, context: CallbackContext) -> int:
    """Send message on `/start`."""
    user = update.message.from_user
    logger.info(f"User {user.full_name} { user.id}  started the conversation.")
    keyboard = [
        [
            InlineKeyboardButton("Confirmação de bolsa", callback_data=str(SCHOLARSHIP)),
            InlineKeyboardButton("Verificar pendência", callback_data=str(CHECK_PENDENCY)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "Olá! Sou o bot Pretuxin! Escolha uma das opções abaixo:", reply_markup=reply_markup)
    
    return BOLSA

def restart_process(update: Update, context: CallbackContext) -> int:
    """Ask the user for info about the selected predefined choice."""
    query = update.callback_query
    query.answer()
    query.edit_message_reply_markup(reply_markup=None)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="""Você não confirmou a recusa da bolsa, para reiniciar o processo você precisa digitar /start""")



def yes_confirm(update: Update, context: CallbackContext) -> int:
    """Ask the user for info about the selected predefined choice."""
    query = update.callback_query
    query.answer()
    query.edit_message_reply_markup(reply_markup=None)
    notion.confirm_scholarship(context.user_data["user_name"], context.user_data["user_email"], context.user_data["user_course_name"], context.user_data["user_course_title"], context.user_data["user_end_time"], context.user_data["user_activity"], update.effective_user.id)
    notion.remove_user_after_confirm(context.user_data["user_id_notion"])
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Obrigado por confirmar!")
    context.bot.send_video(chat_id=update.effective_chat.id,
                               video="https://c.tenor.com/sIkK8k5WuN0AAAAC/will-smith-fresh-prince.gif")    

def yes_confirm_check(update: Update, context: CallbackContext) -> int:
    """Ask the user for info about the selected predefined choice."""
    keyboard = [
            [
                InlineKeyboardButton("Sim", callback_data=str(YES_CONFIRM)),
                InlineKeyboardButton("Não", callback_data=str(RESTART)),
            ]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Você tem certeza que deseja confirmar a bolsa?", reply_markup=reply_markup)
    query = update.callback_query
    query.answer()
    query.edit_message_reply_markup(reply_markup=None)
    return BOLSA


def no_confirm(update: Update, context: CallbackContext) -> int:
    """Ask the user for info about the selected predefined choice."""
    query = update.callback_query
    query.answer()
    query.edit_message_reply_markup(reply_markup=None)
    notion.refuse_scholarship(context.user_data["user_name"], context.user_data["user_email"], context.user_data["user_course_name"], context.user_data["user_course_title"], context.user_data["user_end_time"], context.user_data["user_activity"], update.effective_user.id)
    notion.remove_user_after_confirm(context.user_data["user_id_notion"])
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="A PretUX agradece! Seu nome será removido da lista!")
    context.bot.send_video(chat_id=update.effective_chat.id,
                               video="https://c.tenor.com/UAdpvL0E4t4AAAAC/my-wife-and-kids-hurt.gif")

def no_confirm_check(update: Update, context: CallbackContext) -> int:
    """Ask the user for info about the selected predefined choice."""
    keyboard = [
            [
                InlineKeyboardButton("Sim", callback_data=str(NO_CONFIRM)),
                InlineKeyboardButton("Não", callback_data=str(RESTART)),
            ]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Você tem certeza que deseja recusar a bolsa?", reply_markup=reply_markup)
    query = update.callback_query
    query.answer()
    query.edit_message_reply_markup(reply_markup=None)

    return BOLSA



def scholarship(update: Update, context: CallbackContext) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    user_info = notion.main(text)
    if user_info[0]["status"] == 'is_pending':
        update.message.reply_text(
            "Desculpe, não podemos confirmar a sua inscrição. Uma pendência foi encontrada:\n\n"
            "Pendência: " + user_info[0]["activity"] + "\n\n"
            "Nome: " + user_info[0]["name"] + "\n"
            "E-mail: " + user_info[0]["email"] + "\n"
            "Curso: " + user_info[0]["course_name"] + "\n",
        )
        context.bot.send_video(chat_id=update.effective_chat.id,
                               video="https://c.tenor.com/N2UCqEZRRVAAAAAC/gloria-maria.gif")

    if user_info[0]["status"] == 'not_contemplated':
        update.message.reply_text(
            "Poxa, seu nome não está na lista de pessoas contempladas.")
        context.bot.send_video(chat_id=update.effective_chat.id,
                               video="https://c.tenor.com/BViD0bI6hYAAAAAC/futureofrep-tiffany.gif")
    if user_info[0]["status"] == 'contemplated':
        keyboard = [
            [
                InlineKeyboardButton("Confirmar", callback_data=str(YES_CONFIRM)),
                InlineKeyboardButton("Recusar", callback_data=str(NO_CONFIRM)),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "Parabéns! Você é umas das pessoas contempladas para o curso abaixo:  \n\n"
            "Nome: " + user_info[0]["name"] + "\n"
            "E-mail: " + user_info[0]["email"] + "\n"
            "Curso: " + user_info[0]["course_name"] + "\n\n"
            "Como forma de retribuição, você vai enviar para gente: " +
            user_info[0]["activity"] + "\n\n"
            "Você deseja confirmar ou recusar a bolsa?", reply_markup=reply_markup
        )
        context.user_data["user_id_notion"] = user_info[0]["user_id"]
        context.user_data["user_name"] = user_info[0]["name"]
        context.user_data["user_email"] = user_info[0]["email"]
        context.user_data["user_course_name"] = user_info[0]["course_name"]
        context.user_data["user_course_title"] = user_info[0]["course_title"]
        context.user_data["user_activity"] = user_info[0]["activity"]
        context.user_data["user_end_time"] = user_info[0]["end_time"]
        
    return CHECK


def check_email(update: Update, context: CallbackContext) -> str:
    """Choose to add mother or father."""

    text = 'Vamos lá! Envie o seu email, por favor ...'

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text)
    query = update.callback_query.data
    if query == str(CHECK_PENDENCY):
        return PENDENCIAS
    elif query == str(SCHOLARSHIP):
        return EMAIL


def check_pendency(update: Update, context: CallbackContext) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    user_info = notion.check_pendency(text)
    if user_info[0]["status"] == 'is_pending':
        update.message.reply_text(
            "Iihh, encontrei a pendência abaixo:\n\n"
            "Pendencia: " + user_info[0]["activity"] + "\n\n"
            "Nome: " + user_info[0]["name"] + "\n"
            "E-mail: " + user_info[0]["email"] + "\n"
            "Curso: " + user_info[0]["course_name"] + "\n\n"
            "Ainda não enviou o seu artigo para gente? É só mandar para: somos@pretux.com.br \n"
            "Lembrando que, enquanto o artigo não for enviado, você não pode concorrer a novas bolsas."
            
        )
        context.bot.send_video(chat_id=update.effective_chat.id,
                               video="https://t8j5n5j3.rocketcdn.me/wp-content/uploads/2015/12/1-37.jpg")
    if user_info[0]["status"] == 'is_not_pending':
        update.message.reply_text(
            "Uhuul, você não tem pendênciae e pode concorrer as novas bolsas!")
    return BOLSA





def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("1809587161:AAE6sC3000arbFBR_sQdzwt3K9yMXa1L34A")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Setup conversation handler with the states BOLSA and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    pendencia_handler = [
            MessageHandler(Filters.regex('[A-Za-z0-9\\._-]+@[A-Za-z0-9]+\\..(\\.[A-Za-z]+)*'), check_pendency),
    ]
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            BOLSA: [
                CallbackQueryHandler(check_email, pattern='^' + str(SCHOLARSHIP) + '$'),
                CallbackQueryHandler(check_email, pattern='^' + str(CHECK_PENDENCY) + '$'),
                CallbackQueryHandler(yes_confirm, pattern='^' + str(YES_CONFIRM) + '$'),
                CallbackQueryHandler(no_confirm, pattern='^' + str(NO_CONFIRM) + '$'),
                CallbackQueryHandler(restart_process, pattern='^' + str(RESTART) + '$'),
            ],
            PENDENCIAS: pendencia_handler,
            EMAIL: [
                MessageHandler(Filters.regex(
                    '[A-Za-z0-9\\._-]+@[A-Za-z0-9]+\\..(\\.[A-Za-z]+)*'), scholarship),
            ],
            CHECK: [
                CallbackQueryHandler(yes_confirm_check, pattern='^' + str(YES_CONFIRM) + '$'),
                CallbackQueryHandler(no_confirm_check, pattern='^' + str(NO_CONFIRM) + '$'),
            ]
        },
        fallbacks=[CommandHandler('start', start)],
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
