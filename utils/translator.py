from deep_translator import GoogleTranslator

def translate(text, from_lang, to_lang):
    return GoogleTranslator(source=from_lang if from_lang else "auto", target=to_lang).translate(text)

if __name__ == "__main__":
    sentence = "My name is Parampreet Singh. I am doing Bachelors of Science in Data Science and Applications from IIT Madras, India."
    print(translate(sentence, "en", "hi"))