import string
from tqdm import tqdm
import pickle

alpha = string.ascii_lowercase

with open('l5w.txt') as f:
    words = f.read().splitlines()

hint2words = {}
word2hints = {}

for a in alpha:
    for pos in range(-5, 6):
        hint2words[a+str(pos)] = set()

for word in words:
    word2hints[word] = []

for word in tqdm(words):
    for a in alpha:
        if a not in word: 
            hint2words[a+'0'].add(word)
            continue
        
        #if a is in the word
        for i in range(5):
            if word[i]==a: hint2words[a+str(i+1)].add(word)
            else: hint2words[a+str(-i-1)].add(word)

for hint in hint2words:
    for word in hint2words[hint]:
        word2hints[word].append(hint)
                
with open('hint2words.bin', 'wb') as f:
    pickle.dump(hint2words, f)
    
with open('word2hints.bin', 'wb') as f:
    pickle.dump(word2hints, f)