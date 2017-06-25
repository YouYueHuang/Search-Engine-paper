# Boring preliminaries
%pylab inline
import re
import math
import string
from collections import Counter
from __future__ import division

TEXT = file('big.txt').read()
len(TEXT)

def tokens(text):
    "List all the word tokens (consecutive letters) in a text. Normalize to lowercase."
    return re.findall('[a-z]+', text.lower()) 

tokens('This is: A test, 1, 2, 3, this is.')

WORDS = tokens(BIG)
len(WORDS)

print(WORDS[:10])

def sample(bag, n=10):
    "Sample a random n-word sentence from the model described by the bag of words."
    return ' '.join(random.choice(bag) for _ in range(n))

sample(WORDS)

Counter(tokens('Is this a test? It is a test!'))

COUNTS = Counter(WORDS)

print COUNTS.most_common(10)

for w in tokens('the rare and neverbeforeseen words'):
    print COUNTS[w], w

M = COUNTS['the']
yscale('log'); xscale('log'); title('Frequency of n-th most frequent word and 1/n line.')
plot([c for (w, c) in COUNTS.most_common()])
plot([M/i for i in range(1, len(COUNTS)+1)]);

def correct(word):
    "Find the best spelling correction for this word."
    # Prefer edit distance 0, then 1, then 2; otherwise default to word itself.
    candidates = (known(edits0(word)) or 
                  known(edits1(word)) or 
                  known(edits2(word)) or 
                  [word])
    return max(candidates, key=COUNTS.get)

def known(words):
    "Return the subset of words that are actually in the dictionary."
    return {w for w in words if w in COUNTS}

def edits0(word): 
    "Return all strings that are zero edits away from word (i.e., just word itself)."
    return {word}

def edits2(word):
    "Return all strings that are two edits away from this word."
    return {e2 for e1 in edits1(word) for e2 in edits1(e1)}

def edits1(word):
    "Return all strings that are one edit away from this word."
    pairs      = splits(word)
    deletes    = [a+b[1:]           for (a, b) in pairs if b]
    transposes = [a+b[1]+b[0]+b[2:] for (a, b) in pairs if len(b) > 1]
    replaces   = [a+c+b[1:]         for (a, b) in pairs for c in alphabet if b]
    inserts    = [a+c+b             for (a, b) in pairs for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

def splits(word):
    "Return a list of all possible (first, rest) pairs that comprise word."
    return [(word[:i], word[i:]) 
            for i in range(len(word)+1)]

alphabet = 'abcdefghijklmnopqrstuvwxyz'

splits('wird')

print edits0('wird')

print edits1('wird')

print len(edits2('wird'))

map(correct, tokens('Speling errurs in somethink. Whutever; unusuel misteakes everyware?'))

def correct_text(text):
    "Correct all the words within a text, returning the corrected text."
    return re.sub('[a-zA-Z]+', correct_match, text)

def correct_match(match):
    "Spell-correct word in match, and preserve proper upper/lower/title case."
    word = match.group()
    return case_of(word)(correct(word.lower()))

def case_of(text):
    "Return the case-function appropriate for text: upper, lower, title, or just str."
    return (str.upper if text.isupper() else
            str.lower if text.islower() else
            str.title if text.istitle() else
            str)

map(case_of, ['UPPER', 'lower', 'Title', 'CamelCase'])

correct_text('Speling Errurs IN somethink. Whutever; unusuel misteakes?')

correct_text('Audiance sayzs: tumblr ...')

def pdist(counter):
    "Make a probability distribution, given evidence from a Counter."
    N = sum(counter.values())
    return lambda x: counter[x]/N

P = pdist(COUNTS)

for w in tokens('"The" is most common word in English'):
    print P(w), w

def Pwords(words):
    "Probability of words, assuming each word is independent of others."
    return product(Pword(w) for w in words)

def product(nums):
    "Multiply the numbers together.  (Like `sum`, but with multiplication.)"
    result = 1
    for x in nums:
        result *= x
    return result

tests = ['this is a test', 
         'this is a unusual test',
         'this is a neverbeforeseen test']

for test in tests:
    print Pwords(tokens(test)), test

def memo(f):
    "Memoize function f, whose args must all be hashable."
    cache = {}
    def fmemo(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]
    fmemo.cache = cache
    return fmemo

max(len(w) for w in COUNTS)

def splits(text, start=0, L=20):
    "Return a list of all (first, rest) pairs; start <= len(first) <= L."
    return [(text[:i], text[i:]) 
            for i in range(start, min(len(text), L)+1)]

print splits('word')
print splits('reallylongtext', 1, 4)

@memo
def segment(text):
    "Return a list of words that is the most probable segmentation of text."
    if not text: 
        return []
    else:
        candidates = ([first] + segment(rest) 
                      for (first, rest) in splits(text, 1))
        return max(candidates, key=Pwords)

segment('choosespain')

segment('speedofart')

decl = ('wheninthecourseofhumaneventsitbecomesnecessaryforonepeople' +
        'todissolvethepoliticalbandswhichhaveconnectedthemwithanother' +
        'andtoassumeamongthepowersoftheearththeseparateandequalstation' +
        'towhichthelawsofnatureandofnaturesgodentitlethem')

print(segment(decl))

Pwords(segment(decl))

Pwords(segment(decl * 2))

Pwords(segment(decl * 3))

segment('smallandinsignificant')

segment('largeandinsignificant')

print(Pwords(['large', 'and', 'insignificant']))
print(Pwords(['large', 'and', 'in', 'significant']))

def load_counts(filename, sep='\t'):
    """Return a Counter initialized from key-value pairs, 
    one on each line of filename."""
    C = Counter()
    for line in open(filename):
        key, count = line.split(sep)
        C[key] = int(count)
    return C

COUNTS1 = load_counts('count_1w.txt')
COUNTS2 = load_counts('count_2w.txt')

P1w = pdist(COUNTS1)
P2w = pdist(COUNTS2)

print len(COUNTS1), sum(COUNTS1.values())/1e9
print len(COUNTS2), sum(COUNTS2.values())/1e9

COUNTS2.most_common(30)

def Pwords2(words, prev='<S>'):
    "The probability of a sequence of words, using bigram data, given prev word."
    return product(cPword(w, (prev if (i == 0) else words[i-1]) )
                   for (i, w) in enumerate(words))

# Change Pwords to use P1w (the bigger dictionary) instead of Pword
def Pwords(words):
    "Probability of words, assuming each word is independent of others."
    return product(P1w(w) for w in words)

def cPword(word, prev):
    "Conditional probability of word, given previous word."
    bigram = prev + ' ' + word
    if P2w(bigram) > 0 and P1w(prev) > 0:
        return P2w(bigram) / P1w(prev)
    else: # Average the back-off value and zero.
        return P1w(word) / 2

print Pwords(tokens('this is a test'))
print Pwords2(tokens('this is a test'))
print Pwords2(tokens('is test a this'))

@memo 
def segment2(text, prev='<S>'): 
    "Return best segmentation of text; use bigram data." 
    if not text: 
        return []
    else:
        candidates = ([first] + segment2(rest, first) 
                      for (first, rest) in splits(text, 1))
        return max(candidates, key=lambda words: Pwords2(words, prev))

print segment2('choosespain')
print segment2('speedofart')
print segment2('smallandinsignificant')
print segment2('largeandinsignificant')

adams = ('faroutintheunchartedbackwatersoftheunfashionableendofthewesternspiral' +
         'armofthegalaxyliesasmallunregardedyellowsun')
print segment(adams)
print segment2(adams)

P1w('unregarded')

tolkein = 'adrybaresandyholewithnothinginittositdownonortoeat'
print segment(tolkein)
print segment2(tolkein)

def test_segmenter(segmenter, tests):
    "Try segmenter on tests; report failures; return fraction correct."
    return sum([test_one_segment(segmenter, test) 
               for test in tests]), len(tests)

def test_one_segment(segmenter, test):
    words = tokens(test)
    result = segmenter(cat(words))
    correct = (result == words)
    if not correct:
        print 'expected', words
        print 'got     ', result
    return correct

proverbs = ("""A little knowledge is a dangerous thing
  A man who is his own lawyer has a fool for his client
  All work and no play makes Jack a dull boy
  Better to remain silent and be thought a fool that to speak and remove all doubt;
  Do unto others as you would have them do to you
  Early to bed and early to rise, makes a man healthy, wealthy and wise
  Fools rush in where angels fear to tread
  Genius is one percent inspiration, ninety-nine percent perspiration
  If you lie down with dogs, you will get up with fleas
  Lightning never strikes twice in the same place
  Power corrupts; absolute power corrupts absolutely
  Here today, gone tomorrow
  See no evil, hear no evil, speak no evil
  Sticks and stones may break my bones, but words will never hurt me
  Take care of the pence and the pounds will take care of themselves
  Take care of the sense and the sounds will take care of themselves
  The bigger they are, the harder they fall
  The grass is always greener on the other side of the fence
  The more things change, the more they stay the same
  Those who do not learn from history are doomed to repeat it"""
  .splitlines())

test_segmenter(segment, proverbs)

test_segmenter(segment2, proverbs)

tests = ['this is a test', 
         'this is a unusual test',
         'this is a nongovernmental test',
         'this is a neverbeforeseen test',
         'this is a zqbhjhsyefvvjqc test']

for test in tests:
    print Pwords(tokens(test)), test

def pdist_additive_smoothed(counter, c=1):
    """The probability of word, given evidence from the counter.
    Add c to the count for each item, plus the 'unknown' item."""
    N = sum(counter.values())          # Amount of evidence
    Nplus = N + c * (len(counter) + 1) # Evidence plus fake observations
    return lambda word: (counter[word] + c) / Nplus 

P1w = pdist_additive_smoothed(COUNTS1)

P1w('neverbeforeseen')

segment('thisisatestofsegmentationofalongsequenceofwords')

singletons = (w for w in COUNTS if COUNTS[w] == 1)

lengths = map(len, singletons)

Counter(lengths).most_common()

1357 / sum(COUNTS.values())

hist(lengths, bins=len(set(lengths)));

def pdist_good_turing_hack(counter, onecounter, base=1/26., prior=1e-8):
    """The probability of word, given evidence from the counter.
    For unknown words, look at the one-counts from onecounter, based on length.
    This gets ideas from Good-Turing, but doesn't implement all of it.
    prior is an additional factor to make unknowns less likely.
    base is how much we attenuate probability for each letter beyond longest."""
    N = sum(counter.values())
    N2 = sum(onecounter.values())
    lengths = map(len, [w for w in onecounter if onecounter[w] == 1])
    ones = Counter(lengths)
    longest = max(ones)
    return (lambda word: 
            counter[word] / N if (word in counter) 
            else prior * (ones[len(word)] / N2 or 
                          ones[longest] / N2 * base ** (len(word)-longest)))

# Redefine P1w
P1w = pdist_good_turing_hack(COUNTS1, COUNTS)

segment.cache.clear()
segment('thisisatestofsegmentationofaverylongsequenceofwords')

print P1w('francisco')
print P1w('individuals')

print [bigram for bigram in COUNTS2 if bigram.endswith('francisco')]

print [bigram for bigram in COUNTS2 if bigram.endswith('individuals')]

def rot(msg, n=13): 
    "Encode a message with a rotation (Caesar) cipher." 
    return encode(msg, alphabet[n:]+alphabet[:n])

def encode(msg, key): 
    "Encode a message with a substitution cipher." 
    table = string.maketrans(upperlower(alphabet), upperlower(key))
    return msg.translate(table) 

def upperlower(text): return text.upper() + text.lower()  

rot('This is a secret message.', 1)

rot('This is a secret message.')

rot(rot('This is a secret message.'))

def decode_rot(secret):
    "Decode a secret message that has been encoded with a rotation cipher."
    candidates = [rot(secret, i) for i in range(len(alphabet))]
    return max(candidates, key=lambda msg: Pwords(tokens(msg)))

msg = 'Who knows the answer?'
secret = rot(msg, 17)

print(secret)
print(decode_rot(secret))

def encode(msg, key): 
    "Encode a message with a substitution cipher; remove non-letters." 
    msg = cat(tokens(msg))  ## Change here
    table = string.maketrans(upperlower(alphabet), upperlower(key))
    return msg.translate(table) 

def decode_rot(secret):
    """Decode a secret message that has been encoded with a rotation cipher,
    and which has had all the non-letters squeezed out."""
    candidates = [segment(rot(secret, i)) for i in range(len(alphabet))]
    return max(candidates, key=lambda msg: Pwords(msg))

msg = 'Who knows the answer this time? Anyone? Bueller?'
secret = rot(msg, 19)

print(secret)
print(decode_rot(secret))

candidates = [segment(rot(secret, i)) for i in range(len(alphabet))]

for c in candidates:
    print c, Pwords(c)