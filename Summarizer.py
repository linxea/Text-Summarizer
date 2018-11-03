
from nltk.probability import FreqDist
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import nltk.data
import codecs
import sys
import re

class Summarizer:
    # TODO: Change to Python 3 syntax
    def reorderSentences(self, sentences, input):
        # sentences.sort(key=lambda s1, s2:
        #                       input.find(s1) - input.find(s2))
        return sentences

    def getSummarizedText(self, input, num_sentences):
        tokenizer = RegexpTokenizer('\w+')

        # get the frequency of each word in the input
        base_words = [word.lower()
                      for word in tokenizer.tokenize(input)]
        words = [word for word in base_words if word not in stopwords.words()]
        word_frequencies = FreqDist(words)

        # now create a set of the most frequent words
        most_frequent_words = [pair[0] for pair in
                               word_frequencies.keys()]

        # break the input up into sentences.  working_sentences is used
        # for the analysis, but actual_sentences is used in the results
        # so capitalization will be correct.
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        actual_sentences = sent_detector.tokenize(input)
        working_sentences = [sentence.lower()
                             for sentence in actual_sentences]

        # iterate over the most frequent words, and add the first sentence
        # that inclues each word to the result.
        output_sentences = []

        for word in most_frequent_words:
            for i in range(0, len(working_sentences)):
                if (word in working_sentences[i]
                        and actual_sentences[i] not in output_sentences):
                    output_sentences.append(actual_sentences[i])
                    break
                if len(output_sentences) >= num_sentences:
                    break
            if len(output_sentences) >= num_sentences:
                break

        # sort the output sentences back to their original order
        return self.reorderSentences(output_sentences, input)

    def processText(self, input, numberOfSentences):
        return " ".join(self.getSummarizedText(input, numberOfSentences))

    def cleanArticleText(self,text):
        # Remove unwanted characters
        text = re.sub(r'https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
        text = re.sub(r'\<a href', ' ', text)
        text = re.sub(r'&amp;', '', text)
        # text = re.sub(r'[_"\-;%()|+&=*%.,!?:#$@\[\]/]', ' ', text)
        text = re.sub(r'[_"\-;%()|+&=*%:#$@\[\]/]', ' ', text)
        text = re.sub(r'<br />', ' ', text)
        text = re.sub(r'\'', ' ', text)
        text = re.sub(r'[^\x00-\x7F]', ' ', text)
        # Remove unwanted spacings
        text = re.sub(r'\s+', ' ', text)
        return text


# Take in filename as argument
args = sys.argv
filename = args[1]
file = codecs.open(filename, encoding='utf-8')
articleText = file.read()

# Clean article content
summarize = Summarizer()
cleanedText = summarize.cleanArticleText(articleText)

numberOfSentences = 1
summary = summarize.processText(cleanedText, numberOfSentences)

print (summary)
