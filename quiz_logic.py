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
        self.current_quiz = None
        self.answer = ""
        self.definition = ""

    # 카테고리 설정
    def set_category(self, category):
        self.category = category
        self.word_list = QUIZ_BANK[category]

    # 새 문제 만들기
    def make_quiz(self):
        self.current_quiz = random.choice(self.word_list)

        self.answer = self.current_quiz["word"]
        self.definition = self.current_quiz["definition"]

        return self.definition

    # 정답 확인
    def check_answer(self, user_answer):
        user_answer = user_answer.strip()

        if user_answer == self.answer:
            return True
        else:
            return False

    # 정답 반환
    def get_answer(self):
        return self.answer