import random

class Hangman_game(object):
    def __init__(self, words_file):
        self.words_list = self.make_list(words_file)

    def make_list(self, file):
        with open(file, "r") as txt:
            full_list = txt.read().splitlines()
        return full_list
    
    def pick_word(self, words):
        return random.choice(words)
    
    def start_game(self):
        word = self.pick_word(self.words_list)
        length = len(word)
        letters = list(word)
        guessed_words = []
        lives = 6
        current_state = []

        current_state = ["_" for _ in word]
        print(letters)

        while lives > 0:
            if "".join(current_state) == "".join(word):
                print("You guessed the word correctly, You won")
                break

            print(current_state)
            guess = input("Guess a letter of the word: ")
            # implement the edge cases:
            # -> if no input: ask again
            # -> word length input restriction
            # -> input only a-z char
            if guess in guessed_words:
                print("letter already guessed, guess other letter")
            elif guess in word:
                for idx in range(length):
                    if guess == word[idx]:
                        current_state[idx] = guess
                guessed_words.append(guess)
            elif guess not in word:
                lives -= 1
                guessed_words.append(guess)
                print("wrong guess, lives left:", lives)

        if lives == 0:
            print("try again, you lost")
     
if __name__ == "__main__":
    game = Hangman_game("words_250000_train.txt")
    game.start_game()