
from nltk.probability import FreqDist
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from Denoise import Denoise
import nltk.data
import codecs
import sys
import re
import time

class Summarizer:
    def reorderSentences(self, sentences, originalSentences):
        sentences.sort(key=lambda s1: originalSentences.find(s1))
        return sentences

    def getSummarizedText(self, input, numberOfSentences):

        unwantedSentence = ['Chapter']

        # Calculate the frequency of each word in the input
        tokenizer = RegexpTokenizer('\w+')
        baseWords = [word.lower() for word in tokenizer.tokenize(input)]
        baseWordsWithoutStopWords = [word for word in baseWords if word not in stopwords.words() and unwantedSentence]
        # Frequency Distribution
        wordFrequencies = FreqDist(baseWordsWithoutStopWords)
        mostFrequentWords = [pair[0] for pair in wordFrequencies.keys()]

        # Split input into sentences in lowercase to be analysed by tokenizers/punkt
        sentDetector = nltk.data.load('tokenizers/punkt/english.pickle')
        sentencesRaw = sentDetector.tokenize(input)
        sentencesToBeAnalyzed = [sentence.lower() for sentence in sentencesRaw]

        # For each of most frequent words, and add the first sentence
        # that inclues each word to the output result.
        outputSentences = []

        for word in mostFrequentWords:
            for i in range(len(sentencesToBeAnalyzed)):
                # Only keep sentence that has appear frequently once
                if (word in sentencesToBeAnalyzed[i]
                        and sentencesRaw[i] not in outputSentences):
                    outputSentences.append(sentencesRaw[i])
                    break
                if len(outputSentences) >= numberOfSentences:
                    break
            if len(outputSentences) >= numberOfSentences:
                break

        # sort the output sentences back to their original order
        return self.reorderSentences(outputSentences, input)

    def processText(self, input, numberOfSentences):
        return " ".join(self.getSummarizedText(input, numberOfSentences))

# Take in filename as argument
startTime = time.time()
args = sys.argv
filename = args[1]
file = codecs.open(filename, encoding='utf-8')
articleText = file.read()

# Clean article content
summarize = Summarizer()
denoise = Denoise()
cleanedText = denoise.denoiseText(articleText)

# Summarize cleaned article into 2 sentences
numberOfSentences = 2
summary = summarize.processText(cleanedText, numberOfSentences)

# Print summary in console
print (summary)

countTime =  round(time.time() - startTime)
print ("Time taken:", str(countTime) + "s")