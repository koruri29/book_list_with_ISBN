import sys # BS4「FeatureNotFound」エラー対策
import requests # インターネットアクセス
from bs4 import BeautifulSoup # レスポンス整形
import urllib.parse # パーセントエンコーディング・デコーディング

sys.path.append("lib.bs4") # BS4エラー対策

def getSearchResults(url, *keywords):
    encoded = encodeKeywords(keywords)
    url += encoded
    #print(url)
    
    response = requests.get(url)
    
    response.encoding = response.apparent_encoding
    filename = "download.txt"
    f = open(filename, mode="w")
    with open(filename, mode="w") as f:
        f.write(response.text)    
    soup = BeautifulSoup(response.content, "html.parser")
    
    #検索にヒットしなかった場合
    not_found = soup.find("div", attrs = {"class": "noHitBox"})
    if not_found != None:
        return print("検索結果が0件です。")
    
    #書籍タイトル取得
    # title_parents = soup.find_all("p", attres = {"class": "itemttl"})
    title_parents = soup.select("p.itemttl > a")
    # print(title_parents)
    titles = []
    count = 0
    for title_parent in title_parents:
        titles.append(title_parent.contents[0])
        print(titles[count])
        count += 1
    

def encodeKeywords(*keywords):
    double_encoded = ""
    for keyword in keywords:
        if (type(keyword) != "<class 'str'>"): # 文字列型か判定、変換
            keyword = str(keyword)
        encoded = urllib.parse.quote(keyword[3:-4], '/', encoding='shift_jis') # 引数1は(['キーワード'],)の形から整形している
        double_encoded = urllib.parse.quote(encoded, '/', encoding='shift_jis')
    return double_encoded


# メインルーチン
# url = "https://www.bookoffonline.co.jp/"
url = "https://www.bookoffonline.co.jp/display/L001,st=a,q="
# keywords = ["オブジェクト指向超入門"]

print("本のタイトルを入力してください。")
keywords = input(">> ")
keywords = keywords.replace("　", " ")
keywords = keywords.split()


getSearchResults(url, keywords)
