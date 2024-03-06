import bs4
class HTMLTranslator:
    def __init__(self, filename, from_lang, to_lang, translator):
        self.filename = filename
        self.from_lang = from_lang
        self.to_lang = to_lang
        self.translator = translator
        with open(self.filename, "r", encoding="utf-8") as file:
            self.html_content = file.read()
        soup = bs4.BeautifulSoup(self.html_content, 'html.parser')
        self.body_content = soup.body

    def iterate_and_translate_nodes(self, node):
        for i in node.children:
            if isinstance(i, bs4.element.NavigableString):
                if i.strip() != "":
                    if _is_valid_sentence(i):
                        i.replace_with(self.translator(i, self.from_lang, self.to_lang))
            else:
                self.iterate_and_translate_nodes(i)

    def translate_html(self):
        self.iterate_and_translate_nodes(self.body_content)
        new_soup = bs4.BeautifulSoup(str(self.body_content), 'html.parser')
        with open(f"{self.filename.rstrip(".html")}_translated.html", "w") as outfile:
            outfile.write(str(new_soup))


def _is_valid_sentence(sentence):
    sentence = str(sentence)
    sentence = sentence.replace(' ', '')
    if len(sentence.strip()) == 1:
        return False
    sentence = sentence.replace('-', '')
    sentence = sentence.replace('_', '')
    return sentence.isalpha() or sentence.isalnum()

if __name__ == "__main__":
    import translator
    HTMLTranslator("../index.html", "en", "hi", translator.translate).translate_html()