# gui.py
# tkinter를 사용한 퀴즈 GUI 실행 파일입니다.

import tkinter as tk
from quiz_logic import QuizManager


quiz_manager = QuizManager()


def show_start_screen():
    quiz_frame.pack_forget()
    result_frame.pack_forget()
    start_frame.pack(fill="both", expand=True)


def show_quiz_screen():
    start_frame.pack_forget()
    result_frame.pack_forget()
    quiz_frame.pack(fill="both", expand=True)


def show_result_screen():
    quiz_frame.pack_forget()
    start_frame.pack_forget()
    result_frame.pack(fill="both", expand=True)

    final_score_label.config(
        text=f"최종 점수: {quiz_manager.get_score()} / {quiz_manager.get_total_count()}"
    )


def start_quiz():
    category = category_var.get()
    total_count = int(count_var.get())

    quiz_manager.start_quiz(category, total_count)

    show_quiz_screen()
    show_new_quiz()


def show_new_quiz():
    definition = quiz_manager.make_quiz()

    if definition is None:
        show_result_screen()
        return

    question_count_label.config(
        text=f"문제 {quiz_manager.get_current_count()} / {quiz_manager.get_total_count()}"
    )

    score_label.config(
        text=f"점수: {quiz_manager.get_score()}"
    )

    question_label.config(text=definition)

    answer_entry.delete(0, tk.END)
    result_label.config(text="")
    answer_label.config(text="")

    submit_button.config(state="normal")
    next_button.config(state="disabled")


def submit_answer():
    user_answer = answer_entry.get()

    is_correct = quiz_manager.check_answer(user_answer)

    if is_correct:
        result_label.config(text="정답입니다.")
        answer_label.config(text="")
    else:
        result_label.config(text="오답입니다.")
        answer_label.config(text="정답: " + quiz_manager.get_answer())

    score_label.config(
        text=f"점수: {quiz_manager.get_score()}"
    )

    submit_button.config(state="disabled")

    if quiz_manager.is_finished():
        next_button.config(text="결과 보기", state="normal")
    else:
        next_button.config(text="다음 문제", state="normal")


def next_action():
    if quiz_manager.is_finished():
        show_result_screen()
    else:
        show_new_quiz()


window = tk.Tk()
window.title("우리말샘 한국어 퀴즈")
window.geometry("700x500")


# 시작 화면
start_frame = tk.Frame(window)

start_title = tk.Label(
    start_frame,
    text="우리말샘 한국어 퀴즈",
    font=("맑은 고딕", 24)
)
start_title.pack(pady=40)

start_description = tk.Label(
    start_frame,
    text="뜻풀이를 보고 알맞은 단어를 맞혀 보세요.",
    font=("맑은 고딕", 13)
)
start_description.pack(pady=10)

category_label = tk.Label(
    start_frame,
    text="카테고리 선택",
    font=("맑은 고딕", 14)
)
category_label.pack(pady=10)

category_var = tk.StringVar(value="일반어")

category_button_frame = tk.Frame(start_frame)
category_button_frame.pack()

tk.Radiobutton(
    category_button_frame,
    text="일반어",
    variable=category_var,
    value="일반어",
    font=("맑은 고딕", 12)
).pack(side="left", padx=10)

tk.Radiobutton(
    category_button_frame,
    text="교육",
    variable=category_var,
    value="교육",
    font=("맑은 고딕", 12)
).pack(side="left", padx=10)

tk.Radiobutton(
    category_button_frame,
    text="동물",
    variable=category_var,
    value="동물",
    font=("맑은 고딕", 12)
).pack(side="left", padx=10)

count_label = tk.Label(
    start_frame,
    text="문제 개수 선택",
    font=("맑은 고딕", 14)
)
count_label.pack(pady=20)

count_var = tk.StringVar(value="5")

count_button_frame = tk.Frame(start_frame)
count_button_frame.pack()

tk.Radiobutton(
    count_button_frame,
    text="5문제",
    variable=count_var,
    value="5",
    font=("맑은 고딕", 12)
).pack(side="left", padx=10)

tk.Radiobutton(
    count_button_frame,
    text="10문제",
    variable=count_var,
    value="10",
    font=("맑은 고딕", 12)
).pack(side="left", padx=10)

start_button = tk.Button(
    start_frame,
    text="퀴즈 시작",
    font=("맑은 고딕", 14),
    command=start_quiz
)
start_button.pack(pady=40)


# 퀴즈 화면
quiz_frame = tk.Frame(window)

top_info_frame = tk.Frame(quiz_frame)
top_info_frame.pack(pady=20)

question_count_label = tk.Label(
    top_info_frame,
    text="문제 0 / 0",
    font=("맑은 고딕", 13)
)
question_count_label.pack(side="left", padx=30)

score_label = tk.Label(
    top_info_frame,
    text="점수: 0",
    font=("맑은 고딕", 13)
)
score_label.pack(side="left", padx=30)

question_label = tk.Label(
    quiz_frame,
    text="",
    font=("맑은 고딕", 14),
    wraplength=580,
    justify="center"
)
question_label.pack(pady=50)

answer_entry = tk.Entry(
    quiz_frame,
    font=("맑은 고딕", 14),
    width=30
)
answer_entry.pack(pady=10)

button_frame = tk.Frame(quiz_frame)
button_frame.pack(pady=20)

submit_button = tk.Button(
    button_frame,
    text="정답 확인",
    font=("맑은 고딕", 12),
    command=submit_answer
)
submit_button.pack(side="left", padx=10)

next_button = tk.Button(
    button_frame,
    text="다음 문제",
    font=("맑은 고딕", 12),
    command=next_action
)
next_button.pack(side="left", padx=10)

result_label = tk.Label(
    quiz_frame,
    text="",
    font=("맑은 고딕", 15)
)
result_label.pack(pady=10)

answer_label = tk.Label(
    quiz_frame,
    text="",
    font=("맑은 고딕", 13)
)
answer_label.pack(pady=5)


# 결과 화면
result_frame = tk.Frame(window)

result_title = tk.Label(
    result_frame,
    text="퀴즈 종료",
    font=("맑은 고딕", 24)
)
result_title.pack(pady=60)

final_score_label = tk.Label(
    result_frame,
    text="최종 점수: 0 / 0",
    font=("맑은 고딕", 18)
)
final_score_label.pack(pady=20)

restart_button = tk.Button(
    result_frame,
    text="처음으로 돌아가기",
    font=("맑은 고딕", 14),
    command=show_start_screen
)
restart_button.pack(pady=40)

window.bind("<Return>", lambda event: submit_answer())

show_start_screen()

window.mainloop()