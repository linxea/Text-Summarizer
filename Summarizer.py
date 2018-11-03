
from nltk.probability import FreqDist
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from Denoise import Denoise
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
        # Calculate the frequency of each word in the input
        tokenizer = RegexpTokenizer('\w+')
        baseWords = [word.lower() for word in tokenizer.tokenize(input)]
        baseWordsWithoutStopWords = [word for word in baseWords if word not in stopwords.words()]
        wordFrequencies = FreqDist(baseWordsWithoutStopWords)
        mostFrequentWords = [pair[0] for pair in wordFrequencies.keys()]

        # Split input into sentences.  working_sentences is used
        # for the analysis, but actual_sentences is used in the results
        # so capitalization will be correct.
        sentDetector = nltk.data.load('tokenizers/punkt/english.pickle')
        sentencesRaw = sentDetector.tokenize(input)
        sentencesToBeAnalyzed = [sentence.lower() for sentence in sentencesRaw]

        # Iterate over the most frequent words, and add the first sentence
        # that inclues each word to the result.
        outputSentences = []

        for word in mostFrequentWords:
            for i in range(len(sentencesToBeAnalyzed)):
                if (word in sentencesToBeAnalyzed[i]
                        and sentencesRaw[i] not in outputSentences):
                    outputSentences.append(sentencesRaw[i])
                    break
                if len(outputSentences) >= num_sentences:
                    break
            if len(outputSentences) >= num_sentences:
                break

        # sort the output sentences back to their original order
        return self.reorderSentences(outputSentences, input)

    def processText(self, input, numberOfSentences):
        return " ".join(self.getSummarizedText(input, numberOfSentences))

# Take in filename as argument
args = sys.argv
filename = args[1]
file = codecs.open(filename, encoding='utf-8')
articleText = file.read()

# Clean article content
summarize = Summarizer()
denoise = Denoise()
cleanedText = denoise.denoiseText(articleText)

# Summarize cleaned article
numberOfSentences = 3
summary = summarize.processText(cleanedText, numberOfSentences)

# Print summary in console
print (summary)
