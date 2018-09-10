# -*- coding: utf-8 -*-
"""
Created on Sat Sep  10 19:44:28 2018

@author: Arlind Original solution
"""
import re
from collections import Counter
def words(text): return re.findall(r'\w+', text.lower())
"creates a dictionary using as keys the words of the given text and as value the count of the word in the given document"
WORDS = Counter(words(open('big.txt').read()))
"""starting from a dictionary generates a new dictionary where each key of the old dictionary
is one delete away from a key of the new dictionary. The new dictionary as value has the original value in the 
old dictionary Ex. old thre:three new thr:thre, the:thre ..."""            
def add1distancetodictionary(originaldict):
    dicttoreturn=dict()
    for y in originaldict:
        splits     = [(y[:i], y[i:])    for i in range(len(y) + 1)]
        deletes    = [L + R[1:]               for L, R in splits if R]
        for j in deletes:
            if j in dicttoreturn:
                " if the key already exists in the dictionary adds the new string to the existing set"
                dicttoreturn[j].add(y)
            else:
                "creates a new set with just the initial word as key"
                dicttoreturn[j] = {y}
    return dicttoreturn
"""creating a new dictionary having as value the keys of the dictionary words and as keys the keys of 
dictionary WORDS after deleting one char"""
DeletedWords1=add1distancetodictionary(WORDS)
DeletedWords2=add1distancetodictionary(DeletedWords1)

N=sum(WORDS.values())
def P(word): 
    "Probability of `word`."
    return WORDS[word] / N

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or knowndis1([word]) or known(edits1(word)) or knowndis1(edits1(word)) or knowndis2([word]) or knowndis1(edits2(word)) or(knowndis2(edits1(word))) or (knowndis2(edits2(word))) or [word])


def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)
def knowndis1(words): 
    "The subset of `words` that appear in the dictionary of DeletedWords1." 
    return  set(y for w in words if w in DeletedWords1 for y in DeletedWords1[w])
def knowndis2(words):
    "The subset of `words` that appear in the dictionary of DeletedWords2." 
    return  set(z for w in words if w in DeletedWords2 for y in DeletedWords2[w] for z in DeletedWords1[y])

def edits1(word):
    "All edits that are one edit away from `word`."
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    return set(deletes)

def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))



def unit_tests():
    assert correction('speling') == 'spelling'              # insert
    assert correction('korrectud') == 'corrected'           # replace 2
    assert correction('bycycle') == 'bicycle'               # replace
    assert correction('inconvient') == 'inconvenient'       # insert 2
    assert correction('arrainged') == 'arranged'            # delete
    assert correction('peotry') =='poetry'                  # transpose
    assert correction('peotryy') =='poetry'                 # transpose + delete
    assert correction('word') == 'word'                     # known
    assert correction('quintessential') == 'quintessential' # unknown
    assert words('This is a TEST.') == ['this', 'is', 'a', 'test']
    assert Counter(words('This is a test. 123; A TEST this is.')) == (
           Counter({'123': 1, 'a': 2, 'is': 2, 'test': 2, 'this': 2}))
    assert len(WORDS) == 32198
    assert sum(WORDS.values()) == 1115585
    assert WORDS.most_common(10) == [
     ('the', 79809),
     ('of', 40024),
     ('and', 38312),
     ('to', 28765),
     ('in', 22023),
     ('a', 21124),
     ('that', 12512),
     ('he', 12401),
     ('was', 11410),
     ('it', 10681)]
    assert WORDS['the'] == 79809
    assert P('quintessential') == 0
    assert 0.07 < P('the') < 0.08
    return 'unit_tests pass'

def spelltest(tests, verbose=False):
    "Run correction(wrong) on all (right, wrong) pairs; report results."
    import time
    start = time.clock()
    good, unknown = 0, 0
    n = len(tests)
    for right, wrong in tests:
        w = correction(wrong)
        good += (w == right)
        if w != right:
            unknown += (right not in WORDS)
            if verbose:
                print('correction({}) => {} ({}); expected {} ({})'
                      .format(wrong, w, WORDS[w], right, WORDS[right]))
    dt = time.clock() - start
    print('{:.0%} of {} correct ({:.0%} unknown) at {:.0f} words per second '
          .format(good / n, n, unknown / n, n / dt))
    
def Testset(lines):
    "Parse 'right: wrong1 wrong2' lines into [('right', 'wrong1'), ('right', 'wrong2')] pairs."
    return [(right, wrong)
            for (right, wrongs) in (line.split(':') for line in lines)
            for wrong in wrongs.split()]

print(unit_tests())
spelltest(Testset(open('spell-testset1.txt'))) # Development set
spelltest(Testset(open('spell-testset2.txt')))