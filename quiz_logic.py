# quiz_logic.py
# 퀴즈 내부 로직을 담당하는 파일입니다.

import random
from quizbank import general_word_list, education_word_list, animal_word_list


QUIZ_BANK = {
    "일반어": general_word_list,
    "교육": education_word_list,
    "동물": animal_word_list
}


class QuizManager:
    def __init__(self):
        self.category = "일반어"
        self.word_list = QUIZ_BANK[self.category]

        self.total_count = 5
        self.current_count = 0
        self.score = 0

        self.current_quiz = None
        self.answer = ""
        self.definition = ""

    def start_quiz(self, category, total_count):
        self.category = category
        self.word_list = QUIZ_BANK[category]

        self.total_count = total_count
        self.current_count = 0
        self.score = 0

        self.current_quiz = None
        self.answer = ""
        self.definition = ""

    def make_quiz(self):
        if self.current_count >= self.total_count:
            return None

        self.current_quiz = random.choice(self.word_list)
        self.answer = self.current_quiz["word"]
        self.definition = self.current_quiz["definition"]

        self.current_count += 1

        return self.definition

    def check_answer(self, user_answer):
        user_answer = user_answer.strip()

        if user_answer == self.answer:
            self.score += 1
            return True
        else:
            return False

    def get_answer(self):
        return self.answer

    def get_current_count(self):
        return self.current_count

    def get_total_count(self):
        return self.total_count

    def get_score(self):
        return self.score

    def is_finished(self):
        return self.current_count >= self.total_count
    def get_candidates(self, user_input):
        user_input = user_input.strip()

        if user_input == "":
            return []

        candidates = []

        for wordset in self.word_list:
            word = wordset["word"]

        if word.startswith(user_input):
            candidates.append(word)

        return candidates[:3]