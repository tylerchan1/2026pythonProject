import requests

api = "Z5dLEnB4-gc3a-3l1i-nfEG-lCpwtN4d"
url = "https://kli.korean.go.kr/term/api/search.do"

word_bank = []


def load_word():
    global word_bank
    for i in ["ㄱ","ㄴ","ㄷ","ㄹ","ㅁ"]:
        params = {
        "key": api,
        "apiSearchWord": i,
        "num" : "3",
        "sort" : "wt",
        }
            
        response = requests.get(url, params=params)
        data = response.json()
            
        word = data["channel"]["return_object"][0]["resultlist"][0]["word"]
        
        print(word)

        word_bank.append(word)
        print(word_bank)
        






def add_words():
    global word_bank 
    
    while True:
        k = input("단어입력 (종료하려면 '종료!' 입력): ")
        
        if k == "종료!":
            print("단어 입력을 종료합니다.")
            break
            
        params = {
            "key": api,
            "apiSearchWord": k,
            "num" : "3",
            "sort" : "wt",
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        word = data["channel"]["return_object"][0]["resultlist"][0]["word"]
        
        mean_list = []
        for a in range(3):
            mean = data["channel"]["return_object"][0]["resultlist"][a]["definition"]
            print(mean)
            mean_list.append(mean)
            
        word_bank.append({"word": word, "means": mean_list})
        print(f"-> '{word}' 단어가 추가되었습니다.\n")
#add_words()
load_word()