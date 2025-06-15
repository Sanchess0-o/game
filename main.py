import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import random
import time

# Параметры записи
duration = 5  # секунды записи
sample_rate = 44100

# Словарь по уровням сложности
words_by_level = {
    "easy": {"кот": "cat", "собака": "dog", "яблоко": "apple", "молоко": "milk", "солнце": "sun", "машина": "car"},
    "medium": {"банан": "banana", "школа": "school", "друг": "friend", "окно": "window", "жёлтый": "yellow"},
    "hard": {"технология": "technology", "университет": "university", "информация": "information", "произношение": "pronunciation", "воображение": "imagination"}
}

print('Привет! Это игра для проверки твоих знаний по английскому языку. Программа покажет слово на русском, а ты должен будешь назвать это слово на английском.')
time.sleep(2)

# Выбор уровня сложности
level = input('Выбери словарь по уровню сложности - easy, medium, hard: ')
if level not in words_by_level:
    print('Нет такого уровня!')

word_dict = words_by_level[level]
score = 0
mistakes = 0

print(f'Вы выбрали уровень: {level}')

# Главный игровой цикл
while mistakes < 3:
    # Выбираем случайное слово
    russian_word, correct_translation = random.choice(list(word_dict.items()))
    print(f"\nСлово на русском: {russian_word}")
    print("Переведи на английский...")

    # Записываем голос
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()  # Ждём окончания записи
    wav.write("output.wav", sample_rate, recording)  # Сохраняем запись

    print("Запись завершена, теперь распознаём...")
    recognizer = sr.Recognizer()

    # Распознаём речь
    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)

    try:
        # Преобразуем речь в текст
        text = recognizer.recognize_google(audio, language="en-US")
        print(f"Ты сказал: {text}")

        # Сравниваем с правильным переводом
        if text.lower() == correct_translation:
            print("Правильный ответ!")
            score += 1
        else:
            print(f"Неправильный ответ! Правильный перевод: {correct_translation}")
            mistakes += 1

    except sr.UnknownValueError:
        print("Не удалось распознать речь.")
    except sr.RequestError as e:
        print(f"Ошибка сервиса: {e}")

    print(f"Текущий счёт: {score}")
    print(f"Ошибки: {mistakes}/3")

# Завершение игры
print("\nИгра окончена!")
print(f"Ваш итоговый счёт: {score}")

