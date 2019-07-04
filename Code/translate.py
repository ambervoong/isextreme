import pandas as pd
from time import sleep
from googletrans import Translator

def translate(pathfile):
    PATHFILE = pathfile
    SAVE = pathfile
    STARTROW = 0
    uncorrupted = pd.read_csv(PATHFILE)
    ENDROW = len(uncorrupted["tweet"])

    # Add a translated column
    uncorrupted["translated"] = uncorrupted["tweet"]

    tr = Translator()
    for i in range(STARTROW, ENDROW):
        try:
            print("Begin: " + str(i))
            original = uncorrupted["translated"].iloc[i]
            if tr.detect(original).lang != 'en':
                translated = tr.translate(uncorrupted["translated"].iloc[i]).text
                same = original == translated

                #writes google translate output to dataframe
                uncorrupted["translated"].iloc[i] = translated

                if not same:
                    print("Translated ")
                    #writing dataframe to csv to save progress
                    uncorrupted.to_csv(SAVE, encoding='utf-8-sig')
                    print("Write Success " + str(i) + ": " + uncorrupted["translated"].iloc[i])

                sleep(1.5)
            else:
                print("No translation required: ")
                print(uncorrupted["translated"][i])

            # sleep(1.5) if you're going over 20 tweets then put sleep here so you don't get banned.
        except Exception as e:
            print("EXCEPTION: " + uncorrupted["translated"][i])
            print(e)
            print()
            continue
        print() # newline makes it easier to see


    uncorrupted.to_csv(SAVE,encoding='utf-8-sig') # thisworks


