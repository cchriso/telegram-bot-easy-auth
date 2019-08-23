from telegram.ext import Updater, CommandHandler
from telegram import ChatAction, ReplyKeyboardMarkup, ReplyKeyboardRemove, InputMediaPhoto
import time
import telegram

updater = Updater('your TOKEN here')

file =  open('admins.txt',"r")
admins = []
for val in file.read().split():
    admins.append(int(val))
file.close()

help_txt = "Here you have to write all of your commands "
welcome_message = "Willkommen zum Gratis McDonalds Bot!\n/help for further guidance"
command_error = "Error! Please provide a valid command, a list of all commands will be provided with /help"
request = "Your request for using this bot was sent to all admins, when they approved you, you will be notified!"
admin_approval_form = "There is a new request for using the bot"

def validating(cid):
    file = open('allowed_user.txt', "r")
    allowed_user = []
    for val in file.read().split():
        allowed_user.append(int(val))
    file.close()
    if cid in allowed_user:
        return True
    else:
        return False

def failed_attempts(cid,name,content):
    with open('failed_attempts.txt',"a") as file:
        file.write(f"""{cid} {name} - {content}\n""")
        file.close()

def admin_check(cid):
    if cid in admins:
        return True
    else:
        return False

def send_to_admin(cid,name,bot):
    #markup = bot.ReplyKeyboardMarkup()
    menu_keyboard = [[f"""/add {cid}"""], ['/dismiss']]
    #send to all admins
    text = f"""{admin_approval_form}\n\nUsername: {name}\nchat_id: {cid}\n\nFor approval send /add {cid}\nor you just click the button on your keyboard"""
    menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True, resize_keyboard=True)
    for admin in admins:
        bot.sendMessage(chat_id=admin,text=text, reply_markup=menu_markup)
    return 0


def start(bot, update):
    cid = update.message.chat_id
    name = update.message.from_user.username
    content = update.message.text
    if validating(cid) == True:
        bot.sendMessage(chat_id=cid, text=welcome_message)
    else:
        failed_attempts(cid,name,content)
        send_to_admin(cid,name,bot)
        bot.sendMessage(chat_id=cid, text=request)

def dismiss(bot,update):
    # todo: in zeile bestaetigen
    cid = update.message.chat_id
    name = update.message.from_user.username
    content = update.message.text
    if admin_check(cid) == True:
        for admin in admins:
            markup = ReplyKeyboardRemove()
            bot.sendMessage(admin, text=f"""Request declined from: {name}""", reply_markup=markup)
    else:
        failed_attempts(cid,name,content)

def help(bot,update):
    cid = update.message.chat_id
    name = update.message.from_user.username
    content = update.message.text
    if validating(cid) == True:
	       bot.sendMessage(chat_id=cid, text=help_txt)
    else:
        failed_attempts(cid,name,content)


def add(bot,update):
    cid = update.message.chat_id
    name = update.message.from_user.username
    content = update.message.text
    if admin_check(cid) == True:
        if content != "/add":
            try:
                new_user = content.strip('/add ')
                new_user = f"""{new_user}\n"""
                new_user_raw = new_user.strip('\n')

                with open('allowed_user.txt',"a") as file:
                    file.write(new_user)
                    file.close()
                bot.sendMessage(chat_id=new_user_raw, text=f"""Hey!\nYou are now approved, have fun using this bot!""")
                for admin in admins:
                    markup = ReplyKeyboardRemove(selective=False)
                    bot.sendMessage(chat_id=admin, text=f"""{name} added {new_user}He/She is now able to interact with the bot!""",reply_markup=markup)

            except:
                failed_attempts(cid,name,content)
                bot.sendMessage(chat_id=cid, text="Please provide a valid chat_id!")
        else:
            bot.sendMessage(chat_id=cid, text="You have to provide any chat_id my friend, otherwise i can\'t do a thing!")
    else:
        failed_attempts(cid,name,content)
        bot.sendMessage(chat_id=cid, text=command_error)


def hello(bot, update):
    update.message.reply_text('Hello {}'.format(update.message.chat_id))


updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('dismiss', dismiss))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('add', add))

updater.start_polling(poll_interval=1)
updater.idle()
