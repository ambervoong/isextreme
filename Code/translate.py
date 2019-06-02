import pandas as pd
from time import sleep
from googletrans import Translator

PATHFILE = '/home/owo/Downloads/isextreme-master/Translate/translated.csv'
STARTROW = 1
ENDROW = 2395


uncorrupted = pd.read_csv(PATHFILE)
tr = Translator()    #ard 893 #did from 2394-3030, 3030-8500, 8500-10938
#uncorrupted["translated"] = uncorrupted["tweet"] #i think this reverts any progress between sessions?
for i in range(STARTROW, ENDROW):
    try:
        print("Begin: " + str(i))
        original = uncorrupted["tweet"].iloc[i]
        translated = tr.translate(uncorrupted["tweet"].iloc[i]).text
        same = original == translated

        #writes google translate output to dataframe
        uncorrupted["translated"].iloc[i] = translated 

        if not same:
            print("Translated! (maybe!)")
            #writing dataframe to csv to save progress
            uncorrupted.to_csv(PATHFILE,encoding='utf-8-sig')
            print("Write Success! " + str(i) + ": " + uncorrupted["translated"].iloc[i])
        else:
            print("no translated required: ")
            print(uncorrupted["translated"][i])
        sleep(3)
    except Exception:
        print("EXCEPTION: " + uncorrupted["translated"][i])
        print()
        continue
    print() # newline makes it easier to see


uncorrupted.to_csv(PATHFILE,encoding='utf-8-sig') # thisworks
