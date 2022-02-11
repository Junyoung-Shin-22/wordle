import string
import numpy as np
import pickle

with open('l5w.txt') as f:
    all_words = f.read().splitlines()

with open('hint2words.bin', 'rb') as f:
    hint2words = pickle.load(f)

with open('word2hints.bin', 'rb') as f:
    word2hints = pickle.load(f)

def get_result(answer, guess):
    result = ''

    for i in range(5):
        if guess[i] == answer[i]:
            result += '1'
        elif guess[i] in answer:
            result += '2'
        else:
            result += '0'

    return result

def get_hints(guess, result):
    hints = []
    
    for i in range(5):
        if result[i] == '1': hints.append(guess[i]+str(i+1)) #green
        elif result[i] == '0': hints.append(guess[i]+'0') #gray
        elif result[i] == '2': hints.append(guess[i]+str(-i-1)) #yellow
    
    return hints

def get_possible_words(words, hints):
    possible_words = set(words)
    
    for hint in hints:
        possible_words &= hint2words[hint]
    
    return possible_words

def test_guess(words, answer, guess):
    if answer==guess: return {answer, }
    
    result = get_result(answer, guess)
    hints = get_hints(guess, result)
    pws = get_possible_words(words, hints)
    
    return pws

def hint_frequency(words):
    hints = {hint:0 for hint in hint2words}
    
    for word in words:
        for hint in word2hints[word]: hints[hint] += 1
    
    return sorted(hints.items(), key=lambda x:x[1])

def get_optimal_guess(words):
    optimal_guess = list(words)[0]
    
    #min_max_group_size = len(words)
    min_avg_group_size = len(words)
    
    for guess in all_words:
        #max_group_size = 0
        avg_group_size = 0
        
        for possible_answer in words:
            pw = test_guess(words, possible_answer, guess)
            l = len(pw)
            avg_group_size += l/len(words)
            #if l > max_group_size: max_group_size = l

        '''if max_group_size < min_max_group_size:
            min_max_group_size = max_group_size
            optimal_guess = guess'''
        
        if avg_group_size < min_avg_group_size:
            min_avg_group_size = avg_group_size
            optimal_guess = guess
    
    return optimal_guess

def play():
    pw = all_words
    i = 0
    
    while True:
        i += 1
        print('[round %d]' % i)
        
        guess = input("your guess (type in 'exit' to exit): ")
        if guess == 'exit': 
            return False
        
        result = input('result: ')
        
        hints = get_hints(guess, result)
        pw = list(get_possible_words(pw, hints))
        
        if len(pw) == 1: 
            break
        if len(pw) == 0:
            print('something went wrong. restarting the game. \n')
            return False
        
        print('there are %d possible answers.' % len(pw))
        
        if len(pw) < 100:
            optimal_guess = get_optimal_guess(pw)
            print('try:', optimal_guess)
        
        print()
        #print(*sorted(pw), sep='\n')
   
    ans = list(pw)[0]
    print('answer:', ans)
    print()
    
    return True

if __name__ == '__main__':
    while play():
        pass