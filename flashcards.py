#! python3
# flashcards.py - smart learning app using flashcards. Request a csv file with question-answer pairs

import sys
import os
import logging
import csv
from random import randint, shuffle
from math import ceil

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# flags
exit_flag = False


# class of Card object
class Card:
    def __init__(self, obverse='blank', reverse='blank', number=None):
        self.obverse = obverse
        self.reverse = reverse
        self.number = number
        self.correct = 0
        self.wrong = 0


# get filepath from system arguments
def get_flashcards_path():
    cards_file_path = sys.argv[1]
    if not os.path.exists(cards_file_path):
        logging.error(f"{cards_file_path} - file not found!")
        return False
    elif not os.path.basename(cards_file_path).endswith('.csv'):
        logging.error(f"{os.path.basename(cards_file_path)} is not a csv file!")
        return False
    else:
        logging.debug(f"Path is correct.")
        return cards_file_path


# read data from file
def read_flashcards_file(path):
    card_data = []
    with open(path, 'r') as file:
        csv_reader = csv.reader(file)
        for number, row in enumerate(csv_reader):
            obverse = row[0]
            reverse = row[1]
            card_data.append(Card(obverse, reverse, number))
    return card_data


# take answer from user
# return True if correct, False if incorrect
def ask_question(number, question, answer):
    global exit_flag

    user_answer = input(f"{number + 1}. {question}: ")

    if user_answer == 'EXIT':
        exit_flag = True
        logging.debug(f'users answer = EXIT, exit_flag = {exit_flag}')
        return False
    elif user_answer == answer:
        print('Correct!')
        return True
    else:
        print(f'Wrong! Correct answer is {answer}!')
        return False


# ask user a question
def examine_user(card, question_type=0, hint=False):
    global exit_flag

    if question_type == 0:
        question = card.obverse
        answer = card.reverse
    elif question_type == 1:
        question = card.reverse
        answer = card.obverse
    else:  # question_type == 2
        coin = randint(0, 1)
        examine_user(card, coin)

    result = ask_question(card.number, question, answer)

    # if exit flag is True, reset flag, return False
    if exit_flag:
        exit_flag = False
        return False
    else:
        if result:
            card.correct += 1
        else:
            card.wrong += 1

    return True


def play(deck):
    while True:
        game_mode = input('Choose game mode: learn/test. Type EXIT to quit')

        if game_mode == 'learn':
            learn_mode(deck)

        elif game_mode == 'EXIT':
            print('Farewell!')
            sys.exit()
        else:
            print(game_mode + ' is not a valid choice!')


# learn mode:
# groups cards into subdecks
# then loops subdeck until user won't guess all questions
# skips ones that user pass
# then takes next subdeck
def learn_mode(deck):
    print(f"Learn mode. Type in EXIT to quit.")

    subdeck_size = 5

    number_of_cards = len(deck)
    number_of_subdecks = ceil(number_of_cards / subdeck_size)
    last_subdeck_size = number_of_cards % subdeck_size

    question_counter = 0
    points = 0
    subdeck_num = 0

    while subdeck_num < number_of_subdecks:

        # pick the next subdeck, the last one might have less cards
        if subdeck_num == number_of_subdecks - 1 and last_subdeck_size:
            subdeck = deck[subdeck_num * subdeck_size:subdeck_num * subdeck_size + last_subdeck_size]
            logging.debug(
                f"subdeck {subdeck_num}/{number_of_subdecks}, cards {subdeck_num * subdeck_size}:{subdeck_num * subdeck_size + last_subdeck_size}, last")
        else:
            subdeck = deck[subdeck_num * subdeck_size:subdeck_num * subdeck_size + subdeck_size]
            logging.debug(f"subdeck:{[r.reverse for r in subdeck]}")
            logging.debug(
                f"subdeck {subdeck_num}/{number_of_subdecks}, cards {subdeck_num * subdeck_size}:{(subdeck_num + 1) * subdeck_size}")

        # loop until not all questions in subdeck quessed correctly
        while not all_cards_correct(subdeck):
            for card in subdeck:
                if card.correct < 1:
                    # if examine_user returns false, finish game
                    if not examine_user(card):
                        summarize(deck)
                        return False

        subdeck_num += 1

    summarize(deck)
    return True


# show stats of the game
def summarize(deck):
    corrects = 0
    wrongs = 0

    for card in deck:
        corrects += card.correct
        wrongs += card.wrong

    if corrects+wrongs==0:
        print("Game finished!")
    else:
        percentage = int(corrects / (corrects + wrongs) * 100)
        print("Game finished!")
        print(f"Your score is {corrects}/{wrongs + corrects} ({percentage}%)")


# checks if every card has at least one correct point
def all_cards_correct(deck):
    for card in deck:
        if card.correct == 0:
            return False
    return True


# todo reset deck scores after game
# todo smart learn?
# todo test mode
# todo save/read scores
# todo handle typos

def game():
    path = get_flashcards_path()
    if not path:
        sys.exit()
    flashcards_data = read_flashcards_file(path)
    learn_mode(flashcards_data)


flashcards_data = read_flashcards_file(r"E:\stuff\Maciej\_PYTHON\apps\flashcards\very.csv")
learn_mode(flashcards_data[0:7])
