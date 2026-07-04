#                                 o                                   
#             ºo   öº   Ö   ºö  º    º o                              
#        .oººö ºÖ     ö º  o  Ö  ö         _________                  
#       . ______          ______________  |         |      _____      
#     _()_||__|| ________ |            |  |_________|   __||___||__   
#    (         | |      | |            |  |Y_____00_|  |_         _|  
#  /-OO----OO**=*OO--OO*=*OO--------OO*=*OO-------OO*=*OO-------OO*=P 
#  ████████  ███████  ████████  ███████▒   ██████  ███   ███ ███  ███ 
#  ████████▒█████████ ████████▒█████████▒ ███████▒ ███   ███▒███▒ ███▒
#  ███▒ ███▒███   ███▒███▒▒▒▒▒▒███▒▒▒███▒ ███▒███▒ █████████▒███▒ ███▒
#  ███▒ ███▒███ █▒███▒████████  ▒▒▒ ███▒  ███▒███▒ █████████▒████████▒
#  ███▒ ███▒███ ▒▒███▒███▒▒▒▒▒▒███  ▒███▒ ███▒███▒  ▒▒▒▒▒███▒████████▒
#  ███▒ ███▒█████████▒████████ █████████▒█████████▒█████████▒███▒▒███▒
#  ███▒ ███▒▒███████▒▒████████▒▒███████▒▒███▒▒▒███▒████████▒▒███▒ ███▒
#   ▒▒▒  ▒▒▒  ▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒  ▒▒▒▒ ▒▒▒▒ ▒▒▒▒▒▒▒▒▒ ▒▒▒  ▒▒▒ AKA Матершиник
#                                                                     
#  v 1.0.0                                                            
#  04.07.26                                                           
#                                                                     
# Телеграм бот, который реагирует на сообщения с неправильно написаной нецензурной лексикой, отправляя в ответ видео.
# Вдохновлён шуточной командой sl для линукс и юникс систем, которая выводит анимацию поезда в терминале при ошибочном вводе команды ls.                                                        
#                                                                     
# Контрибьюторы: Tema Normalny (@Tema_Normalny on tg), //:DAVIDHAIT (@DAVIDHAIT on tg).                
# Бот был создан для чата тиктокера МишШиш414 - РАЙ.
#        
# Для работы бота необходимо установить библиотеку aiogram. Это можно сделать с помощью pip: pip install aiogram.
# Также, если вы пользователь NixOS, можно использовать команду nix-shell -p python310Packages.aiogram для установки aiogram,
# или использовать файл shell.nix прикреплённый к репозиторию, чтобы создать среду с установленной библиотекой aiogram.                                                                   
# !!! И НЕ ЗАБУДТЬЕ ПОСТАВИТЬ ТОКЕН !!!
# 
# Если хотите помочь с разработкой бота, можете написать мне в телеграм - @DAVIDHAIT
# (...Да, бот был частично создан на NixOS, всем советую :D)                                                                    

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import BaseFilter
from aiogram.types import FSInputFile, Message
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN", "")
VIDEO_PATH = os.getenv("VIDEO_PATH", "video.mp4")

if not TOKEN:
    raise SystemExit("Ошибка: BOT_TOKEN не найден в .env файле")

with open("words.txt", encoding="utf-8") as f:
    BAD_WORDS = {line.strip() for line in f if line.strip()}


bot = Bot(token=TOKEN)
dp = Dispatcher()

class ContainsBadWord(BaseFilter):
    cached_animation_id: str | None = None

    async def __call__(self, message: Message) -> bool:
        if not message.text:
            return False
        
        words = message.text.lower().split()
        
        for word in words:
            cleaned_word = word.strip(".,!?\"'()@#$-_")
            if cleaned_word in BAD_WORDS:
                return True
        return False

@dp.message(ContainsBadWord())
async def handle_bad_words(message: Message):
    try:
        if ContainsBadWord.cached_animation_id:
            await message.reply_animation(animation=ContainsBadWord.cached_animation_id)
        else:
            video_file = FSInputFile(VIDEO_PATH)
            sent = await message.reply_animation(animation=video_file)
            if sent.animation:
                ContainsBadWord.cached_animation_id = sent.animation.file_id
                logging.info(f"Анимация закеширована: {ContainsBadWord.cached_animation_id}")
    except FileNotFoundError:
        logging.error(f"Видео не найдено: {VIDEO_PATH}")
    except TelegramAPIError as e:
        logging.error(f"Ошибка Telegram API: {e}")
    except Exception as e:
        logging.exception(f"Неизвестная ошибка: {e}")

async def main():
    print("Бот запущен, печка разогрета, котёл кипит...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

# фрокинов иди нахуй 

# — Епа, кнезу, Џенова и Лука сега не се ништо повеќе од имоти,
# од поместија на фамилијата Бонапарта. Не, ви велам однапред,
# ако не ми кажете дека имаме војна, ако сè уште си дозволите
# да ги браните сите гадости, сите ужаси на тој Антихрист (жими
# Бога, јас верувам дека е Антихрист) — јас повеќе не ве познавам,
# вие веќе не сте мой пријател, вие веќе не сте мой верен роб,
# како што велите. Е па, добар ден, добар ден. Гледам дека ве
# исплашив, седнете и раскажувајте.
# Така зборуваше во јули 1805 година познатата Ана Павловна Шерер,
# деверуша и блиска соработка на императорката Марија Фјодоровна,
# пречекувајќи го важниот и висок државник, кнезот Василиј, кој
# прв дојде на нејзината вечерна забава. Ана Павловна кашлаше
# веќе неколку дена, таа имаше грип, како што велеше таа (грипот
# тогаш беше нов збор, употребуван само од ретки луѓе).
# Во писмата што ги праќаше утрото со лакеј во црвена ливерија,
# на сите без разлика им пишуваше:
# „Ако немате ништо подобро да правите, грофе (или кнезу), и ако
# перспективата да поминете една вечер кај кутрата болна не ви е
# премногу страшна, ќе ми биде многу мило да ве видам кај мене
# меѓу седум и десет часот. Ана Шерер“.
# — Господи, каков жесток напад! — одговори кнезот, влегувајќи
# во собата, во извезена дворска униформа, во чорапи, чевли
# и со ѕвезди на градите, со светло израз на своето рамнодушно
# лице, без воопшто да се збуни од ваквиот пречек.
# Тој зборуваше на оној префинет француски јазик, на кој не
# само што зборуваа, туку и мислеа нашите дедовци, и со оние
# тивки, покровителствени интонации што му приличат на еден
# значаен човек кој остарел во високото општество и на дворот.
# Тој и приоѓаше на Ана Павловна, ѝ ја бакнуваше раката,
# покажувајќи ѝ ја својата ќелава, парфимирана и светла глава,
# и мирно седна на софата.