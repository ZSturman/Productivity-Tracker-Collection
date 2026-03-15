import speech_recognition as sr

def listen_and_transcribe():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak Anything :")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print("You said : {}".format(text))
        except:
            print("Sorry could not recognize your voice")

listen_and_transcribe()
