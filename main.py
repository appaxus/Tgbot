import time
import datetime
from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import time, datetime
import asyncio
import threading

bot = TeleBot("5954183098:AAEP8LI2yfgA2WDkYVQyXg3NV6szlHstCCk")

users = []
scores = {}


@bot.message_handler(commands=['start'])
def start(message):
    users.append(message.chat.id)
    bot.send_message(chat_id=message.chat.id,
                     text="Hi, this bot is needed to check the regularity of sports. Every morning it will send a task, after completing which you will need to click yes. After that, the bot will immediately send a message if today is Monday - shoulder workout, Tuesday - abs workout, Wednesday - leg workout, Thursday - biceps and triceps workout, Friday - back workout, Saturday - abs workout, Sunday - squats. On each following day, the user receives a message with the type of workout at 8 a.m.")


def send_workout_message():
    today = datetime.now().weekday()
    if today == 0:
        message = "Today is Monday, it's shoulder workout day!"
    elif today == 1:
        message = "Today is Tuesday, it's abs workout day!"
    elif today == 2:
        message = "Today is Wednesday, it's leg workout day!"
    elif today == 3:
        message = "Today is Thursday, it's biceps and triceps workout day!"
    elif today == 4:
        message = "Today is Friday, it's back workout day!"
    elif today == 5:
        message = "Today is Saturday, it's abs workout day!"
    else:
        message = "Today is Sunday, it's squats day!"

    done_button = InlineKeyboardButton("Done", callback_data="done")
    keyboard = InlineKeyboardMarkup()
    keyboard.add(done_button)

    for user in users:
        bot.send_message(chat_id=user, text=message, reply_markup=keyboard)
        if user not in scores:
            scores[user] = 0


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user = call.from_user.id
    if call.data == "done":
        scores[user] += 1
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Workout done! Your score is now {}".format(scores[user]))
    else:
        bot.answer_callback_query(callback_query_id=call.id)


@bot.message_handler(commands=['score'])
def score(message):
    message_text = "Scores of all registered users:\n"
    for user, score in scores.items():
        message_text += f"{user}: {score}\n"
    bot.send_message(chat_id=message.from_user.id, text=message_text)


async def schedule_workout_message():
    message_sent = False
    while True:
        next_time = time(8, 0)
        while not message_sent:
            current_time = datetime.now().time()
            if current_time >= next_time:
                send_workout_message()
                message_sent = True
            await asyncio.sleep(60)
        message_sent = False
        await asyncio.sleep(24*60*60)


if __name__ == '__main__':
    bot_thread = threading.Thread(target=bot.polling)
    bot_thread.start()
    asyncio.run(schedule_workout_message())
