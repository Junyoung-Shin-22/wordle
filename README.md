# wordle 1.0.0

`python wordle_play.py`

Or, to play in the hard mode:

`python wordle_play.py --hard`

(Solving Wordle in hard mode is usually faster, but less optimal.)

## 1. How To Use
1. For the first round, enter 'serai' or 'lares' into Wordle.
1. Enter the result from Wordle into the script as a five-digit number (Grey: 0, Green: 1, Yellow: 2)
1. Enter the suggested word into Wordle
1. Repeat 2 and 3 until you get the final answer.


## 2. Example
Wordle from Aug. 8, 2022.

![image](https://user-images.githubusercontent.com/35788350/183581651-87b4b01c-3732-4bab-9a7d-32d4bbc1fa4b.png)

```
$ python wordle_play.py
[round 1]
(suggestion: 'serai' or 'lares')

your guess (type in 'exit' to exit): serai
result (type in 'exit' to exit): 00002

[round 2]
there are 513 possible answers.
(suggestion: 'linty')                                                                                                                                                   

your guess (type in 'exit' to exit): linty
result (type in 'exit' to exit): 02220

[round 3]
there are 20 possible answers.
(suggestion: 'count')                                                                                                                                                   

your guess (type in 'exit' to exit): count
result (type in 'exit' to exit): 00221

[round 4]
there are 3 possible answers.
(suggestion: 'affix')                                                                                                                                                   

your guess (type in 'exit' to exit): affix
result (type in 'exit' to exit): 00110

[round 5]
answer: unfit
```
