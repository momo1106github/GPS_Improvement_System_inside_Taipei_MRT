import speech_recognition as sr

r = sr.Recognizer()
mic = sr.Microphone()

while 1:
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            print(r.recognize_google(audio, language='zh-TW'))
        except print("Cannot recognize"):
            pass