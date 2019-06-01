import pandas as pd
from time import sleep
from googletrans import Translator

uncorrupted = pd.read_csv('Data/scraped/translated.csv')
tr = Translator()    #ard 893
uncorrupted["translated"] = uncorrupted["tweet"]
for i in range(2394, 6000):
    try:
        uncorrupted["translated"].iloc[i] = tr.translate(uncorrupted["translated"].iloc[i]).text
        print(uncorrupted["translated"][i])
        print(i)
        sleep(5)
    except Exception:
        continue


uncorrupted.to_csv('Data/scraped/translated.csv',encoding='utf-8-sig') # thisworks
