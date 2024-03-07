import bs4
from string import punctuation
class HTMLTranslator:
    def __init__(self, filename, from_lang, to_lang, translator):
        self.filename = filename
        self.from_lang = from_lang
        self.to_lang = to_lang
        self.translator = translator
        with open(self.filename, "r", encoding="utf-8") as file:
            self.html_content = file.read()
        soup = bs4.BeautifulSoup(self.html_content, 'html.parser')
        self.head = soup.head
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
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        {self.head}
        </head>
        <body>
        {self.body_content}
        </html>
        """
        new_soup = bs4.BeautifulSoup(html, 'html.parser')
        output = f"{self.filename.rstrip('.html')}_translated.html"
        with open(output, "w", encoding="utf-8") as outfile:
            outfile.write(str(new_soup))
        
        return output


def _is_valid_sentence(sentence):
    sentence = str(sentence).strip()
    sentence = sentence.replace(' ', '')
    sentence = sentence.replace('\n', '')
    if len(sentence.strip()) == 1:
        return False
    for i in punctuation:
        sentence = sentence.replace(i, '')
    return sentence.isalpha() or sentence.isalnum()

if __name__ == "__main__":
    import translator
    HTMLTranslator("../index.html", "en", "hi", translator.translate).translate_html()