from itertools import product
from tqdm import tqdm

def _memo(func):
    memo = {}

    def _memo_inner(*args):
        if args in memo:
            return memo[args]
        
        res = func(*args)
        memo[args] = res
        return res
    
    return _memo_inner

with open('data/wordle_words.txt') as f:
    WORDS = f.read().splitlines()
    
RESULTS = [''.join(r) for r in product('012', repeat=5)]

@_memo
def get_result(answer, guess):
    result = ''

    for i in range(len(answer)):
        if guess[i] not in answer:
            result += '0'
        elif guess[i] == answer[i]:
            result += '1'
        else:
            if guess.count(guess[i]) > 1:
                result += '0'
            else:
                result += '2'
    
    return result

def get_possible_words(words, guess, result):
    return [word for word in words if get_result(word, guess) == result]

_METRICS =\
    {
        'max':
            lambda freq, _: max(freq),
        'mean':
            lambda freq, words: sum(i**2 for i in freq)/len(words),
    }

def get_optimal_guess(words, metric='max', hard=False ,pbar=False):
    assert metric in _METRICS
    
    if hard:
        guesses = words
    else:
        guesses = WORDS

    if pbar:
        guesses = tqdm(guesses, desc='searching for optimal guess', leave=False)

    optimal_guess = ''
    min_m = len(WORDS)
    
    for guess in guesses:
        results_freq = {r:0 for r in RESULTS}
        
        for possible_answer in words:
            result = get_result(possible_answer, guess)
            results_freq[result] += 1

        freq = results_freq.values()
        m = _METRICS[metric](freq, words)
        
        if m < min_m:
            min_m = m
            optimal_guess = guess
    
    return optimal_guess