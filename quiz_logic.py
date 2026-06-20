# quiz_logic.py
# 퀴즈 내부 로직을 담당하는 파일입니다.

import random
from quizbank import general_word_list, education_word_list, animal_word_list


# 카테고리 이름과 실제 단어 리스트 연결
QUIZ_BANK = {
    "일반어": general_word_list,
    "교육": education_word_list,
    "동물": animal_word_list
}


class QuizManager:
    def __init__(self):
        # 기본 카테고리 설정
        self.category = "일반어"
        self.word_list = QUIZ_BANK[self.category]

        # 기본 문제 수와 진행 상태
        self.total_count = 5
        self.current_count = 0
        self.score = 0

        # 현재 문제 정보
        self.current_quiz = None
        self.answer = ""
        self.definition = ""

    def start_quiz(self, category, total_count):
        # 새 퀴즈 시작 시 상태 초기화

        self.category = category
        self.word_list = QUIZ_BANK[category]

        self.total_count = total_count
        self.current_count = 0
        self.score = 0

        self.current_quiz = None
        self.answer = ""
        self.definition = ""

    def make_quiz(self):
        # 새 문제 생성

        # 이미 정해진 문제 수를 다 풀었으면 종료 신호 반환
        if self.current_count >= self.total_count:
            return None

        # 현재 카테고리 단어 목록에서 무작위로 하나 선택
        self.current_quiz = random.choice(self.word_list)

        # 정답 단어와 뜻풀이 저장
        self.answer = self.current_quiz["word"]
        self.definition = self.current_quiz["definition"]

        # 문제 수 증가
        self.current_count += 1

        # GUI에는 뜻풀이만 넘김
        return self.definition

    def check_answer(self, user_answer):
        # 사용자가 입력한 답과 실제 정답 비교

        user_answer = user_answer.strip()

        if user_answer == self.answer:
            self.score += 1
            return True
        else:
            return False

    def get_answer(self):
        # 현재 문제의 정답 반환
        return self.answer

    def get_current_count(self):
        # 현재까지 출제된 문제 수 반환
        return self.current_count

    def get_total_count(self):
        # 전체 문제 수 반환
        return self.total_count

    def get_score(self):
        # 현재 점수 반환
        return self.score

    def is_finished(self):
        # 현재 문제가 마지막 문제인지 확인
        return self.current_count >= self.total_count

    """
    def get_candidates(self, user_input):
        # 기존 퀴즈 데이터 안에서 자동완성 후보 찾기
        # 현재 GUI에서는 api.py의 get_wordSet_candidates()를 사용 중

        user_input = user_input.strip()

        if user_input == "":
            return []

        candidates = []

        for wordset in self.word_list:
            word = wordset["word"]

        if word.startswith(user_input):
            candidates.append(word)

        return candidates[:3]
    """