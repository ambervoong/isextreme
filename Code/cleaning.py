import pandas as pd
import numpy as np
import re

def remove_urls(text):
    temp = re.sub(r'http\S+|www\S+', '', text)
    return temp

def no_emojis_hashtags(text):
    # Removes hahstags as well!
    temp = re.sub(r'[^ A-Za-z0-9.,:;\'\"`~!@#$%^&*()\\-_=+\[\]?/><{}]', '', text)
    return temp

def remove_RT_users_hashtags(text):
    temp = text.replace("RT ", '')
    temp = re.sub(r'[@#]\S+', '', temp) # REMOVES HASHTAGS AND USERS completely.
    return temp

def clean(pathfile):
    PATHFILE = pathfile
    df = pd.read_csv(PATHFILE)
    col = df["translated"]
    # Remove URLs, hashtags, users, and RT tags.
    assert isinstance(df, pd.DataFrame), "Input data is not a pandas dataframe, it is of type " \
                                                                                + str(type(col))
    texts = np.array(col)
    cleaned = []
    for text in texts:
        temp = remove_urls(str(text))
        #temp = no_emojis_hashtags(temp) # We are keeping the emojis.
        temp = remove_RT_users_hashtags(temp)
        cleaned.append(temp.strip())
    df["cleaned"] = cleaned
    df.to_csv(PATHFILE, encoding='utf-8-sig')
