#!/usr/bin/env python3

import csv
from collections import namedtuple

Word = namedtuple('Word', ['word', 'tag', 'lemma'])


def process_word(w, d):
    s = preprocess_str(w)
    if s in d:
        lemma, tag = d[s]
    else:
        lemma, tag = w, 'NI'
    return f'{w}{{{lemma}={tag}}}'


def preprocess_str(s: str):
    s = s.lower()
    s = s.replace('ё', 'е')
    return s


word_tag = {
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


def load_dictionary(filename):
    lemma_dict = dict()
    with open(filename, newline='', encoding='cp1251') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            for word in row[2:]:
                lemma_dict[preprocess_str(word)] = (preprocess_str(row[0]), word_tag[row[1]])
            lemma_dict[preprocess_str(row[0])] = (preprocess_str(row[0]), word_tag[row[1]])
    return lemma_dict


def main():
    lemma_dict = load_dictionary('data/odict.csv')
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
