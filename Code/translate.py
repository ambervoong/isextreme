import pandas as pd
from time import sleep
from googletrans import Translator

uncorrupted = pd.read_csv('/home/owo/Downloads/isextreme-master/Translate/translated.csv')
tr = Translator()    #ard 893 #did from 2394-3030
#uncorrupted["translated"] = uncorrupted["tweet"] #i think this reverts any progress between sessions?
for i in range(2394, 6000):
    try:
        original = uncorrupted["tweet"].iloc[i]
        uncorrupted["translated"].iloc[i] = tr.translate(uncorrupted["tweet"].iloc[i]).text
        same = original == uncorrupted["translated"].iloc[i]
        print(uncorrupted["translated"][i])
        print(i)
        if not same:
            print("Translated! (maybe!)")
            uncorrupted.to_csv('/home/owo/Downloads/isextreme-master/Translate/translated.csv',encoding='utf-8-sig')
            print("Write Success! " + str(i) + ": " + uncorrupted["translated"].iloc[i])
        sleep(3)
    except Exception:
        print("EXCEPTION: " + uncorrupted["translated"][i])
        continue


uncorrupted.to_csv('/home/owo/Downloads/isextreme-master/Translate/translated.csv',encoding='utf-8-sig') # thisworks
