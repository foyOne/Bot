from datetime import datetime

import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import RegexSetting
import Database
import Model
from Model import Exercise
import Settings
import Utils
import Message
import json
import os

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)
db = Database.SQLiteDataBase(Settings.Connection)

def start(update: Update, context: CallbackContext) -> None:
    print(update)
    user = update.effective_user
    update.message.reply_text(Message.Message['Start'])


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(Message.Message['Help'])

def unknown(update: Update, context: CallbackContext):
    text = "К сожалению, я не знаю такой команды. Воспользуетесь /help для дополнительной информации."
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def GetStatistics(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    ses = db.GetSession()
    file2send = ''
    try:
        response = ses.query(Exercise.Date).filter(Exercise.ChatId == chat_id).distinct().order_by(Exercise.Date).all()
        if len(response) == 0:
            context.bot.send_message(chat_id=chat_id, text=Message.Message['StatisticNotData'])
            return
        
        current = os.path.abspath(os.path.dirname(__file__))
        name = ''
        if update.effective_chat.type == 'private':
            name = f'{update.effective_chat.first_name}-{update.effective_chat.last_name}-statistics.json'
        else:
            name = f'chat-{chat_id}-statistics.json'
        file2send = os.path.join(current, 'statistics', name)

        dateList = [t[0] for t in response]
        with open(file2send, 'w', encoding='utf-8') as file:
            globalObject = dict()
            for d in dateList:
                r = ses.query(Exercise).filter(Exercise.Date == d).all()
                collection = []
                dateString = datetime.strftime(d, '%d.%m.%Y')
                for row in r:
                    record = [row.Name, row.Sets, row.Times]
                    if row.Weight > 0:
                        record.append(row.Weight)
                    collection.append(record)
                globalObject[dateString] = collection
            json.dump(globalObject, file, indent=4, ensure_ascii=False)
        
        context.bot.send_document(chat_id=chat_id, document=open(file2send, 'rb'))

    except Exception as e :
        print(e)
        context.bot.send_message(chat_id=update.effective_chat.id, text=Message.Message['InternalError'])


def AddExercise(update: Update, context: CallbackContext):
    if update.message:

        data = list(context.match.groups())
        if not Utils.ParseData(data):
            context.bot.send_message(chat_id=update.effective_chat.id, text=Message.Message['IncorrentData'])
            return
        
        data.append(update.effective_chat.id)
        fields = Exercise.GetActualFields()
        fullData = dict(zip(fields, data))
        ses = db.GetSession()
        try:
            ex = Exercise(**fullData)
            ses.add(ex)
            ses.commit()
        except:
            ses.rollback()
            context.bot.send_message(chat_id=update.effective_chat.id, text=Message.Message['AddNotOk'])
            return
        context.bot.send_message(chat_id=update.effective_chat.id, text=Message.Message['AddOk'])


def DeleteAll(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    ses = db.GetSession()
    try:
        ses.query(Exercise).filter(Exercise.ChatId == chat_id).delete()
        ses.commit()
    except:
        ses.rollback()
        context.bot.send_message(chat_id=chat_id, text=Message.Message['DeleteAllNotOk'])
        return
    context.bot.send_message(chat_id=chat_id, text=Message.Message['DeleteAllOk'])

def Info(update: Update, context: CallbackContext):
    command = context.match.group(1)
    context.bot.send_message(chat_id=update.effective_chat.id, text=Message.Info[command])

def main() -> None:

    db.init(Model.Base)
    updater = Updater(Settings.Token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler('add', AddExercise, filters=Filters.regex(RegexSetting.ADD)))
    dispatcher.add_handler(CommandHandler('delete_all', DeleteAll, filters=Filters.regex(RegexSetting.DELETE_ALL)))
    dispatcher.add_handler(CommandHandler('statistics', GetStatistics, filters=Filters.regex(RegexSetting.STATISTICS)))
    dispatcher.add_handler(CommandHandler('info', Info, filters=Filters.regex(RegexSetting.INFO)))


    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
    db.Dispose()


if __name__ == '__main__':
    main()