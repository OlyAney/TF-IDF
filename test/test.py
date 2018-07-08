import os
import sys

sys.path.append('..')
from KeywordCalculator import *

keys_directory = os.getcwd() + '/keys'
documents_directory = os.getcwd() + '/documents/'

document_keywords = {}
document_keywords_calculated = {}

for filename in os.listdir(keys_directory):
    document_name = documents_directory + filename.strip('.key') + '.txt'
    corpus_document_names = list(map(lambda filename: documents_directory + filename, os.listdir(documents_directory)))

    calculator = KeywordsCalculator(document_name, corpus_document_names, 12)
    document_keywords_calculated[filename] = calculator.getKeywords()

    print(filename + ': ' + str(document_keywords_calculated[filename]))
    with open('output/' + filename, 'w+') as f:
        for keyword in document_keywords_calculated[filename]:
            f.write(keyword[0] + '\n')

    document_keywords[filename] = []
    for line in open('keys/' + filename, 'r'):
        document_keywords[filename].append(line.strip().lower())

