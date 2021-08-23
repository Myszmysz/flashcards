#! python3
# flashcards.py - smart learning app using flashcards. Request a csv file with question-answer pairs

import sys
import os
import logging
import csv
from random import randint, shuffle

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


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
            card_data.append(Card(row[0], row[1], number))
    return card_data


# take answer from user
def ask_question(question, answer):
    user_answer = input(question + ": ")
    if user_answer == answer:
        print('Correct!')
        return True
    else:
        print(f'Wrong! Correct answer is {answer}!')
        return False


# ask user a question
def examine_user(card, question_type=0, hint=False):
    if question_type == 0:  # normal
        result = ask_question(card.obverse, card.reverse)
        if result:
            card.correct += 1
            return True
        else:
            card.wrong += 1
            return False
    elif question_type == 1:  # reverse
        result = ask_question(card.reverse, card.obverse)
        if result:
            card.correct += 1
            return True
        else:
            card.wrong += 1
            return False
    elif question_type == 2:  # random
        coin = randint(0, 1)
        examine_user(card, coin)


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


# learn mode
def learn_mode(deck):
    print(f"Learn mode. Type in EXIT to quit.")

    number_of_cards = len(deck)
    question_counter = 0
    points = 0

    while question_counter < number_of_cards:
        if examine_user(deck[question_counter]):
            points += 1
        question_counter += 1

    if question_counter == number_of_cards:
        print(f"Finished. You earned {points} out of {number_of_cards}!")


def smart_learn_mode(deck):
    print(f"Smart learn mode. Type in EXIT to quit.")

    obverse_list = list(deck.keys())
    failed_list = []
    barrel = []

    question_counter = 0
    last = 0
    points = 0
    while True:
        question_counter += 1

        shuffle(obverse_list)
        if len(failed_list) > 3:
            shuffle(failed_list)
            draw = failed_list.pop(0)
        else:
            draw = obverse_list.pop(0)

        coin = randint(0, 1)
        if coin == 0:
            question = draw
            answer = deck[question]
        else:
            answer = draw
            question = deck[answer]

        print(f'{question_counter}. ', end='')
        result = ask_question(question, answer, hint=True)
        if result == "EXIT":
            print(f'You answered correctly {points} times. Goodbye!')
            sys.exit()
        elif result:
            points += 1
        else:  # if wrong answer
            failed_list.append(draw)


# todo test mode
# todo save/read scores
# todo handle typos

def game():
    path = get_flashcards_path()
    if not path:
        sys.exit()
    flashcards_data = read_flashcards_file(path)
    learn_mode(flashcards_data[:10])

game()

#todo 