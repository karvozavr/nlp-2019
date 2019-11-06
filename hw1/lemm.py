#!/usr/bin/env python3

import csv
import operator
import os
from collections import namedtuple
from collections import defaultdict
import xml.etree.ElementTree as ET
from tqdm import tqdm

Word = namedtuple('Word', ['word', 'tag', 'lemma'])


def process_word(w, d):
    s = preprocess_str(w)
    t = None
    if s in d:
        lemma, t = d[s]
    else:
        lemma = w

    if not frequencies[w]:
        tag = 'NI'
    else:
        tag = max(frequencies[w].items(), key=lambda x: x[1][1])[0]
        if tag != 'NI':
            lemma = frequencies[w][tag][0]

    if tag == 'NI' and t is not None:
        tag = t

    return f'{w}{{{lemma}={tag}}}'


def preprocess_str(s: str):
    s = s.lower()
    s = s.replace('ё', 'е')
    return s


word_tag = {
    'ADJF': 'A',
    'ADJS': 'A',
    'COMP': 'A',
    'NOUN': 'S',
    'VERB': 'V',
    'CONJ': 'CONJ',
    'PREP': 'PR',
    'ADVB': 'ADV',
    'INTJ': 'ADV',
    'PRED': 'ADV',
    'NPRO': 'ADV',
    'PRCL': 'ADV',
    'Prnt': 'ADV',
    'PNCT': 'NI',
    'INFN': 'V',
    'PRTF': 'V',
    'PRTS': 'V',
    'GRND': 'V',
    'UNKN': 'NI',
    'NUMR': 'NI',
    'NUMB': 'NI',
    'LATN': 'NI',
    'ROMN': 'NI',
    'SYMB': 'NI',
}

word_tag2 = {
    'п': 'A',
    'м': 'S',
    'ж': 'S',
    'с': 'S',
    'мо': 'S',
    'жо': 'S',
    'со': 'S',
    'мн.': 'S',
    'нсв': 'V',
    'св': 'V',
    'св-нсв': 'V',
    'союз': 'CONJ',
    'предл.': 'PR',
    'част.': 'ADV',
    'вводн.': 'ADV',
    'числ.-п': 'ADV',
    'числ.': 'ADV',
    'сравн.': 'ADV',
    'предик.': 'ADV',
    'мс-п': 'ADV',
    'мо-жо': 'ADV',
    'межд.': 'ADV',
    'н': 'ADV'
}

frequencies = defaultdict(dict)


def load_dictionary():
    lemma_dict = dict()

    corpora = os.listdir('data/opcorpora')

    for doc in corpora:
        filename = os.path.join('data/opcorpora', doc)

        tree = ET.parse(filename)
        docs = tree.findall('.//token')

        for token in docs:
            word = token.attrib['text']
            word = preprocess_str(word)

            lemma = token.find('tfr/v/l').attrib['t']
            lemma = preprocess_str(lemma)

            tag = token.find('tfr/v/l/g').attrib['v']
            tag = word_tag[tag]

            d = frequencies[word]

            if tag in d:
                d[tag] = (d[tag][0], d[tag][1] + 1)
            else:
                d[tag] = (lemma, 1)

            lemma_dict[word] = (lemma, tag)
            lemma_dict[lemma] = (lemma, tag)

    return lemma_dict


def load_odict(filename, lemma_dict):
    with open(filename, newline='', encoding='cp1251') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            for word in row[2:]:
                tag = word_tag2[row[1]]
                lemma_dict[preprocess_str(word)] = preprocess_str(row[0]), tag
            lemma_dict[preprocess_str(row[0])] = preprocess_str(row[0]), tag


def main():
    lemma_dict = load_dictionary()
    load_odict('data/odict.csv', lemma_dict)
    with open('input.txt') as f:
        for line in f.readlines():
            line = line.replace(',', '')
            line = line.replace('.', '')
            line = line.replace('!', '')
            line = line.replace('?', '')
            line = line.replace('\n', '')
            for w in line.split(' '):
                print(process_word(w, lemma_dict), end=' ')
            print()


if __name__ == '__main__':
    main()
