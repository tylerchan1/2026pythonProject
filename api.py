import requests

API_KEY = "BFE31A9FF95BC6ED61AFFE7A0AFDBD82"
API_URL = "https://opendict.korean.go.kr/api/search"

def make_wordset(item):
    return {
        "word": item["word"],
        "definition": item["sense"][0]["definition"]
    }

def get_wordSet(keyword):
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

    item = data["channel"]["item"][0]

    return make_wordset(item)

def get_wordSet_candidates(keyword):
    keyword = keyword.strip()

    if keyword == "":
        return []

    candidates = []
    seen_words = set()

    start = 1

    while len(candidates) < 3 and start <= 300:
        params = {
            "key": API_KEY,
            "q": keyword,
            "req_type": "json",
            "start": str(start),
            "num": "100",
            "part": "word",
            "sort": "dict",
            "advanced": "y",
            "target": "1",
            "method": "start",
            "type1": "word"
        }

        response = requests.get(API_URL, params=params)
        data = response.json()

        items = data["channel"].get("item", [])
        

        if len(items) == 0:
            break

        for item in items:
            word = item["word"]
            word = word.replace("-", "")

            # 이미 나온 단어는 제외
            if word in seen_words:
                continue

            # 입력값과 완전히 같은 단어는 제외
            if word == keyword:
                continue

            # 입력값으로 시작하지 않으면 제외
            if not word.startswith(keyword):
                continue

            # 공백이 있는 구 단위 표현은 일단 제외
            if " " in word:
                continue

            seen_words.add(word)
            candidates.append(word)

            if len(candidates) >= 3:
                break

        start += 100

    return candidates
#테스트용
#wordset = get_wordSet(input("검색: "))

#word = wordset["word"]
#definition = wordset["definition"]

#print(word)
#print(definition)