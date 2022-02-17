import string
import numpy as np
import pickle
from itertools import product
from tqdm import tqdm

with open('data/l5w.txt') as f:
    all_words = f.read().splitlines()

with open('data/hint2words.bin', 'rb') as f:
    hint2words = pickle.load(f)

with open('data/word2hints.bin', 'rb') as f:
    word2hints = pickle.load(f)
    
all_results = [''.join(r) for r in product('012', repeat=5)]
result_pairs = {}

def get_result(answer, guess):
    if (answer, guess) in result_pairs:
        return result_pairs[(answer, guess)]
    
    result = ''

    for i in range(5):
        if guess[i] == answer[i]:
            result += '1'
        elif guess[i] in answer:
            result += '2'
        else:
            result += '0'
    
    result_pairs[(answer, guess)] = result
    return result

def get_hints(guess, result):
    hints = set()
    
    for i in range(5):
        if result[i] == '1': hints.add(guess[i]+str(i+1)) #green
        elif result[i] == '0': hints.add(guess[i]+'0') #gray
        elif result[i] == '2': hints.add(guess[i]+str(-i-1)) #yellow
    
    return hints

'''
def get_possible_words(words, hints):
    possible_words = set(words)
    
    for hint in hints:
        possible_words &= hint2words[hint]
    
    return possible_words
'''

def get_possible_words(words, hints):
    h = set(hints)
    
    possible_words = set(word for word in words if h <= set(word2hints[word]))
    
    return possible_words

def get_num_of_possible_words(words, hints):
    pw = get_possible_words(words, hints)
    
    return len(pw)

def get_possible_words_with_result(words, guess, result):
    if result == '11111': return {guess, }
    
    hints = get_hints(guess, result)
    pw = get_possible_words(words, hints)
    
    return pw

def get_possible_words_after_guess(words, answer, guess):
    if answer==guess: return {answer, }
    
    result = get_result(answer, guess)
    hints = get_hints(guess, result)
    pw = get_possible_words(words, hints)
    
    return pw

def get_optimal_guess(words, metric='max', pbar=False):
    assert metric in ['mean', 'max', 'var']
    if len(words)==1: list(words)[0]
    
    optimal_guess = ''
    
    min_m = 1000000
    
    if pbar:
        all_guesses = tqdm(all_words, desc='searching for optimal guess', leave=False)
    else:
        all_guesses = all_words
    
    for guess in all_guesses:
        results_freq = {r:0 for r in all_results}
        
        for possible_answer in words:
            result = get_result(possible_answer, guess)
            results_freq[result] += 1

        freq = results_freq.values()
        
        if metric == 'max':
            m = max(freq)
        
        elif metric == 'mean':
            m = sum(i**2 for i in freq)/len(words)
        
        else:
            m = sum(i**3-i**2 for i in freq)/len(words)
        
        if m < min_m:
            min_m = m
            optimal_guess = guess
    
    return optimal_guess

def get_user_guess():
    while True:
        guess = input("your guess (type in 'exit' to exit): ")

        if guess == 'exit': 
            exit()

        elif guess in all_words:
            return guess
        
        print('invalid guess.')

def get_user_result():
    while True:
        result = input("result (type in 'exit' to exit): ")
        
        if result == 'exit':
            exit()
        
        elif result in all_results:
            return result
        
        print('invalid result.')

def play():
    pw = all_words
    i = 0
    
    while True:
        i += 1
        print('[round %d]' % i)
        
        if len(pw) == 1:
            print('answer:', pw[0])
            return
        
        if i == 1: 
            print("(suggestion: 'serai' or 'lares')\n")
            
        else:
            print('there are %d possible answers.' % len(pw))
        
            optimal_guess = get_optimal_guess(pw, 'max')
            print("(suggestion: '%s')\n" % optimal_guess)
        
        guess = get_user_guess()
        result = get_user_result()
        
        hints = get_hints(guess, result)
        pw = list(get_possible_words(pw, hints))
        
        print()


if __name__ == '__main__':
    play()