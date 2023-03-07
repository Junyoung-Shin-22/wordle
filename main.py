from wordle import *
import sys

def _get_user_guess():
    while True:
        guess = input("your guess: ")

        if guess in WORDS:
            return guess
        
        print('invalid guess.')
        return None

def _get_user_result():
    while True:
        result = input("result: ")
        
        if result in RESULTS:
            return result
        
        print('invalid result.')
        return None

def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--hard':
        hard = True
    else:
        hard = False

    words = WORDS[:]
    round = 0
    history = []
    
    while True:
        round += 1
        if hard:
            print(f'[round {round} (hard)]')
        else:
            print(f'[round {round}]')

        history.append(len(words))
        
        if len(words) == 1:
            print('answer:', words[0])
            print('-'.join(map(str, history)))
            input('press enter to exit')
            return
        
        if round == 1: 
            print("(suggestion: 'serai' or 'lares')\n")
            
        else:
            print(f'there are {len(words)} possible answers.')
            if len(words) <= 10: 
                print('candidates are:', ', '.join(words))
        
            optimal_guess = get_optimal_guess(words, 'max', hard=hard, pbar=True)
            print(f"(suggestion: '{optimal_guess}')\n")
        
        guess = _get_user_guess()
        result = _get_user_result()
        print()

        words = get_possible_answers(words, guess, result)

if __name__ == '__main__':
    main()