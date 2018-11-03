import re
from bs4 import BeautifulSoup

class Denoise:
    def stripHtml(self, text):
        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text()

    def removeUnwantedCharacters(self, text):
        text = re.sub(r'https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
        text = re.sub(r'\<a href', ' ', text)
        text = re.sub(r'&amp;', '', text)
        text = re.sub(r'[_"\;%()|+&=*%:#$@\[\]/]', ' ', text)
        text = re.sub(r'<br />', ' ', text)
        text = re.sub(r'\'', ' ', text)
        text = re.sub(r'[^\x00-\x7F]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'e.g.,', '', text)
        return text

    def denoiseText(self, text):
        text = self.stripHtml(text)
        text = self.removeUnwantedCharacters(text)
        return text
