import pymongo
import requests

from API import api_key, deviceid, app_id

payload = {"api_key": api_key, "deviceid": deviceid, "app_id": app_id}

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
dblist = myclient.list_database_names()
print(dblist)
mydb = myclient["wordsdb"]
mycol = mydb["words"]

with open("words_alpha.txt", "r") as f:
    words = f.readlines()
    print(words)
    print(len(words))

for word in words:
    word = word.strip('\n')
    print(word)

    myquery = {"word": word}
    mydoc = mycol.find(myquery)
    if mydoc.count() == 0:
        URL = "http://restcdn.dictionary.com/v2/word.json/%s/learnersDictionary" % word
        r = requests.get(URL, params=payload)
        print(r.json())
        x = mycol.insert_one({"word": word, "json": r.json()})
        print(x)
