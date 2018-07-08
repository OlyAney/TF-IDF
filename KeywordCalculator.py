import collections
import math
import re
import operator
from nltk.corpus import wordnet, stopwords
from nltk.stem import WordNetLemmatizer

PUNCTUATION_SYMBOLS = ' |!|@|#|\$|%|\^|&|\*|\(|\)|_|-|\+|=|\{|\[|]|}|`|~|;|:|"|/|>|\.|\?|<|,'

class KeywordsCalculator:
    def __init__(self, filename, corpus_filenames, k):
        self.k = k
        self.lemmatizer = WordNetLemmatizer()

        text = open(filename, 'r').read()
        corpus = []
        for f in corpus_filenames:
            corpus.append(open(f, 'r+').read())

        self.text = self.process(text)
        self.corpus = list(map(lambda t: self.process(t), corpus))

    def process(self, text):
        words = filter(None, re.split(PUNCTUATION_SYMBOLS, text))
        lemmatized_words = list(map(
            lambda word: self.lemmatizer
                .lemmatize(word, self.get_pos(word))
                .lower(),
            words
        ))

        lemmatized_words = [word for word in lemmatized_words if word != '\n']
        return lemmatized_words


    def get_pos(self, word):
        words_synonym_sets = wordnet.synsets(word)

        pos_counts = collections.Counter()
        for pos in ['n', 'v', 'a', 'r']:
            pos_counts[pos] = len([item for item in words_synonym_sets if item.pos() == pos])

        most_common_pos_list = pos_counts.most_common(3)
        return most_common_pos_list[0][0]

    def calculateTF(self):
        terms_frequencies = collections.Counter(self.text)
        for i in terms_frequencies:
            terms_frequencies[i] /= float(len(terms_frequencies))
        return dict(terms_frequencies)

    def calculateIDF(self, word):
        return math.log10(len(self.corpus) / (1 + sum([1.0 for text in self.corpus if word in text])))

    def getKeywords(self):
        weighted_words = collections.defaultdict(float)
        terms_frequencies = self.calculateTF()
        for word in terms_frequencies.keys():
            weighted_words[word] = round(self.calculateIDF(word) * terms_frequencies[word], 4)

        return sorted(weighted_words.items(), key=operator.itemgetter(1))[-self.k:]
