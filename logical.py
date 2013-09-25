__author__ = 'nchugueva'

import re
from random import uniform
from collections import defaultdict

r_alphabet = re.compile(u'[A-Za-zа-яА-Я-]{2,}|[.,:;?!]+')

def gen_lines(corpus):
    data = open(corpus) #, encoding="utf-8"
    for line in data:
        yield line.lower()

def gen_tokens(lines):
    for line in lines:
        for token in r_alphabet.findall(line):
            yield token

def gen_trigrams(tokens):
    for word in tokens:
        word = "$$" + word + "$$"
        for i in range(0, len(word) - 2):
            yield tuple(word[i:i+3])

def train(corpus):
    lines = gen_lines(corpus)
    tokens = gen_tokens(lines)
    trigrams = gen_trigrams(tokens)

    bi, tri = defaultdict(lambda: 0.0), defaultdict(lambda: 0.0)

    for t0, t1, t2 in trigrams:
        bi[t0, t1] += 1
        tri[t0, t1, t2] += 1

    model = {}
    for (t0, t1, t2), freq in tri.items():
        p = (t2, freq/bi[t0, t1])
        if (t0, t1) in model:
            model[t0, t1].append(p)
        else:
            model[t0, t1] = [p]
        # print("Append:", t0, t1, p)
    return model

def generate_name(model):
    name = ''
    t0, t1 = '$', '$'
    while 1:
        t0, t1 = t1, unirand(model[t0, t1])
        if t1 == '$': break
        if t1 in ('.!?,;:') or t0 == '$':
            name += t1
        else:
            name += ' ' + t1
        # print("Name:", name)
    return name.capitalize()

def unirand(seq):
    sum_, freq_ = 0, 0
    for item, freq in seq:
        sum_ += freq
    rnd = uniform(0, sum_)
    for token, freq in seq:
        freq_ += freq
        if rnd < freq_:
            return token

if __name__ == '__main__':
    model = train('words.txt')
    names = set(generate_name(model).replace(' ', '') for i in range(1000))
    #open("names.txt", "wt", encoding="utf-8").write("\n".join(sorted(names)))
    print("\n".join(sorted(names)))
    for i in range(1):
        print(generate_name(model))

# lines = gen_lines('words.txt')
# tokens = gen_tokens(lines)
# trigrams = gen_trigrams(tokens)