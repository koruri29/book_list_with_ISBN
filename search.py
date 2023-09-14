import sys # BS4「FeatureNotFound」エラー対策
import requests # インターネットアクセス
from bs4 import BeautifulSoup # レスポンス整形
import urllib.parse # パーセントエンコーディング・デコーディング

sys.path.append("lib.bs4") # BS4エラー対策

def getSearchResults(url, *keywords):
    encoded = encodeKeywords(keywords)
    url += encoded
    
    response = requests.get(url)
    
    # 確認出力用
    # response.encoding = response.apparent_encoding
    # filename = "download.txt"
    # f = open(filename, mode="w")
    # with open(filename, mode="w") as f:
    #     f.write(response.text)    
    
    
    #書籍タイトル取得
    soup = BeautifulSoup(response.content, "html.parser")
    book_items = soup.select("h3.heightLine-2 > a")
    
    if book_items == None:
        print("検索結果が0件です。")
        return
    
    items = {}
    for book_item in book_items:
        book_title = book_item.contents[0]
        book_link = urllib.parse.urljoin(url, book_item.get("href"))
        isbn = book_link[38:]
        items[book_title] = isbn
    return items
    

def encodeKeywords(*keywords):
    encoded = ""
    for keyword in keywords:
        if (type(keyword) != "<class 'str'>"): # 文字列型か判定、変換
            keyword = str(keyword)
        encoded += urllib.parse.quote(keyword[3:-4], '/', encoding='utf-8') # 引数1は(['キーワード'],)の形から整形している
        encoded += "%E3%80%80" # 半角スペースのエンコーディング
    return encoded


# メインルーチン
url = "https://www.kinokuniya.co.jp/disp/CSfDispListPage_001.jsp?qs=true&ptk=01&q="
# keywords = ["オブジェクト指向超入門"]

print("本のタイトルを入力してください。")
keywords = input(">> ")
keywords = keywords.replace("　", " ")
keywords = keywords.split()


items = getSearchResults(url, keywords)

if items != None:
    for k in items:
        print(k)
        print(items[k])
