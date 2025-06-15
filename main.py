import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import random
import time

duration = 5  # секунды записи
sample_rate = 44100

words_by_level = {
    "easy": ["кот","собака", "яблоко", "молоко", "солнце", "машина"],
    "medium": ["банан", "школа", "друг", "окно", "жёлтый"],
    "hard": ["технология", "университет", "информация", "произношение", "воображение"]
}

print('Привет! это игра для проверки твоих знаний по английскому языку. Программа покажет слово на русском , а ты должен будешь назвать это слово на английском')
time.sleep(2)
level = input('Выбери словарь по уровню сложности - easy, medium, hard')
if level not in words_by_level:
    print('нету такого уровня')
word_dict = words_by_level[level]
score = 0
mistakes = 0
print('Вы выбрали уровень: {level}')

random.choice(words_by_level[level])

print("Переведи на английский...")
recording = sd.rec(
  int(duration * sample_rate), # длительность записи в сэмплах
  samplerate=sample_rate,      # частота дискретизации
  channels=1,                  # 1 — это моно
  dtype="int16")               # формат аудиоданных
sd.wait()  
wav.write("output.wav", sample_rate, recording)
print("Запись завершена, теперь распознаём...")
recognizer = sr.Recognizer()
with sr.AudioFile("output.wav") as source:
    audio = recognizer.record(source)

try:
    text = recognizer.recognize_google(audio, language="en-US")
    print("Ты сказал:", text)
    translator = Translator()
    translated = translator.translate(text, dest='ru') 


except sr.UnknownValueError:             # - если Google не понял речь (шум, молчание)
    print("Не удалось распознать речь.")
except sr.RequestError as e:             # - если нет интернета или API недоступен
    print(f"Ошибка сервиса: {e}")