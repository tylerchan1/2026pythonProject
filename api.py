import requests

# 우리말샘 Open API 인증 키
API_KEY = "BFE31A9FF95BC6ED61AFFE7A0AFDBD82"

# 우리말샘 단어 검색 API 주소
API_URL = "https://opendict.korean.go.kr/api/search"


def make_wordset(item):
    # API 응답 item에서 퀴즈에 필요한 값만 추출
    return {
        "word": item["word"],
        "definition": item["sense"][0]["definition"]
    }


def get_wordSet(keyword):
    # 키워드 하나로 단어와 뜻풀이 가져오기

    params = {
        "key": API_KEY,
        "q": keyword,
        "req_type": "json",
        "start": "1",
        "num": "10",
        "part": "word",
        "sort": "dict"
    }

    response = requests.get(API_URL, params=params)

    data = response.json()

    # 검색 결과 중 첫 번째 단어만 사용
    item = data["channel"]["item"][0]

    return make_wordset(item)


def get_wordSet_candidates(keyword):
    # 입력값으로 시작하는 자동완성 후보 단어 검색

    keyword = keyword.strip()

    # 입력값이 없으면 후보도 없음
    if keyword == "":
        return []

    candidates = []
    seen_words = set()

    # 검색 결과 시작 위치
    start = 1

    # 후보 3개를 찾을 때까지 검색
    # start 제한은 API 요청이 너무 길어지는 것 방지
    while len(candidates) < 3 and start <= 300:
        params = {
            "key": API_KEY,
            "q": keyword,
            "req_type": "json",
            "start": str(start),
            "num": "100",
            "part": "word",
            "sort": "dict",

            # 고급 검색 사용
            "advanced": "y",

            # 표제어 대상 검색
            "target": "1",

            # 입력값으로 시작하는 단어 검색
            "method": "start",

            # 단어 기준 검색
            "type1": "word"
        }

        response = requests.get(API_URL, params=params)
        data = response.json()

        # item이 없을 수도 있으니까 기본값은 빈 리스트
        items = data["channel"].get("item", [])
        

        # 더 이상 검색 결과가 없으면 종료
        if len(items) == 0:
            break

        for item in items:
            word = item["word"]

            # 우리말샘 결과에 붙는 '-' 제거
            word = word.replace("-", "")

            # 이미 나온 단어는 제외
            if word in seen_words:
                continue

            # 입력값과 완전히 같은 단어는 후보에서 제외
            if word == keyword:
                continue

            # 혹시 API 결과가 섞일 수 있으니 한 번 더 필터링
            if not word.startswith(keyword):
                continue

            # 구 단위 표현은 후보에서 제외
            if " " in word:
                continue

            seen_words.add(word)
            candidates.append(word)

            # 후보는 최대 3개만 표시
            if len(candidates) >= 3:
                break

        # 다음 검색 묶음으로 이동
        start += 100

    return candidates


# 테스트용
#wordset = get_wordSet(input("검색: "))

#word = wordset["word"]
#definition = wordset["definition"]

#print(word)
#print(definition)