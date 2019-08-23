# telegram-bot-easy-auth
This is a basic authentication system for telegram bots written in python and the help of https://python-telegram-bot.org/
you have to install https://python-telegram-bot.org/ this pip

just insert your token from your bot and start using the auth system! (generate your bot with the @Botfather bot on telegram)

you will get your chat_id if you start your bot and have a look in the logfile, where everything gets logged (failed_attempts.txt), the first number is your chat_id, simply add it to admins.txt and you are admin

to add someone to the allowed_user.txt, simply add his/her chat_id to the allowed_user.txt or if you are admin use the /add {chat_id} command
