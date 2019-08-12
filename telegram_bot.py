#!/usr/bin/env python3.7
import time
import telebot

file =  open('admins.txt',"r")
admins = []
for val in file.read().split():
    admins.append(int(val))
file.close()

request = "Your request for using this bot was sent to all admins, when they approved you, you will be notified!"
admin_approval_form = "There is a new request for using the bot"
command_error = "Error! Please write a valid command"
welcome_message = "Welcome to the .. Bot!"

bot = telebot.TeleBot("TOKEN")

def validating(cid):
    file =  open('allowed_user.txt',"r")
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
    file =  open('admins.txt',"r")
    admins = []
    for val in file.read().split():
        admins.append(int(val))
    file.close()
    if cid in admins:
        return True
    else:
        return False

def send_to_admin(cid,name):
    #send to all admins
    for admin in admins:
        bot.send_message(admin, f"""{admin_approval_form}\n\nUsername: {name}\nchat_id: {cid}\n\nFor approval send /add {cid}""")
    return 0

@bot.message_handler(commands=['start'])
def start(message):
    cid = message.chat.id
    name = message.chat.username
    content = message.text
    if validating(cid) == True:
        bot.reply_to(message, welcome_message)
    else:
        failed_attempts(cid,name,content)
        send_to_admin(cid, name)
        bot.reply_to(message, request)

@bot.message_handler(commands=['add'])
def add_user(message):
    cid = message.chat.id
    name = message.chat.username
    content = message.text
    if admin_check(cid) == True:
        if message.text != "/add":
            try:
                new_user = message.text.strip('/add ')
                new_user = f"""{new_user}\n"""
                new_user_raw = new_user.strip('\n')
                bot.send_message(new_user_raw, f"""Hey {name}!\nYou are now approved, have fun using this bot!""")

                with open('allowed_user.txt',"a") as file:
                    file.write(new_user)
                    file.close()
                for admin in admins:
                    bot.send_message(admin, f"""{name} added {new_user}He/She is now able to interact with the bot!""")

            except:
                failed_attempts(cid,name,content)
                bot.reply_to(message, "Please provide a valid chat_id!")
        else:
            bot.reply_to(message, "Please provide a chat id")
    else:
        failed_attempts(cid,name,content)
        bot.reply_to(message, command_error)

#writes all false commands to the logfile
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    cid = message.chat.id
    name = message.chat.username
    content = message.text
    if validating(cid) == True:
        bot.reply_to(message, command_error)
    else:
        failed_attempts(cid,name,content)

bot.polling()
while True:
    time.sleep(0)
