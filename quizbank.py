from api import get_wordSet

GENERAL_KEYWORDS = ["하루", "사람", "마음", "시간", "생각", "길", "집", "말", "눈", "손"]
EDUCATION_KEYWORDS = ["교육", "학습", "학교", "수업", "평가", "교사", "학생", "교실", "시험", "교과"]
ANIMAL_KEYWORDS = ["동물", "새", "물고기", "곤충", "고양이", "강아지", "말", "소", "닭", "개"]


def make_word_list(keywords):
    word_list = []

    for keyword in keywords:
        wordset = get_wordSet(keyword)
        word_list.append(wordset)

    return word_list


general_word_list = make_word_list(GENERAL_KEYWORDS)
education_word_list = make_word_list(EDUCATION_KEYWORDS)
animal_word_list = make_word_list(ANIMAL_KEYWORDS)


# test용
print("=== 일반어 ===")
for wordset in general_word_list:
    print(wordset["word"], ":", wordset["definition"])

print("\n=== 교육 ===")
for wordset in education_word_list:
    print(wordset["word"], ":", wordset["definition"])

print("\n=== 동물 ===")
for wordset in animal_word_list:
    print(wordset["word"], ":", wordset["definition"])