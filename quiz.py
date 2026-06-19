import random
import api


def play_quiz():
    if not api.quiz_bank:
        print("퀴즈를 낼 단어가 없습니다! 먼저 단어를 입력해 주세요.")
        return

    target_data = random.choice(api.quiz_bank)
    correct_word = target_data["word"]
    quiz_mean = random.choice(target_data["means"])

    print("\n" + "=" * 40)
    print(f" [ 퀴즈 - 총 {len(api.quiz_bank)}개 단어 중 출제 ]")
    print(f"문제(뜻): {quiz_mean}")
    print("=" * 40)

    user_answer = input("이 뜻을 가진 단어는 무엇일까요?: ").strip()

    if user_answer == correct_word:
        print("\n정답입니다!")
    else:
        print(f"\n틀렸습니다! 정답은 [{correct_word}] 입니다.")


play_quiz()