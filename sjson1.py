import requests
import random

api = "Z5dLEnB4-gc3a-3l1i-nfEG-lCpwtN4d"
url = "https://kli.korean.go.kr/term/api/search.do"

k = input("단어입력:")

params = {
    "key": api,
    "apiSearchWord": k,
    "num" : "3",
    "sort" : "wt",
}

response = requests.get(url, params=params)
data = response.json()

word = data["channel"]["return_object"][0]["resultlist"][0]["word"]
for a in range(3):
    mean = data["channel"]["return_object"][0]["resultlist"][a]["definition"]
    print(mean)