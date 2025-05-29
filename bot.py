import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from deep_translator import GoogleTranslator
import json


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='bot_messages.log',
    encoding='utf-8'
)
logger = logging.getLogger(__name__)

translator = GoogleTranslator(source='auto', target='ru')


def get_random_joke():
    response = requests.get(f'http://rzhunemogu.ru/RandJSON.aspx?CType=1')
    if response.status_code == 200:
        cleaned_response = response.text.replace(
            "\r", "").replace("\n", "").replace("\t", "")
        joke = json.loads(cleaned_response)
        if 'content' in joke:
            joke_text = joke['content']
            joke_text_ru = translator.translate(joke_text)
            return joke_text_ru
    return "Не удалось получить шутку."


def get_random_joke_18():
    response = requests.get(f'http://rzhunemogu.ru/RandJSON.aspx?CType=11')
    if response.status_code == 200:
        cleaned_response = response.text.replace(
            "\r", "").replace("\n", "").replace("\t", "")
        joke = json.loads(cleaned_response)
        if 'content' in joke:
            joke_text = joke['content']
            joke_text_ru = translator.translate(joke_text)
            return joke_text_ru
    return "Не удалось получить шутку."


def get_poem():
    response = requests.get(
        f'http://rzhunemogu.ru/RandJSON.aspx?CType=3')
    if response.status_code == 200:
        cleaned_response = response.text.replace(
            "\r", "").replace("\n", "").replace("\t", "")
        poem = json.loads(cleaned_response)
        if 'content' in poem:
            poem_text = poem['content']
            poem_text_ru = translator.translate(poem_text)
            return poem_text_ru
    return "Не удалось получить стих."


def get_poem_18():
    response = requests.get(f'http://rzhunemogu.ru/RandJSON.aspx?CType=13')
    if response.status_code == 200:
        cleaned_response = response.text.replace(
            "\r", "").replace("\n", "").replace("\t", "")
        poem = json.loads(cleaned_response)
        if 'content' in poem:
            poem_text = poem['content']
            poem_text_ru = translator.translate(poem_text)
            return poem_text_ru
    return "Не удалось получить стих."


def get_random_meme():
    response = requests.get('https://random.dog/woof.json')
    if response.status_code == 200:
        meme = response.json()
        return meme['url']
    else:
        logger.error(f"Ошибка при получении мема: {response.status_code}")
        return "Не удалось получить мем."


def get_fact():
    response = requests.get(
        'https://uselessfacts.jsph.pl/random.json?language=en')
    if response.status_code == 200:
        fact = response.json()['text']
        fact_ru = translator.translate(fact)
        return f"Факт: {fact_ru}\n\n"
    else:
        logger.error(f"Ошибка при получении факта: {response.status_code}")
        return "Не удалось получить факт."


async def start(update: Update, context: CallbackContext):
    user_message = update.message.text
    user = update.effective_user
    logger.info(f"Пользователь {user.id} ({user.username}): {user_message}")

    response_text = (
        "Привет! Я твой чат-бот для шуток и мемов. Выбери команду:\n"
        "/joke - случайная шутка\n"
        "/joke_18 - шутка для взрослых\n"
        "/poem - случайное стихотворение\n"
        "/poem_18 - стихотворение для взрослых\n"
        "/meme - случайный мем про собак\n"
        "/fact - интересный факт"
    )
    await update.message.reply_text(response_text)
    logger.info(f"Бот ответил пользователю {user.id}: {response_text}")


async def joke(update: Update, context: CallbackContext):
    user_message = update.message.text
    user = update.effective_user
    logger.info(f"Пользователь {user.id} ({user.username}): {user_message}")

    response_text = get_random_joke()
    await update.message.reply_text(response_text)
    logger.info(f"Бот ответил пользователю {user.id}: {response_text}")


async def joke_18(update: Update, context: CallbackContext):
    user_message = update.message.text
    user = update.effective_user
    logger.info(f"Пользователь {user.id} ({user.username}): {user_message}")

    response_text = get_random_joke_18()
    await update.message.reply_text(response_text)
    logger.info(f"Бот ответил пользователю {user.id}: {response_text}")


async def poem(update: Update, context: CallbackContext):
    user_message = update.message.text
    user = update.effective_user
    logger.info(f"Пользователь {user.id} ({user.username}): {user_message}")

    response_text = get_poem()
    await update.message.reply_text(response_text)
    logger.info(f"Бот ответил пользователю {user.id}: {response_text}")


async def poem_18(update: Update, context: CallbackContext):
    user_message = update.message.text
    user = update.effective_user
    logger.info(f"Пользователь {user.id} ({user.username}): {user_message}")

    response_text = get_poem_18()
    await update.message.reply_text(response_text)
    logger.info(f"Бот ответил пользователю {user.id}: {response_text}")


async def meme(update: Update, context: CallbackContext):
    user_message = update.message.text
    user = update.effective_user
    logger.info(f"Пользователь {user.id} ({user.username}): {user_message}")

    response_text = get_random_meme()
    await update.message.reply_text(response_text)
    logger.info(f"Бот ответил пользователю {user.id}: {response_text}")


async def fact(update: Update, context: CallbackContext):
    user_message = update.message.text
    user = update.effective_user
    logger.info(f"Пользователь {user.id} ({user.username}): {user_message}")

    response_text = get_fact()
    await update.message.reply_text(response_text)
    logger.info(f"Бот ответил пользователю {user.id}: {response_text}")


def main():

    logger.info("Запуск бота")
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("joke", joke))
    application.add_handler(CommandHandler("joke_18", joke_18))
    application.add_handler(CommandHandler("poem", poem))
    application.add_handler(CommandHandler("poem_18", poem_18))
    application.add_handler(CommandHandler("meme", meme))
    application.add_handler(CommandHandler("fact", fact))

    application.run_polling()


if __name__ == '__main__':
    main()
