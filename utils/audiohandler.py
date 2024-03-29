import speech_recognition as sr
r = sr.Recognizer()

def transcribe_audio(filepath):
    with sr.AudioFile(filepath) as source:
        audio = r.record(source)
        try:
            text = r.recognize_google(audio)
            return text
        except Exception as e:
            return -1

if __name__ == "__main__":     
    print(transcribe_audio("../hindi.wav"))