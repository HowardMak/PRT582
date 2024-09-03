"""Using Python to design a game called ScrabbleScore"""

import random
import time
import threading
from nltk.corpus import words


class ScrabbleScore:
    """
    This is the class for ScrabbleScore
    """
    score_table: list
    word_list = set(words.words())

    def __init__(self) -> None:
        self.init_score_table()

    def init_score_table(self) -> None:
        """
        Initialisation
        """
        self.score_table = [1] * 26
        for letter in ['D', 'G']:
            self.score_table[ord(letter) - ord('A')] = 2
        for letter in ['B', 'C', 'M', 'P']:
            self.score_table[ord(letter) - ord('A')] = 3
        for letter in ['F', 'H', 'V', 'W', 'Y']:
            self.score_table[ord(letter) - ord('A')] = 4
        self.score_table[ord('K') - ord('A')] = 5
        for letter in ['J', 'X']:
            self.score_table[ord(letter) - ord('A')] = 8
        for letter in ['Q', 'Z']:
            self.score_table[ord(letter) - ord('A')] = 10

    def add_up(self, word: str) -> int:
        """
        Add up letter scores and return score

        Args:
            word (str): word

        Returns:
            int: score
        """
        final_score = 0
        for letter in word:
            final_score += self.get_value(letter)

        return final_score

    def get_value(self, letter: chr) -> int:
        """
        Get the value of the letter

        Args:
            letter (chr): letter

        Returns:
            int: value
        """
        if "A" <= letter <= "Z":
            return self.score_table[ord(letter) - ord('A')]
        if "a" <= letter <= "z":
            return self.score_table[ord(letter) - ord('a')]
        return 0

    def validate_input(self, user_input: str):
        """
        determine whether the input is valid

        Args:
            user_input (str): user input

        Raises:
            Exception: raised when there is no alphabet

        Returns:
            int: the number of letters
        """
        letter_cnt = 0
        for letter in user_input:
            if ("A" <= letter <= "Z") or ("a" <= letter <= "z"):
                letter_cnt += 1
        if letter_cnt == 0:
            raise RuntimeError("You did not enter any alphabet!")

        return letter_cnt

    def validate_word(self, word: str):
        """
        determine whether the word is in the dictionary

        Args:
            word (str): word

        Returns:
            bool: whether the word is in the dictionary
        """
        return word.lower() in self.word_list

    def countdown(self, seconds: int, stop_event: threading.Event):
        """
        A timer thread

        Args:
            seconds (int): limited seconds
            stop_event (threading.Event): event object
        """
        while seconds and not stop_event.is_set():
            mins, secs = divmod(seconds, 60)
            timer = f'{str(mins).zfill(2)}:{str(secs).zfill(2)}'
            print(timer, end="\r")
            time.sleep(1)
            seconds -= 1

        if not stop_event.is_set():
            print("\n Time's up!")

    def get_user_input(self, stop_event: threading.Event):
        """
        Get user input and check return score

        Args:
            stop_event (threading.Event): event object

        Returns:
            [int, bool]: score, is valid
        """
        required_letter_cnt = random.randint(0, 10)
        is_valid = True
        try:
            user_input = input(
                "Please input a word with "
                f"{required_letter_cnt} "
                "words in 15 seconds:\n"
            )
            stop_event.set()
            if self.validate_input(user_input) != required_letter_cnt:
                raise RuntimeError(
                    "You did not enter as required, you get 0 points!"
                    )
            if not self.validate_word(user_input):
                raise RuntimeError(
                    "The word is not a valid word from the dictionary"
                    )
            return [self.add_up(user_input), is_valid]
        except RuntimeError as err:
            print(err)
            is_valid = False
            return [0, is_valid]

    def play_for_one_round(self):
        """
        get score and used time in one round

        Returns:
            [int, int]: score and used time
        """
        stop_event = threading.Event()
        timer_thread = threading.Thread(
            target=self.countdown,
            args=(15, stop_event)
        )
        timer_thread.start()
        begin_time = time.time()
        score, is_valid = self.get_user_input(stop_event)
        used_time = time.time() - begin_time
        timer_thread.join()

        print(f"You got: {score} scores, used: {used_time: .02f}s")
        return [score, min(15.0, used_time) if is_valid else 15]

    def play(self):
        """
        main program
        """
        rounds = 1
        tot_score, tot_time = 0, 0
        while rounds <= 10:
            user_option = input(
                f"Round: {rounds}\n"
                "Please select: \n1.Play;\n2.Exit.\n"
                "Select: "
            )
            if int(user_option) == 1:
                try:
                    curr_score, curr_time = self.play_for_one_round()
                    tot_score += curr_score
                    tot_time += curr_time
                    rounds += 1
                except RuntimeError as runtime_error:
                    print(runtime_error)
                    continue
            elif int(user_option) == 2:
                print("Exited")
                break
            else:
                print("Incorrect input! Please re-enter!")
                time.sleep(1)
                continue
            print("=" * 40)

        print(
            f"Your totol score is {tot_score},"
            f"total used time is {tot_time}s"
        )
