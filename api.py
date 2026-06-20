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
    params = {
        "key": API_KEY,
        "q": keyword,
        "req_type": "json",
        "start": "1",
        "num": "10",
        "part": "word",
        "sort": "dict",
        "advanced": "y",
        "target": "1",
        "method": "start",
        "type1": "word"
    }

    response = requests.get(API_URL, params=params)
    data = response.json()

    items = data["channel"]["item"]

    candidates = []

    for item in items:
        wordset = make_wordset(item)
        candidates.append(wordset["word"])

        if len(candidates) >= 3:
            break

    return candidates

#테스트용
#wordset = get_wordSet(input("검색: "))

#word = wordset["word"]
#definition = wordset["definition"]

#print(word)
#print(definition)