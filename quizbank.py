from api import get_wordSet

# 카테고리별 기본 검색 키워드
GENERAL_KEYWORDS = ["하루", "사람", "마음", "시간", "생각", "길", "집", "말", "눈", "손"]
EDUCATION_KEYWORDS = ["교육", "학습", "학교", "수업", "평가", "교사", "학생", "교실", "시험", "교과"]
ANIMAL_KEYWORDS = ["동물", "새", "물고기", "곤충", "고양이", "강아지", "말", "소", "닭", "개"]


def make_word_list(keywords):
    # 키워드 목록을 실제 퀴즈 단어 목록으로 변환

    word_list = []

    for keyword in keywords:
        # API에서 단어와 뜻풀이 가져오기
        wordset = get_wordSet(keyword)

        # 퀴즈 데이터 리스트에 추가
        word_list.append(wordset)

    return word_list


# 프로그램 실행 시 카테고리별 퀴즈 데이터 생성
general_word_list = make_word_list(GENERAL_KEYWORDS)
education_word_list = make_word_list(EDUCATION_KEYWORDS)
animal_word_list = make_word_list(ANIMAL_KEYWORDS)


# test용
"""
print("=== 일반어 ===")
for wordset in general_word_list:
    print(wordset["word"], ":", wordset["definition"])

print("\n=== 교육 ===")
for wordset in education_word_list:
    print(wordset["word"], ":", wordset["definition"])

print("\n=== 동물 ===")
for wordset in animal_word_list:
    print(wordset["word"], ":", wordset["definition"])
"""