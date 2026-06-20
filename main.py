# gui.py
# tkinter를 사용한 퀴즈 GUI 실행 파일입니다.

import tkinter as tk
from quiz_logic import QuizManager
from api import get_wordSet_candidates


# 퀴즈 진행 상태를 관리하는 객체
quiz_manager = QuizManager()

# 자동완성 검색 예약 id
# 키를 누를 때마다 바로 검색하지 않고 0.3초 뒤에 검색하기 위해 사용
search_after_id = None


# -----------------------------
# 화면 전환 함수
# -----------------------------

def show_start_screen():
    # 퀴즈 화면과 결과 화면을 숨기고 시작 화면 표시
    quiz_frame.pack_forget()
    result_frame.pack_forget()
    start_frame.pack(fill="both", expand=True)


def show_quiz_screen():
    # 시작 화면과 결과 화면을 숨기고 퀴즈 화면 표시
    start_frame.pack_forget()
    result_frame.pack_forget()
    quiz_frame.pack(fill="both", expand=True)


def show_result_screen():
    # 퀴즈 화면과 시작 화면을 숨기고 결과 화면 표시
    quiz_frame.pack_forget()
    start_frame.pack_forget()
    result_frame.pack(fill="both", expand=True)

    # 최종 점수 표시
    final_score_label.config(
        text=f"최종 점수: {quiz_manager.get_score()} / {quiz_manager.get_total_count()}"
    )


# -----------------------------
# 퀴즈 실행 함수
# -----------------------------

def start_quiz():
    # 시작 화면에서 선택한 카테고리와 문제 수 가져오기
    category = category_var.get()
    total_count = int(count_var.get())

    # 퀴즈 상태 초기화
    quiz_manager.start_quiz(category, total_count)

    # 퀴즈 화면으로 이동 후 첫 문제 표시
    show_quiz_screen()
    show_new_quiz()


def show_new_quiz():
    # 새 문제 생성
    definition = quiz_manager.make_quiz()

    # 더 이상 문제가 없으면 결과 화면으로 이동
    if definition is None:
        show_result_screen()
        return

    # 현재 문제 번호 표시
    question_count_label.config(
        text=f"문제 {quiz_manager.get_current_count()} / {quiz_manager.get_total_count()}"
    )

    # 현재 점수 표시
    score_label.config(
        text=f"점수: {quiz_manager.get_score()}"
    )

    # 문제로 뜻풀이 표시
    question_label.config(text=definition)

    # 이전 입력값과 자동완성 후보 초기화
    answer_entry.delete(0, tk.END)
    candidate_listbox.delete(0, tk.END)

    # 이전 결과 메시지 초기화
    result_label.config(text="")
    answer_label.config(text="")

    # 정답 확인 버튼 활성화
    submit_button.config(state="normal")

    # 다음 문제 버튼은 정답 확인 전까지 비활성화
    next_button.config(state="disabled")
    next_button.config(text="다음 문제")


def submit_answer():
    # 입력창에 적힌 답 가져오기
    user_answer = answer_entry.get()

    # 빈 입력 방지
    if user_answer.strip() == "":
        result_label.config(text="정답을 입력하거나 보기에서 선택하세요.")
        return

    # 정답 판정
    is_correct = quiz_manager.check_answer(user_answer)

    if is_correct:
        result_label.config(text="정답입니다.")
        answer_label.config(text="")
    else:
        result_label.config(text="오답입니다.")
        answer_label.config(text="정답: " + quiz_manager.get_answer())

    # 점수 표시 갱신
    score_label.config(
        text=f"점수: {quiz_manager.get_score()}"
    )

    # 한 문제에서 중복 제출 방지
    submit_button.config(state="disabled")

    # 정답 확인 후 자동완성 후보 목록 제거
    candidate_listbox.delete(0, tk.END)

    # 마지막 문제면 결과 보기 버튼으로 변경
    if quiz_manager.is_finished():
        next_button.config(text="결과 보기", state="normal")
    else:
        next_button.config(text="다음 문제", state="normal")


def next_action():
    # 마지막 문제를 푼 상태면 결과 화면으로 이동
    if quiz_manager.is_finished():
        show_result_screen()
    else:
        show_new_quiz()


# -----------------------------
# 자동완성 후보 함수
# -----------------------------

def update_candidates(event=None):
    # 키 입력이 발생할 때마다 자동완성 검색 예약

    global search_after_id

    # 이전 검색 예약이 남아 있으면 취소
    # 빠르게 타이핑할 때 API 요청이 너무 많이 나가는 것 방지
    if search_after_id is not None:
        window.after_cancel(search_after_id)

    # 0.3초 뒤에 실제 검색 실행
    search_after_id = window.after(300, search_candidates)


def search_candidates():
    # 실제 자동완성 검색 실행

    global search_after_id

    # 예약 id 초기화
    search_after_id = None

    # 입력창의 현재 값 가져오기
    user_input = answer_entry.get().strip()

    # 기존 후보 목록 삭제
    candidate_listbox.delete(0, tk.END)

    # 입력값이 없으면 검색하지 않음
    if user_input == "":
        return

    try:
        # API에서 자동완성 후보 3개 가져오기
        candidates = get_wordSet_candidates(user_input)

        # 후보 목록을 Listbox에 표시
        for word in candidates:
            candidate_listbox.insert(tk.END, word)

    except Exception as e:
        # GUI가 멈추지 않도록 오류는 콘솔에만 출력
        print("자동완성 검색 오류:", e)


def select_candidate(event=None):
    # 자동완성 후보를 클릭했을 때 입력창에 반영

    selected = candidate_listbox.curselection()

    # 선택된 항목이 없으면 종료
    if len(selected) == 0:
        return

    index = selected[0]
    word = candidate_listbox.get(index)

    # 입력창을 선택한 후보 단어로 교체
    answer_entry.delete(0, tk.END)
    answer_entry.insert(0, word)

    # 후보 선택 후 목록 삭제
    candidate_listbox.delete(0, tk.END)


# -----------------------------
# tkinter 기본 창
# -----------------------------

window = tk.Tk()
window.title("우리말샘 한국어 퀴즈")
window.geometry("700x550")


# -----------------------------
# 시작 화면
# -----------------------------

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


# 카테고리 선택
category_label = tk.Label(
    start_frame,
    text="카테고리 선택",
    font=("맑은 고딕", 14)
)
category_label.pack(pady=10)

# 기본 카테고리는 일반어
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


# 문제 개수 선택
count_label = tk.Label(
    start_frame,
    text="문제 개수 선택",
    font=("맑은 고딕", 14)
)
count_label.pack(pady=20)

# 기본 문제 수는 5문제
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


# -----------------------------
# 퀴즈 화면
# -----------------------------

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
question_label.pack(pady=40)


answer_entry = tk.Entry(
    quiz_frame,
    font=("맑은 고딕", 14),
    width=30
)
answer_entry.pack(pady=5)

# 키를 누를 때마다 자동완성 후보 갱신 예약
answer_entry.bind("<KeyRelease>", update_candidates)


candidate_listbox = tk.Listbox(
    quiz_frame,
    font=("맑은 고딕", 12),
    width=30,
    height=3
)
candidate_listbox.pack(pady=5)

# 후보 단어 클릭 시 입력창에 반영
candidate_listbox.bind("<<ListboxSelect>>", select_candidate)


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


# -----------------------------
# 결과 화면
# -----------------------------

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


# 엔터키로 정답 제출
window.bind("<Return>", lambda event: submit_answer())


# 첫 화면 표시
show_start_screen()


# GUI 실행
window.mainloop()